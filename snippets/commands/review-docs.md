---
agpm:
  version: "1.0.0"
---

# Documentation Review Command

## Your task

Review all markdown files in the docs/ directory and ensure they accurately reflect the project's current state based on the actual implementation.

**CRITICAL**: When comprehensive documentation updates are needed, delegate to specialized agents instead of making extensive edits directly.

## Argument Parsing

1. Parse the review mode from arguments:
   - `--check-only`: Only report what needs updating without making changes
   - `--auto-update`: Make necessary updates to documentation files (default)
   - Arguments: $ARGUMENTS

## Systematic Review Process

2. Systematically review each documentation file in docs/:

   **Identify all documentation files**:
   - List all markdown files in the docs/ directory
   - Include subdirectories (e.g., docs/api/, docs/guides/)
   - Note the purpose of each documentation file

3. For each documentation file, verify accuracy against the implementation:

   **Cross-reference with source code**:
   - Check API endpoints against actual route definitions
   - Verify request/response models against implementation
   - Validate data models against actual schema definitions
   - Confirm configuration options against actual usage in source code
   - Check deployment configs against actual deployment files
   - Verify setup/installation instructions against project structure
   - Validate workflows against actual implementation

4. Analyze recent changes to identify what affects documentation:
   - New API endpoints or routes added
   - Changed request/response schemas
   - Modified behavior or functionality
   - Removed endpoints or deprecated features
   - New data models or schema changes
   - Changes to deployment or configuration
   - Performance improvements or architecture changes
   - New dependencies or requirements

## Accuracy Checks

5. For each documentation file, check for:

   **Accuracy issues**:
   - API endpoints that don't exist in code
   - Request/response examples that don't match implementation
   - Configuration options that aren't used
   - Data fields or models that don't exist
   - Setup/deployment instructions that are outdated
   - Features described but not present
   - Incorrect version numbers or compatibility info

   **Completeness issues**:
   - Missing API endpoints present in code
   - Undocumented request/response fields
   - Missing configuration options
   - Undocumented data models or fields
   - Missing deployment options or requirements
   - Incomplete setup instructions
   - Missing error codes or responses
   - Undocumented dependencies

   **Consistency issues**:
   - Conflicting information between files
   - Inconsistent terminology or naming
   - Mismatched examples across documents
   - Different formatting styles
   - Broken cross-references between docs
   - Inconsistent command examples

## Update Strategy

6. Based on the review, determine what updates are needed:

   **Types of updates to make**:
   - Correct outdated or incorrect information
   - Add documentation for missing features
   - Update examples to match current implementation
   - Fix broken cross-references
   - Standardize formatting and terminology
   - Remove documentation for deprecated features
   - Add clarifications where behavior is unclear

   **For comprehensive documentation improvements, delegate to specialized agents:**
   - Use appropriate task delegation mechanism to invoke specialized agents
   - The agent should handle:
     * Creating detailed API documentation
     * Writing comprehensive usage examples
     * Generating architectural explanations
     * Ensuring consistent documentation style

## Apply Updates

7. Apply updates based on mode:

   **Check-only mode (--check-only)**:
   - Report all discrepancies found per file
   - List specific sections needing updates
   - Show what information is missing or incorrect
   - Provide suggested changes without applying them
   - Summary of issues by severity (critical, important, minor)

   **Auto-update mode (--auto-update or default)**:
   - Make targeted edits to fix discrepancies
   - Preserve existing documentation structure
   - Add new sections only if necessary
   - Update examples to match current implementation
   - Ensure all code snippets are valid
   - Maintain consistent formatting across files

## Quality Standards

8. Maintain documentation quality standards:
   - Keep language clear and technical
   - Use consistent formatting (headers, lists, code blocks)
   - Ensure examples are complete and runnable
   - Include both success and error response examples
   - Provide command-line examples where applicable
   - Use proper markdown syntax
   - Keep files focused on their specific topic

## Validation Guidelines

9. General validation guidelines:

   **API Documentation**:
   - Verify all endpoints exist in source code
   - Check HTTP methods match implementation
   - Validate request/response schemas
   - Ensure authentication/authorization is documented
   - Include pagination details where applicable
   - Document rate limiting if present

   **Data Model Documentation**:
   - Verify all entities and fields exist
   - Check relationship definitions
   - Validate migration/schema documentation
   - Ensure constraints are documented
   - Include data type information

   **Deployment Documentation**:
   - Verify container build instructions work
   - Check deployment configuration accuracy
   - Validate environment variable lists
   - Ensure resource requirements are accurate
   - Include troubleshooting sections

   **Setup/Installation Documentation**:
   - Verify all dependencies are listed
   - Check installation commands are correct
   - Validate configuration steps
   - Ensure prerequisites are documented
   - Include platform-specific notes if needed

## Summary Report

10. Generate a summary report:
    - Total files reviewed
    - Number of issues found per file
    - Critical issues requiring immediate attention
    - Suggested improvements for clarity
    - Overall documentation health assessment

## Examples of Issues to Detect

- API endpoint path differs from documentation
- Response field types don't match implementation
- Configuration variable names are incorrect
- Data model fields are missing or renamed
- Deployment commands reference wrong paths
- Authentication mechanism is incorrectly described
- Pagination parameters don't match API

## Usage Examples

- Default: automatically review and update all docs
- `--check-only`: report discrepancies without making changes
- `--auto-update`: explicitly update documentation (same as default)
