---
description: Run code quality checks (formatting, linting, type checking) based on the language style guide
agpm:
  version: "1.1.0"
  templating: true
dependencies:
  snippets:
    - name: lint-command
      path: ../../snippets/commands/lint.md
      install: false
  agents:
    - name: linting-standard
      path: ../agents/linting-standard.md
      tool: opencode
    - name: linting-advanced
      path: ../agents/linting-advanced.md
      tool: opencode
---
**IMPORTANT**: You are being asked to directly run code quality checks - analyze the code, apply fixes if requested, and run tests to verify changes. Do NOT ask for permission or confirmation.

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

- This command is designed for OpenCode
- Use the Bash tool to run linting commands directly
- Suggest agent invocations for complex issues that require refactoring
