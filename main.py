import subprocess
from typing import List
from dataclasses import dataclass

SWIFTLINT_APP = "/usr/local/bin/swiftlint"


def main():
    output = subprocess.getoutput(f"{SWIFTLINT_APP}")
    swiftlint_result = SwiftlintResult.from_swiftlint_output(output=output)

    if swiftlint_result.serious > 0:
        raise Exception(
            f"{swiftlint_result.serious} serious issues found.\n{swiftlint_result.listed_errors}"
        )

    print(
        f"Swiftlint found no serious issues and found {swiftlint_result.violations} violations.\n{swiftlint_result.listed_warning}"
    )


@dataclass
class SwiftlintResult:
    warnings: List[str]
    errors: List[str]

    @property
    def violations(self):
        return len(self.warnings)

    @property
    def serious(self):
        return len(self.errors)

    @property
    def listed_warning(self):
        return "\n".join(self.warnings)

    @property
    def listed_errors(self):
        return "\n".join(self.errors)

    @staticmethod
    def from_swiftlint_output(output: str):
        output_line_by_line = output.splitlines()

        warnings: List[str] = []
        errors: List[str] = []
        for line in output_line_by_line[1:]:
            if "Linting '" in line:
                continue

            if ": warning: " in line:
                warnings.append(line)
                continue

            if ": error: " in line:
                errors.append(line)
                continue

        return SwiftlintResult(warnings=warnings, errors=errors)


main()
