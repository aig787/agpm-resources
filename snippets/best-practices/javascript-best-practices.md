---
agpm:
  version: "1.1.0"
---
# JavaScript Best Practices

This document defines technical best practices for JavaScript development, covering tools, patterns, testing, security, and performance optimization.

## Core Principles

1. **Idiomatic JavaScript**: Write code that follows JavaScript conventions and modern ES6+ standards
2. **Zero Warnings Policy**: All code must pass linting without warnings
3. **Consistent Formatting**: All code must be formatted with Prettier
4. **Type Safety**: Use TypeScript or JSDoc for type annotations
5. **Error Handling**: Implement proper exception handling and validation
6. **Clean Architecture**: Separate concerns with clear architectural layers
7. **Test Coverage**: Maintain >70% test coverage
8. **Security First**: Follow security best practices from the start

## Mandatory Completion Checklist

Before considering any JavaScript code complete, you MUST:

1. ✅ Run formatter (`prettier --write .`)
2. ✅ Run linter (`eslint .`)
3. ✅ Run type checker (`tsc --noEmit` if using TypeScript)
4. ✅ Run tests (`npm test` or `jest`)
5. ✅ Verify test coverage (`npm run test:coverage` - target >70%)
6. ✅ Verify all dependencies are properly declared

## Development Tools

### Package Management: npm (Recommended)

**Use `npm` for modern JavaScript projects**: Standard package manager with extensive ecosystem

```bash
# Initialize new project
npm init -y

# Install dependencies
npm install express lodash axios

# Install dev dependencies
npm install --save-dev eslint prettier jest typescript @types/node

# Run scripts
npm start
npm test
npm run lint

# Manage dependencies
npm outdated
npm audit fix
npm update
```

### Alternative: pnpm

```bash
# Install pnpm
npm install -g pnpm

# Initialize new project
pnpm init

# Install dependencies
pnpm add express lodash axios

# Install dev dependencies
pnpm add -D eslint prettier jest typescript

# Run scripts
pnpm dev
pnpm test
pnpm lint
```

### Dependency Best Practices

- **Pin exact versions in production**: `package-lock.json` handles this automatically
- **Use semantic versioning**: Understand `^`, `~`, and exact versions
- **Keep dependencies updated**: Regularly review and update
- **Security auditing**: Use `npm audit` or `pnpm audit`
- **Separate dev dependencies**: Keep development tools separate from production deps
- **Document dependency choices**: Explain why specific packages are required

## Type Safety

### TypeScript (Recommended)

**Use TypeScript for type safety**:

```bash
# Initialize TypeScript project
npx tsc --init

# Install type definitions
npm install --save-dev @types/node @types/express
```

**Basic TypeScript usage**:

```typescript
// Function with type annotations
function processUser(user: { id: number; name: string }): string {
  return `User: ${user.name} (${user.id})`;
}

// Interface for object shapes
interface User {
  id: number;
  name: string;
  email?: string; // Optional property
}

// Generic function
function first<T>(items: T[]): T | undefined {
  return items[0];
}

// Union types
type Status = "pending" | "approved" | "rejected";
```

### JSDoc for JavaScript Projects

**Use JSDoc annotations when not using TypeScript**:

```javascript
/**
 * Process a user object
 * @param {{id: number, name: string, email?: string}} user - User object
 * @returns {string} Formatted user string
 * @throws {Error} When user data is invalid
 */
function processUser(user) {
  if (!user.id || !user.name) {
    throw new Error("Invalid user data");
  }
  return `User: ${user.name} (${user.id})`;
}

/**
 * Get first item from array
 * @template T
 * @param {T[]} items - Array of items
 * @returns {T|undefined} First item or undefined
 */
function first(items) {
  return items[0];
}
```

## Error Handling

### Exception Best Practices

**Use specific error types**:

```javascript
// Good - specific error
class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.name = "ValidationError";
    this.field = field;
  }
}

// Avoid - generic error
throw new Error("Something went wrong");
```

**Create custom error hierarchy**:

```javascript
class AppError extends Error {
  constructor(message, code = "UNKNOWN_ERROR") {
    super(message);
    this.name = "AppError";
    this.code = code;
  }
}

class DatabaseError extends AppError {
  constructor(message, originalError) {
    super(message, "DATABASE_ERROR");
    this.originalError = originalError;
  }
}

class NotFoundError extends AppError {
  constructor(resource, id) {
    super(`${resource} with id ${id} not found`, "NOT_FOUND");
    this.resource = resource;
    this.id = id;
  }
}
```

**Handle exceptions properly**:

```javascript
try {
  const result = await riskyOperation();
  return result;
} catch (error) {
  if (error instanceof ValidationError) {
    logger.warn(`Validation failed: ${error.message}`);
    throw error; // Re-raise to let caller handle
  } else if (error instanceof DatabaseError) {
    logger.error(`Database error: ${error.message}`, { originalError: error.originalError });
    throw new AppError("Service temporarily unavailable", "SERVICE_UNAVAILABLE");
  } else {
    logger.error(`Unexpected error: ${error.message}`, { error });
    throw new AppError("Internal server error", "INTERNAL_ERROR");
  }
}
```

**Use async/await with proper error handling**:

```javascript
// Good - proper async error handling
async function fetchUserData(userId) {
  try {
    const user = await userRepository.findById(userId);
    if (!user) {
      throw new NotFoundError("User", userId);
    }
    return user;
  } catch (error) {
    logger.error(`Failed to fetch user ${userId}`, { error });
    throw error;
  }
}

// Avoid - promise chains without error handling
function fetchUserDataBad(userId) {
  return userRepository.findById(userId)
    .then(user => {
      if (!user) throw new Error("User not found");
      return user;
    });
  // Missing catch block
}
```

## Data Validation

### Validation Libraries

**Use Joi or Zod for validation**:

```javascript
// Using Joi
const Joi = require("joi");

const userSchema = Joi.object({
  name: Joi.string().min(1).max(100).required(),
  email: Joi.string().email().required(),
  age: Joi.number().integer().min(0).max(150),
});

function validateUser(userData) {
  const { error, value } = userSchema.validate(userData);
  if (error) {
    throw new ValidationError(error.details[0].message, error.details[0].path.join("."));
  }
  return value;
}

// Using Zod (TypeScript-friendly)
const { z } = require("zod");

const UserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional(),
});

function validateUser(userData) {
  return UserSchema.parse(userData);
}
```

### Validation Best Practices

- **Validate at API boundaries**: Never trust external input
- **Use schema validation**: Joi, Zod, or similar libraries
- **Provide clear error messages**: Help users understand what went wrong
- **Sanitize input**: Remove or escape potentially dangerous content

```javascript
// Input sanitization example
function sanitizeInput(input) {
  if (typeof input !== "string") return input;
  
  return input
    .trim()
    .replace(/[<>]/g, "") // Remove HTML tags
    .replace(/javascript:/gi, ""); // Remove javascript: URLs
}
```

## Testing Strategy

### Jest Framework

**Project structure**:

```
myproject/
├── src/
│   ├── index.js
│   ├── services/
│   │   └── userService.js
│   └── utils/
│       └── helpers.js
├── tests/
│   ├── setup.js           # Test setup
│   ├── services/
│   │   └── userService.test.js
│   └── utils/
│       └── helpers.test.js
├── package.json
└── jest.config.js
```

### Writing Tests

**Basic test**:

```javascript
describe("calculateTotal", () => {
  test("calculates sum of numbers", () => {
    const result = calculateTotal([10, 20, 30]);
    expect(result).toBe(60);
  });
});
```

**Using fixtures and setup**:

```javascript
// tests/setup.js
const { User } = require("../src/models");

beforeEach(() => {
  // Reset database before each test
  User.clear();
});

// tests/services/userService.test.js
const userService = require("../../src/services/userService");

describe("UserService", () => {
  test("creates user with valid data", () => {
    const userData = { name: "John", email: "john@example.com" };
    const user = userService.create(userData);
    
    expect(user.name).toBe("John");
    expect(user.email).toBe("john@example.com");
    expect(user.id).toBeDefined();
  });
});
```

**Mocking external dependencies**:

```javascript
const userService = require("../src/services/userService");
const emailService = require("../src/services/emailService");

jest.mock("../src/services/emailService");

describe("UserService", () => {
  test("sends welcome email when creating user", async () => {
    emailService.sendWelcomeEmail.mockResolvedValue(true);
    
    const userData = { name: "John", email: "john@example.com" };
    await userService.createAndNotify(userData);
    
    expect(emailService.sendWelcomeEmail).toHaveBeenCalledWith(
      userData.email,
      userData.name
    );
  });
});
```

**Testing async code**:

```javascript
describe("async functions", () => {
  test("resolves with correct data", async () => {
    const result = await fetchData(123);
    expect(result).toEqual({ id: 123, name: "Test" });
  });

  test("rejects with error", async () => {
    await expect(fetchData(-1)).rejects.toThrow("Invalid ID");
  });
});
```

### Testing Best Practices

- **Aim for >70% coverage**: Use `jest --coverage`
- **Test isolation**: Each test should be independent
- **Use descriptive test names**: `userCreation_withValidData_createsUser`
- **Test edge cases**: Empty inputs, null values, boundary conditions
- **Use test categories**:
  ```javascript
  describe("UserService", () => {
    describe("create", () => {
      test("with valid data creates user", () => {});
      test("with invalid email throws error", () => {});
    });
  });
  ```

## Linting & Code Quality

### ESLint Configuration

**Recommended `.eslintrc.js`**:

```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
    jest: true,
  },
  extends: [
    "eslint:recommended",
    "@typescript-eslint/recommended",
    "prettier",
  ],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
  },
  plugins: ["@typescript-eslint"],
  rules: {
    "no-console": "warn",
    "no-unused-vars": "error",
    "prefer-const": "error",
    "no-var": "error",
    "object-shorthand": "error",
    "prefer-arrow-callback": "error",
    "prefer-template": "error",
    "template-curly-spacing": "error",
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
  },
};
```

### Prettier Configuration

**`.prettierrc`**:

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
```

### Linting Categories

**Mechanical fixes (safe to auto-fix)**:

- **no-unused-vars**: Unused variables
- **prefer-const**: Use const instead of let when possible
- **object-shorthand**: Use shorthand object properties
- **prefer-arrow-callback**: Use arrow functions for callbacks
- **template-curly-spacing**: Consistent template literal spacing

**Complex fixes (requires analysis)**:

- **no-console**: Console statements in production code
- **complexity**: Cyclomatic complexity - refactor complex functions
- **max-depth**: Nested depth - simplify nested structures
- **max-params**: Too many parameters - consider options object

## Async Programming

### Async/Await Best Practices

**Use async/await for I/O operations**:

```javascript
// Good - async/await
async function fetchUserData(userId) {
  try {
    const user = await userRepository.findById(userId);
    const profile = await profileRepository.findByUserId(userId);
    return { ...user, profile };
  } catch (error) {
    logger.error(`Failed to fetch user ${userId}`, { error });
    throw error;
  }
}

// Avoid - promise chains
function fetchUserDataBad(userId) {
  return userRepository.findById(userId)
    .then(user => profileRepository.findByUserId(userId))
    .then(profile => ({ ...user, profile }))
    .catch(error => {
      logger.error(`Failed to fetch user ${userId}`, { error });
      throw error;
    });
}
```

**Concurrent operations with Promise.all**:

```javascript
// Good - concurrent execution
async function fetchAllUsers(userIds) {
  const promises = userIds.map(id => userRepository.findById(id));
  const users = await Promise.all(promises);
  return users;
}

// Handle partial failures
async function fetchAllUsersWithFailures(userIds) {
  const results = await Promise.allSettled(
    userIds.map(id => userRepository.findById(id))
  );
  
  const users = results
    .filter(result => result.status === "fulfilled")
    .map(result => result.value);
    
  const failures = results
    .filter(result => result.status === "rejected")
    .map(result => result.reason);
    
  return { users, failures };
}
```

### Async Guidelines

- **Use async/await over promises**: More readable and easier to debug
- **Handle errors properly**: Always use try/catch with async/await
- **Use Promise.all for concurrency**: When operations can run in parallel
- **Avoid callback hell**: Prefer async/await or promise chains
- **Don't mix callbacks and promises**: Choose one pattern and stick to it

## Database Best Practices

### ORMs and Query Builders

**Use modern ORMs like Prisma or TypeORM**:

```javascript
// Prisma example
const { PrismaClient } = require("@prisma/client");
const prisma = new PrismaClient();

async function createUser(userData) {
  return await prisma.user.create({
    data: userData,
    include: {
      profile: true,
    },
  });
}

async function findUsersWithPosts() {
  return await prisma.user.findMany({
    include: {
      posts: {
        orderBy: {
          createdAt: "desc",
        },
        take: 10,
      },
    },
  });
}
```

### Query Optimization

**Avoid N+1 queries**:

```javascript
// Bad - N+1 queries
async function getUsersWithPostsBad() {
  const users = await prisma.user.findMany();
  for (const user of users) {
    user.posts = await prisma.post.findMany({
      where: { userId: user.id },
    });
  }
  return users;
}

// Good - single query with include
async function getUsersWithPostsGood() {
  return await prisma.user.findMany({
    include: {
      posts: true,
    },
  });
}
```

**Implement pagination**:

```javascript
async function getUsersPage(page = 1, pageSize = 20) {
  const skip = (page - 1) * pageSize;
  
  const [users, total] = await Promise.all([
    prisma.user.findMany({
      skip,
      take: pageSize,
      orderBy: { createdAt: "desc" },
    }),
    prisma.user.count(),
  ]);
  
  return {
    users,
    pagination: {
      page,
      pageSize,
      total,
      totalPages: Math.ceil(total / pageSize),
    },
  };
}
```

## Security Best Practices

### Input Validation

**Always validate and sanitize input**:

```javascript
// Good - parameterized queries prevent SQL injection
const user = await prisma.user.findFirst({
  where: {
    id: userId, // Prisma handles parameterization
  },
});

// Bad - vulnerable to injection (if using raw queries)
const query = `SELECT * FROM users WHERE id = ${userId}`; // Don't do this!
```

### Authentication and Authorization

**Use secure authentication practices**:

```javascript
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");

// Hash passwords
async function hashPassword(password) {
  const saltRounds = 12;
  return await bcrypt.hash(password, saltRounds);
}

// Verify passwords
async function verifyPassword(password, hashedPassword) {
  return await bcrypt.compare(password, hashedPassword);
}

// Generate JWT tokens
function generateToken(user) {
  return jwt.sign(
    { 
      userId: user.id, 
      email: user.email 
    },
    process.env.JWT_SECRET,
    { expiresIn: "24h" }
  );
}
```

### Security Guidelines

- **Validate all user input**: Never trust external data
- **Use parameterized queries**: Prevent SQL injection
- **Implement authentication & authorization**: JWT, OAuth2, etc.
- **Enable HTTPS**: Always use TLS in production
- **Implement rate limiting**: Prevent abuse
- **Don't log sensitive data**: Passwords, tokens, API keys
- **Regular security audits**: Use `npm audit` and security scanners
- **Implement CSRF protection**: For state-changing operations
- **Keep dependencies updated**: Address security vulnerabilities

```bash
# Security scanning
npm audit
npm audit fix

# Use security-focused packages
npm install helmet cors express-rate-limit
```

## Performance Optimization

### Profiling

**Profile before optimizing**:

```javascript
// Node.js built-in profiler
node --prof app.js
node --prof-process isolate-*.log > processed.txt

// Or use clinic.js
npm install -g clinic
clinic doctor -- node app.js
clinic flame -- node app.js
```

### Memory Management

**Use efficient data structures**:

```javascript
// Good - use Map for frequent lookups
const userCache = new Map();

function getUser(id) {
  if (userCache.has(id)) {
    return userCache.get(id);
  }
  
  const user = fetchUserFromDatabase(id);
  userCache.set(id, user);
  return user;
}

// Avoid - array.find for large datasets
function getUserBad(id) {
  return allUsers.find(user => user.id === id);
}
```

### Caching

**Use caching for expensive operations**:

```javascript
const NodeCache = require("node-cache");
const cache = new NodeCache({ stdTTL: 600 }); // 10 minutes

async function getExpensiveData(key) {
  const cached = cache.get(key);
  if (cached) {
    return cached;
  }
  
  const data = await fetchExpensiveDataFromAPI(key);
  cache.set(key, data);
  return data;
}
```

### Performance Guidelines

- **Profile before optimizing**: Use Node.js profiler or clinic.js
- **Use efficient data structures**: Map/Set for lookups, avoid array.find on large arrays
- **Implement caching**: Redis or in-memory for frequently accessed data
- **Use connection pooling**: For database and HTTP connections
- **Batch operations**: Reduce round trips to database/API
- **Use lazy loading**: Load data only when needed
- **Optimize database queries**: Proper indexing, avoid N+1
- **Consider streaming**: For large data processing
- **Choose appropriate algorithms**: Based on data size and access patterns

## Project Structure

**Recommended structure**:

```
myproject/
├── package.json              # Project configuration
├── package-lock.json         # Dependency lock file
├── README.md                 # Project documentation
├── .gitignore                # Git ignore file
├── .env.example              # Environment variables template
├── .eslintrc.js              # ESLint configuration
├── .prettierrc               # Prettier configuration
├── jest.config.js            # Jest configuration
├── tsconfig.json             # TypeScript configuration
├── src/
│   ├── index.js              # Application entry point
│   ├── config/               # Configuration
│   │   ├── database.js
│   │   └── server.js
│   ├── controllers/          # Request handlers
│   │   ├── userController.js
│   │   └── authController.js
│   ├── services/             # Business logic
│   │   ├── userService.js
│   │   └── authService.js
│   ├── models/               # Data models
│   │   ├── User.js
│   │   └── Post.js
│   ├── middleware/           # Express middleware
│   │   ├── auth.js
│   │   └── validation.js
│   ├── routes/               # Route definitions
│   │   ├── users.js
│   │   └── auth.js
│   ├── utils/                # Utility functions
│   │   ├── logger.js
│   │   └── helpers.js
│   └── types/                # TypeScript types (if using TS)
│       └── index.d.ts
├── tests/                    # Tests
│   ├── setup.js
│   ├── controllers/
│   ├── services/
│   └── utils/
├── docs/                     # Documentation
└── scripts/                  # Utility scripts
```

## CI/CD Integration

### Pre-commit Hooks

**`.husky/pre-commit`**:

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Run linting and formatting
npm run lint
npm run format

# Run tests
npm test

# Check for security vulnerabilities
npm audit --audit-level moderate
```

### CI Pipeline Steps

1. **Install dependencies**: `npm ci`
2. **Run linting**: `npm run lint`
3. **Run type checking**: `npm run type-check` (if using TypeScript)
4. **Run tests with coverage**: `npm run test:coverage`
5. **Security audit**: `npm audit --audit-level moderate`
6. **Check formatting**: `npm run format:check`

## Context7 Integration

Always use Context7 MCP server for current documentation when developing JavaScript projects:

### Key Libraries

- `/nodejs/node` - Node.js runtime documentation
- `/expressjs/express` - Web framework
- `/prisma/prisma` - Modern ORM
- `/typescriptlang/typescript` - TypeScript language
- `/facebook/jest` - Testing framework
- `/eslint/eslint` - Linting tool
- `/prettier/prettier` - Code formatter
- `/nodejs/undici` - HTTP client

### Example Usage

```
Create an Express.js application with TypeScript, Prisma ORM, and JWT authentication.
Include proper async patterns, validation, and error handling.
use context7 /expressjs/express /prisma/prisma /typescriptlang/typescript
```

## Summary

- **Use modern tools**: `npm`, `eslint`, `prettier`, `jest`, `typescript`
- **Type everything**: TypeScript or JSDoc for type safety
- **Test thoroughly**: >70% coverage, unit + integration tests
- **Validate all input**: Never trust external data
- **Handle errors properly**: Custom error types, proper async error handling
- **Optimize when needed**: Profile first, then optimize
- **Secure by default**: Authentication, validation, encryption
- **Follow clean architecture**: Separate concerns, clear layers
- **Automate quality checks**: CI/CD, pre-commit hooks
- **Keep dependencies updated**: Security and features

These practices ensure robust, maintainable, and secure JavaScript applications.