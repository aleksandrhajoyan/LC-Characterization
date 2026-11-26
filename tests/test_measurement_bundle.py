"""Explicitly synthetic software fixtures, never experimental measurements."""

from contextlib import contextmanager, redirect_stdout
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import stat
import struct
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zlib

from photonicsai_analyst import (
    ValidationIssue,
    ValidationReport,
    validate_measurement_bundle,
)
from photonicsai_analyst.__main__ import main


def chunk(kind, payload=b""):
    return (struct.pack(">I", len(payload)) + kind + payload +
            struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF))


def synthetic_png(depth=8, width=2, height=2, *, color=0,
                  compression=0, filtering=0, interlace=0):
    """Generate software-test bytes; dimensions are not camera specifications."""
    header = struct.pack(">IIBBBBB", width, height, depth, color,
                         compression, filtering, interlace)
    rows = (b"\x00" + b"\x00" * width * (depth // 8)) * height
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) +
            chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND"))


class MeasurementBundleTests(unittest.TestCase):
    @contextmanager
    def fixture(self, depth=8):
        # All fixture creation/mutation is confined to this context. No parent
        # temp-directory enumeration or pre-existing temporary files are used.
        with tempfile.TemporaryDirectory(prefix="photonicsai_c04a_") as directory:
            root = Path(directory)
            (root / "images").mkdir()
            data = synthetic_png(depth)
            (root / "images/frame_0000.png").write_bytes(data)
            manifest = {
                "schema_version": "1.0",
                "measurement_id": "synthetic-software-fixture",
                "data_origin": "test_fixture",
                "acquired_at": "2000-01-01T00:00:00Z",
                "operator_id": "fixture-placeholder",
                "sample_id": "fixture-placeholder",
                "procedure_id": None,
                "camera": {
                    "manufacturer": None,
                    "model": None,
                    "pixel_format": f"mono{depth}",
                    "exposure_time": None,
                    "roi_px": {"x": 0, "y": 0, "width": 2, "height": 2},
                    "binning": {"x": 1, "y": 1},
                },
                "frames": [{
                    "frame_index": 0,
                    "file": "images/frame_0000.png",
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "captured_at": "2000-01-01T00:00:00+00:00",
                    "width_px": 2,
                    "height_px": 2,
                }],
                "notes": "Synthetic software-test artifact; not experimental data.",
            }
            self.write_manifest(root, manifest)
            yield root, manifest

    def write_manifest(self, root, manifest):
        self.assertEqual(manifest["data_origin"], "test_fixture")
        (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    def replace_png(self, root, manifest, data):
        (root / "images/frame_0000.png").write_bytes(data)
        manifest["frames"][0]["sha256"] = hashlib.sha256(data).hexdigest()
        self.write_manifest(root, manifest)

    def assert_issue(self, root, code):
        report = validate_measurement_bundle(root)
        self.assertFalse(report.valid, report.to_dict())
        self.assertIn(code, [issue.code for issue in report.issues], report.to_dict())
        self.assertTrue(all(issue.severity == "error" for issue in report.issues))
        return report

    def test_valid_synthetic_mono8_and_input_unchanged(self):
        with self.fixture() as (root, _):
            paths = [root / "manifest.json", root / "images/frame_0000.png"]
            before = [(p.read_bytes(), p.stat().st_mtime_ns) for p in paths]
            names_before = sorted(str(p.relative_to(root)) for p in root.rglob("*"))
            report = validate_measurement_bundle(root)
            self.assertTrue(report.valid, report.to_dict())
            self.assertEqual(report.files_checked, 1)
            self.assertEqual(report.data_origin, "test_fixture")
            self.assertEqual(report.issues, [])
            self.assertEqual(before, [(p.read_bytes(), p.stat().st_mtime_ns) for p in paths])
            self.assertEqual(names_before, sorted(str(p.relative_to(root)) for p in root.rglob("*")))
            serialized = json.loads(json.dumps(report.to_dict()))
            self.assertEqual(serialized["measurement_id"], "synthetic-software-fixture")
            self.assertEqual(serialized["bundle_root"], str(root.resolve()))

    def test_valid_synthetic_mono16(self):
        with self.fixture(16) as (root, _):
            self.assertTrue(validate_measurement_bundle(root).valid)

    def test_missing_required_manifest_fields(self):
        # data_origin is deliberately never removed or changed in fixtures.
        fields = ("schema_version", "measurement_id", "acquired_at", "operator_id",
                  "sample_id", "procedure_id", "camera", "frames", "notes")
        with self.fixture() as (root, original):
            for name in fields:
                with self.subTest(field=name):
                    manifest = deepcopy(original)
                    del manifest[name]
                    self.write_manifest(root, manifest)
                    self.assert_issue(root, "FIELD_MISSING")

    def test_missing_nested_fields(self):
        with self.fixture() as (root, original):
            for name in original["camera"]:
                with self.subTest(camera_field=name):
                    manifest = deepcopy(original)
                    del manifest["camera"][name]
                    self.write_manifest(root, manifest)
                    self.assert_issue(root, "FIELD_MISSING")
            for name in original["frames"][0]:
                with self.subTest(frame_field=name):
                    manifest = deepcopy(original)
                    del manifest["frames"][0][name]
                    self.write_manifest(root, manifest)
                    self.assert_issue(root, "FIELD_MISSING")

    def test_sha256_mismatch(self):
        with self.fixture() as (root, manifest):
            manifest["frames"][0]["sha256"] = "0" * 64
            self.write_manifest(root, manifest)
            self.assert_issue(root, "HASH_MISMATCH")

    def test_path_traversal_and_windows_aliases(self):
        unsafe = ("../outside.png", "images/../frame.png", "/absolute.png",
                  "C:/outside.png", "//host/share/frame.png", r"images\frame.png",
                  "images/frame.png:stream.png", "images//frame.png", "./frame.png",
                  "images/NUL.png", "images/CON.png", "images /frame.png",
                  "images/frame\x00.png")
        with self.fixture() as (root, manifest):
            for value in unsafe:
                with self.subTest(path=value):
                    manifest["frames"][0]["file"] = value
                    self.write_manifest(root, manifest)
                    report = self.assert_issue(root, "PATH_UNSAFE")
                    self.assertEqual(report.files_checked, 0)

    def test_png_dimension_mismatch(self):
        with self.fixture() as (root, manifest):
            manifest["frames"][0]["width_px"] = 3
            self.write_manifest(root, manifest)
            self.assert_issue(root, "DIMENSION_MISMATCH")

    def test_pixel_format_bit_depth_mismatch(self):
        with self.fixture() as (root, manifest):
            manifest["camera"]["pixel_format"] = "mono16"
            self.write_manifest(root, manifest)
            self.assert_issue(root, "PIXEL_FORMAT_MISMATCH")

    def test_malformed_or_truncated_png(self):
        data = synthetic_png()
        corruptions = (b"not a PNG", data[:8], data[:12], data[:-1],
                       data[:33] + struct.pack(">I", 100000) + b"IDAT")
        with self.fixture() as (root, manifest):
            for index, damaged in enumerate(corruptions):
                with self.subTest(corruption=index):
                    self.replace_png(root, manifest, damaged)
                    self.assert_issue(root, "PNG_INVALID")

    def test_png_crc_failure(self):
        with self.fixture() as (root, manifest):
            damaged = bytearray(synthetic_png())
            damaged[29] ^= 1  # Corrupt only the IHDR checksum, then refresh SHA-256.
            self.replace_png(root, manifest, bytes(damaged))
            report = self.assert_issue(root, "PNG_CRC_INVALID")
            self.assertNotIn("HASH_MISMATCH", [issue.code for issue in report.issues])

    def test_duplicate_frame_index(self):
        with self.fixture() as (root, manifest):
            data = synthetic_png()
            (root / "images/second.png").write_bytes(data)
            second = dict(manifest["frames"][0], file="images/second.png")
            manifest["frames"].append(second)
            self.write_manifest(root, manifest)
            report = self.assert_issue(root, "DUPLICATE_FRAME_INDEX")
            self.assertNotIn("DUPLICATE_FRAME_FILE", [i.code for i in report.issues])

    def test_duplicate_frame_file(self):
        with self.fixture() as (root, manifest):
            manifest["frames"].append(dict(manifest["frames"][0], frame_index=1))
            self.write_manifest(root, manifest)
            report = self.assert_issue(root, "DUPLICATE_FRAME_FILE")
            self.assertNotIn("DUPLICATE_FRAME_INDEX", [i.code for i in report.issues])

    def test_naive_or_invalid_timestamp(self):
        values = ("2000-01-01T00:00:00", "2000-02-30T00:00:00Z",
                  "2000-01-01T00:00:00+24:00", "2000-01-01T00:00:00+00:60",
                  "not a timestamp")
        with self.fixture() as (root, original):
            for location in ("acquired_at", "captured_at"):
                for value in values:
                    with self.subTest(location=location, value=value):
                        manifest = deepcopy(original)
                        target = manifest if location == "acquired_at" else manifest["frames"][0]
                        target[location] = value
                        self.write_manifest(root, manifest)
                        self.assert_issue(root, "TIMESTAMP_INVALID")

    def test_explicit_timestamp_offsets_and_fraction(self):
        with self.fixture() as (root, manifest):
            manifest["acquired_at"] = "2000-01-01T00:00:00.125+04:00"
            manifest["frames"][0]["captured_at"] = "2000-01-01T00:00:00-03:30"
            self.write_manifest(root, manifest)
            self.assertTrue(validate_measurement_bundle(root).valid)

    def run_cli(self, root):
        return subprocess.run(
            [sys.executable, "-B", "-m", "photonicsai_analyst", str(root)],
            cwd=root, capture_output=True, text=True, check=False,
        )

    def test_cli_valid_returns_zero_json_only_and_no_output_file(self):
        with self.fixture() as (root, _):
            names_before = sorted(str(p.relative_to(root)) for p in root.rglob("*"))
            result = self.run_cli(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            self.assertTrue(json.loads(result.stdout)["valid"])
            self.assertEqual(names_before, sorted(str(p.relative_to(root)) for p in root.rglob("*")))

    def test_cli_invalid_returns_two_json_only(self):
        with self.fixture() as (root, manifest):
            del manifest["sample_id"]
            self.write_manifest(root, manifest)
            result = self.run_cli(root)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(result.stderr, "")
            report = json.loads(result.stdout)
            self.assertFalse(report["valid"])
            self.assertIn("FIELD_MISSING", [i["code"] for i in report["issues"]])

    def test_cli_internal_failure_returns_one_and_error_report(self):
        with self.fixture() as (root, _):
            output = io.StringIO()
            with (patch.object(sys, "argv", ["photonicsai_analyst", str(root)]),
                  patch("photonicsai_analyst.__main__.validate_measurement_bundle",
                        side_effect=RuntimeError("injected software-test failure")),
                  redirect_stdout(output)):
                self.assertEqual(main(), 1)
            report = json.loads(output.getvalue())
            self.assertFalse(report["valid"])
            self.assertEqual(report["issues"][0]["code"], "INTERNAL_ERROR")

    def test_cli_usage_returns_two_json_only(self):
        output = io.StringIO()
        with patch.object(sys, "argv", ["photonicsai_analyst"]), redirect_stdout(output):
            self.assertEqual(main(), 2)
        self.assertFalse(json.loads(output.getvalue())["valid"])

    def test_missing_manifest_and_missing_root(self):
        with tempfile.TemporaryDirectory(prefix="photonicsai_c04a_") as directory:
            root = Path(directory)
            self.assert_issue(root, "MANIFEST_NOT_FOUND")
            self.assert_issue(root / "never-created-bundle", "MANIFEST_NOT_FOUND")

    def test_malformed_json_duplicate_keys_and_nonfinite_constants(self):
        with self.fixture() as (root, manifest):
            original = json.dumps(manifest)
            invalid_json = (
                '{"data_origin": "test_fixture",',
                original[:-1] + ', "sample_id": "duplicate-placeholder"}',
                original.replace('"exposure_time": null', '"exposure_time": NaN'),
            )
            for text in invalid_json:
                with self.subTest(text=text):
                    (root / "manifest.json").write_text(text, encoding="utf-8")
                    self.assert_issue(root, "MANIFEST_JSON_INVALID")

    def test_invalid_utf8_manifest(self):
        with self.fixture() as (root, _):
            (root / "manifest.json").write_bytes(b'{"data_origin":"test_fixture","notes":"\xff"}')
            self.assert_issue(root, "MANIFEST_JSON_INVALID")

    def test_manifest_types_and_values(self):
        cases = (("schema_version", 1, "FIELD_TYPE_INVALID"),
                 ("schema_version", "2.0", "FIELD_VALUE_INVALID"),
                 ("measurement_id", "with spaces", "FIELD_VALUE_INVALID"),
                 ("measurement_id", "a" * 129, "FIELD_VALUE_INVALID"),
                 ("operator_id", " ", "FIELD_VALUE_INVALID"),
                 ("sample_id", None, "FIELD_TYPE_INVALID"),
                 ("procedure_id", "", "FIELD_VALUE_INVALID"),
                 ("notes", [], "FIELD_TYPE_INVALID"),
                 ("camera", [], "FIELD_TYPE_INVALID"),
                 ("frames", {}, "FIELD_TYPE_INVALID"),
                 ("frames", [], "FIELD_VALUE_INVALID"),
                 ("frames", [None], "FIELD_TYPE_INVALID"))
        with self.fixture() as (root, original):
            for name, value, code in cases:
                with self.subTest(field=name, value=value):
                    manifest = deepcopy(original)
                    manifest[name] = value
                    self.write_manifest(root, manifest)
                    self.assert_issue(root, code)

    def test_camera_types_and_ranges(self):
        cases = (("manufacturer", "", "FIELD_VALUE_INVALID"),
                 ("model", False, "FIELD_TYPE_INVALID"),
                 ("pixel_format", "rgb8", "FIELD_VALUE_INVALID"),
                 ("roi_px", None, "FIELD_TYPE_INVALID"),
                 ("roi_px", {"x": True, "y": 0, "width": 2, "height": 2}, "FIELD_TYPE_INVALID"),
                 ("roi_px", {"x": -1, "y": 0, "width": 2, "height": 2}, "FIELD_VALUE_INVALID"),
                 ("roi_px", {"x": 0, "y": 0, "width": 0, "height": 2}, "FIELD_VALUE_INVALID"),
                 ("roi_px", {"x": 0, "y": 0, "width": 2}, "FIELD_MISSING"),
                 ("binning", {"x": 0, "y": 1}, "FIELD_VALUE_INVALID"),
                 ("binning", {"x": 1.5, "y": 1}, "FIELD_TYPE_INVALID"),
                 ("exposure_time", [], "FIELD_TYPE_INVALID"),
                 ("exposure_time", {"value": True, "unit": "s"}, "FIELD_TYPE_INVALID"),
                 ("exposure_time", {"value": 0, "unit": "s"}, "FIELD_VALUE_INVALID"),
                 ("exposure_time", {"value": -1, "unit": "s"}, "FIELD_VALUE_INVALID"),
                 ("exposure_time", {"value": 1, "unit": "unknown"}, "FIELD_VALUE_INVALID"),
                 ("exposure_time", {"unit": "s"}, "FIELD_MISSING"),
                 ("exposure_time", {"value": 1}, "FIELD_MISSING"))
        # Numbers above exercise software validation branches, not device settings.
        with self.fixture() as (root, original):
            for name, value, code in cases:
                with self.subTest(field=name, value=value):
                    manifest = deepcopy(original)
                    manifest["camera"][name] = value
                    self.write_manifest(root, manifest)
                    self.assert_issue(root, code)

    def test_exposure_finite_positive_numbers_and_units_without_conversion(self):
        with self.fixture() as (root, manifest):
            for unit in ("us", "ms", "s"):
                with self.subTest(unit=unit):
                    manifest["camera"]["exposure_time"] = {"value": 0.5, "unit": unit}
                    self.write_manifest(root, manifest)
                    self.assertTrue(validate_measurement_bundle(root).valid)
            # A syntactically JSON number overflowing a float must not be accepted.
            text = json.dumps(manifest).replace('"value": 0.5', '"value": 1e999')
            (root / "manifest.json").write_text(text, encoding="utf-8")
            self.assert_issue(root, "FIELD_VALUE_INVALID")

    def test_frame_types_ranges_hash_format_and_extension(self):
        cases = (("frame_index", True, "FIELD_TYPE_INVALID"),
                 ("frame_index", -1, "FIELD_VALUE_INVALID"),
                 ("width_px", 0, "FIELD_VALUE_INVALID"),
                 ("height_px", False, "FIELD_TYPE_INVALID"),
                 ("sha256", "A" * 64, "HASH_FORMAT_INVALID"),
                 ("sha256", "a" * 63, "HASH_FORMAT_INVALID"),
                 ("sha256", None, "HASH_FORMAT_INVALID"),
                 ("file", 1, "FIELD_TYPE_INVALID"),
                 ("file", "images/frame.jpg", "FILE_EXTENSION_INVALID"),
                 ("file", "images/missing.png", "FILE_MISSING"))
        with self.fixture() as (root, original):
            for name, value, code in cases:
                with self.subTest(field=name, value=value):
                    manifest = deepcopy(original)
                    manifest["frames"][0][name] = value
                    self.write_manifest(root, manifest)
                    self.assert_issue(root, code)

    def test_case_insensitive_png_extension(self):
        with self.fixture() as (root, manifest):
            data = synthetic_png()
            (root / "images/upper.PNG").write_bytes(data)
            manifest["frames"][0]["file"] = "images/upper.PNG"
            self.write_manifest(root, manifest)
            self.assertTrue(validate_measurement_bundle(root).valid)

    def test_png_required_chunks_order_lengths_and_termination(self):
        signature = b"\x89PNG\r\n\x1a\n"
        ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", 2, 2, 8, 0, 0, 0, 0))
        idat = chunk(b"IDAT", zlib.compress(b"\x00\x00\x00" * 2))
        iend = chunk(b"IEND")
        cases = (signature + idat + ihdr + iend,
                 signature + ihdr + ihdr + idat + iend,
                 signature + chunk(b"IHDR", b"\x00" * 12) + idat + iend,
                 signature + ihdr + iend,
                 signature + ihdr + idat,
                 signature + ihdr + idat + chunk(b"IEND", b"x"),
                 signature + ihdr + idat + iend + b"trailing",
                 signature + ihdr + idat + iend + iend)
        with self.fixture() as (root, manifest):
            for index, data in enumerate(cases):
                with self.subTest(case=index):
                    self.replace_png(root, manifest, data)
                    self.assert_issue(root, "PNG_INVALID")

    def test_png_header_properties(self):
        cases = ({"width": 0}, {"height": 0}, {"color": 2}, {"color": 4},
                 {"depth": 4}, {"compression": 1}, {"filtering": 1}, {"interlace": 2})
        with self.fixture() as (root, manifest):
            for properties in cases:
                with self.subTest(properties=properties):
                    self.replace_png(root, manifest, synthetic_png(**properties))
                    self.assert_issue(root, "PNG_INVALID")

    def test_interlace_one_container_accepted_without_decoding(self):
        # C04A intentionally does not decode/verify Adam7 scanline content.
        with self.fixture() as (root, manifest):
            self.replace_png(root, manifest, synthetic_png(interlace=1))
            self.assertTrue(validate_measurement_bundle(root).valid)

    def test_directory_is_not_a_frame_file(self):
        with self.fixture() as (root, manifest):
            (root / "images/directory.png").mkdir()
            manifest["frames"][0]["file"] = "images/directory.png"
            self.write_manifest(root, manifest)
            self.assert_issue(root, "FILE_TYPE_INVALID")

    def test_file_symlink_rejected(self):
        with self.fixture() as (root, manifest):
            link = root / "images/link.png"
            try:
                link.symlink_to(root / "images/frame_0000.png")
            except (OSError, NotImplementedError) as error:
                self.skipTest(f"Symlink creation unavailable for this process: {error}")
            manifest["frames"][0]["file"] = "images/link.png"
            self.write_manifest(root, manifest)
            self.assertEqual(self.assert_issue(root, "FILE_SYMLINK_REJECTED").files_checked, 0)

    def test_parent_directory_symlink_rejected(self):
        with self.fixture() as (root, manifest):
            try:
                (root / "linked-images").symlink_to(root / "images", target_is_directory=True)
            except (OSError, NotImplementedError) as error:
                self.skipTest(f"Directory symlink creation unavailable for this process: {error}")
            manifest["frames"][0]["file"] = "linked-images/frame_0000.png"
            self.write_manifest(root, manifest)
            self.assertEqual(self.assert_issue(root, "FILE_SYMLINK_REJECTED").files_checked, 0)

    def test_mocked_symlink_and_reparse_attributes_rejected_before_frame_read(self):
        # Exercise both rejection mechanisms even on Windows without link
        # privileges. These mocks are not evidence of real junction handling.
        with self.fixture() as (root, _):
            original_lstat = Path.lstat
            targets = (root, root / "manifest.json", root / "images",
                       root / "images/frame_0000.png")
            for target in targets:
                for link_kind in ("symlink", "reparse"):
                    with self.subTest(target=target.name, kind=link_kind):
                        def fixture_lstat(path):
                            if path == target:
                                return SimpleNamespace(
                                    st_mode=stat.S_IFLNK if link_kind == "symlink" else stat.S_IFREG,
                                    st_file_attributes=0x400 if link_kind == "reparse" else 0,
                                )
                            return original_lstat(path)

                        with (patch.object(Path, "lstat", fixture_lstat),
                              patch.object(Path, "read_bytes", side_effect=AssertionError(
                                  "Rejected link must not cause frame bytes to be read."))):
                            report = self.assert_issue(root, "FILE_SYMLINK_REJECTED")
                        self.assertEqual(report.files_checked, 0)

    def test_unreadable_frame_becomes_validation_error(self):
        with self.fixture() as (root, _):
            with patch.object(Path, "read_bytes", side_effect=PermissionError("test-only denial")):
                self.assertEqual(self.assert_issue(root, "FILE_UNREADABLE").files_checked, 0)

    def test_temporary_directory_cleanup_on_failure(self):
        root = None
        with self.assertRaisesRegex(RuntimeError, "fixture cleanup probe"):
            with self.fixture() as (root, _):
                self.assertTrue(root.exists())
                raise RuntimeError("fixture cleanup probe")
        self.assertIsNotNone(root)
        self.assertFalse(root.exists())  # Check only this test process's own path.

    def test_public_dataclasses_json_conversion(self):
        issue = ValidationIssue("error", "FIELD_MISSING", "sample_id", "Missing.")
        report = ValidationReport(False, "placeholder-only", issues=[issue])
        self.assertEqual(json.loads(json.dumps(report.to_dict()))["issues"][0]["code"],
                         "FIELD_MISSING")


if __name__ == "__main__":
    unittest.main()
