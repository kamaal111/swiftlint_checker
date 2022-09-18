import subprocess
from typing import Optional
from dataclasses import dataclass

SWIFTLINT_APP = "/usr/local/bin/swiftlint"


def main():
    output = subprocess.getoutput(f"{SWIFTLINT_APP}")

    result = output.splitlines()[-1].strip()
    swiftlint_result = SwiftlintResult.from_swiftlint_result(result=result)

    if swiftlint_result.serious is None:
        raise Exception("Could not parse serious count")

    if swiftlint_result.serious > 0:
        raise Exception(f"{swiftlint_result.serious} serious issues found")

    print(
        f"Swiftlint found no serious issues and found {swiftlint_result.violations} violations"
    )


@dataclass
class SwiftlintResult:
    violations: Optional[int] = None
    serious: Optional[int] = None

    @staticmethod
    def from_swiftlint_result(result: str):
        splitted_result = result.split(" ")
        if len(splitted_result) < 6:
            return

        violations = splitted_result[3]
        serious = splitted_result[5]
        try:
            amount_of_violation_warnings = int(violations)
            amount_of_serious_errors = int(serious)
        except (ValueError, TypeError):
            return

        return SwiftlintResult(
            violations=amount_of_violation_warnings, serious=amount_of_serious_errors
        )


main()
