---
name: import
description: |
  Convert an artifact (agent, command, or snippet) into split architecture with AGPM templating.
  Supports direct import from file or interactive creation mode.
  For agents/commands: Creates snippet, Claude Code wrapper, and OpenCode wrapper.
  For snippets: Option to import directly or create wrappers with custom additions.
argument-hint: |
  [<artifact-path>] [--type <agent|command|snippet>] [--target <path>] [--name <name>]
agpm:
  templating: true
dependencies:
  snippets:
    - name: import-base
      path: ../../snippets/commands/import.md
      tool: agpm
---

## Your Task

Convert an artifact into the split architecture pattern with AGPM templating.

**IMPORTANT**: You are being asked to perform the import directly - analyze the artifact, create the three files, and report the results. Do NOT ask for permission or confirmation unless files already exist.

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

- This command is designed for OpenCode
- Follow the OpenCode execution pattern from the core algorithm
- Use tools and permissions as specified in frontmatter
- This is a private command for repository maintenance
