---
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*), Bash(wc:*), Read, Edit, Grep, Glob, Task
description: Review changes and update CLAUDE.md and/or AGENTS.md to reflect current architecture
argument-hint: '[ --check-only | --auto-update ] - e.g., "--check-only" to only report needed updates'
agpm:
  version: "1.1.1"
  templating: true
dependencies:
  snippets:
    - name: update-agentic-context-logic
      path: ../../snippets/commands/update-agentic-context.md
      version: "snippet-command-update-agentic-context-^v1.1.0"
      tool: agpm
      install: false
  agents:
    - name: backend-engineer
      path: ../agents/backend-engineer.md
      version: "claude-code-agent-backend-engineer-^v1.1.0"
      tool: claude-code
    - name: general-purpose
      path: ../agents/general-purpose.md
      version: "claude-code-agent-general-purpose-^v1.1.0"
      tool: claude-code
---
{{ agpm.deps.snippets.update_agentic_context_logic.content }}

## Context

- Current changes: !`git diff HEAD`
- Files changed: !`git status --short`
- Recent commits: !`git log --oneline -10`

## Tool-Specific Notes

- This command is designed for Claude Code
- Use the Task tool to delegate complex documentation updates:
  * Use `backend-engineer` agent for architectural documentation
  * Use `general-purpose` agent for architecture reviews and codebase exploration
- Available agents for delegation are declared in the frontmatter dependencies
- Use allowed-tools from frontmatter for git operations and file edits
- Character count commands (for 20k limit checks):
  * `wc -c CLAUDE.md` - check CLAUDE.md character count
  * `wc -c AGENTS.md` - check AGENTS.md character count

## Execution

Follow the logic in the referenced snippet file. Parse arguments, analyze changes, and update context files as needed.
