#!/usr/bin/env python3
"""Test a regex pattern against text or a file, with matches highlighted.

Prints each match with its position and captured groups, and shows the
input with matches wrapped in << >> (or ANSI colour with --color).
"""
import argparse
import re
import sys

FLAG_MAP = {
    "IGNORECASE": re.IGNORECASE, "MULTILINE": re.MULTILINE,
    "DOTALL": re.DOTALL, "VERBOSE": re.VERBOSE, "ASCII": re.ASCII,
}


def highlight(text, matches, color):
    """Return text with each match wrapped in markers or ANSI colour."""
    if not matches:
        return text
    out, last = [], 0
    for match in matches:
        start, end = match.span()
        out.append(text[last:start])
        piece = text[start:end] or "(empty match)"
        if color:
            out.append(f"\x1b[1;32m{piece}\x1b[0m")
        else:
            out.append(f"<<{piece}>>")
        last = end
    out.append(text[last:])
    return "".join(out)


def main():
    parser = argparse.ArgumentParser(
        description="Test a regex pattern against text or a file.")
    parser.add_argument("pattern", help="Regular expression to test")
    parser.add_argument("text", nargs="?",
                        help="Text to test (omit when using --file)")
    parser.add_argument("--file", help="Read the text to test from a file")
    parser.add_argument("--flags", default="",
                        help="Comma-separated flags: IGNORECASE,MULTILINE,DOTALL,"
                             "VERBOSE,ASCII")
    parser.add_argument("--color", action="store_true",
                        help="Highlight matches with ANSI colour instead of << >>")
    parser.add_argument("--count-only", action="store_true",
                        help="Only print the number of matches")
    parser.add_argument("--max-matches", type=int, default=20,
                        help="Maximum matches to list in detail (default: 20)")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as exc:
            print(f"Error: cannot read file: {exc}", file=sys.stderr)
            return 1
    elif args.text is not None:
        text = args.text
    else:
        print("Error: provide text or --file", file=sys.stderr)
        return 1

    flags = 0
    for name in args.flags.split(","):
        name = name.strip().upper()
        if not name:
            continue
        if name not in FLAG_MAP:
            print(f"Error: unknown flag {name!r} (try IGNORECASE, MULTILINE, "
                  "DOTALL, VERBOSE, ASCII)", file=sys.stderr)
            return 1
        flags |= FLAG_MAP[name]

    try:
        regex = re.compile(args.pattern, flags)
    except re.error as exc:
        print(f"Error: invalid regex: {exc}", file=sys.stderr)
        return 1

    matches = list(regex.finditer(text))
    print(f"Pattern: {args.pattern!r}")
    print(f"Matches: {len(matches)}")
    if args.count_only:
        return 0 if matches else 1
    if not matches:
        print("No matches found.")
        return 1

    for i, match in enumerate(matches[:args.max_matches], 1):
        groups = match.groups()
        print(f"  {i}. [{match.start()}:{match.end()}] {match.group()!r}"
              + (f"  groups={groups}" if groups else ""))
    if len(matches) > args.max_matches:
        print(f"  ... and {len(matches) - args.max_matches} more")
    print("\nHighlighted text:")
    print(highlight(text, matches, args.color))
    return 0


if __name__ == "__main__":
    sys.exit(main())
