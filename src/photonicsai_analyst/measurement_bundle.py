"""Read-only metadata, integrity, and PNG-container checks; no pixel analysis.

Validity describes the proposed interchange contract only. Neither provenance,
scientific correctness, image quality, nor hardware safety is authenticated.
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime
import hashlib
import json
import math
import os
from pathlib import Path, PureWindowsPath
import re
import stat
import struct
from typing import Literal
import zlib


@dataclass
class ValidationIssue:
    severity: Literal["error", "warning"]
    code: str
    path: str
    message: str


@dataclass
class ValidationReport:
    valid: bool
    bundle_root: str
    measurement_id: str | None = None
    data_origin: str | None = None
    files_checked: int = 0
    issues: list[ValidationIssue] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Return a fresh JSON-serializable dictionary."""
        return asdict(self)

    def _error(self, code: str, path: str, message: str) -> None:
        self.valid = False
        self.issues.append(ValidationIssue("error", code, path, message))


_MISSING = object()
_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
_TIMESTAMP = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
    r"(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})"
)


def _required(obj: dict, name: str, path: str, report: ValidationReport):
    if name not in obj:
        report._error("FIELD_MISSING", path, "Required field is missing.")
        return _MISSING
    return obj[name]


def _string(value, path: str, report: ValidationReport, *, nullable=False,
            empty=False) -> bool:
    if value is _MISSING:
        return False
    if value is None and nullable:
        return True
    if not isinstance(value, str):
        report._error("FIELD_TYPE_INVALID", path, "Expected a string" +
                      (" or null." if nullable else "."))
        return False
    if not empty and not value.strip():
        report._error("FIELD_VALUE_INVALID", path, "String must not be blank.")
        return False
    return True


def _object(value, path: str, report: ValidationReport) -> bool:
    if value is _MISSING:
        return False
    if not isinstance(value, dict):
        report._error("FIELD_TYPE_INVALID", path, "Expected an object.")
        return False
    return True


def _integer(value, minimum: int, path: str, report: ValidationReport) -> bool:
    if value is _MISSING:
        return False
    # JSON booleans are not integers in this contract.
    if type(value) is not int:
        report._error("FIELD_TYPE_INVALID", path, "Expected an integer.")
        return False
    if value < minimum:
        report._error("FIELD_VALUE_INVALID", path,
                      f"Integer must be at least {minimum}.")
        return False
    return True


def _timestamp(value, path: str, report: ValidationReport) -> None:
    if not _string(value, path, report):
        return
    try:
        if not _TIMESTAMP.fullmatch(value):
            raise ValueError
        # datetime checks the calendar; check offset components explicitly
        # because fromisoformat accepts some overflowing offset components.
        if not value.endswith("Z"):
            if int(value[-5:-3]) > 23 or int(value[-2:]) > 59:
                raise ValueError
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.utcoffset() is None:
            raise ValueError
    except (ValueError, OverflowError):
        report._error("TIMESTAMP_INVALID", path,
                      "Use a valid YYYY-MM-DDTHH:MM:SS[.fraction]"
                      " timestamp ending in Z or an explicit +/-HH:MM offset.")


def _camera(value, report: ValidationReport) -> str | None:
    if not _object(value, "camera", report):
        return None
    for name in ("manufacturer", "model"):
        _string(_required(value, name, f"camera.{name}", report),
                f"camera.{name}", report, nullable=True)
    pixel_format = _required(value, "pixel_format", "camera.pixel_format", report)
    if _string(pixel_format, "camera.pixel_format", report):
        if pixel_format not in ("mono8", "mono16"):
            report._error("FIELD_VALUE_INVALID", "camera.pixel_format",
                          "Expected mono8 or mono16.")
            pixel_format = None
    else:
        pixel_format = None
    exposure = _required(value, "exposure_time", "camera.exposure_time", report)
    if exposure is not None and _object(exposure, "camera.exposure_time", report):
        number = _required(exposure, "value", "camera.exposure_time.value", report)
        if number is not _MISSING:
            if type(number) not in (int, float):
                report._error("FIELD_TYPE_INVALID", "camera.exposure_time.value",
                              "Expected a finite positive number.")
            elif number <= 0 or (isinstance(number, float) and not math.isfinite(number)):
                report._error("FIELD_VALUE_INVALID", "camera.exposure_time.value",
                              "Expected a finite positive number.")
        unit = _required(exposure, "unit", "camera.exposure_time.unit", report)
        if _string(unit, "camera.exposure_time.unit", report):
            if unit not in ("us", "ms", "s"):
                report._error("FIELD_VALUE_INVALID", "camera.exposure_time.unit",
                              "Expected us, ms, or s; no unit conversion is performed.")
    for name, fields in (("roi_px", (("x", 0), ("y", 0), ("width", 1), ("height", 1))),
                         ("binning", (("x", 1), ("y", 1)))):
        location = f"camera.{name}"
        item = _required(value, name, location, report)
        if _object(item, location, report):
            for key, minimum in fields:
                _integer(_required(item, key, f"{location}.{key}", report),
                         minimum, f"{location}.{key}", report)
    return pixel_format


def _is_link(info: os.stat_result) -> bool:
    # Windows junctions and other reparse points must not escape containment.
    return (stat.S_ISLNK(info.st_mode) or
            bool(getattr(info, "st_file_attributes", 0) &
                 getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)))


def _safe_file(root: Path, parts: list[str], location: str,
               report: ValidationReport, *, manifest=False) -> Path | None:
    candidate = root
    try:
        for part in parts:
            candidate = candidate / part
            info = candidate.lstat()
            if _is_link(info):
                report._error("FILE_SYMLINK_REJECTED", location,
                              "Symlinks and reparse points are not accepted, including parent directories.")
                return None
        resolved = candidate.resolve()
        if not resolved.is_relative_to(root):
            report._error("PATH_UNSAFE", location, "Path resolves outside the bundle root.")
            return None
        if not stat.S_ISREG(info.st_mode):
            report._error("FILE_TYPE_INVALID", location, "Expected a regular file.")
            return None
        return resolved
    except FileNotFoundError:
        report._error("MANIFEST_NOT_FOUND" if manifest else "FILE_MISSING",
                      location, "Required file does not exist.")
    except (OSError, ValueError, RuntimeError):
        report._error("FILE_UNREADABLE", location, "Cannot safely access the required file.")
    return None


def _frame_parts(value, path: str, report: ValidationReport) -> list[str] | None:
    if not _string(value, path, report):
        return None
    parts = value.split("/")
    # Reject Windows drives, UNC paths, device paths and alternate data streams
    # even when the validator is run on a POSIX system.
    if ("\\" in value or ":" in value or "\x00" in value or
            any(p in ("", ".", "..") or p.endswith((".", " ")) or
                PureWindowsPath(p).is_reserved() for p in parts)):
        report._error("PATH_UNSAFE", path,
                      "Use a relative POSIX path with no traversal, aliases, drives, or device names.")
        return None
    if not value.lower().endswith(".png"):
        report._error("FILE_EXTENSION_INVALID", path, "Frame path must end in .png.")
        return None
    return parts


def _png(data: bytes, location: str, pixel_format: str | None,
         width, height, report: ValidationReport) -> None:
    def invalid(message):
        report._error("PNG_INVALID", location, message)

    if not data.startswith(_PNG_SIGNATURE):
        invalid("PNG signature is missing or invalid.")
        return
    offset = len(_PNG_SIGNATURE)
    ihdr_seen = idat_seen = False
    while offset < len(data):
        if len(data) - offset < 12:
            invalid("Truncated PNG chunk header or trailer.")
            return
        length, kind = struct.unpack_from(">I4s", data, offset)
        end = offset + 12 + length
        if length > 0x7FFFFFFF or end > len(data):
            invalid("Invalid chunk length or truncated PNG chunk.")
            return
        payload = data[offset + 8:end - 4]
        stored_crc = struct.unpack_from(">I", data, end - 4)[0]
        if zlib.crc32(kind + payload) & 0xFFFFFFFF != stored_crc:
            report._error("PNG_CRC_INVALID", location, "PNG chunk CRC does not match its bytes.")
            return
        if not re.fullmatch(rb"[A-Za-z]{4}", kind) or kind[2] & 32:
            invalid("Invalid PNG chunk type or reserved bit.")
            return
        if not ihdr_seen and kind != b"IHDR":
            invalid("IHDR must be the first PNG chunk.")
            return
        if kind == b"IHDR":
            if ihdr_seen or length != 13:
                invalid("IHDR must appear exactly once with length 13.")
                return
            ihdr_seen = True
            actual_w, actual_h, depth, color, compression, filtering, interlace = (
                struct.unpack(">IIBBBBB", payload))
            if actual_w == 0 or actual_h == 0:
                invalid("PNG width and height must be positive.")
            if color != 0:
                invalid("Only PNG color type 0 (grayscale) is supported.")
            if depth not in (8, 16):
                invalid("Only 8-bit or 16-bit PNG samples are supported.")
            if pixel_format in ("mono8", "mono16") and depth != {"mono8": 8, "mono16": 16}[pixel_format]:
                report._error("PIXEL_FORMAT_MISMATCH", location,
                              "PNG bit depth does not match camera.pixel_format.")
            if compression != 0 or filtering != 0 or interlace not in (0, 1):
                invalid("Unsupported PNG compression, filter, or interlace method.")
            if ((width is not None and actual_w != width) or
                    (height is not None and actual_h != height)):
                report._error("DIMENSION_MISMATCH", location,
                              "PNG dimensions differ from frame metadata.")
        elif kind == b"IDAT":
            idat_seen = True
        elif kind == b"IEND":
            if length != 0:
                invalid("IEND must have an empty payload.")
            if not idat_seen:
                invalid("At least one IDAT chunk is required.")
            if end != len(data):
                invalid("IEND must terminate the file; trailing bytes are not allowed.")
            return
        offset = end
    invalid("PNG is missing its terminating IEND chunk.")


def _json_object(pairs: list[tuple]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON object member.")
        result[key] = value
    return result


def _reject_constant(value: str):
    raise ValueError("Non-finite JSON constants are not allowed.")


def validate_measurement_bundle(bundle_root: Path) -> ValidationReport:
    """Check an explicitly supplied, stable offline bundle without modifying it.

    Ordinary invalid inputs become issues. No directory enumeration, pixel
    decompression, camera identification, or scientific interpretation occurs.
    """
    root = Path(bundle_root)
    report = ValidationReport(valid=True, bundle_root=str(root))
    try:
        info = root.lstat()
        if _is_link(info):
            report._error("FILE_SYMLINK_REJECTED", "bundle_root",
                          "Bundle root must not be a symlink or reparse point.")
            return report
        if not stat.S_ISDIR(info.st_mode):
            report._error("FIELD_TYPE_INVALID", "bundle_root", "Expected a directory.")
            return report
        root = root.resolve()
        report.bundle_root = str(root)
    except FileNotFoundError:
        report._error("MANIFEST_NOT_FOUND", "manifest.json", "Bundle root does not exist.")
        return report
    except (OSError, ValueError, RuntimeError):
        report._error("PATH_UNSAFE", "bundle_root", "Cannot resolve the bundle root.")
        return report
    manifest_path = _safe_file(root, ["manifest.json"], "manifest.json", report, manifest=True)
    if manifest_path is None:
        return report
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"),
                              object_pairs_hook=_json_object,
                              parse_constant=_reject_constant)
    except (ValueError, UnicodeError, RecursionError):
        report._error("MANIFEST_JSON_INVALID", "manifest.json",
                      "Expected UTF-8 JSON with unique object keys and no non-finite constants.")
        return report
    except OSError:
        report._error("FILE_UNREADABLE", "manifest.json", "Cannot read the manifest.")
        return report
    if not _object(manifest, "manifest.json", report):
        return report
    for name in ("schema_version", "measurement_id", "data_origin", "operator_id", "sample_id"):
        value = _required(manifest, name, name, report)
        if not _string(value, name, report):
            continue
        if name == "schema_version" and value != "1.0":
            report._error("FIELD_VALUE_INVALID", name, "Expected schema version 1.0.")
        elif name == "measurement_id":
            report.measurement_id = value
            if not re.fullmatch(r"[A-Za-z0-9._-]{1,128}", value):
                report._error("FIELD_VALUE_INVALID", name, "Identifier must match [A-Za-z0-9._-]{1,128}.")
        elif name == "data_origin":
            report.data_origin = value
            if value not in ("real_measurement", "test_fixture"):
                report._error("FIELD_VALUE_INVALID", name, "Expected real_measurement or test_fixture.")
    _timestamp(_required(manifest, "acquired_at", "acquired_at", report), "acquired_at", report)
    _string(_required(manifest, "procedure_id", "procedure_id", report),
            "procedure_id", report, nullable=True)
    _string(_required(manifest, "notes", "notes", report),
            "notes", report, nullable=True, empty=True)
    pixel_format = _camera(_required(manifest, "camera", "camera", report), report)
    frames = _required(manifest, "frames", "frames", report)
    if frames is _MISSING:
        return report
    if not isinstance(frames, list):
        report._error("FIELD_TYPE_INVALID", "frames", "Expected a list.")
        return report
    if not frames:
        report._error("FIELD_VALUE_INVALID", "frames", "At least one frame is required.")
    indices = set()
    files = set()
    for index, frame in enumerate(frames):
        location = f"frames[{index}]"
        if not _object(frame, location, report):
            continue
        frame_index = _required(frame, "frame_index", f"{location}.frame_index", report)
        if _integer(frame_index, 0, f"{location}.frame_index", report):
            if frame_index in indices:
                report._error("DUPLICATE_FRAME_INDEX", f"{location}.frame_index", "Frame index is repeated.")
            indices.add(frame_index)
        _timestamp(_required(frame, "captured_at", f"{location}.captured_at", report),
                   f"{location}.captured_at", report)
        dimensions = []
        for name in ("width_px", "height_px"):
            value = _required(frame, name, f"{location}.{name}", report)
            dimensions.append(value if _integer(value, 1, f"{location}.{name}", report) else None)
        expected_hash = _required(frame, "sha256", f"{location}.sha256", report)
        hash_ok = isinstance(expected_hash, str) and bool(re.fullmatch(r"[0-9a-f]{64}", expected_hash))
        if expected_hash is not _MISSING and not hash_ok:
            report._error("HASH_FORMAT_INVALID", f"{location}.sha256", "Expected 64 lowercase hexadecimal characters.")
        file_value = _required(frame, "file", f"{location}.file", report)
        parts = _frame_parts(file_value, f"{location}.file", report)
        if parts is None:
            continue
        file_key = os.path.normcase("/".join(parts))
        if file_key in files:
            report._error("DUPLICATE_FRAME_FILE", f"{location}.file", "Frame file path is repeated.")
        files.add(file_key)
        file_path = _safe_file(root, parts, f"{location}.file", report)
        if file_path is None:
            continue
        try:
            data = file_path.read_bytes()
        except OSError:
            report._error("FILE_UNREADABLE", f"{location}.file", "Cannot read frame bytes.")
            continue
        report.files_checked += 1
        if hash_ok and hashlib.sha256(data).hexdigest() != expected_hash:
            report._error("HASH_MISMATCH", f"{location}.sha256", "SHA-256 does not match frame file bytes.")
        _png(data, file_value, pixel_format, *dimensions, report)
    return report
