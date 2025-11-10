#!/usr/bin/env python3
"""
Bootstrap version script for AGPM artifacts.

This script:
1. Finds all artifact files in the repository
2. Adds initial version to frontmatter (if not present)
3. Generates initial git tags for all artifacts
4. Creates a summary report

Usage:
    python bootstrap-versions.py [--dry-run] [--default-version VERSION] [--output TAGS_FILE]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# Artifact patterns to process
ARTIFACT_PATTERNS = [
    'snippets/**/*.md',
    'claude-code/**/*.md',
    'opencode/**/*.md',
    'claude-code/hooks/*.json',
    'claude-code/mcp-servers/*.json',
    'opencode/mcp-servers/*.json',
]

# Files to exclude
EXCLUDE_FILES = [
    'README.md',
    'CLAUDE.md',
    'AGENTS.md',
]


def parse_frontmatter(content: str) -> Tuple[Optional[Dict], str, str]:
    """
    Parse YAML frontmatter from markdown content.

    Returns:
        Tuple of (frontmatter_dict, frontmatter_text, body_text)
    """
    # Match YAML frontmatter (--- at start and end)
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return None, "", content

    frontmatter_text = match.group(1)
    body = match.group(2)

    # Simple YAML parsing (for version field only)
    frontmatter = {}

    # Parse nested agpm.version field
    in_agpm_section = False
    for line in frontmatter_text.split('\n'):
        stripped = line.strip()

        # Detect agpm section
        if stripped == 'agpm:':
            in_agpm_section = True
            continue

        # If we're in agpm section, look for version
        if in_agpm_section:
            # Check if we've left the agpm section (non-indented key)
            if stripped and not line.startswith(' ') and not line.startswith('\t'):
                in_agpm_section = False
            elif 'version:' in stripped:
                # Extract version value
                version_match = re.search(r'version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)["\']?', stripped)
                if version_match:
                    frontmatter['version'] = version_match.group(1)

    return frontmatter, frontmatter_text, body


def parse_json_agpm_version(content: str) -> Tuple[Optional[str], bool]:
    """
    Parse JSON content to extract agpm.version.

    Returns:
        Tuple of (version, is_valid_json)
    """
    try:
        data = json.loads(content)
        if isinstance(data, dict) and 'agpm' in data:
            agpm_section = data['agpm']
            if isinstance(agpm_section, dict) and 'version' in agpm_section:
                return agpm_section['version'], True
        return None, True
    except json.JSONDecodeError:
        return None, False


def update_frontmatter_version(frontmatter_text: str, version: str) -> str:
    """
    Update version in frontmatter text.

    Args:
        frontmatter_text: Original YAML frontmatter text
        version: Version to set

    Returns:
        Updated frontmatter text
    """
    # Check if agpm.version already exists
    if re.search(r'agpm:\s*\n.*?version:', frontmatter_text, re.DOTALL):
        # Update existing version
        updated = re.sub(
            r'(agpm:\s*\n(?:.*\n)*?.*version:\s*)["\']?[0-9]+\.[0-9]+\.[0-9]+["\']?',
            f'\\1"{version}"',
            frontmatter_text,
            count=1
        )
    else:
        # Add version to existing agpm section or create new agpm section
        if 'agpm:' in frontmatter_text:
            # Add version to existing agpm section
            updated = re.sub(
                r'(agpm:)\s*\n',
                f'\\1\n  version: "{version}"\n',
                frontmatter_text,
                count=1
            )
        else:
            # Add new agpm section at the end
            updated = frontmatter_text + f'\nagpm:\n  version: "{version}"'

    return updated


def parse_artifact_path(filepath: Path) -> Tuple[str, str, str]:
    """
    Parse artifact path to extract tool, category, and name.

    Returns:
        Tuple of (tool, category, artifact_name)
    """
    parts = filepath.parts

    # Determine tool
    if parts[0] == 'snippets':
        tool = 'snippet'
    elif parts[0] == 'claude-code':
        tool = 'claude-code'
    elif parts[0] == 'opencode':
        tool = 'opencode'
    else:
        raise ValueError(f"Unknown tool in path: {filepath}")

    # Handle different path structures for different artifact types
    if len(parts) < 2:
        raise ValueError(f"Invalid artifact path structure: {filepath}")

    # Special handling for JSON files (hooks and mcp-servers)
    if filepath.suffix == '.json':
        if parts[1] == 'hooks':
            category = 'hook'
        elif parts[1] == 'mcp-servers':
            category = 'mcp-server'
        else:
            raise ValueError(f"Unknown JSON file category in path: {filepath}")
    else:
        # Markdown files (agents, commands, best-practices, styleguides, etc.)
        if len(parts) < 3:
            raise ValueError(f"Invalid artifact path structure: {filepath}")

        category = parts[1]

        # Special handling for category names
        if category == 'agents':
            category = 'agent'
        elif category == 'commands':
            category = 'command'

    # Extract artifact name (filename without extension)
    artifact_name = filepath.stem

    # For best-practices and styleguides, remove the suffix
    if category == 'best-practices' and artifact_name.endswith('-best-practices'):
        artifact_name = artifact_name.replace('-best-practices', '')
    elif category == 'styleguides' and artifact_name.endswith('-styleguide'):
        artifact_name = artifact_name.replace('-styleguide', '')

    return tool, category, artifact_name


def generate_tag_name(filepath: Path, version: str) -> str:
    """
    Generate git tag name according to convention.

    Format: {tool}-{category}-{artifact-name}-v{semver}
    """
    tool, category, name = parse_artifact_path(filepath)
    return f"{tool}-{category}-{name}-v{version}"


def find_artifacts() -> List[Path]:
    """
    Find all artifact files in the repository.

    Returns:
        List of Path objects for artifact files
    """
    artifacts = []

    for pattern in ARTIFACT_PATTERNS:
        for filepath in Path('.').glob(pattern):
            # Skip excluded files
            if filepath.name in EXCLUDE_FILES:
                continue

            # Include .md and .json files
            if filepath.suffix in ['.md', '.json']:
                artifacts.append(filepath)

    return sorted(artifacts)


def process_artifact(
    filepath: Path,
    default_version: str,
    dry_run: bool = False
) -> Tuple[Optional[str], bool]:
    """
    Process a single artifact file.

    Args:
        filepath: Path to artifact file
        default_version: Default version to use if not present
        dry_run: If True, don't write changes

    Returns:
        Tuple of (tag_name, was_updated)
    """
    content = filepath.read_text(encoding='utf-8')
    updated = False
    version = None

    # Handle JSON files (hooks and mcp-servers)
    if filepath.suffix == '.json':
        existing_version, is_valid = parse_json_agpm_version(content)

        if not is_valid:
            print(f"Warning: Invalid JSON in {filepath} (skipping)", file=sys.stderr)
            return None, False

        if existing_version:
            version = existing_version
            print(f"✓ {filepath}: already has version {version}")
            updated = False
        else:
            version = default_version
            print(f"+ {filepath}: adding version {version}")

            # Parse and update JSON
            try:
                data = json.loads(content)
                if 'agpm' not in data:
                    data['agpm'] = {}
                data['agpm']['version'] = version

                # Write updated content (unless dry-run)
                if not dry_run:
                    filepath.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')

                updated = True
            except json.JSONDecodeError:
                print(f"Warning: Could not parse JSON in {filepath} (skipping)", file=sys.stderr)
                return None, False

    # Handle markdown files
    else:
        # Parse frontmatter
        frontmatter, frontmatter_text, body = parse_frontmatter(content)

        if frontmatter_text == "":
            print(f"Warning: No frontmatter in {filepath} (skipping)", file=sys.stderr)
            return None, False

        # Check if version already exists
        has_version = frontmatter and 'version' in frontmatter

        if has_version:
            version = frontmatter['version']
            print(f"✓ {filepath}: already has version {version}")
            updated = False
        else:
            version = default_version
            print(f"+ {filepath}: adding version {version}")

            # Update frontmatter
            updated_frontmatter = update_frontmatter_version(frontmatter_text, version)

            # Reconstruct file content
            updated_content = f"---\n{updated_frontmatter}\n---\n{body}"

            # Write updated content (unless dry-run)
            if not dry_run:
                filepath.write_text(updated_content, encoding='utf-8')

            updated = True

    # Generate tag name
    tag = generate_tag_name(filepath, version)

    return tag, updated


def main():
    parser = argparse.ArgumentParser(
        description='Bootstrap versions for all AGPM artifacts'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without making changes'
    )
    parser.add_argument(
        '--default-version',
        default='1.0.0',
        help='Default version for artifacts without version (default: 1.0.0)'
    )
    parser.add_argument(
        '--output',
        default='initial-tags.txt',
        help='Output file for generated tags (default: initial-tags.txt)'
    )

    args = parser.parse_args()

    print("AGPM Artifact Version Bootstrap")
    print("=" * 50)
    print()

    # Find all artifacts
    print("Finding artifacts...")
    artifacts = find_artifacts()
    print(f"Found {len(artifacts)} artifact files")
    print()

    if args.dry_run:
        print("Running in DRY-RUN mode (no files will be modified)")
        print()

    # Process each artifact
    tags = []
    updated_count = 0

    for filepath in artifacts:
        tag, was_updated = process_artifact(filepath, args.default_version, args.dry_run)

        if tag:
            tags.append(tag)

        if was_updated:
            updated_count += 1

    print()
    print("=" * 50)
    print(f"Processed: {len(artifacts)} artifacts")
    print(f"Updated: {updated_count} artifacts")
    print(f"Generated: {len(tags)} tags")

    # Write tags to output file
    if tags:
        output_path = Path(args.output)
        output_path.write_text('\n'.join(tags) + '\n', encoding='utf-8')
        print(f"Tags written to: {args.output}")

    if args.dry_run:
        print()
        print("DRY-RUN: No files were actually modified")
        print("Run without --dry-run to apply changes")

    print()
    print("Next steps:")
    print("1. Review the changes")
    print("2. Commit the updated artifacts")
    print("3. Create tags: bash .github/scripts/create-tags.sh initial-tags.txt")


if __name__ == '__main__':
    main()
