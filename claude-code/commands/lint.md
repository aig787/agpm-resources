---
allowed-tools: "Task, Bash, Read"
description: |
  Run code quality checks (formatting, linting, type checking) based on the language style guide
argument-hint: "[ --fix | --check ] [ --all ] [ --doc ] [ --test ] - e.g., \"--fix --test\" or \"--check --all\""
agpm:
  version: "1.0.0"
  templating: true
dependencies:
  snippets:
    - name: lint-command
      path: ../../snippets/commands/lint.md
      install: false
  agents:
    - name: linting-standard
      path: ../agents/linting-standard.md
      tool: claude-code
    - name: linting-advanced
      path: ../agents/linting-advanced.md
      tool: claude-code
---
## Context

- Current working directory: !`pwd`

## Argument Parsing

Arguments received: $ARGUMENTS

Parse the arguments for the following flags:
- `--fix`: Apply automatic fixes where possible
- `--check`: Run in CI mode (strict checking, fail on warnings)
- `--all`: Run all checks including type checking and tests
- `--doc`: Add comprehensive documentation
- `--test`: Run tests after fixes to ensure nothing broke
- If no arguments: Run standard checks

## Command Execution

{{ agpm.deps.snippets.lint_command.content }}

## Tool-Specific Notes

- This command is designed for Claude Code
- Use the Task tool for agent delegation when complex issues are found
- Use allowed-tools from frontmatter (Task, Bash, Read)
