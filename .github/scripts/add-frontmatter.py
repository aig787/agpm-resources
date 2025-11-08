#!/usr/bin/env python3
"""
Add minimal YAML frontmatter to snippet files that don't have it.

This script adds basic frontmatter with agpm.version field to enable
versioning for all snippet artifacts.
"""

import sys
from pathlib import Path
from typing import List


# Files that should have frontmatter added
TARGET_FILES = [
    # Snippet agents without frontmatter
    "snippets/agents/general-purpose.md",
    "snippets/agents/git-expert.md",
    "snippets/agents/github-actions-expert.md",
    "snippets/agents/kubernetes-expert.md",
    # Best practices
    "snippets/best-practices/golang-best-practices.md",
    "snippets/best-practices/java-best-practices.md",
    "snippets/best-practices/javascript-best-practices.md",
    "snippets/best-practices/python-best-practices.md",
    "snippets/best-practices/rust-best-practices.md",
    "snippets/best-practices/typescript-best-practices.md",
    # Styleguides
    "snippets/styleguides/golang-styleguide.md",
    "snippets/styleguides/java-styleguide.md",
    "snippets/styleguides/javascript-styleguide.md",
    "snippets/styleguides/python-styleguide.md",
    "snippets/styleguides/rust-styleguide.md",
    "snippets/styleguides/typescript-styleguide.md",
    # Commands
    "snippets/commands/checkpoint.md",
    "snippets/commands/gh-pr-create.md",
    "snippets/commands/review-docs.md",
    "snippets/commands/squash.md",
    "snippets/commands/update-agentic-context.md",
    "snippets/commands/update-docs.md",
    "snippets/commands/update-docstrings.md",
    # Rules
    "snippets/rules/commit-attribution.md",
    "snippets/rules/pr-self-review.md",
]


def has_frontmatter(content: str) -> bool:
    """Check if content already has YAML frontmatter."""
    return content.startswith('---\n')


def add_frontmatter(filepath: Path, default_version: str = "1.0.0", dry_run: bool = False) -> bool:
    """
    Add minimal frontmatter to a file.

    Returns True if frontmatter was added, False if it already existed.
    """
    if not filepath.exists():
        print(f"Warning: File not found: {filepath}", file=sys.stderr)
        return False

    content = filepath.read_text(encoding='utf-8')

    if has_frontmatter(content):
        print(f"✓ {filepath}: already has frontmatter")
        return False

    # Create minimal frontmatter with version
    frontmatter = f"""---
agpm:
  version: "{default_version}"
---

"""

    # Prepend frontmatter to content
    updated_content = frontmatter + content

    if not dry_run:
        filepath.write_text(updated_content, encoding='utf-8')
        print(f"+ {filepath}: added frontmatter with version {default_version}")
    else:
        print(f"+ {filepath}: would add frontmatter with version {default_version}")

    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Add frontmatter to snippet files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    parser.add_argument(
        '--default-version',
        default='1.0.0',
        help='Default version to use (default: 1.0.0)'
    )

    args = parser.parse_args()

    print("Adding frontmatter to snippet files")
    print("=" * 50)

    if args.dry_run:
        print("DRY-RUN mode: No files will be modified")

    print()

    added_count = 0
    skipped_count = 0

    for filepath_str in TARGET_FILES:
        filepath = Path(filepath_str)
        was_added = add_frontmatter(filepath, args.default_version, args.dry_run)

        if was_added:
            added_count += 1
        else:
            skipped_count += 1

    print()
    print("=" * 50)
    print(f"Processed: {len(TARGET_FILES)} files")
    print(f"Added frontmatter: {added_count} files")
    print(f"Already had frontmatter: {skipped_count} files")

    if args.dry_run:
        print()
        print("DRY-RUN: No files were actually modified")
        print("Run without --dry-run to apply changes")


if __name__ == '__main__':
    main()
