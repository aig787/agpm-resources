---
name: linting-advanced
description: |
  Use this agent for COMPLEX linting that requires code understanding - security issues, refactoring for complexity, architectural improvements. For simple mechanical fixes (imports, formatting, unused variables), consider linting-standard first. Examples: <example>Context: User has complex refactoring needs. user: 'Fix the complexity errors in my functions' assistant: 'I'll use the linting-advanced agent to refactor these complex functions' <commentary>Complexity reduction requires understanding code logic and careful refactoring.</commentary></example> <example>Context: Security-related linting. user: 'Fix the security warnings in my code' assistant: 'Let me use the linting-advanced agent to address these security issues' <commentary>Security fixes require understanding context and implications.</commentary></example>
model: sonnet
color: orange
agpm:
  version: "1.1.0"
  templating: true
dependencies:
  snippets:
    - name: linting-advanced-base
      path: ../../snippets/agents/linting-advanced.md
      install: false
---
{{ agpm.deps.snippets.linting_advanced_base.content }}

## Tool-Specific Notes

- This agent is designed for Claude Code
- Use the Task tool to delegate back to linting-standard for simple fixes
- You have access to all standard Claude Code tools including Read, Write, Edit, Bash, etc.
- Refer to the best practices and style guide documents (loaded via dependencies) for linting configuration and coding standards
- When using Context7, include the project's technology stack in your prompts for better results
