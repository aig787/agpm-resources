---
description: Perform comprehensive PR self-review with language-specific checks
agpm:
  version: "1.1.1"
  templating: true
dependencies:
  snippets:
    - name: pr-self-review-base
      path: ../../snippets/commands/pr-self-review.md
      version: "snippet-command-pr-self-review-^v1.1.0"
      tool: agpm
      install: false
---
## Your task

Perform a comprehensive pull request self-review based on the arguments provided.

**IMPORTANT**: You are being asked to directly perform a PR self-review - run the appropriate checks, delegate to agents, and generate a comprehensive report. DO NOT ask for permission or confirmation.

{{ agpm.deps.snippets.pr_self_review_base.content }}

## Argument Parsing

Parse the arguments from the command invocation:

- Arguments received: $ARGUMENTS
- Parse for flags: `--quick`, `--full`, `--security`, `--performance`
- Pass parsed arguments to the sub-logic referenced above

**Flag Examples**:
```
/pr-self-review                # full comprehensive review
/pr-self-review --quick        # basic checks only
/pr-self-review --security     # focused security review
/pr-self-review --performance  # performance-focused analysis
```

## Execution

Based on the parsed arguments and configuration file, execute the appropriate review logic:

- If `--quick`: Run basic formatting and linting checks
- If `--full` or no args: Run comprehensive review with all checks
- If `--security`: Focus on security-focused review
- If `--performance`: Focus on performance analysis

## Tool-Specific Notes

- This command is designed for OpenCode
- Use the Bash tool to run commands directly
- Suggest invoking specialized agents when needed (e.g., "Please invoke linting-advanced agent")
- Report issues found and provide actionable recommendations
