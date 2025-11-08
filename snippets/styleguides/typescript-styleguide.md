---
agpm:
  version: "1.1.0"
---
# TypeScript Style Guide

This document defines the code style standards for TypeScript projects. It covers formatting, naming conventions, type annotations, imports, and documentation style.

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
- **Spaces around type annotations**: `name: string`, not `name:string`

### Trailing Commas
- **Use trailing commas** in multi-line structures:
  ```typescript
  const items: string[] = [
    "first",
    "second",
    "third",  // trailing comma
  ];

  const config: Config = {
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
  - Generic type parameters: `T`, `K`, `V`

**Examples**:
```typescript
// Good
let userCount: number = 10;
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Avoid
let uc: number = 10;
function calcTot(items: Item[]): number {
  return items.reduce((s, i) => s + i.price, 0);
}
```

### Classes and Interfaces
- **Use `PascalCase`** for class names, interface names, and type aliases
- **Use nouns** for class and interface names
- **Do NOT prefix** interfaces with `I` (avoid `IUser`, prefer `User`)
- **Use clear, descriptive names**

**Examples**:
```typescript
// Good
interface User {
  id: number;
  name: string;
  email: string;
}

class UserAccount {
  constructor(
    private username: string,
    private email: string
  ) {}
}

type HTTPResponse = {
  statusCode: number;
  data: unknown;
};

// Avoid
interface IUser {  // Don't prefix with I
  id: number;
  name: string;
}

class user_account {  // Use PascalCase
  constructor(username: string, email: string) {}
}
```

### Type Parameters (Generics)
- **Use single uppercase letters** for simple generics: `T`, `K`, `V`
- **Use descriptive names** for complex generics: `TUser`, `TResponse`
- **Common conventions**:
  - `T` - Type (general)
  - `K` - Key
  - `V` - Value
  - `E` - Element
  - `R` - Return type

**Examples**:
```typescript
// Good - simple generics
function first<T>(items: T[]): T | undefined {
  return items[0];
}

interface Map<K, V> {
  get(key: K): V | undefined;
  set(key: K, value: V): void;
}

// Good - complex generics with descriptive names
function fetchData<TRequest, TResponse>(
  request: TRequest
): Promise<TResponse> {
  // implementation
}

// Avoid - inconsistent naming
function process<t>(item: t): t {  // Use uppercase
  return item;
}
```

### Constants
- **Use `SCREAMING_SNAKE_CASE`** for constants
- Define at module level or in appropriate scope
- Use `const` declaration with explicit type

**Examples**:
```typescript
const MAX_CONNECTIONS: number = 100;
const DEFAULT_TIMEOUT: number = 30000;
const API_BASE_URL: string = "https://api.example.com";

// For objects that shouldn't be reassigned
const CONFIG = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
} as const;  // Use 'as const' for literal types
```

### Enums
- **Use `PascalCase`** for enum names
- **Use `PascalCase`** for enum members
- **Prefer string enums** over numeric enums for clarity
- **Prefer const enums** when values are compile-time only

**Examples**:
```typescript
// Good - string enum
enum UserRole {
  Admin = "ADMIN",
  Editor = "EDITOR",
  Viewer = "VIEWER",
}

// Good - const enum for performance
const enum Direction {
  Up = "UP",
  Down = "DOWN",
  Left = "LEFT",
  Right = "RIGHT",
}

// Avoid - numeric enum (less clear)
enum Status {
  Pending,    // 0
  Approved,   // 1
  Rejected,   // 2
}
```

### Private and Protected
- **Use `private` modifier** for private properties (not underscore prefix)
- **Use `protected` modifier** for protected members
- **Use `readonly`** for immutable properties
- **Use `#` for truly private fields** (ECMAScript private fields)

**Examples**:
```typescript
class MyClass {
  public name: string;           // Public property
  protected role: string;        // Protected property
  private secret: string;        // Private property
  readonly id: number;           // Readonly property
  #trulyPrivate: string;         // ECMAScript private field

  constructor(name: string, role: string, secret: string) {
    this.name = name;
    this.role = role;
    this.secret = secret;
    this.id = Math.random();
    this.#trulyPrivate = "hidden";
  }

  public getName(): string {
    return this.name;
  }

  protected getRoleInternal(): string {
    return this.role;
  }

  private getSecret(): string {
    return this.secret;
  }
}
```

### Boolean Names
- **Prefix with `is`, `has`, or `should`** for clarity
- **Use affirmative names**

**Examples**:
```typescript
// Good
let isActive: boolean = true;
let hasPermission: boolean = false;
let shouldRetry: boolean = true;

// Avoid
let active: boolean = true;  // ambiguous
let noPermission: boolean = true;  // negative naming
```

### File and Module Names
- **Use `kebab-case`** for file names: `user-service.ts`
- **Use `PascalCase`** for React components: `UserProfile.tsx`
- **Use `camelCase`** for module exports when appropriate
- **Index files**: Use `index.ts` for module entry points

**Examples**:
```typescript
// File: user-service.ts
export class UserService {
  // implementation
}

// File: config/database.ts
export const databaseConfig = {
  host: "localhost",
  port: 5432,
};

// File: UserProfile.tsx (React component)
export const UserProfile: React.FC<UserProfileProps> = (props) => {
  // implementation
};
```

## Type Annotations

### Explicit vs Inferred Types

**Let TypeScript infer when obvious**:
```typescript
// Good - inference is clear
const count = 10;  // Inferred as number
const name = "Alice";  // Inferred as string
const items = [1, 2, 3];  // Inferred as number[]

// Avoid - redundant annotations
const count: number = 10;
const name: string = "Alice";
```

**Use explicit types when needed**:
```typescript
// Good - explicit when inference unclear
let result: string | null = null;
const users: User[] = [];

// Good - function parameters and return types
function greet(name: string, age: number): string {
  return `Hello ${name}, you are ${age} years old`;
}
```

### Function Signatures

**Always type parameters and return values**:
```typescript
// Good - explicit types
function processUser(user: User): string {
  return `User: ${user.name}`;
}

async function fetchData(id: number): Promise<Data> {
  const response = await fetch(`/api/data/${id}`);
  return response.json();
}

// Good - arrow functions
const multiply = (a: number, b: number): number => a * b;

// Good - void return type
function logMessage(message: string): void {
  console.log(message);
}
```

### Interfaces vs Type Aliases

**Use interfaces for object shapes**:
```typescript
// Good - interface for objects
interface User {
  id: number;
  name: string;
  email?: string;  // Optional property
  readonly createdAt: Date;  // Readonly property
}

// Good - interface extension
interface Admin extends User {
  permissions: string[];
}
```

**Use type aliases for unions, primitives, tuples**:
```typescript
// Good - type for unions
type Status = "pending" | "approved" | "rejected";

// Good - type for complex unions
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };

// Good - type for tuples
type Point = [number, number];

// Good - type for mapped types
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};
```

### Generic Constraints

**Use constraints to restrict type parameters**:
```typescript
// Good - constrain to objects with id
function findById<T extends { id: number }>(
  items: T[],
  id: number
): T | undefined {
  return items.find(item => item.id === id);
}

// Good - constrain to specific types
function merge<T extends object, U extends object>(
  obj1: T,
  obj2: U
): T & U {
  return { ...obj1, ...obj2 };
}

// Good - keyof constraint
function getProperty<T, K extends keyof T>(
  obj: T,
  key: K
): T[K] {
  return obj[key];
}
```

### Utility Types

**Use built-in utility types**:
```typescript
// Partial - make all properties optional
type PartialUser = Partial<User>;

// Required - make all properties required
type RequiredUser = Required<User>;

// Readonly - make all properties readonly
type ReadonlyUser = Readonly<User>;

// Pick - select specific properties
type UserPreview = Pick<User, "id" | "name">;

// Omit - exclude specific properties
type UserWithoutEmail = Omit<User, "email">;

// Record - create object type with specific keys
type UserRoles = Record<string, User[]>;

// ReturnType - extract return type
type FetchResult = ReturnType<typeof fetchData>;

// Parameters - extract parameter types
type FetchParams = Parameters<typeof fetchData>;
```

### Union and Intersection Types

**Use discriminated unions for type-safe states**:
```typescript
// Good - discriminated union
type APIResponse<T> =
  | { status: "success"; data: T }
  | { status: "error"; error: string }
  | { status: "loading" };

function handleResponse<T>(response: APIResponse<T>): void {
  switch (response.status) {
    case "success":
      console.log(response.data);  // Type-safe access
      break;
    case "error":
      console.error(response.error);  // Type-safe access
      break;
    case "loading":
      console.log("Loading...");
      break;
  }
}
```

**Use intersection types to combine types**:
```typescript
// Good - combine types
type Timestamped = {
  createdAt: Date;
  updatedAt: Date;
};

type Entity = {
  id: number;
  name: string;
};

type TimestampedEntity = Entity & Timestamped;

const user: TimestampedEntity = {
  id: 1,
  name: "Alice",
  createdAt: new Date(),
  updatedAt: new Date(),
};
```

### Type Assertions

**Use type assertions sparingly**:
```typescript
// Good - when you know more than TypeScript
const input = document.getElementById("input") as HTMLInputElement;

// Good - as const for literal types
const config = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
} as const;

// Avoid - overusing assertions
const value = someFunction() as any;  // Loses type safety
```

### Type Guards

**Use type guards for narrowing**:
```typescript
// Good - user-defined type guard
function isString(value: unknown): value is string {
  return typeof value === "string";
}

// Good - narrowing with type guard
function processValue(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase();
  }
  return value.toString();
}

// Good - discriminated union guard
function isSuccess<T>(
  response: APIResponse<T>
): response is { status: "success"; data: T } {
  return response.status === "success";
}
```

## Import Organization

### Import Grouping

Organize imports in groups with one blank line between each:

1. **Node.js built-in modules** (using `node:` prefix)
2. **Third-party packages**
3. **Local modules** (relative imports)
4. **Type-only imports** (using `import type`)

Within each group, sort imports alphabetically.

### Import Style

**Prefer ES6 imports with type annotations**:

```typescript
// Node.js built-ins (use node: prefix)
import fs from "node:fs";
import path from "node:path";
import { EventEmitter } from "node:events";

// Third-party packages
import express from "express";
import cors from "cors";
import helmet from "helmet";
import { PrismaClient } from "@prisma/client";

// Local modules
import { User, Post } from "../models";
import userService from "../services/userService";
import { validateUser } from "../utils/validation";

// Type-only imports (separate)
import type { Request, Response, NextFunction } from "express";
import type { UserRole } from "../types";
```

**Use type-only imports for types**:

```typescript
// Good - type-only import
import type { User, UserRole } from "./types";

// Avoid - mixing value and type imports when type is sufficient
import { User } from "./types";  // Only use when importing both types and values
```

**Group imports from same module**:

```typescript
// Good
import { readFile, writeFile } from "node:fs/promises";
import { Router, Request, Response } from "express";

// Acceptable
import readFile from "node:fs/promises";
import writeFile from "node:fs/promises";
```

### Import Example

```typescript
// Node.js built-ins
import fs from "node:fs";
import path from "node:path";
import { EventEmitter } from "node:events";

// Third-party packages
import express from "express";
import cors from "cors";
import helmet from "helmet";
import { PrismaClient } from "@prisma/client";

// Local modules
import { User, Post } from "../models";
import userService from "../services/userService";
import { validateUser } from "../utils/validation";

// Type-only imports
import type { Request, Response, NextFunction } from "express";
import type { UserRole, UserPermissions } from "../types";
```

### Default vs Named Exports

**Use named exports for utilities**:

```typescript
// utils/helpers.ts
export function formatDate(date: Date): string {
  return date.toISOString().split("T")[0];
}

export function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Import
import { formatDate, validateEmail } from "./utils/helpers";
```

**Use default exports for main classes/modules**:

```typescript
// services/userService.ts
class UserService {
  // implementation
}

export default UserService;

// Import
import UserService from "./services/userService";
```

## Documentation Style

### TSDoc Format

- **Use `/** */` for documentation blocks**
- **First line**: Brief summary (one line, imperative mood)
- **Blank line** after summary if there's more content
- **Detailed description**: Multi-paragraph explanation if needed
- **Tags**: Document parameters, return values, and examples

### Module Documentation

Place at the top of every TypeScript file:

```typescript
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

```typescript
/**
 * Calculates the total cost including tax.
 *
 * @param items - Array of item prices
 * @param taxRate - Tax rate as a decimal (e.g., 0.08 for 8%)
 * @returns Total cost with tax applied
 * @throws {@link ValidationError} If taxRate is negative
 *
 * @example
 * ```typescript
 * const items = [10, 20, 30];
 * const total = calculateTotal(items, 0.08);
 * console.log(total); // 64.8
 * ```
 */
function calculateTotal(items: number[], taxRate: number): number {
  if (taxRate < 0) {
    throw new ValidationError("Tax rate cannot be negative");
  }

  const subtotal = items.reduce((sum, price) => sum + price, 0);
  return subtotal * (1 + taxRate);
}
```

### Interface and Type Documentation

```typescript
/**
 * Represents a user account.
 *
 * @interface User
 */
interface User {
  /** Unique user identifier */
  id: number;

  /** User's display name */
  name: string;

  /** User's email address (optional) */
  email?: string;

  /** Account creation timestamp */
  readonly createdAt: Date;
}

/**
 * API response status.
 *
 * @typedef {string} Status
 */
type Status = "pending" | "approved" | "rejected";
```

### Class Documentation

```typescript
/**
 * Service for managing user accounts.
 *
 * Handles user creation, authentication, and profile management.
 * Integrates with authentication service for token management.
 *
 * @class UserService
 */
class UserService {
  /**
   * Creates a new user service instance.
   *
   * @param database - Database connection instance
   */
  constructor(private database: Database) {}

  /**
   * Creates a new user account.
   *
   * @param userData - User data for account creation
   * @returns Newly created user
   * @throws {@link ValidationError} If user data is invalid
   * @throws {@link DatabaseError} If database operation fails
   *
   * @example
   * ```typescript
   * const service = new UserService(db);
   * const user = await service.createUser({
   *   name: "Alice",
   *   email: "alice@example.com"
   * });
   * ```
   */
  async createUser(userData: CreateUserData): Promise<User> {
    // implementation
  }
}
```

### Short Documentation

For simple functions with clear type signatures, documentation may be minimal:

```typescript
/** Returns the username for the given user ID. */
function getUsername(userId: number): string {
  return database.query(userId).username;
}

/** Default timeout duration in milliseconds. */
const DEFAULT_TIMEOUT = 30000;
```

## Error Handling

### Custom Error Classes

```typescript
// Base application error
class AppError extends Error {
  constructor(
    message: string,
    public code: string = "UNKNOWN_ERROR",
    public statusCode: number = 500
  ) {
    super(message);
    this.name = "AppError";
    Error.captureStackTrace(this, this.constructor);
  }
}

// Validation error
class ValidationError extends AppError {
  constructor(
    message: string,
    public field?: string
  ) {
    super(message, "VALIDATION_ERROR", 400);
    this.name = "ValidationError";
  }
}

// Not found error
class NotFoundError extends AppError {
  constructor(
    public resource: string,
    public id: number | string
  ) {
    super(
      `${resource} with id ${id} not found`,
      "NOT_FOUND",
      404
    );
    this.name = "NotFoundError";
  }
}
```

### Exception Handling

```typescript
// Good - specific exception handling
async function fetchUser(userId: number): Promise<User> {
  try {
    const user = await userRepository.findById(userId);
    if (!user) {
      throw new NotFoundError("User", userId);
    }
    return user;
  } catch (error) {
    if (error instanceof NotFoundError) {
      throw error; // Re-throw known errors
    } else if (error instanceof DatabaseError) {
      logger.error(`Database error fetching user ${userId}`, { error });
      throw new AppError("Service unavailable", "SERVICE_UNAVAILABLE", 503);
    } else {
      logger.error(`Unexpected error fetching user ${userId}`, { error });
      throw new AppError("Internal server error", "INTERNAL_ERROR", 500);
    }
  }
}
```

### Type Guards for Errors

```typescript
// Type guard for custom errors
function isAppError(error: unknown): error is AppError {
  return error instanceof AppError;
}

// Type guard for validation errors
function isValidationError(error: unknown): error is ValidationError {
  return error instanceof ValidationError;
}

// Usage
try {
  await riskyOperation();
} catch (error) {
  if (isValidationError(error)) {
    console.log(`Validation failed on field: ${error.field}`);
  } else if (isAppError(error)) {
    console.log(`App error: ${error.code}`);
  } else {
    console.error("Unknown error:", error);
  }
}
```

## Async/Await Style

### Typed Async Functions

```typescript
// Good - explicit Promise return type
async function fetchUser(userId: number): Promise<User> {
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
}

// Good - void async function
async function logUserActivity(userId: number): Promise<void> {
  await logger.log(`User ${userId} activity`);
}
```

### Concurrent Execution

```typescript
// Good - concurrent execution with proper typing
async function fetchMultipleUsers(
  userIds: number[]
): Promise<User[]> {
  const promises = userIds.map(id => fetchUser(id));
  return Promise.all(promises);
}

// Handle partial failures with typed results
type SettledResult<T> =
  | { status: "fulfilled"; value: T }
  | { status: "rejected"; reason: Error };

async function fetchMultipleUsersWithFailures(
  userIds: number[]
): Promise<{ users: User[]; failures: Error[] }> {
  const results = await Promise.allSettled(
    userIds.map(id => fetchUser(id))
  );

  const users = results
    .filter((result): result is PromiseFulfilledResult<User> =>
      result.status === "fulfilled"
    )
    .map(result => result.value);

  const failures = results
    .filter((result): result is PromiseRejectedResult =>
      result.status === "rejected"
    )
    .map(result => result.reason);

  return { users, failures };
}
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
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking",
    "prettier",
  ],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
    project: "./tsconfig.json",
  },
  plugins: ["@typescript-eslint"],
  rules: {
    "no-console": "warn",
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/strict-boolean-expressions": "error",
    "@typescript-eslint/no-floating-promises": "error",
    "@typescript-eslint/prefer-nullish-coalescing": "warn",
    "@typescript-eslint/prefer-optional-chain": "warn",
  },
};
```

### TypeScript Configuration

**`tsconfig.json`**:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "lib": ["ES2022"],
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

## Summary

- **Formatting**: Use Prettier, 80-100 char lines, 2-space indents, semicolons
- **Naming**: `camelCase` for functions/variables, `PascalCase` for classes/interfaces/types, `SCREAMING_SNAKE_CASE` for constants
- **Type Safety**: Explicit types for function parameters/returns, let inference work for simple cases
- **Interfaces vs Types**: Interfaces for objects, types for unions/primitives/tuples
- **Imports**: Group in Node.js → third-party → local, use type-only imports, sort alphabetically
- **Error Handling**: Custom error classes with type guards, proper async error handling
- **Async/Await**: Explicit Promise return types, use Promise.all for concurrency
- **Documentation**: TSDoc blocks with type references and examples
- **Generics**: Use constraints and descriptive names for complex cases
- **Tools**: Prettier for formatting, ESLint for linting, strict TypeScript configuration

This style guide ensures consistent, type-safe, and maintainable TypeScript code across all projects.
