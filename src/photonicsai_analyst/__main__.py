"""Print a validation report as JSON; never persist a report or alter inputs."""

import json
from pathlib import Path
import sys

from .measurement_bundle import ValidationIssue, ValidationReport, validate_measurement_bundle


def main() -> int:
    arguments = sys.argv[1:]
    if len(arguments) != 1:
        report = ValidationReport(False, "", issues=[ValidationIssue(
            "error", "CLI_USAGE_INVALID", "bundle_root",
            "Usage: python -m photonicsai_analyst <bundle_root>",
        )])
        status = 2
    else:
        try:
            report = validate_measurement_bundle(Path(arguments[0]))
            status = 0 if report.valid else 2
        except Exception:
            # Avoid tracebacks or unrelated environment details in stdout.
            report = ValidationReport(False, arguments[0], issues=[ValidationIssue(
                "error", "INTERNAL_ERROR", "bundle_root",
                "Unexpected internal validation failure; no valid result is available.",
            )])
            status = 1
    print(json.dumps(report.to_dict(), allow_nan=False))
    return status


if __name__ == "__main__":
    sys.exit(main())
