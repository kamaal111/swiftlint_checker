import subprocess
from typing import Optional

SWIFTLINT_APP = "/usr/local/bin/swiftlint"


def main():
    process = subprocess.Popen(f"{SWIFTLINT_APP}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.stdout.readlines()
    if len(output) < 1:
        raise Exception("No output from swiftlint")

    result = output[-1].decode("utf-8").strip()
    swiftlint_result = SwiftlintResult(result)

    if swiftlint_result.serious is None:
        raise Exception("Could not parse serious count")

    if swiftlint_result.serious > 0:
        raise Exception(f"{swiftlint_result.serious} serious issues found")

    print(f"Swiftlint found no serious issues and found {swiftlint_result.violations} violations")


class SwiftlintResult(object):
    violations: Optional[int] = None
    serious: Optional[int] = None

    def __init__(self, result: str):
        splitted_result = result.split(" ")
        if len(splitted_result) < 6:
            return

        violations = splitted_result[3]
        serious = splitted_result[5]
        try:
            self.violations = int(violations)
            self.serious = int(serious)
        except (ValueError, TypeError):
            return


main()
