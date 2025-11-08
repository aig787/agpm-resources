---
agpm:
  version: "1.0.0"
---

# Documentation Update Command

## Your task

Review recent changes and ensure README.md and all documentation files accurately reflect the project's current state.

**CRITICAL**: When comprehensive documentation updates are needed, delegate to specialized agents instead of making extensive edits directly.

## Argument Parsing

1. Parse the update mode from arguments:
   - `--check-only`: Only report what needs updating without making changes
   - `--auto-update`: Make necessary updates to documentation (default)
   - Arguments: $ARGUMENTS

## Analyze Recent Changes

2. Analyze recent changes to understand what has been modified:
   - New API endpoints or routes added
   - Changed request/response schemas
   - Modified behavior or functionality
   - Removed endpoints or deprecated features
   - New data models or schema changes
   - Changes to deployment or configuration
   - Performance improvements or architecture changes
   - New dependencies or requirements
   - Security updates or authentication changes

## Review Documentation Files

3. Read the current README.md and related documentation files:

   **Common files to check**:
   - **README.md**: Main landing page and overview
   - **docs/api.md** or **docs/api/**: API documentation
   - **docs/deployment.md**: Deployment instructions
   - **docs/architecture.md**: Technical architecture and design
   - **docs/configuration.md**: Configuration options and settings
   - **docs/testing.md**: Testing strategy and coverage
   - **docs/security.md**: Security considerations
   - **docs/development.md** or **CONTRIBUTING.md**: Development guidelines
   - **docs/troubleshooting.md**: Common issues and solutions
   - Any other project-specific documentation files

   **Critical sections to check**:
   - **Features list**: New capabilities or removed features
   - **API Endpoints**: New routes, handlers, or schemas
     - Request/response models and validation
     - Authentication requirements
     - Error response formats
   - **Installation**: Changes to build or deployment process
   - **Quick Start**: Changes to usage or setup
   - **Data Models**: New entities, fields, or relationships
   - **Configuration**: New settings or environment variables
   - **Security**: Authentication, authorization, access control
   - **Dependencies**: New or removed packages/libraries

## Determine Needed Updates

4. Based on the changes, determine what documentation updates are needed:

   **Types of updates to make**:
   - Add documentation for new features or endpoints
   - Update request/response schemas
   - Correct outdated information
   - Add new usage examples
   - Update data model documentation
   - Update configuration options
   - Update performance claims if improvements were made
   - Fix any inaccuracies introduced by recent changes
   - Remove documentation for deprecated features

   **For comprehensive documentation improvements, delegate to specialized agents:**
   - Use appropriate task delegation mechanism to invoke specialized agents
   - The agent should handle:
     * Creating detailed API documentation
     * Writing comprehensive usage examples
     * Generating architectural explanations
     * Ensuring consistent documentation style
   - The agent will handle complex documentation patterns and ensure quality

   **Where to apply updates**:
   - **README.md**: Overview, quick start, feature list
   - **API documentation**: Endpoints, request/response examples
   - **Deployment documentation**: Setup and configuration instructions
   - **Architecture documentation**: Design decisions, technical details
   - **Configuration documentation**: Settings and environment variables
   - **Testing documentation**: Test strategy, coverage requirements
   - **Security documentation**: Authentication, authorization, best practices

## Apply Updates

5. Apply updates based on mode:

   **Check-only mode (--check-only)**:
   - Report all discrepancies found
   - List specific sections needing updates
   - Show what information is missing or incorrect
   - Provide suggested changes without applying them

   **Auto-update mode (--auto-update or default)**:
   - Make minimal, targeted edits to fix discrepancies
   - Preserve existing documentation structure and style
   - Add new sections only if necessary for new features
   - Update examples to match current implementation
   - Ensure all code snippets are valid

## Quality and Accuracy

6. Focus on accuracy and completeness:
   - Verify all examples work with current implementation
   - Ensure request/response examples are valid
   - Check that deployment instructions are current
   - Validate that feature descriptions match actual behavior
   - Confirm integration details are complete

7. Maintain documentation quality:
   - Keep language clear and concise
   - Preserve existing formatting conventions
   - Ensure examples are practical and helpful
   - Maintain consistent terminology throughout
   - Don't remove useful existing content
   - Keep README.md as a concise landing page
   - Put detailed content in appropriate docs/ files
   - Ensure cross-references between docs are accurate

## Change-to-Documentation Mapping

Examples of changes that require documentation updates:
- Adding a new API endpoint → Document in API documentation
- Changing request/response schemas → Update API examples and models
- Adding new data model → Update data model documentation
- Modifying deployment configuration → Update deployment documentation
- Improving performance → Update performance claims if made
- Adding new dependencies → Update dependency lists
- Changing authentication flow → Update security documentation
- Adding new feature → Update README and feature documentation
- Deprecating functionality → Mark as deprecated in docs
- Changing configuration options → Update configuration documentation

## Usage Examples

- Default: automatically update documentation based on changes
- `--check-only`: report what needs updating without changes
- `--auto-update`: explicitly update documentation (same as default)
