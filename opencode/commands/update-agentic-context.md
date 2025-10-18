---
description: Review changes and update CLAUDE.md and/or AGENTS.md to reflect current architecture
agpm:
  templating: true
dependencies:
  snippets:
    - name: update-agentic-context-logic
      path: ../../snippets/commands/update-agentic-context.md
      tool: agpm
  agents:
    - name: backend-engineer
      path: ../agents/backend-engineer.md
      tool: opencode
    - name: general-purpose
      path: ../agents/general-purpose.md
      tool: opencode
---

## Your task

Review code changes and update AI context files (CLAUDE.md, AGENTS.md) to reflect current architecture and implementation.

**IMPORTANT**: You are being asked to directly review changes and update context files - analyze the diff, read the files, apply updates, and report results. Do NOT ask for permission or confirmation.

**IMPORTANT**: This command extends the shared base prompt. Read the complete command logic from:

- `{{ agpm.deps.snippets.update_agentic_context_logic.install_path }}`

## Argument Parsing

Parse the arguments from the command invocation:

- Arguments received: $ARGUMENTS
- Parse for flags: `--check-only`, `--auto-update`
- Pass parsed arguments to the sub-logic referenced above

**Flag Examples**:
```
/update-agentic-context                    # auto-update mode (default)
/update-agentic-context --check-only       # report needed updates only
/update-agentic-context --auto-update      # explicit auto-update
```

## Execution

Based on the parsed arguments, execute the appropriate logic from the sub-command file:

- If `--check-only`: Report discrepancies without making changes
- If `--auto-update` or no flags: Update context files to match current codebase
- Analyze git diff to understand changes
- Read CLAUDE.md and/or AGENTS.md if they exist
- Update files based on architectural and implementation changes
- Check character counts (20,000 character limit for both files)

## Tool-Specific Notes

- This command is designed for OpenCode
- Use Bash tool to run git commands and character count checks:
  * `git diff HEAD` - see current changes
  * `git status --short` - see changed files
  * `git log --oneline -10` - see recent commits
  * `wc -c CLAUDE.md` - check CLAUDE.md character count
  * `wc -c AGENTS.md` - check AGENTS.md character count
- Use Read tool to examine existing context files
- Use Edit tool to update context files
- For complex documentation updates, suggest invoking specialized agents:
  * Invoke `backend-engineer` for architectural documentation
  * Invoke `general-purpose` for architecture reviews
- Report any issues found and changes made
