---
name: update-examples
description: |
  Scan all artifacts in the repository, identify top-level dependencies (those not referenced by other artifacts), and update examples/agpm.toml with these entries.
allowed-tools: Read, Write, Edit, Glob, Bash(pwd:*)
agpm:
  templating: true
dependencies:
  snippets:
    - name: update-examples-base
      path: ../../snippets/commands/update-examples.md
      tool: agpm
---

{{ agpm.deps.snippets.update_examples_base.content }}

## Project Context

- **Repository**: agpm-resources
- **Purpose**: Maintain examples/agpm.toml with top-level artifacts for users to install
- **Structure**:
  - `snippets/` - Tool-agnostic business logic (library code)
  - `claude-code/` - Claude Code wrappers (user-facing)
  - `opencode/` - OpenCode wrappers (user-facing)
  - `private/` - Project-specific utilities
  - `examples/` - Example configurations for users

## Tool-Specific Notes

- This command is designed for Claude Code
- Follow the Claude Code execution pattern from the core algorithm
- Use allowed-tools as specified in frontmatter
- This is a private command for repository maintenance
