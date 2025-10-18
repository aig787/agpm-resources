---
description: Review and update all documentation files in docs/ directory for accuracy
agpm:
  templating: true
dependencies:
  snippets:
    - name: review-docs-command
      path: ../../snippets/commands/review-docs.md
      tool: agpm
---

## Your task

Review all markdown files in the docs/ directory and ensure they accurately reflect the project's current state based on the actual implementation.

**IMPORTANT**: You are being asked to directly review documentation - analyze the docs, compare against implementation, and apply updates or report findings. Do NOT ask for permission or confirmation.

**IMPORTANT**: This command extends the shared base prompt. Read the complete command logic from:

- `{{ agpm.deps.snippets.review_docs_command.install_path }}`

## Argument Parsing

Parse the arguments from the command invocation:

- Arguments received: $ARGUMENTS
- Parse for flags: `--check-only`, `--auto-update`

**Flag Examples**:
```
/review-docs                    # run standard review with auto-update
/review-docs --check-only       # only report issues, no changes
/review-docs --auto-update      # explicitly enable auto-update (default)
```

## Execution

Based on the parsed arguments, execute the appropriate logic from the command file:

- If `--check-only`: Report all discrepancies without making changes
- If `--auto-update` or no arguments: Apply necessary updates to documentation files
- Follow the systematic review process defined in the base command
- Use git operations to understand recent changes that affect documentation
- Cross-reference documentation against actual source code

## Tool-Specific Notes

- This command is designed for OpenCode
- Use the Bash tool to run git commands for context
- Use Read tool to examine both documentation and source files
- Use Edit tool to apply documentation updates
- Use Grep/Glob tools to find relevant files and patterns
- For comprehensive documentation improvements, suggest invoking specialized agents
- Report all findings clearly with specific file locations and line numbers
