---
description: Complex linting requiring code understanding - security, refactoring, architectural improvements. Delegates simple fixes to linting-standard.
mode: subagent
temperature: 0.1
tools:
  read: true
  write: true
  edit: true
  bash: true
  glob: true
permission:
  edit: allow
  bash: ask
agpm:
  templating: true
dependencies:
  snippets:
    - name: linting-advanced-base
      path: ../../snippets/agents/linting-advanced.md
      tool: agpm
---

{{ agpm.deps.snippets.linting_advanced_base.content }}

**Additional tool-specific context**:

- For OpenCode specific features, refer to OpenCode documentation
- Agent invocation: Suggest invoking specialized agents when needed (e.g., "Please invoke linting-standard agent")
