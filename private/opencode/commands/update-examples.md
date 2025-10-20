---
description: |
  Scan all artifacts in the repository, identify top-level dependencies (those not referenced by other artifacts), and update examples/agpm.toml with these entries.
tools:
  read: true
  write: true
  edit: true
  glob: true
  bash: true
permission:
  write: allow
  edit: allow
  bash: allow
agpm:
  templating: true
dependencies:
  snippets:
    - name: update-examples-base
      path: ../../snippets/commands/update-examples.md
      tool: agpm
---

## Your task

Scan all artifacts and update examples/agpm.toml with top-level dependencies.

**IMPORTANT**: You are being asked to directly analyze the repository and update the TOML file - do NOT ask for permission or confirmation. Execute the analysis and update automatically.

{{ agpm.deps.snippets.update_examples_base.content }}

## Project Context

- **Repository**: agpm-resources
- **Current working directory**: Should be repository root
- **Target file**: `examples/agpm.toml`
- **Artifact directories**: `claude-code/`, `opencode/`, `snippets/`

## Tool-Specific Notes

- This command is designed for OpenCode
- Follow the OpenCode execution pattern from the core algorithm
- Use tools and permissions as specified in frontmatter
- This is a private command for repository maintenance
