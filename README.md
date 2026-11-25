# regex-tester

Test a regex pattern against text or a file, with matches highlighted and captured groups shown.

## Requirements

- Python 3 (standard library only — no third-party packages)

## How to run

```bash
cd 058-regex-tester
python3 main.py '\d+' 'order 123 shipped'
```

Run `python3 main.py --help` to see all options.

## Example

```bash
python3 main.py '\d+' 'order 123 shipped'
```

Sample output:

```
Pattern: '\\d+'
Matches: 1
  1. [6:9] '123'

Highlighted text:
order <<123>> shipped
```

## Notes

Use `--file` to test a file instead of inline text, `--flags IGNORECASE,MULTILINE` for regex flags, `--color` for ANSI highlighting instead of `<< >>`, and `--count-only` to print just the match count.

## License

MIT — see [LICENSE](LICENSE).
