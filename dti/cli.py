"""Command line: `dti list` and `dti run <report> [--date YYYY-MM-DD] [--dry-run]`."""

import argparse
import sys
from datetime import date
from pathlib import Path

from dti.reports.base import REGISTRY, get_report


def _cmd_list(_args) -> int:
    import dti.reports  # noqa: F401

    for name in sorted(REGISTRY):
        print(f"{name:30} {REGISTRY[name].title}")
    return 0


def _cmd_run(args) -> int:
    run_date = date.fromisoformat(args.date) if args.date else date.today()
    draft = get_report(args.report)(run_date).run()

    out = Path(args.out) / f"{run_date.isoformat()}_{draft.report}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(draft.html, encoding="utf-8")
    print(f"{draft.subject}: {'EMPTY' if draft.empty else 'ok'}, {len(draft.flags)} flag(s) -> {out}")
    for f in draft.flags:
        print(f"  ! {f.item + ': ' if f.item else ''}{f.message}")

    if not args.dry_run:
        from dti import store

        with store.connect() as conn:
            print(f"saved draft #{store.save_draft(conn, draft)} for review")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="dti", description="Daily Trading Info automation")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="list available reports").set_defaults(func=_cmd_list)

    r = sub.add_parser("run", help="run one report and write its HTML draft")
    r.add_argument("report")
    r.add_argument("--date", help="run date YYYY-MM-DD (default: today)")
    r.add_argument("--out", default="out", help="directory for rendered HTML (default: out/)")
    r.add_argument("--dry-run", action="store_true", help="render only; don't save a draft for review")
    r.set_defaults(func=_cmd_run)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
