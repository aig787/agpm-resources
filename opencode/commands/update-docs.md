---
description: Review changes and update README.md to stay current with implementation
agpm:
  templating: true
dependencies:
  snippets:
    - name: update-docs-command
      path: ../../snippets/commands/update-docs.md
      tool: agpm
---

## Your task

Review recent changes and ensure README.md and all documentation files accurately reflect the project's current state.

**IMPORTANT**: You are being asked to directly update documentation - analyze the changes, compare against docs, and apply updates or report findings. Do NOT ask for permission or confirmation.

**IMPORTANT**: This command extends the shared base prompt. Read the complete command logic from:

- `{{ agpm.deps.snippets.update_docs_command.install_path }}`

## Argument Parsing

Parse the arguments from the command invocation:

- Arguments received: $ARGUMENTS
- Parse for flags: `--check-only`, `--auto-update`

**Flag Examples**:
```
/update-docs                    # run standard update with auto-update
/update-docs --check-only       # only report needed updates, no changes
/update-docs --auto-update      # explicitly enable auto-update (default)
```

## Execution

Based on the parsed arguments, execute the appropriate logic from the command file:

- If `--check-only`: Report all discrepancies without making changes
- If `--auto-update` or no arguments: Apply necessary updates to documentation files
- Follow the update process defined in the base command
- Use git operations to understand recent changes
- Cross-reference documentation against actual implementation
- Apply minimal, targeted edits to keep docs current

## Tool-Specific Notes

- This command is designed for OpenCode
- Use the Bash tool to run git commands for context on recent changes
- Use Read tool to examine both documentation and source files
- Use Edit or MultiEdit tools to apply documentation updates
- Use Grep tool to find relevant implementation details
- For comprehensive documentation improvements, suggest invoking specialized agents
- Focus on keeping documentation accurate and up-to-date with recent changes
- Report all updates made with specific file locations
