---
description: Fast linting and formatting (optimized for speed with quick model)
mode: subagent
temperature: 0.0
tools:
  read: true
  write: false
  edit: true
  bash: true
  glob: true
permission:
  edit: allow
  bash: allow
agpm:
  templating: true
dependencies:
  snippets:
    - name: linting-standard-base
      path: ../../snippets/agents/linting-standard.md
      install: false
---

{{ agpm.deps.snippets.linting_standard_base.content }}

**Additional tool-specific context**:

- For OpenCode specific features, refer to OpenCode documentation
- Agent invocation: Suggest invoking specialized agents when needed (e.g., "Please invoke linting-advanced agent")
