"""Compare the compiled solution with a simple interval-list model."""

import random
import subprocess
import sys


def check(executable, operations):
    intervals = []
    expected = []
    for operation in operations:
        if operation == "B":
            expected.append(len(intervals))
        else:
            _, left, right = operation.split()
            left, right = int(left), int(right)
            remaining = [(a, b) for a, b in intervals if b < left or a > right]
            expected.append(len(intervals) - len(remaining))
            intervals = remaining + [(left, right)]
    data = str(len(operations)) + "\n" + "\n".join(operations) + "\n"
    result = subprocess.run(
        [executable], input=data, text=True, capture_output=True, check=True
    )
    actual = list(map(int, result.stdout.split()))
    assert actual == expected, (operations, expected, actual)


def main():
    executable = sys.argv[1] if len(sys.argv) > 1 else "./code"
    check(executable, ["A 10 15", "A 17 19", "A 12 17", "A 90 99", "A 11 12", "B"])
    check(executable, ["B", "A 1 1", "A 100000 100000", "B", "A 1 100000", "B",
                       "A 2 3", "A 3 4", "A 3 4", "A 5 5", "B"])
    randomizer = random.Random(2673)
    for _ in range(200):
        operations = []
        for _ in range(500):
            if randomizer.randrange(4) == 0:
                operations.append("B")
            else:
                left = randomizer.randint(1, 100)
                right = randomizer.randint(left, 100)
                operations.append(f"A {left} {right}")
        check(executable, operations)
    operations = [f"A {i} {i}" for i in range(1, 100001)]
    operations += ["A 1 100000", "B"] + ["A 1 1"] * 99998
    result = subprocess.run(
        [executable], input="200000\n" + "\n".join(operations) + "\n",
        text=True, capture_output=True, check=True, timeout=2,
    )
    assert list(map(int, result.stdout.split())) == [0] * 100000 + [100000] + [1] * 99999
    print("Passed sample, boundary, 200 randomized, and maximum-size cases.")


if __name__ == "__main__":
    main()
