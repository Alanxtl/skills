#!/usr/bin/env python3
"""Initialize a paper reproduction workspace from bundled templates."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TEMPLATE_FILES = [
    "paper_brief.md",
    "artifact_inventory.md",
    "implementation_plan.md",
    "gap_tracker.md",
    "experiment_log.csv",
    "validation_report.md",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a standard reproduction workspace for one paper."
    )
    parser.add_argument("--title", required=True, help="Human-readable paper title.")
    parser.add_argument(
        "--slug",
        required=True,
        help="Lowercase hyphen-case identifier, for example my-paper-2024.",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Base output directory. The script creates <out>/<slug>/.",
    )
    return parser.parse_args()


def validate_slug(slug: str) -> None:
    if not SLUG_PATTERN.fullmatch(slug):
        raise ValueError(
            "Invalid slug. Use lowercase letters, digits, and single hyphens only."
        )


def render_text(text: str, title: str, slug: str, created_date: str) -> str:
    return (
        text.replace("__PAPER_TITLE__", title)
        .replace("__PAPER_SLUG__", slug)
        .replace("__DATE_CREATED__", created_date)
    )


def init_workspace(title: str, slug: str, out_dir: Path) -> tuple[Path, list[Path]]:
    template_dir = Path(__file__).resolve().parent.parent / "assets" / "templates"
    if not template_dir.is_dir():
        raise FileNotFoundError(f"Template directory not found: {template_dir}")

    case_dir = out_dir / slug
    if case_dir.exists():
        raise FileExistsError(f"Output directory already exists: {case_dir}")

    case_dir.mkdir(parents=True, exist_ok=False)
    created_date = datetime.now().date().isoformat()
    created_files: list[Path] = []

    for template_name in TEMPLATE_FILES:
        template_path = template_dir / template_name
        if not template_path.is_file():
            raise FileNotFoundError(f"Template file not found: {template_path}")

        target_path = case_dir / template_name
        rendered = render_text(
            template_path.read_text(encoding="utf-8"),
            title=title,
            slug=slug,
            created_date=created_date,
        )
        target_path.write_text(rendered, encoding="utf-8")
        created_files.append(target_path)

    return case_dir, created_files


def main() -> int:
    args = parse_args()

    try:
        validate_slug(args.slug)
        case_dir, created_files = init_workspace(
            title=args.title,
            slug=args.slug,
            out_dir=Path(args.out).expanduser().resolve(),
        )
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(f"[OK] Created reproduction workspace: {case_dir}")
    for path in created_files:
        print(f"[OK] Created {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
