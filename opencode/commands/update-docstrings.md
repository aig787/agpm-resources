---
description: Review code changes and ensure all related documentation is accurate and up-to-date
agpm:
  version: "1.1.0"
  templating: true
dependencies:
  snippets:
    - name: update-docstrings-logic
      path: ../../snippets/commands/update-docstrings.md
      version: "snippet-command-update-docstrings-^v1.1.0"
      tool: agpm
      install: false
---
## Your task

Review the current code changes and ensure all related documentation accurately reflects the implementation.

**IMPORTANT**: You are being asked to directly review and update documentation - analyze the changes, identify issues, and apply updates as needed. Do NOT ask for permission or confirmation.

{{ agpm.deps.snippets.update_docstrings_logic.content }}

## Argument Parsing

Parse the arguments from the command invocation:

- Arguments received: $ARGUMENTS
- Parse for flags: `--check-only`, `--auto-update`, `--focus=<module>`
- Pass parsed arguments to the sub-logic referenced above

**Flag Examples**:
```
/update-docstrings                    # automatically update docs based on code changes
/update-docstrings --check-only       # report documentation issues without changes
/update-docstrings --focus=api        # focus on API module documentation
/update-docstrings --focus=core       # focus on core module documentation
```

## Execution

Based on the parsed arguments, execute the appropriate logic from the sub-command file:

- If `--check-only`: Report documentation issues without making changes
- If `--auto-update` or no flags: Update documentation to match code changes
- If `--focus=<module>`: Concentrate on specific module documentation
- Use specialized agents for complex documentation updates (delegate using agent invocation)

## Context Gathering

Before reviewing documentation, gather context:
- Run `git diff HEAD` to see current changes
- Run `git status --short` to list modified files
- Run `git log --oneline -5` to understand recent work
- Identify which modules or components were modified

## Tool-Specific Notes

- This command is designed for OpenCode
- Use the Bash tool to run git commands for analyzing changes
- Use Read/Edit tools to review and update documentation
- For comprehensive documentation updates, invoke specialized backend engineer agents
- Report documentation issues found and fixes applied
