---
name: import
description: |
  Convert an artifact (agent, command, or snippet) into split architecture with AGPM templating.
  Supports direct import from file or interactive creation mode.
  For agents/commands: Creates snippet, Claude Code wrapper, and OpenCode wrapper.
  For snippets: Option to import directly or create wrappers with custom additions.
argument-hint: |
 [<artifact-path>] [--type <agent|command|snippet>] [--target <path>] [--name <name>]
allowed-tools: Read, Write, Edit, Glob, Bash(mkdir:*), Bash(pwd:*), AskUserQuestion
agpm:
  templating: true
dependencies:
  snippets:
    - name: import-base
      path: ../../snippets/commands/import.md
      tool: agpm
---

{{ agpm.deps.snippets.import_base.content }}

## Project Context

- **Repository**: agpm-resources
- **Purpose**: Split architecture for AI coding assistant artifacts
- **Structure**:
  - `snippets/` - Tool-agnostic business logic
  - `claude-code/` - Claude Code wrappers
  - `opencode/` - OpenCode wrappers
  - `private/` - Project-specific utilities

## Tool-Specific Notes

- This command is designed for Claude Code
- Follow the Claude Code execution pattern from the core algorithm
- Use allowed-tools as specified in frontmatter
- This is a private command for repository maintenance
