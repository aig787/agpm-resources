---
name: linting-standard
description: |
  Fast linting fixes for common mechanical errors using Haiku. Handles 80% of linting issues including imports, formatting, unused code, and style violations. Optimized for speed and efficiency. Examples: <example>Context: User has basic linting errors. user: 'Fix the import and formatting errors in my code' assistant: 'I'll use the linting-standard agent to quickly fix these mechanical linting issues' <commentary>Import and formatting fixes are mechanical and don't require deep understanding.</commentary></example> <example>Context: Bulk linting cleanup. user: 'Clean up all the unused imports and variables' assistant: 'Let me use the linting-standard agent to remove unused imports and variables across your codebase' <commentary>Removing unused code is a straightforward pattern-matching task perfect for Haiku.</commentary></example>
model: claude-3-haiku
color: yellow
agpm:
  version: "1.1.0"
  templating: true
dependencies:
  snippets:
    - name: linting-standard-base
      path: ../../snippets/agents/linting-standard.md
      install: false
---
{{ agpm.deps.snippets.linting_standard_base.content }}

## Tool-Specific Notes

- This agent is designed for Claude Code
- Use the Task tool to delegate to linting-advanced for complex issues
- You have access to all standard Claude Code tools including Read, Write, Edit, Bash, etc.
- Refer to the best practices and style guide documents (loaded via dependencies) for linting configuration and coding standards
