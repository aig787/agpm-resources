---
agpm:
  version: "1.1.0"
  templating: true
dependencies:
  snippets:
    - name: styleguide
      path: ../styleguides/{{ agpm.project.language }}-styleguide.md
      install: false
    - name: best-practices
      path: ../best-practices/{{ agpm.project.language }}-best-practices.md
      install: false
---
# Pull Request Self-Review Command

## Overview

This command performs comprehensive pull request self-reviews following standardized review guidelines and language-specific style conventions. It reviews changes and generates a report - it does NOT create or submit a pull request. It's designed to help you evaluate your changes before deciding to create a PR.

## Execution Approach

**IMPORTANT**: Batch related operations thoughtfully; schedule tool calls only in parallel when the workflow benefits from it.

**CRITICAL**: Use the Task tool to delegate to specialized agents for code analysis, NOT Grep or other direct tools. Agents have context about the project and can provide deeper insights.

### Agent Delegation Strategy

- Prefer the Task tool for broad or multi-file code analysis
- Use direct Read/Grep commands for targeted inspections and pattern searches
- Provide agents with specific context about what changed
- Include relevant file paths and change summaries in prompts

## Review Execution Steps

### Step 1: Parse Arguments and Determine Review Target

**IMPORTANT**: First check what arguments were provided: $ARGUMENTS

#### Determine the Review Target

Review targets in order of precedence:

1. **DEFAULT (no arguments)**: Review uncommitted working directory changes
   - This is the PRIMARY use case - reviewing your work-in-progress before committing
   - Use `git status --short` to list modified/staged files
   - Use `git diff HEAD --stat` to see all uncommitted changes (staged + unstaged)
   - **DO NOT review branch commits or commit history when no arguments provided**
   - Examples: `/pr-self-review`, `/pr-self-review --quick`

2. **DIFF keyword**: Review only staged (but uncommitted) changes
   - Arguments contain the DIFF keyword (e.g., `DIFF`, `HEAD..DIFF`, `HEAD~2..DIFF`)
   - DIFF represents staged changes ready for commit (`git diff --cached`)
   - For ranges like `HEAD..DIFF`: Use `git diff --cached HEAD --stat`
   - For ranges like `HEAD~2..DIFF`: Use `git diff --cached HEAD~2 --stat`
   - Use `git diff --cached --name-status` to list staged files
   - Examples: `/pr-self-review DIFF`, `/pr-self-review HEAD~2..DIFF`

3. **HEAD keyword**: Review the most recent commit
   - Argument is exactly `HEAD` (not `HEAD~1` or other variations)
   - This reviews the last committed work on the current branch
   - Use `git show --stat HEAD` for commit details
   - Use `git diff-tree --no-commit-id --name-status -r HEAD` to list files
   - Examples: `/pr-self-review HEAD`, `/pr-self-review HEAD --quick`

4. **Commit range**: Review multiple commits
   - Pattern: `<ref>..<ref>` (e.g., `abc123..def456`, `main..HEAD`, `origin/main..HEAD`)
   - Use `git log --oneline <range>` to see commit history
   - Use `git diff --stat <range>` and `git diff --name-status <range>` for changes
   - Examples: `/pr-self-review main..HEAD`, `/pr-self-review abc123..def456 --security`

5. **Single commit**: Review one specific commit
   - Pattern: 6-40 character hex string (e.g., `abc123`, `5b3ee1d`) or `HEAD~N`
   - Use `git show --stat <commit>` for commit details
   - Use `git diff-tree --no-commit-id --name-status -r <commit>` to list files
   - Examples: `/pr-self-review abc123`, `/pr-self-review HEAD~1`, `/pr-self-review 5b3ee1d --quick`

#### Determine the Review Type

Parse review type from remaining arguments after the target:

- `--quick`: Basic formatting and linting only
- `--full`: Complete review with all checks (default if no flag specified)
- `--security`: Focus on security implications
- `--performance`: Focus on performance analysis

**Focus Rule**: Only review tracked files in version control. Ignore untracked files marked with `??` in git status.

### Step 2: Detect if This is a Historical Review

**IMPORTANT**: Check if we're reviewing historical changes vs current work-in-progress.

**Detection Logic**:

- **Current Work Review** (run automated checks):
  - No arguments (uncommitted changes)
  - `DIFF` keyword (staged but uncommitted changes ready for commit)
  - Ranges ending in `DIFF` (like `HEAD..DIFF`, `HEAD~2..DIFF`)
    - These review committed work plus staged changes
  - `HEAD` by itself (reviewing the most recent commit on current branch)
  - Commit range ending in `HEAD` (like `main..HEAD`, `origin/main..HEAD`, `HEAD~3..HEAD`)
    - These review current work that hasn't been merged/pushed yet

- **Historical Review** (skip automated checks):
  - Single commit hash (like `abc123`, `5b3ee1d`) except `HEAD`
  - Commit range NOT ending in `HEAD` or `DIFF` (like `abc123..def456`, `v1.0..v2.0`)
  - Branch name alone (like `main` when not in a range)

**Why this matters**:
- **Historical**: Automated checks would test current code, not the commits being reviewed
- **Current**: Automated checks test what you're about to commit or have just committed

**For historical reviews**:
- Display: "⚠️  Historical Review: automated checks skipped (would test current code, not historical state)"
- Suggest: "To test historical code: git checkout <commit> && <test-command>"
- Proceed directly to manual code review (skip to Step 4)

**For current work**:
- Run automated checks as usual (Step 3)

### Step 3: Detect Changeset Size and Adapt Review Strategy

**IMPORTANT**: Before running full reviews, analyze the changeset size to determine the appropriate approach.

#### Get Changeset Statistics

- For uncommitted changes: `git diff HEAD --stat`
- For single commit: `git show --stat <commit>`
- For commit range: `git diff --stat <range>`
- Parse the summary line (e.g., "42 files changed, 1523 insertions(+), 891 deletions(-)")

#### Categorize Changeset Size

- **Small** (<500 lines): Standard single-pass review (existing behavior)
- **Medium** (500-2000 lines): Standard review with progress tracking
- **Large** (2000-5000 lines): Chunked review with parallel processing
- **Massive** (>5000 lines): Chunked review + warn user about scope
- **Extreme** (>20000 lines): Suggest alternatives, proceed with best-effort

#### For Large/Massive Changesets, Prepare Chunks

a. **Get detailed file list with line counts**:
   ```bash
   git diff --numstat <target> | grep -v "^-"  # Filter out binary files
   ```
   This outputs: `<additions> <deletions> <filepath>` per line

b. **Group files by module/directory**:
   - Priority 1 (Critical): Core modules, main application logic
   - Priority 2 (Security): Authentication, validation, sensitive data handling
   - Priority 3 (Standard): Other source modules
   - Priority 4 (Low): Tests, docs, config files

c. **Create balanced chunks**:
   - Target: ~1000-1500 total lines (additions + deletions) per chunk
   - Keep related files together (same module/directory)
   - Sort by priority, create chunks that respect module boundaries
   - Example: "Chunk 1: core/ + resolver/ (4 files, 1200 lines)"

d. **Notify user of strategy**:
   ```
   Detected LARGE changeset: 42 files, 3500 lines changed
   Strategy: Parallel chunked review (4 chunks)
   - Chunk 1: core/ + resolver/ (8 files, ~1200 lines)
   - Chunk 2: installer/ + lockfile/ (10 files, ~1000 lines)
   - Chunk 3: templating/ + mcp/ (12 files, ~900 lines)
   - Chunk 4: tests/ (12 files, ~400 lines)
   ```

e. **Use TodoWrite to track chunks**:
   Create a todo list with one item per chunk:
   ```
   TodoWrite([
       {content: "Review chunk 1/4: core/ + resolver/ (8 files)", status: "pending", activeForm: "Reviewing chunk 1/4"},
       {content: "Review chunk 2/4: installer/ + lockfile/ (10 files)", status: "pending", activeForm: "Reviewing chunk 2/4"},
       {content: "Review chunk 3/4: templating/ + mcp/ (12 files)", status: "pending", activeForm: "Reviewing chunk 3/4"},
       {content: "Review chunk 4/4: tests/ (12 files)", status: "pending", activeForm: "Reviewing chunk 4/4"},
       {content: "Aggregate findings and generate report", status: "pending", activeForm: "Aggregating findings"}
   ])
   ```

#### For Extreme Changesets (>20k lines)

- Warn: "⚠️  EXTREME changeset detected: 65k lines changed across 150 files"
- Suggest: "Consider reviewing by smaller commit ranges or individual commits instead"
- Offer to proceed: "Proceeding with best-effort chunked review (may take significant time)"

### Step 4: Run Automated Checks (Current Work Only)

**IMPORTANT**: Skip automated checks for historical reviews - they would test current code, not the commits being reviewed.

**Historical Review**: Display warning and proceed to Step 5 (manual review).

**Current Work Review**: Run automated checks based on review mode and language.

#### Quick Review (`--quick`)

Run these checks IN PARALLEL:
- Formatting tool (e.g., `ruff format`, `prettier`, `gofmt`)
- Linting tool (e.g., `ruff check`, `eslint`, `golangci-lint`)
- Fast test suite (unit tests only)

#### Full Review (`--full` or default)

First, run quick checks, then proceed with language-specific comprehensive checks.

##### Agent Delegation Strategy (Adapts Based on Changeset Size)

**For Small/Medium Changesets (<2000 lines)** - Single-pass review:

Use the Task tool to delegate to specialized agents IN PARALLEL:

1. **Linting Agent**: Check formatting and linting issues
2. **Code Quality Agent**: Review code quality, architecture, adherence to best practices
3. **Test Agent**: Analyze test coverage, quality, and isolation
4. **Documentation Agent**: Review documentation completeness and accuracy:
   - Accuracy - ensure documentation correctly describes what the code does
   - Conciseness - keep documentation brief but informative, avoid verbosity
   - Completeness - all public APIs have proper documentation
   - Examples - verify code examples are correct and runnable
   - Consistency - follow language/framework documentation conventions

Example Task invocation:
```
Task(description="Review code quality",
     prompt="Review the changed files against .agpm/snippets/<language>-best-practices.md covering imports, naming, error handling, patterns, and architecture...",
     subagent_type="<language>-expert-standard")
```

**Systematic Code Duplication Detection**:

Use targeted searches to find duplicate patterns:
- Similar function signatures (potential duplication)
- Similar error handling patterns
- Repeated control flow patterns that could be refactored
- Similar I/O operations
- Duplicate validation logic

**Additional Task for Code Cleanup**:
```
Task(description="Check for deprecated methods and code cleanup",
     prompt="Analyze changed files for:
     1. Deprecated methods - marked for removal or should be deleted
     2. Code duplication - identical or very similar code blocks
     3. Redundant imports - unused imports that should be removed
     4. Dead code - functions, classes, or methods never called or referenced
     5. Verbose documentation - excessively wordy or redundant information
     6. Orphan documentation - docs referencing removed APIs or outdated patterns
     7. Unused variables - variables that should be removed entirely
     8. Similar function patterns - nearly identical logic that could be unified
     9. Repeated error handling - duplicate error creation/propagation patterns
     Focus on recommending removal of deprecated code rather than migration paths.",
     subagent_type="<language>-expert-standard")
```

Run full test suite and documentation build IN PARALLEL:
- Full test suite execution
- Documentation generation/verification
- Cross-platform compatibility checks (if applicable)

**For Large/Massive Changesets (≥2000 lines)** - Chunked parallel review:

**IMPORTANT**: For large changesets, process chunks in parallel to stay within context limits while maintaining thorough coverage.

**For each chunk (process 3-4 chunks in parallel)**:

a. **Mark chunk as in_progress** using TodoWrite before starting

b. **Get files for this chunk**:
   ```bash
   # Extract files for this chunk based on the chunking strategy from Step 3
   git diff --name-only <target> | grep "^<directory-pattern>/"
   ```

c. **Get focused diff for chunk**:
   ```bash
   # Get only the diff for files in this chunk
   git diff <target> -- <file1> <file2> <file3>...
   ```

d. **Launch parallel agent tasks** for this chunk:

Each agent gets:
- **Chunk context**: "Reviewing chunk 2/5: installer/ + lockfile/ modules (10 files, ~1000 lines)"
- **Full changeset scope**: Brief summary of what the entire PR changes
- **Files in chunk**: List of specific files with line change counts
- **Focused diff**: Only the changes for files in this chunk
- **Module context**: Understanding of what this module does in the system

Example prompt structure:
```
Task(description="Review chunk 2/5: installer module",
     prompt="You are reviewing PART of a larger changeset as part of a chunked review strategy.

     FULL CHANGESET SCOPE:
     - Total: 42 files, 3500 lines changed
     - Focus: Refactoring dependency resolution and installation logic
     - This is chunk 2 of 5

     YOUR CHUNK (installer/ + lockfile/):
     - Files: installer/mod.ext (+234/-156), installer/resource_installer.ext (+89/-42), ...
     - Total: 10 files, ~1000 lines
     - Module purpose: Handles resource installation and lockfile management

     Review this chunk for:
     1. Code quality and adherence to language best practices
     2. Architecture alignment with changes from other chunks
     3. Error handling consistency
     4. Test coverage and isolation
     5. Cross-module interaction impacts

     [Include focused diff here]

     Provide findings specific to this chunk. Note any cross-chunk concerns.",
     subagent_type="<language>-expert-standard")
```

Launch similar tasks for:
- Linting agent - linting issues in this chunk
- Test agent - test coverage for this chunk
- Documentation agent - documentation for this chunk

e. **Store chunk findings**:
- Collect agent responses for this chunk
- Tag findings with chunk identifier (e.g., "Chunk 2: installer")
- Note any cross-chunk concerns flagged by agents

f. **Mark chunk as completed** using TodoWrite when all agents finish

**After all chunks complete**:
- Mark "Aggregate findings and generate report" todo as in_progress
- Run full test suite (tests entire codebase, not individual chunks)
- Proceed to result aggregation (see Step 4.5)

**Chunk processing example** (3 chunks in parallel):
```
# Launch chunks 1, 2, 3 in parallel with Task tool
Task(chunk 1) | Task(chunk 2) | Task(chunk 3)

# TodoWrite shows progress:
✓ Review chunk 1/4: core/ + resolver/
⊙ Review chunk 2/4: installer/ + lockfile/  (in progress)
⊙ Review chunk 3/4: templating/ + mcp/      (in progress)
⊙ Review chunk 4/4: tests/                  (pending)

# When batch completes, launch next batch
Task(chunk 4)
```

#### Security Review (`--security`)

Use Task with specialized agent for security-focused review:
```
Task(description="Security review",
     prompt="Review for security issues per language best practices: credentials in code, input validation, path traversal, unsafe operations, platform-specific security concerns...",
     subagent_type="<language>-expert-standard")
```

Additionally run targeted searches IN PARALLEL:
- Credential patterns: `(password|token|secret|api_key)\s*=\s*"`
- Hardcoded secrets in configuration files
- Input validation issues
- Injection vulnerabilities (SQL, command, path traversal, etc.)
- Unsafe language features (if applicable)
- Weak cryptography usage
- Error messages exposing sensitive information

Verify no secrets in version-controlled files

#### Performance Review (`--performance`)

Build in release/production mode if applicable

Use Task with specialized agent for performance-focused review:
```
Task(description="Performance review",
     prompt="Review for performance issues per language best practices: blocking operations in async code, unnecessary allocations, algorithmic complexity, lock contention, resource cleanup...",
     subagent_type="<language>-expert-standard")
```

Check for common anti-patterns:
- Blocking operations in async contexts
- Synchronous I/O in async code
- Excessive object allocation or cloning
- Missing resource cleanup
- Potential deadlocks in concurrent code
- Inefficient algorithms or data structures
- Missing capacity hints for collections
- Unnecessary collection conversions

#### Enhanced Unused Code Detection

Run systematic searches for unused code patterns:
- Unused imports
- Private functions that might be unused
- TODO/FIXME comments suggesting removal
- Commented-out code
- Unused constants and variables
- Dead code paths

### Step 4.5: Result Aggregation (Chunked Reviews Only)

**IMPORTANT**: If you performed a chunked review (Large/Massive changeset), aggregate findings before generating the final report.

#### Deduplication Strategy

a. **Collect all findings** from chunk reviews:
   - Group by finding type: errors, warnings, suggestions, security issues, etc.
   - Preserve chunk context for each finding

b. **Deduplicate similar issues**:
   - **Identical issues**: Same error/warning in multiple chunks
     - Example: "Missing error context" found in chunks 1, 2, 4
     - Consolidate: "Missing error context in 3 chunks (core, installer, mcp)"

   - **Pattern-based duplicates**: Same issue type across different files
     - Example: Linting warning "unused-import" in 8 different files
     - Consolidate: "unused-import pattern detected (8 occurrences across chunks 1-3)"

   - **Cross-chunk concerns**: Issues flagged by multiple agents
     - Example: Chunk 2 agent notes dependency on chunk 1 changes
     - Link findings: "Installer changes depend on resolver refactoring (see chunk 1 findings)"

c. **Categorize by severity**:
   - **Critical**: Security issues, breaking changes, data loss risks
   - **High**: Architecture violations, significant bugs, missing tests
   - **Medium**: Code quality issues, incomplete docs, minor bugs
   - **Low**: Style issues, typos, suggestions

d. **Identify cross-cutting concerns**:
   - Issues that span multiple chunks (architectural)
   - Patterns repeated across modules (refactoring opportunities)
   - Missing integration points between chunks

e. **Calculate aggregate metrics**:
   - Total issues by severity
   - Coverage by module (which chunks were clean vs. problematic)
   - Most common issue types
   - Example: "15 total issues: 2 critical (security), 5 high (architecture), 8 medium (docs)"

**Aggregation Example**:

```
Chunk 1 findings:
- [High] Missing error context in resolver/mod.ext:245
- [Medium] Verbose docstring in resolver/version_resolver.ext:120
- [Low] Linting issue in resolver/mod.ext:300

Chunk 2 findings:
- [High] Missing error context in installer/mod.ext:180
- [Critical] Path traversal risk in installer/resource_installer.ext:95
- [Low] Linting issue in installer/mod.ext:200

Aggregated findings:
- [Critical] Path traversal risk in installer/resource_installer.ext:95
- [High] Missing error context pattern (2 occurrences: resolver, installer)
- [Medium] Verbose docstring in resolver/version_resolver.ext:120
- [Low] Linting issue pattern (2 occurrences: resolver, installer)

Summary: 1 critical, 1 high, 1 medium, 1 low (grouped from 5 original findings)
```

**Mark aggregation todo as completed** when finished.

### Step 5: Manual Review - Apply Review Dimensions

For manual review, systematically check each dimension:

#### Code Quality

**Language Best Practices**

- Code follows language idioms and conventions from best practices file
- No deprecated APIs or patterns
- Appropriate use of language features
- Clear and descriptive naming
- Proper error handling
- No code duplication (DRY principle)
- Adherence to style guide for formatting and naming

**Design Principles**

- Single Responsibility Principle (SRP)
- Open/Closed Principle
- Dependency Inversion where appropriate
- Separation of concerns
- Proper abstraction levels

**Readability**

- Code is self-documenting where possible
- Complex logic has explanatory comments
- Function/method length is reasonable
- Nesting depth is manageable
- Clear control flow

**Additional Quality Checks**

- Deprecated code removal: Methods/functions marked for removal that should be deleted
- Code duplication: Identical or very similar code blocks that should be refactored
- Unused variables: Variables that should be removed entirely
- Dead code: Functions, classes, or methods never referenced
- File size limits: Ensure source files stay within reasonable size (check project standards)

#### Architecture

**Module Structure**

- Logical organization of code
- Clear module boundaries
- Appropriate coupling between components
- Dependencies flow in the right direction
- No circular dependencies
- Module structure alignment with architecture documentation

**Design Patterns**

- Appropriate patterns used for the problem
- No over-engineering
- Patterns implemented correctly
- Consistent pattern usage across codebase

**API Design**

- Clear and consistent interface design
- Backward compatibility maintained (if required)
- Appropriate abstraction levels
- Well-defined contracts

**Async/Concurrency** (if applicable)

- Proper use of async/await patterns
- No race conditions
- Appropriate use of locks/synchronization

#### Security

**Authentication & Authorization**

- No authentication bypass vulnerabilities
- Proper authorization checks
- Secure session management
- No hardcoded credentials

**Input Validation**

- All user input is validated
- Protection against injection attacks (SQL, command, etc.)
- Proper sanitization of data
- Appropriate use of parameterized queries

**Data Protection**

- Sensitive data is encrypted in transit
- Sensitive data is encrypted at rest (where required)
- No secrets in code or logs
- Proper data isolation (multi-tenancy)
- No exposure of internal details in error messages

**Secrets Management**

- No hardcoded passwords or API keys
- Environment variables used appropriately
- No credentials in version control
- Secure credential rotation supported

**Common Vulnerability Patterns**

- No SQL injection risks
- No command injection risks
- No path traversal vulnerabilities
- No insecure deserialization
- No SSRF (Server-Side Request Forgery) risks

#### Database (if applicable)

**Schema Changes**

- Migration files present for schema changes
- Migrations are reversible
- No data loss in migrations
- Proper indexing strategy
- Backward compatible changes (if required)

**Query Patterns**

- No N+1 query problems
- Efficient use of indexes
- Appropriate query optimization
- Proper use of transactions
- Connection pooling configured correctly

**Data Integrity**

- Foreign key constraints where appropriate
- Data validation at database level
- No orphaned records
- Proper cascade behavior

#### Performance

**Async/Concurrency** (if applicable)

- No blocking operations in async context
- Proper use of async libraries
- No race conditions
- Appropriate use of locks/semaphores

**Resource Usage**

- No memory leaks
- Efficient resource allocation
- Proper cleanup of resources
- Appropriate batch sizes for bulk operations

**Optimization Opportunities**

- Caching used where beneficial
- Lazy loading implemented where appropriate
- Database queries optimized
- Unnecessary computations eliminated

**Scalability Considerations**

- Code handles increased load gracefully
- No bottlenecks identified
- Proper pagination for large datasets
- Resource limits respected

#### Testing

**Test Coverage**

- New code has appropriate test coverage
- Critical paths are well-tested
- Edge cases are tested
- Error conditions are tested

**Test Quality**

- Tests are maintainable
- Tests are not flaky
- Tests are fast enough
- Tests verify behavior, not implementation

**Testing Patterns**

- Appropriate use of mocking/stubbing
- Mock signatures match real APIs
- Integration tests where needed
- Unit tests are properly isolated
- Tests use proper isolation mechanisms (no shared state)

**Test Organization**

- Tests are well-organized
- Test names are descriptive
- Test fixtures are appropriate
- Setup/teardown is proper

#### Documentation

**Code Documentation**

- Complex logic is explained
- Public APIs are documented
- Function/method purposes are clear
- Important decisions are documented

**Docstrings Reviewed for Accuracy and Conciseness**:
- Ensure documentation correctly describes what the code does
- Keep documentation brief but informative, avoid verbosity
- Verify examples use proper attributes and are runnable
- **Verbose documentation**: Identify documentation that is excessively wordy or redundant
- **Orphan documentation**: Check for docs referencing removed APIs or outdated patterns

**API Documentation**

- API changes are documented
- New endpoints documented
- Request/response formats clear
- Authentication requirements documented

**README & Guides**

- README updated for user-facing changes
- Setup instructions accurate
- Examples updated
- Breaking changes documented

**Architectural Documentation**

- Design decisions documented
- Architecture diagrams updated (if needed)
- Data flow documented (if changed)
- Integration points documented

### Step 6: Generate Summary Report

Create a comprehensive summary report with:

#### 1. Changes Overview
- Files modified/added/deleted
- Brief description of changes
- Scope and purpose

#### 2. Test Results
- **For historical reviews**: "Automated checks skipped (historical review)"
- **For current changes**: Pass/fail status of automated checks
- Coverage metrics
- Type checking results (if applicable)
- Failed test details

#### 3. Issues Found
- **For chunked reviews**: Use aggregated findings from Step 4.5
- Group by severity (Critical/High/Medium/Low) with file:line references
- Include cross-chunk concerns and patterns
- Provide specific examples and concrete fix suggestions

#### 4. Security Analysis
- Security implications
- Potential vulnerabilities
- Risk assessment
- Mitigation recommendations

#### 5. Performance Impact
- Performance considerations
- Identified bottlenecks
- Optimization opportunities
- Load testing results (if applicable)

#### 6. Database Changes (if applicable)
- Migration requirements
- Schema impact
- Data integrity considerations
- Query performance impact

#### 7. Documentation Impact
- Documentation needing updates
- API changes to document
- Architectural changes
- Breaking changes

#### 8. Final Recommendation
- **✅ Approve**: All checks passed, ready to merge
- **⚠️ Request Changes**: Issues must be addressed
- **💬 Needs Discussion**: Complex changes requiring team input

#### 9. Review Strategy Used
- Note if chunked review was used (e.g., "Chunked review: 4 batches across 42 files")
- Note if historical review with automated checks skipped

## Historical Review Limitations

When reviewing past commits or historical commit ranges, automated checks are skipped to prevent misleading results since they would run against current code, not the historical state.

**Current Work** (automated checks WILL run):
- No arguments (uncommitted changes)
- `DIFF` keyword or ranges ending in `DIFF` (staged changes)
- `HEAD` by itself (most recent commit)
- Ranges ending in `HEAD` (like `main..HEAD` or `origin/main..HEAD`)

**Historical** (automated checks skipped):
- Specific commit hashes (like `abc123`, not `HEAD`)
- Ranges not ending in `HEAD` or `DIFF` (like `abc123..def456`, `v1.0..v2.0`)
- Branch names alone (like `main`)

To run tests on historical code, checkout the commit manually:
```bash
git checkout <commit-hash>
<test-command>
```

## Examples of Usage

### DEFAULT - Review Uncommitted Changes (Most Common)

- `/pr-self-review` - full review of all uncommitted changes (staged + unstaged)
- `/pr-self-review --quick` - quick review of uncommitted changes
- `/pr-self-review --security` - security-focused review of uncommitted changes
- `/pr-self-review --performance` - performance-focused review of uncommitted changes

### DIFF - Review Staged Changes (Current Work)

**All DIFF patterns are current work and will run automated checks.**

- `/pr-self-review DIFF` - review staged changes ready for commit
- `/pr-self-review DIFF --quick` - quick review of staged changes
- `/pr-self-review HEAD..DIFF` - review the most recent commit plus staged changes
- `/pr-self-review HEAD~2..DIFF` - review the last 2 commits plus staged changes

### HEAD - Review Most Recent Commit (Current Work)

**HEAD by itself is current work and will run automated checks.**

- `/pr-self-review HEAD` - full review of the most recent commit
- `/pr-self-review HEAD --quick` - quick review of the most recent commit
- `/pr-self-review HEAD --security` - security review of the most recent commit

### Single Commit Review (Historical)

**Specific commit hashes (not HEAD) are historical and automated checks are skipped.**

- `/pr-self-review abc123` - full review of specific commit (automated checks skipped)
- `/pr-self-review HEAD~1 --quick` - quick review of the previous commit (automated checks skipped)
- `/pr-self-review 5b3ee1d --security` - security review of commit (automated checks skipped)

### Commit Range Review

**Current work (ranges ending in HEAD - automated checks run)**:

- `/pr-self-review main..HEAD` - full review of all changes from main to HEAD
- `/pr-self-review origin/main..HEAD --security` - security review of all changes not yet in origin/main
- `/pr-self-review HEAD~3..HEAD` - review the last 3 commits

**Historical (ranges not ending in HEAD - automated checks skipped)**:

- `/pr-self-review abc123..def456 --quick` - quick review of commits between two historical refs
- `/pr-self-review v1.0..v2.0` - review changes between version tags

## Note

This command only reviews and reports on changes. To create an actual pull request after review, use your tool's PR creation command (e.g., `gh-pr-create`).


{% if agpm.project.styleguide or agpm.project.best_practices %}

## Project Specific Guidelines

**IMPORTANT**: Project-level guidelines supercede all other guidelines.

{% if agpm.project.styleguide %}

### Project Style Guide

{{ agpm.project.styleguide | content }}

{% endif %}
{% if agpm.project.best_practices %}

### Project Best Practices

{{ agpm.project.best_practices | content }}

{% endif %}
{% endif %}

## Language-Specific Guidelines

Apply language-specific conventions and best practices from:

- **Style Guide**: `{{ agpm.deps.snippets.styleguide.content }}`
- **Best Practices**: `{{ agpm.deps.snippets.best_practices.content }}`
