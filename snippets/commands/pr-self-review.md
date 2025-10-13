---
agpm:
  templating: true
dependencies:
  snippets:
    - name: styleguide
      path: ../styleguides/{{ agpm.project.language }}-styleguide.md
      tool: agpm
    - name: best-practices
      path: ../best-practices/{{ agpm.project.language }}-best-practices.md
      tool: agpm
---

# Pull Request Self-Review Command

## Overview

This command performs comprehensive pull request self-reviews following standardized review guidelines and language-specific style conventions. These guidelines apply across languages and frameworks, focusing on code quality, security, performance, and maintainability.

{% if agpm.project.styleguide or  agpm.project.best_practices %}

## Project Specific Guidelines

Apply project-specific conventions and best practices from:

- **Project Style Guide**: `{{ agpm.project.styleguide }}`
- **Project Best Practices**: `{{ agpm.project.best_practices }}`

**IMPORTANT**: Project-level guidelines supercede all other guidelines.
{% endif %}

## Language-Specific Guidelines

Apply language-specific conventions and best practices from:

- **Style Guide**: `{{ agpm.deps.snippets.styleguide.install_path }}`
- **Best Practices**: `{{ agpm.deps.snippets.best_practices.install_path }}`

These files ensure code follows established patterns, idioms, and best practices for the target language.

## Core Review Principles

### 1. Change Context Analysis

Before diving into detailed review, understand the scope:

- **What Changed**: Identify modified, added, and deleted files
- **Change Purpose**: Understand the intent behind modifications
- **Impact Scope**: Assess which components/systems are affected
- **Risk Level**: Evaluate potential for breaking changes

**Focus Rule**: Only review tracked files in version control. Ignore untracked files that aren't part of the change set.

### 2. Automated Checks First

Always run automated checks before manual review:

- **Formatting**: Ensure consistent code style
- **Linting**: Catch common issues and anti-patterns
- **Type Checking**: Verify type safety (if applicable)
- **Tests**: Confirm all tests pass
- **Coverage**: Check test coverage metrics

### 3. Agent Delegation Strategy

For deep code analysis, delegate to specialized agents rather than using direct search tools:

- Provide specific context about what changed
- Include relevant file paths and change summaries
- Run multiple analyses in parallel for efficiency
- Use specialized agents based on the area of concern

## Review Dimensions

### Code Quality

**Language Best Practices**

- [ ] Code follows language idioms and conventions
- [ ] No deprecated APIs or patterns
- [ ] Appropriate use of language features
- [ ] Clear and descriptive naming
- [ ] Proper error handling
- [ ] No code duplication (DRY principle)

**Design Principles**

- [ ] Single Responsibility Principle (SRP)
- [ ] Open/Closed Principle
- [ ] Dependency Inversion where appropriate
- [ ] Separation of concerns
- [ ] Proper abstraction levels

**Readability**

- [ ] Code is self-documenting where possible
- [ ] Complex logic has explanatory comments
- [ ] Function/method length is reasonable
- [ ] Nesting depth is manageable
- [ ] Clear control flow

### Architecture

**Module Structure**

- [ ] Logical organization of code
- [ ] Clear module boundaries
- [ ] Appropriate coupling between components
- [ ] Dependencies flow in the right direction
- [ ] No circular dependencies

**Design Patterns**

- [ ] Appropriate patterns used for the problem
- [ ] No over-engineering
- [ ] Patterns implemented correctly
- [ ] Consistent pattern usage across codebase

**API Design**

- [ ] Clear and consistent interface design
- [ ] Backward compatibility maintained (if required)
- [ ] Appropriate abstraction levels
- [ ] Well-defined contracts

### Security

**Authentication & Authorization**

- [ ] No authentication bypass vulnerabilities
- [ ] Proper authorization checks
- [ ] Secure session management
- [ ] No hardcoded credentials

**Input Validation**

- [ ] All user input is validated
- [ ] Protection against injection attacks (SQL, command, etc.)
- [ ] Proper sanitization of data
- [ ] Appropriate use of parameterized queries

**Data Protection**

- [ ] Sensitive data is encrypted in transit
- [ ] Sensitive data is encrypted at rest (where required)
- [ ] No secrets in code or logs
- [ ] Proper data isolation (multi-tenancy)
- [ ] No exposure of internal details in error messages

**Secrets Management**

- [ ] No hardcoded passwords or API keys
- [ ] Environment variables used appropriately
- [ ] No credentials in version control
- [ ] Secure credential rotation supported

**Common Vulnerability Patterns**

- [ ] No SQL injection risks
- [ ] No command injection risks
- [ ] No path traversal vulnerabilities
- [ ] No insecure deserialization
- [ ] No SSRF (Server-Side Request Forgery) risks

### Database (if applicable)

**Schema Changes**

- [ ] Migration files present for schema changes
- [ ] Migrations are reversible
- [ ] No data loss in migrations
- [ ] Proper indexing strategy
- [ ] Backward compatible changes (if required)

**Query Patterns**

- [ ] No N+1 query problems
- [ ] Efficient use of indexes
- [ ] Appropriate query optimization
- [ ] Proper use of transactions
- [ ] Connection pooling configured correctly

**Data Integrity**

- [ ] Foreign key constraints where appropriate
- [ ] Data validation at database level
- [ ] No orphaned records
- [ ] Proper cascade behavior

### Performance

**Async/Concurrency (if applicable)**

- [ ] No blocking operations in async context
- [ ] Proper use of async libraries
- [ ] No race conditions
- [ ] Appropriate use of locks/semaphores

**Resource Usage**

- [ ] No memory leaks
- [ ] Efficient resource allocation
- [ ] Proper cleanup of resources
- [ ] Appropriate batch sizes for bulk operations

**Optimization Opportunities**

- [ ] Caching used where beneficial
- [ ] Lazy loading implemented where appropriate
- [ ] Database queries optimized
- [ ] Unnecessary computations eliminated

**Scalability Considerations**

- [ ] Code handles increased load gracefully
- [ ] No bottlenecks identified
- [ ] Proper pagination for large datasets
- [ ] Resource limits respected

### Testing

**Test Coverage**

- [ ] New code has appropriate test coverage
- [ ] Critical paths are well-tested
- [ ] Edge cases are tested
- [ ] Error conditions are tested

**Test Quality**

- [ ] Tests are maintainable
- [ ] Tests are not flaky
- [ ] Tests are fast enough
- [ ] Tests verify behavior, not implementation

**Testing Patterns**

- [ ] Appropriate use of mocking/stubbing
- [ ] Mock signatures match real APIs
- [ ] Integration tests where needed
- [ ] Unit tests are properly isolated

**Test Organization**

- [ ] Tests are well-organized
- [ ] Test names are descriptive
- [ ] Test fixtures are appropriate
- [ ] Setup/teardown is proper

### Documentation

**Code Documentation**

- [ ] Complex logic is explained
- [ ] Public APIs are documented
- [ ] Function/method purposes are clear
- [ ] Important decisions are documented

**API Documentation**

- [ ] API changes are documented
- [ ] New endpoints documented
- [ ] Request/response formats clear
- [ ] Authentication requirements documented

**README & Guides**

- [ ] README updated for user-facing changes
- [ ] Setup instructions accurate
- [ ] Examples updated
- [ ] Breaking changes documented

**Architectural Documentation**

- [ ] Design decisions documented
- [ ] Architecture diagrams updated (if needed)
- [ ] Data flow documented (if changed)
- [ ] Integration points documented

## Review Modes

### Quick Review

Focus on essentials for fast feedback:

- Automated formatting and linting
- Basic test execution
- Quick security scan
- Fast style check

**Use When**: Small changes, hotfixes, documentation updates

### Full Review (Standard)

Comprehensive analysis across all dimensions:

- All automated checks
- Manual review of all dimensions
- Complete test suite execution
- Agent-assisted deep analysis
- Coverage and quality metrics

**Use When**: Feature development, refactoring, significant changes

### Security-Focused Review

Deep dive into security implications:

- Security-specific tests and scans
- Detailed threat modeling
- Vulnerability pattern matching
- Authentication/authorization verification
- Data protection review
- Secrets and credential audit

**Use When**: Security-sensitive changes, authentication systems, data handling

### Performance-Focused Review

Analysis of performance impact:

- Performance test execution
- Profiling and benchmarking
- Query analysis
- Resource usage review
- Async/concurrency verification
- Load testing (if configured)

**Use When**: Performance-critical code, database changes, high-load features

## Issue Severity Levels

### Critical

- Security vulnerabilities
- Data loss risks
- Authentication bypass
- Critical performance degradation
- System stability threats

### High

- Significant bugs
- Poor error handling
- Architectural violations
- Missing critical tests
- Performance issues

### Medium

- Code quality issues
- Minor bugs
- Missing documentation
- Suboptimal patterns
- Test gaps

### Low

- Style inconsistencies
- Minor optimizations
- Documentation improvements
- Refactoring opportunities

## Report Structure

### 1. Changes Overview

- Files modified/added/deleted
- Brief description of changes
- Scope and purpose

### 2. Test Results

- Pass/fail status
- Coverage metrics
- Type checking results
- Failed test details

### 3. Issues Found

- Grouped by severity
- File paths and line numbers
- Specific examples
- Concrete fix suggestions

### 4. Security Analysis

- Security implications
- Potential vulnerabilities
- Risk assessment
- Mitigation recommendations

### 5. Performance Impact

- Performance considerations
- Identified bottlenecks
- Optimization opportunities
- Load testing results (if applicable)

### 6. Database Changes

- Migration requirements
- Schema impact
- Data integrity considerations
- Query performance impact

### 7. Documentation Impact

- Documentation needing updates
- API changes to document
- Architectural changes
- Breaking changes

### 8. Final Recommendation

- **✅ Approve**: All checks passed, ready to merge
- **⚠️ Request Changes**: Issues must be addressed
- **💬 Needs Discussion**: Complex changes requiring team input

## Your Task

Perform a comprehensive pull request self-review based on the arguments provided, following the standards defined above and applying the language-specific guidelines.

**IMPORTANT**: Always run multiple independent operations IN PARALLEL by using multiple tool calls in a single message. This significantly improves performance.

**CRITICAL**: Use the Task tool to delegate to specialized agents for code analysis, NOT Grep or other direct tools. Agents have context about the project and can provide deeper insights.

## Execution Steps

### Step 1: Read Required Files

Read the following files IN PARALLEL:

{% if agpm.project.styleguide %}

- Project style guide: `{{ agpm.project.styleguide }}`
  {% endif %}
  {% if agpm.project.best_practices %}
- Project best practices: `{{ agpm.project.best_practices }}`
  {% endif %}
- Language style guide: `{{ agpm.deps.snippets.styleguide.install_path }}`
- Language best practices: `{{ agpm.deps.snippets.best_practices.install_path }}`

### Step 2: Parse Review Type

Parse the review type from arguments:

- `--quick`: Basic formatting and linting only
- `--full`: Complete review with all checks (default if no arguments)
- `--security`: Focus on security implications
- `--performance`: Focus on performance analysis
- Arguments received: $ARGUMENTS

### Step 3: Gather Change Context

Run these commands IN PARALLEL to understand what changed:

- `git diff HEAD` - See current changes
- `git status --short` - See files changed
- `git log --oneline -5` - See recent commits

**IMPORTANT**: Focus only on tracked files - ignore untracked files marked with `??` in git status.

### Step 4: Execute Review Based on Mode

Follow the review mode guidelines defined above:

#### Quick Review (`--quick`)

1. Run automated checks IN PARALLEL:
   - Formatting checks (e.g., ruff, black, prettier)
   - Linting checks (e.g., ruff, eslint, golangci-lint)
   - Fast/unit tests only
2. Apply quick checklist:
   - Automated formatting
   - Basic test execution
   - Quick security scan

#### Full Review (`--full` or default)

1. Run quick checks first IN PARALLEL
2. Use Task tool to delegate deep analysis IN PARALLEL:
   - Delegate to specialized agents (backend-engineer, linting-advanced, etc.)
   - Provide specific context about changes
   - Include file paths and change summaries
3. Apply comprehensive checklist:
   - All review dimensions (Code Quality, Architecture, Security, etc.)
   - All automated checks (formatting, linting, type checking)
   - Complete test suite execution
   - Coverage and quality metrics
4. Check for additional requirements:
   - Database migrations if models changed
   - API documentation updates
   - Configuration file changes

#### Security-Focused Review (`--security`)

1. Run security-focused tests if available
2. Delegate to security-focused agents with Task tool
3. Apply security checklist:
   - Authentication & Authorization
   - Input Validation
   - Data Protection
   - Secrets Management
   - Common Vulnerability Patterns
4. Run targeted pattern searches IN PARALLEL:
   - Search for credential patterns (password, api_key, secret)
   - Search for injection risks (SQL, command, path traversal)
   - Search for hardcoded secrets

#### Performance-Focused Review (`--performance`)

1. Run performance tests if available
2. Delegate to performance-focused agents with Task tool
3. Apply performance checklist:
   - Async/Concurrency patterns
   - Resource Usage
   - Optimization Opportunities
   - Scalability Considerations
4. Search for common anti-patterns:
   - Blocking operations in async code
   - N+1 query patterns
   - Missing database indexes
   - Inefficient resource usage

### Step 5: Apply Review Dimensions

For manual review, systematically check each dimension defined above:

- **Code Quality**: Apply language best practices and design principles from the best practices file, check readability
- **Architecture**: Module structure, design patterns, API design
- **Security**: All security checklists defined above
- **Database**: Schema changes, query patterns, data integrity
- **Performance**: All performance checklists defined above
- **Testing**: Test coverage, quality, patterns, organization
- **Documentation**: Code docs, API docs, README, architectural docs

**Use both language-specific files**:

- Apply the **style guide** to ensure code follows formatting and naming conventions
- Apply the **best practices** to ensure code follows language idioms, patterns, and architectural principles

### Step 6: Generate Summary Report

Create a comprehensive summary report following the report structure defined above:

1. **Changes Overview** - Files modified, description, scope
2. **Test Results** - Pass/fail status, coverage, type checking
3. **Issues Found** - Grouped by severity (Critical/High/Medium/Low) with file:line references
4. **Security Analysis** - Implications, vulnerabilities, mitigation recommendations
5. **Performance Impact** - Considerations, bottlenecks, optimization opportunities
6. **Database Changes** - Migrations, schema impact, data integrity
7. **Documentation Impact** - Updates needed, API changes, architectural changes
8. **Final Recommendation**:
   - ✅ **Approve**: All checks passed, ready to merge
   - ⚠️ **Request Changes**: Issues must be addressed
   - 💬 **Needs Discussion**: Complex changes requiring team input

## Agent Delegation

**ALWAYS** use the Task tool for code analysis following the delegation strategy defined above:

1. Provide agents with specific context about what changed
2. Run multiple Task invocations in parallel for efficiency
3. Include relevant file paths and change summaries in prompts
4. Use specialized agents based on the area of concern:
   - **General code review**: `backend-engineer` or language-specific general agent
   - **Complex linting/refactoring**: `linting-advanced` or `linting-specialist`
   - **Security analysis**: Security-focused agent if available
   - **Performance analysis**: Performance-focused agent if available

Example Task invocation structure:

```
Task(
  description="Brief description of what to review",
  prompt="Review the following changes for [specific concern]:

  Files changed: [list files]
  Change summary: [describe changes]
  Focus areas: [what to look for based on checklist]

  Apply the relevant checklists from the PR self-review standards.
  Ensure code follows the language-specific style guide and best practices.",
  subagent_type="backend-engineer"  # or other appropriate agent
)
```

## Output Format

Present findings following these best practices:

- Use markdown for readability
- Include `file:line` references
- Group related issues
- Prioritize by severity
- Make suggestions actionable
- Don't be pedantic about style if automated tools handle it
- Focus on logic, architecture, and security
- Consider maintainability and future changes
- Balance perfectionism with pragmatism

## Examples

The command supports various review modes:

- **Default** (no args): Full comprehensive review
- **`--quick`**: Quick formatting and linting check
- **`--security`**: Focused security review
- **`--performance`**: Performance-focused analysis

Each mode applies the appropriate checklists defined above, follows the language-specific style guide and best practices, and delegates to specialized agents as needed.
