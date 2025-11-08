---
agpm:
  version: "1.0.0"
  templating: true
dependencies:
  snippets:
    - name: language-styleguide
      path: ../styleguides/{{ agpm.project.language }}-styleguide.md
      install: false
---
## Your task

Run code quality checks for the project based on the language-specific style guide.

## Language Style Guide

**Read the language-specific style guide at**:
- `{{ agpm.deps.snippets.language_styleguide.content }}`

This guide contains:
- **Formatting standards**: Which tools to use (e.g., ruff, prettier, gofmt)
- **Linting tool configuration**: How to configure and run linters
- **Naming conventions**: Language-specific naming patterns
- **Type annotations**: Type system best practices
- **Documentation style**: Docstring/comment standards
- **Error handling patterns**: Exception and error patterns

## Argument Parsing

Parse the arguments:
- `--fix`: Apply automatic fixes where possible
- `--check`: Run in CI mode (strict checking, fail on warnings)
- `--all`: Run all checks including type checking and tests
- `--doc`: Add comprehensive documentation
- `--test`: Run tests after fixes to ensure nothing broke
- If no arguments: Run standard checks
- Arguments: $ARGUMENTS

## Execution Steps

1. **Read the style guide**: Read the language-specific style guide from the path above

2. **Identify linting tools**: From the style guide, identify:
   - Which formatting tools to run (e.g., `ruff format`, `black`, `prettier`)
   - Which linting tools to run (e.g., `ruff check`, `eslint`, `golangci-lint`)
   - Which type checkers to run (e.g., `mypy`, `pyright`, `tsc`)
   - Tool configurations and recommended settings

3. **Execute based on flags**:
   - **No flags / `--check`**: Run standard checks (format check + lint)
   - **`--fix`**: Run auto-fix commands (format + lint --fix)
     - For simple mechanical fixes: Run tool auto-fix commands
     - For complex issues: Delegate to `linting-advanced` agent for refactoring
   - **`--all`**: Run comprehensive checks including type checking
   - **`--doc`**: Focus on documentation linting and improvements
   - **`--test`**: Run test suite to verify changes

4. **Agent delegation**: When complex issues are found that require refactoring:
   - **Simple fixes**: Use tool auto-fix capabilities (e.g., `ruff check --fix`)
   - **Complex fixes**: Delegate to specialized linting agents:
     - `linting-standard`: For straightforward mechanical fixes
     - `linting-advanced`: For complex refactoring, security issues, or code quality improvements

5. **Report results**: Provide clear output of actions taken and any remaining issues

## Examples of usage

- `/lint` - Run standard checks
- `/lint --fix` - Apply automatic fixes
- `/lint --fix --test` - Apply fixes and verify tests
- `/lint --check` - CI mode with strict validation
- `/lint --check --all` - Full CI validation with type checking
- `/lint --all` - Run all checks including type checking
- `/lint --doc` - Add/improve documentation
- `/lint --test` - Run tests to verify changes

## Notes

- The linting tools and commands are determined by the language-specific style guide
- Each language styleguide defines its own tooling (Python: ruff/mypy, JavaScript: eslint/prettier, etc.)
- This makes the command truly language-agnostic
