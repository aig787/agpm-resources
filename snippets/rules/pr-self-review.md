# Pull Request Self-Review Standards

## Overview

This document defines comprehensive standards and checklists for conducting thorough pull request self-reviews. These guidelines apply across languages and frameworks, focusing on code quality, security, performance, and maintainability.

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

## Best Practices

### Parallel Execution
- Run independent checks in parallel
- Invoke multiple specialized agents simultaneously
- Execute test suites concurrently where possible

### Context Provision
- Give agents specific context about changes
- Include file paths and change summaries
- Highlight areas of concern
- Provide relevant background

### Output Formatting
- Use markdown for readability
- Include `file:line` references
- Group related issues
- Prioritize by severity
- Make suggestions actionable

### Focus on Value
- Don't be pedantic about style if automated tools handle it
- Focus on logic, architecture, and security
- Consider maintainability and future changes
- Balance perfectionism with pragmatism
