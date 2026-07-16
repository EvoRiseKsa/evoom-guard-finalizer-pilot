from __future__ import annotations

import sys

from calc.ops import add


def main(argv: list[str]) -> int:
    if len(argv) != 4 or argv[1] != "add":
        print("usage: python -m calc add <left> <right>", file=sys.stderr)
        return 2
    print(add(int(argv[2]), int(argv[3])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
