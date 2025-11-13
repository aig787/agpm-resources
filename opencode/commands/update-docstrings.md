---
description: Review code changes and ensure all related documentation is accurate and up-to-date. Supports positional commit ranges for analyzing historical changes.
agpm:
  version: "1.2.0"
  templating: true
dependencies:
  snippets:
    - name: update-docstrings-logic
      path: ../../snippets/commands/update-docstrings.md
      version: "snippet-command-update-docstrings-^v1.2.0"
      tool: agpm
      install: false
---
## Your task

Review the current code changes and ensure all related documentation accurately reflects the implementation.

**IMPORTANT**: You are being asked to directly review and update documentation - analyze the changes, identify issues, and apply updates as needed. Do NOT ask for permission or confirmation.

{{ agpm.deps.snippets.update_docstrings_logic.content }}

## Argument Parsing

Parse the arguments from the command invocation following the commit command pattern:

- Arguments received: $ARGUMENTS
- **Step 1**: Parse for flags: `--check-only`, `--auto-update`, `--focus=<module>`
- **Step 2**: Extract first non-flag positional argument as commit range
- **Step 3**: Handle `--` separator for additional options
- Pass parsed arguments to the sub-logic referenced above

### Positional Range Examples
**Current Changes (Default)**:
```
/update-docstrings                    # automatically update docs based on current changes
/update-docstrings --check-only       # report documentation issues without changes
/update-docstrings --focus=api        # focus on API module documentation
/update-docstrings --focus=core       # focus on core module documentation
```

**Commit Range Support**:
```
/update-docstrings HEAD~5..HEAD                    # last 5 commits
/update-docstrings --check-only HEAD~3..HEAD      # check-only for last 3 commits
/update-docstrings --focus=api origin/main..HEAD  # api module since divergence from main
/update-docstrings abc123..def456                 # commits between two specific SHAs
/update-docstrings HEAD~10..HEAD -- --focus=api    # range with flag after separator
```

## Execution

Based on the parsed arguments, execute the appropriate logic from the sub-command file:

- If `--check-only`: Report documentation issues without making changes
- If `--auto-update` or no flags: Update documentation to match code changes
- If `--focus=<module>`: Concentrate on specific module documentation
- Use specialized agents for complex documentation updates (delegate using agent invocation)

## Context Gathering

Before reviewing documentation, gather context based on parsed arguments:

**Current Changes (no range provided)**:
- Run `git diff HEAD` to see current changes
- Run `git status --short` to list modified files
- Run `git log --oneline -5` to understand recent work

**Commit Range (positional range provided)**:
- Run `git diff <range>` to see changes in the specified range
- Run `git log --oneline <range>` to show commits being analyzed
- Report the scope of analysis (e.g., "Analyzing 5 commits from abc123 to def456")

**Common analysis steps**:
- Identify which modules or components were modified
- Determine documentation impact based on changes
- Plan documentation updates accordingly

## Tool-Specific Notes

- This command is designed for OpenCode
- Use the Bash tool to run git commands for analyzing changes
- Use Read/Edit tools to review and update documentation
- For comprehensive documentation updates, invoke specialized backend engineer agents
- Report documentation issues found and fixes applied
