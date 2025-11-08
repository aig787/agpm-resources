---
agpm:
  version: "1.1.0"
---
# JavaScript Style Guide

This document defines the code style standards for JavaScript projects. It covers formatting, naming conventions, type annotations, imports, and documentation style.

## Code Formatting

### Line Length
- **Maximum line length**: 80-100 characters (configurable per project)
- **Break long lines** at logical points for readability
- Use Prettier for automatic line breaking

### Indentation
- **Use 2 spaces** per indentation level (enforced by Prettier)
- **Never mix tabs and spaces**
- Continuation lines align with opening delimiter or use hanging indent

### Whitespace
- **One blank line** between top-level functions and classes
- **No blank lines** between consecutive imports
- **One blank line** at end of file
- **No trailing whitespace** on any line
- **Spaces around operators**: `x = y + z`, not `x=y+z`
- **No spaces** inside brackets: `[1, 2, 3]`, not `[ 1, 2, 3 ]`
- **Spaces after commas**: `func(a, b, c)`, not `func(a,b,c)`

### Trailing Commas
- **Use trailing commas** in multi-line structures:
  ```javascript
  const items = [
    "first",
    "second",
    "third",  // trailing comma
  ];

  const config = {
    host: "localhost",
    port: 8080,
    timeout: 30000,  // trailing comma
  };
  ```

### String Quotes
- **Prefer single quotes** for strings: `'hello'`
- **Use double quotes** to avoid escaping: `"He said 'hi'"`
- **Use template literals** for string interpolation: `` `Hello ${name}` ``
- Be consistent within a project

### Semicolons
- **Always use semicolons** at the end of statements
- Prevents automatic semicolon insertion issues
- Required by most linting configurations

## Naming Conventions

### Variables and Functions
- **Use `camelCase`** for variables and functions
- **Use descriptive names** that convey intent
- **Avoid single-letter names** except in:
  - Loop counters: `for (let i = 0; i < 10; i++)`
  - Common mathematical variables: `x, y, z`
  - Callback parameters: `.map(item => item.id)`
  - Array methods: `arr.find(x => x.id)`

**Examples**:
```javascript
// Good
let userCount = 10;
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Avoid
let uc = 10;
function calcTot(items) {
  return items.reduce((s, i) => s + i.price, 0);
}
```

### Classes and Constructors
- **Use `PascalCase`** for class names and constructor functions
- **Use nouns** for class names
- **Use clear, descriptive names**

**Examples**:
```javascript
// Good
class UserAccount {
  constructor(username, email) {
    this.username = username;
    this.email = email;
  }
}

class HTTPResponse {
  constructor(statusCode, data) {
    this.statusCode = statusCode;
    this.data = data;
  }
}

// Avoid
class user_account {
  constructor(username, email) {
    this.username = username;
    this.email = email;
  }
}
```

### Constants
- **Use `SCREAMING_SNAKE_CASE`** for constants
- Define at module level or in appropriate scope
- Use `const` declaration

**Examples**:
```javascript
const MAX_CONNECTIONS = 100;
const DEFAULT_TIMEOUT = 30000;
const API_BASE_URL = "https://api.example.com";

// For objects that shouldn't be reassigned
const CONFIG = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
};
```

### Private and Protected
- **Use underscore prefix** for private properties: `_private`
- **Use underscore prefix** for protected methods: `_protectedMethod`
- **No special prefix** for public properties

**Examples**:
```javascript
class MyClass {
  constructor() {
    this.public = "accessible";
    this._protected = "internal use";
    this._private = "truly private";
  }

  publicMethod() {
    return this.public;
  }

  _protectedMethod() {
    return this._protected;
  }

  _privateMethod() {
    return this._private;
  }
}
```

### Boolean Names
- **Prefix with `is`, `has`, or `should`** for clarity
- **Use affirmative names**

**Examples**:
```javascript
// Good
let isActive = true;
let hasPermission = false;
let shouldRetry = true;

// Avoid
let active = true;  // ambiguous
let noPermission = true;  // negative naming
```

### File and Module Names
- **Use `kebab-case`** for file names: `user-service.js`
- **Use `camelCase`** for module exports when appropriate
- **Index files**: Use `index.js` for module entry points

**Examples**:
```javascript
// File: user-service.js
class UserService {
  // implementation
}

module.exports = { UserService };

// File: config/database.js
const databaseConfig = {
  host: "localhost",
  port: 5432,
};

module.exports = databaseConfig;
```

## Type Annotations

### TypeScript (Recommended)

**Use TypeScript for type safety**:

```typescript
// Function parameters and return types
function greet(name: string, age: number): string {
  return `Hello ${name}, you are ${age} years old`;
}

// Variable annotations
let userCount: number = 0;
let items: string[] = [];
let mapping: Record<string, number> = {};

// Interface for object shapes
interface User {
  id: number;
  name: string;
  email?: string; // Optional property
}

// Union types
type Status = "pending" | "approved" | "rejected";

// Generic functions
function first<T>(items: T[]): T | undefined {
  return items[0];
}
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

/**
 * User object type definition
 * @typedef {Object} User
 * @property {number} id - User ID
 * @property {string} name - User name
 * @property {string} [email] - User email (optional)
 */

/**
 * @param {User} user - User object
 * @returns {string} Formatted user string
 */
function formatUser(user) {
  return `${user.name} (${user.id})`;
}
```

## Import Organization

### Import Grouping

Organize imports in groups with one blank line between each:

1. **Node.js built-in modules**
2. **Third-party packages**
3. **Local modules** (relative imports)

Within each group, sort imports alphabetically.

### Import Style

**Prefer ES6 imports**:

```javascript
// Good - ES6 imports
import fs from "fs";
import path from "path";
import express from "express";
import { User, Post } from "./models";
import userService from "./services/userService";

// Avoid - CommonJS requires (unless necessary)
const fs = require("fs");
const express = require("express");
```

**Group imports from same module**:

```javascript
// Good
import { readFile, writeFile } from "fs/promises";
import { Router, Request, Response } from "express";

// Acceptable
import readFile from "fs/promises";
import writeFile from "fs/promises";
```

**Use absolute imports** (prefer relative imports for local modules):

```javascript
// Good - relative imports for local modules
import { User } from "../models/User";
import userService from "../services/userService";

// Good - absolute imports for packages
import express from "express";
import lodash from "lodash";
```

**Avoid wildcard imports**:

```javascript
// Avoid
import * as utils from "./utils";

// Good
import { formatDate, validateEmail } from "./utils";
```

### Import Example

```javascript
// Node.js built-ins
import fs from "fs";
import path from "path";
import { EventEmitter } from "events";

// Third-party packages
import express from "express";
import cors from "cors";
import helmet from "helmet";
import { PrismaClient } from "@prisma/client";

// Local modules
import { User, Post } from "../models";
import userService from "../services/userService";
import { validateUser } from "../utils/validation";
```

### Default vs Named Exports

**Use named exports for utilities**:

```javascript
// utils/helpers.js
export function formatDate(date) {
  return date.toISOString().split("T")[0];
}

export function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Import
import { formatDate, validateEmail } from "./utils/helpers";
```

**Use default exports for main classes/modules**:

```javascript
// services/userService.js
class UserService {
  // implementation
}

export default UserService;

// Import
import UserService from "./services/userService";
```

## Documentation Style

### JSDoc Format

- **Use `/** */` for documentation blocks**
- **First line**: Brief summary (one line, imperative mood)
- **Blank line** after summary if there's more content
- **Detailed description**: Multi-paragraph explanation if needed
- **Tags**: Document parameters, return values, and examples

### Module Documentation

Place at the top of every JavaScript file:

```javascript
/**
 * User authentication and authorization module.
 *
 * This module provides functionality for user login, logout,
 * token generation, and permission checking.
 *
 * @module auth
 */

import jwt from "jsonwebtoken";
import bcrypt from "bcrypt";
```

### Function Documentation

```javascript
/**
 * Calculates the total cost including tax.
 *
 * @param {number[]} items - Array of item prices
 * @param {number} taxRate - Tax rate as a decimal (e.g., 0.08 for 8%)
 * @returns {number} Total cost with tax applied
 * @throws {Error} If taxRate is negative
 *
 * @example
 * const items = [10, 20, 30];
 * const total = calculateTotal(items, 0.08);
 * console.log(total); // 64.8
 */
function calculateTotal(items, taxRate) {
  if (taxRate < 0) {
    throw new Error("Tax rate cannot be negative");
  }

  const subtotal = items.reduce((sum, price) => sum + price, 0);
  return subtotal * (1 + taxRate);
}
```

### Class Documentation

```javascript
/**
 * Represents a user account with authentication capabilities.
 *
 * This class handles user registration, login, and profile management.
 * It integrates with the authentication service for token management.
 *
 * @class
 */
class UserAccount {
  /**
   * The unique username for the account
   * @type {string}
   */
  username;

  /**
   * The user's email address
   * @type {string}
   */
  email;

  /**
   * Whether the account is currently active
   * @type {boolean}
   */
  isActive;

  /**
   * Creates a new user account.
   *
   * @param {string} username - Unique username for the account
   * @param {string} email - User's email address
   */
  constructor(username, email) {
    this.username = username;
    this.email = email;
    this.isActive = true;
  }

  /**
   * Returns the username for the account.
   *
   * @returns {string} The username
   */
  getUsername() {
    return this.username;
  }
}
```

### Short Documentation

For simple functions, a one-line comment is sufficient:

```javascript
/** Return the username for the given user ID. */
function getUsername(userId) {
  return database.query(userId).username;
}

/** The default timeout duration in milliseconds. */
const DEFAULT_TIMEOUT = 30000;
```

## Comments

### Inline Comments

- **Use sparingly**: Code should be self-documenting
- **Place on separate line** above the code when possible
- **Use for complex logic** that isn't obvious
- **Update comments** when code changes

```javascript
// Good - explains non-obvious logic
// Apply 10% discount for orders over $100, otherwise 5%
const discount = total > 100 ? 0.10 : 0.05;

// Avoid - stating the obvious
// Set x to 5
const x = 5;
```

### Block Comments

- **Use for complex algorithms** or business logic
- **Keep updated** with code changes
- **Indent to match** the code they describe

```javascript
// Check if user has permission to access this resource.
// Permission is granted if:
// 1. User is an admin
// 2. User owns the resource
// 3. Resource is marked as public
if (user.isAdmin || resource.owner === user.id || resource.isPublic) {
  grantAccess();
}
```

### TODO Comments

- **Use TODO** for future improvements:
  ```javascript
  // TODO: Add caching for better performance
  // TODO: Refactor to use async/await
  ```

- **Include context** when helpful:
  ```javascript
  // TODO(username): Add validation for email format
  // TODO: Bug #123 - Handle edge case for empty arrays
  ```

## Error Handling

### Exception Patterns

```javascript
// Custom errors
class UserNotFoundError extends Error {
  constructor(userId) {
    super(`User with ID ${userId} not found`);
    this.name = "UserNotFoundError";
    this.userId = userId;
  }
}

class DatabaseError extends Error {
  constructor(message, originalError) {
    super(message);
    this.name = "DatabaseError";
    this.originalError = originalError;
  }
}

// Specific exception handling
try {
  const user = await getUser(userId);
  return user;
} catch (error) {
  if (error instanceof UserNotFoundError) {
    return null;
  } else if (error instanceof DatabaseError) {
    logger.error(`Database error: ${error.message}`, { originalError: error.originalError });
    throw error;
  } else {
    logger.error(`Unexpected error: ${error.message}`, { error });
    throw new Error("Internal server error");
  }
}
```

### Async Error Handling

```javascript
// Good - proper async error handling
async function fetchUserData(userId) {
  try {
    const user = await userRepository.findById(userId);
    if (!user) {
      throw new UserNotFoundError(userId);
    }
    return user;
  } catch (error) {
    logger.error(`Failed to fetch user ${userId}`, { error });
    throw error;
  }
}

// Avoid - promise chains without proper error handling
function fetchUserDataBad(userId) {
  return userRepository.findById(userId)
    .then(user => {
      if (!user) throw new Error("User not found");
      return user;
    });
  // Missing catch block
}
```

### Best Practices

- **Catch specific errors** - avoid broad `catch (error)`
- **Use async/await** with try/catch blocks
- **Create custom error classes** for different error types
- **Provide context** in error messages
- **Log errors appropriately** with relevant context

## Async/Await Style

### When to Use Async

- **I/O-bound operations**: Database queries, API calls, file operations
- **Concurrent tasks**: Running multiple operations simultaneously
- **High throughput**: Handling many connections (web servers, bots)
- **Avoid for CPU-bound**: Use worker threads or streaming instead

### Basic Async Functions

```javascript
// Define async function
async function fetchUser(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    logger.error(`Failed to fetch user ${userId}`, { error });
    throw error;
  }
}

// Call async function
async function main() {
  try {
    const user = await fetchUser(123);
    console.log(user);
  } catch (error) {
    console.error("Failed to get user:", error);
  }
}

main();
```

### Concurrent Execution

```javascript
// Good - concurrent execution with Promise.all
async function fetchMultipleUsers(userIds) {
  const promises = userIds.map(id => fetchUser(id));
  const users = await Promise.all(promises);
  return users;
}

// Handle partial failures
async function fetchMultipleUsersWithFailures(userIds) {
  const results = await Promise.allSettled(
    userIds.map(id => fetchUser(id))
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

### Best Practices

- **Prefer async/await over promise chains**: More readable and easier to debug
- **Use Promise.all for concurrency**: When operations can run in parallel
- **Handle errors properly**: Always use try/catch with async/await
- **Use Promise.allSettled**: When you need all results, even if some fail
- **Avoid mixing callbacks and promises**: Choose one pattern and stick to it

## Code Organization

### File Organization

1. **Module documentation** (JSDoc block)
2. **Imports** (Node.js → third-party → local)
3. **Module-level constants**
4. **Type definitions** (if using TypeScript/JSDoc)
5. **Classes and functions**
6. **Exports**

### Class Organization

1. **Class documentation** (JSDoc)
2. **Static properties**
3. **Instance properties**
4. **Constructor**
5. **Public methods**
6. **Protected methods** (prefixed with `_`)
7. **Private methods** (prefixed with `_`)

**Example**:
```javascript
/**
 * Service for user management operations.
 */
class UserService {
  // Static property
  static MAX_LOGIN_ATTEMPTS = 3;

  /**
   * Initialize the user service.
   * @param {Database} database - Database instance
   */
  constructor(database) {
    this.database = database;
    this._cache = new Map();
  }

  /**
   * Create a new user account.
   * @param {Object} userData - User data
   * @returns {Promise<User>} Created user
   */
  async createUser(userData) {
    const user = await this.database.create("users", userData);
    this._cache.set(user.id, user);
    return user;
  }

  /**
   * Validate email format (internal use).
   * @param {string} email - Email to validate
   * @returns {boolean} True if valid
   * @private
   */
  _validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}

module.exports = UserService;
```

## Modern JavaScript Features

### ES6+ Features to Use

**Destructuring**:
```javascript
// Good
const { name, email } = user;
const [first, second] = items;

// Avoid
const name = user.name;
const email = user.email;
const first = items[0];
const second = items[1];
```

**Spread operator**:
```javascript
// Good
const newUser = { ...existingUser, lastLogin: new Date() };
const allItems = [...items1, ...items2];

// Avoid
const newUser = Object.assign({}, existingUser, { lastLogin: new Date() });
const allItems = items1.concat(items2);
```

**Arrow functions**:
```javascript
// Good - for callbacks and short functions
const doubled = numbers.map(n => n * 2);
users.forEach(user => console.log(user.name));

// Avoid - for methods that need 'this'
class BadExample {
  constructor() {
    this.items = [];
    // Bad - 'this' is not bound
    setTimeout(function() {
      this.items.push("item"); // Error
    }, 1000);
  }
}

// Good - use arrow function or bind
class GoodExample {
  constructor() {
    this.items = [];
    setTimeout(() => {
      this.items.push("item"); // Works
    }, 1000);
  }
}
```

**Template literals**:
```javascript
// Good
const message = `Hello ${name}, you have ${count} messages.`;
const sql = `
  SELECT * FROM users 
  WHERE active = true 
  ORDER BY created_at DESC
`;

// Avoid
const message = "Hello " + name + ", you have " + count + " messages.";
```

### Optional Chaining and Nullish Coalescing

```javascript
// Good - optional chaining
const city = user?.address?.city ?? "Unknown";
const count = items?.length ?? 0;

// Avoid - verbose checking
const city = user && user.address && user.address.city ? user.address.city : "Unknown";
const count = items && items.length ? items.length : 0;
```

## Formatting and Linting Tools

### Prettier Configuration

**`.prettierrc`**:

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "bracketSpacing": true,
  "arrowParens": "avoid"
}
```

### ESLint Configuration

**`.eslintrc.js`**:

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

### Package.json Scripts

```json
{
  "scripts": {
    "lint": "eslint . --ext .js,.ts",
    "lint:fix": "eslint . --ext .js,.ts --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:coverage": "jest --coverage"
  }
}
```

## Summary

- **Formatting**: Use Prettier, 80-100 char lines, 2-space indents, semicolons
- **Naming**: `camelCase` for functions/variables, `PascalCase` for classes, `SCREAMING_SNAKE_CASE` for constants
- **Type Safety**: TypeScript or JSDoc annotations for better code quality
- **Imports**: Group in Node.js → third-party → local, sort alphabetically, prefer ES6 imports
- **Error Handling**: Custom error classes, proper async error handling with try/catch
- **Async/Await**: Use for I/O operations, prefer Promise.all for concurrency
- **Documentation**: JSDoc blocks with examples and parameter descriptions
- **Modern Features**: Use ES6+ features like destructuring, spread, template literals
- **Tools**: Prettier for formatting, ESLint for linting, TypeScript for type checking

This style guide ensures consistent, readable, and maintainable JavaScript code across all projects.