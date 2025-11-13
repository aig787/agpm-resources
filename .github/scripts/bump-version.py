#!/usr/bin/env python3
"""
Bump version script for AGPM artifacts.

This script:
1. Reads changed artifact files
2. Parses YAML frontmatter
3. Increments version based on bump type
4. Updates frontmatter with new version
5. Generates git tags according to naming convention
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional


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


def bump_version(version: str, bump_type: str) -> str:
    """
    Bump semantic version based on type.

    Args:
        version: Current version (e.g., "1.2.3")
        bump_type: Type of bump ("major", "minor", "patch")

    Returns:
        New version string
    """
    parts = version.split('.')
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")

    return f"{major}.{minor}.{patch}"


def check_tag_exists(tag_name: str) -> bool:
    """
    Check if a git tag exists.

    Args:
        tag_name: Git tag name to check

    Returns:
        True if tag exists, False otherwise
    """
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'rev-parse', tag_name],
            capture_output=True,
            text=True,
            cwd='.'
        )
        return result.returncode == 0
    except Exception:
        return False


def update_frontmatter_version(frontmatter_text: str, new_version: str) -> str:
    """
    Update version in frontmatter text.

    Args:
        frontmatter_text: Original YAML frontmatter text
        new_version: New version to set

    Returns:
        Updated frontmatter text
    """
    # Check if agpm.version already exists
    if re.search(r'agpm:\s*\n.*?version:', frontmatter_text, re.DOTALL):
        # Update existing version
        updated = re.sub(
            r'(agpm:\s*\n(?:.*\n)*?.*version:\s*)["\']?[0-9]+\.[0-9]+\.[0-9]+["\']?',
            f'\\1"{new_version}"',
            frontmatter_text,
            count=1
        )
    else:
        # Add version to existing agpm section or create new agpm section
        if 'agpm:' in frontmatter_text:
            # Add version to existing agpm section
            updated = re.sub(
                r'(agpm:)\s*\n',
                f'\\1\n  version: "{new_version}"\n',
                frontmatter_text,
                count=1
            )
        else:
            # Add new agpm section at the end
            updated = frontmatter_text + f'\nagpm:\n  version: "{new_version}"'

    return updated


def parse_artifact_path(filepath: str) -> Tuple[str, str, str]:
    """
    Parse artifact path to extract tool, category, and name.

    Args:
        filepath: Path to artifact file

    Returns:
        Tuple of (tool, category, artifact_name)

    Examples:
        snippets/agents/backend-engineer.md -> (snippet, agent, backend-engineer)
        claude-code/commands/commit.md -> (claude-code, command, commit)
        claude-code/hooks/agpm-update.json -> (claude-code, hooks, agpm-update)
        claude-code/mcp-servers/context7.json -> (claude-code, mcp, context7)
        snippets/best-practices/python-best-practices.md -> (snippet, best-practices, python)
    """
    path = Path(filepath)
    parts = path.parts

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
    if path.suffix == '.json':
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
        # Keep other categories as-is (best-practices, styleguides, frameworks, rules)

    # Extract artifact name (filename without extension)
    artifact_name = path.stem

    # For best-practices and styleguides, remove the suffix
    if category == 'best-practices' and artifact_name.endswith('-best-practices'):
        artifact_name = artifact_name.replace('-best-practices', '')
    elif category == 'styleguides' and artifact_name.endswith('-styleguide'):
        artifact_name = artifact_name.replace('-styleguide', '')

    return tool, category, artifact_name


def generate_tag_name(filepath: str, version: str) -> str:
    """
    Generate git tag name according to convention.

    Format: {tool}-{category}-{artifact-name}-v{semver}

    Args:
        filepath: Path to artifact file
        version: Semantic version (without 'v' prefix)

    Returns:
        Git tag name
    """
    tool, category, name = parse_artifact_path(filepath)
    return f"{tool}-{category}-{name}-v{version}"


def process_artifact(
    filepath: str,
    bump_type: str,
    dry_run: bool = False
) -> Optional[str]:
    """
    Process a single artifact file.

    Args:
        filepath: Path to artifact file
        bump_type: Version bump type
        dry_run: If True, don't write changes

    Returns:
        Git tag name if successful, None otherwise
    """
    file_path = Path(filepath)

    if not file_path.exists():
        print(f"Warning: File not found: {filepath}", file=sys.stderr)
        return None

    # Read file content
    content = file_path.read_text(encoding='utf-8')
    current_version = None
    new_version = None

    # Handle JSON files (hooks and mcp-servers)
    if file_path.suffix == '.json':
        existing_version, is_valid = parse_json_agpm_version(content)

        if not is_valid:
            print(f"Warning: Invalid JSON in {filepath}", file=sys.stderr)
            return None

        # Get current version and check tag existence
        if existing_version:
            current_version = existing_version
            current_tag = generate_tag_name(filepath, current_version)

            if check_tag_exists(current_tag):
                # Tag exists, bump normally
                new_version = bump_version(current_version, bump_type)
                action_msg = f"{current_version} -> {new_version} (tag existed)"
                should_write_file = True
            else:
                # Tag missing, use current version without bumping
                new_version = current_version
                action_msg = f"{current_version} (missing tag, no bump)"
                should_write_file = False
        else:
            # No version exists, use default and bump
            current_version = '0.1.0'
            new_version = bump_version(current_version, bump_type)
            action_msg = f"initial -> {new_version} (no version)"
            should_write_file = True

        print(f"{filepath}: {action_msg}")

        # Update JSON
        try:
            data = json.loads(content)
            if 'agpm' not in data:
                data['agpm'] = {}
            data['agpm']['version'] = new_version

            # Write updated content (unless dry-run and file needs updating)
            if not dry_run and should_write_file:
                file_path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')

        except json.JSONDecodeError:
            print(f"Warning: Could not parse JSON in {filepath}", file=sys.stderr)
            return None

    # Handle markdown files
    else:
        # Parse frontmatter
        frontmatter, frontmatter_text, body = parse_frontmatter(content)

        if frontmatter_text == "":
            print(f"Warning: No frontmatter found in {filepath}", file=sys.stderr)
            return None

        # Get current version and check tag existence
        if frontmatter and 'version' in frontmatter:
            current_version = frontmatter['version']
            current_tag = generate_tag_name(filepath, current_version)

            if check_tag_exists(current_tag):
                # Tag exists, bump normally
                new_version = bump_version(current_version, bump_type)
                action_msg = f"{current_version} -> {new_version} (tag existed)"
                should_write_file = True
            else:
                # Tag missing, use current version without bumping
                new_version = current_version
                action_msg = f"{current_version} (missing tag, no bump)"
                should_write_file = False
        else:
            # No version exists, use default and bump
            current_version = '0.1.0'
            new_version = bump_version(current_version, bump_type)
            action_msg = f"initial -> {new_version} (no version)"
            should_write_file = True

        print(f"{filepath}: {action_msg}")

        # Update frontmatter
        updated_frontmatter = update_frontmatter_version(frontmatter_text, new_version)

        # Reconstruct file content
        updated_content = f"---\n{updated_frontmatter}\n---\n{body}"

        # Write updated content (unless dry-run and file needs updating)
        if not dry_run and should_write_file:
            file_path.write_text(updated_content, encoding='utf-8')

    # Generate tag name
    tag = generate_tag_name(filepath, new_version)

    return tag


def main():
    parser = argparse.ArgumentParser(description='Bump versions for AGPM artifacts')
    parser.add_argument(
        '--changed-files',
        required=True,
        help='File containing list of changed artifact paths'
    )
    parser.add_argument(
        '--bump-type',
        required=True,
        choices=['major', 'minor', 'patch'],
        help='Type of version bump'
    )
    parser.add_argument(
        '--dry-run',
        default='false',
        help='Run without making changes'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output file for generated tags'
    )

    args = parser.parse_args()

    # Parse dry-run flag
    dry_run = args.dry_run.lower() in ('true', '1', 'yes')

    # Read changed files
    changed_files_path = Path(args.changed_files)
    if not changed_files_path.exists():
        print(f"Error: Changed files list not found: {args.changed_files}", file=sys.stderr)
        sys.exit(1)

    changed_files = [
        line.strip()
        for line in changed_files_path.read_text().splitlines()
        if line.strip()
    ]

    if not changed_files:
        print("No changed files to process")
        sys.exit(0)

    print(f"Processing {len(changed_files)} artifact(s)...")
    print(f"Bump type: {args.bump_type}")
    print(f"Dry run: {dry_run}")
    print()

    # Process each artifact
    tags = []
    for filepath in changed_files:
        tag = process_artifact(filepath, args.bump_type, dry_run)
        if tag:
            tags.append(tag)

    # Write tags to output file
    output_path = Path(args.output)
    output_path.write_text('\n'.join(tags) + '\n', encoding='utf-8')

    print()
    print(f"Generated {len(tags)} tag(s)")

    if dry_run:
        print("(Dry run - no files were modified)")


if __name__ == '__main__':
    main()
