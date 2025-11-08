---
agpm:
  version: "1.0.0"
---

# TypeScript Best Practices

This document defines technical best practices for TypeScript development, covering tools, patterns, testing, security, and performance optimization.

## Core Principles

1. **Strict Type Safety**: Enable all strict TypeScript compiler options
2. **Zero Warnings Policy**: All code must pass linting without warnings
3. **Consistent Formatting**: All code must be formatted with Prettier
4. **Explicit Type Annotations**: Document intent with clear type annotations
5. **Error Handling**: Implement proper exception handling with typed errors
6. **Clean Architecture**: Separate concerns with clear architectural layers
7. **Test Coverage**: Maintain >70% test coverage
8. **Security First**: Follow security best practices from the start

## Mandatory Completion Checklist

Before considering any TypeScript code complete, you MUST:

1. ✅ Run formatter (`prettier --write .`)
2. ✅ Run linter (`eslint .`)
3. ✅ Run type checker (`tsc --noEmit`)
4. ✅ Run tests (`npm test` or `jest`)
5. ✅ Verify test coverage (`npm run test:coverage` - target >70%)
6. ✅ Verify all dependencies are properly declared
7. ✅ Generate and verify type declarations (`tsc --declaration`)

## Development Tools

### Package Management: npm (Recommended)

**Use `npm` for modern TypeScript projects**: Standard package manager with extensive ecosystem

```bash
# Initialize new TypeScript project
npm init -y
npm install --save-dev typescript @types/node

# Initialize TypeScript configuration
npx tsc --init

# Install dependencies
npm install express zod prisma

# Install type definitions
npm install --save-dev @types/express @types/node @types/jest

# Install dev dependencies
npm install --save-dev eslint prettier jest ts-jest ts-node

# Run scripts
npm start
npm test
npm run type-check
npm run build
```

### Alternative: pnpm

```bash
# Install pnpm
npm install -g pnpm

# Initialize new project
pnpm init

# Install TypeScript
pnpm add -D typescript @types/node

# Install dependencies
pnpm add express zod prisma

# Install dev dependencies
pnpm add -D @types/express eslint prettier jest ts-jest
```

### Dependency Best Practices

- **Install type definitions**: Always install `@types/*` packages for third-party libraries
- **Pin exact versions in production**: `package-lock.json` handles this automatically
- **Keep dependencies updated**: Regularly review and update
- **Security auditing**: Use `npm audit` or `pnpm audit`
- **Separate dev dependencies**: Keep development tools separate from production deps
- **Document dependency choices**: Explain why specific packages are required

## TypeScript Configuration

### Strict Mode (Required)

**Always enable strict mode**:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true
  }
}
```

### Recommended Configuration

**`tsconfig.json`**:

```json
{
  "compilerOptions": {
    // Language and Environment
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "ESNext",
    "moduleResolution": "bundler",

    // Strict Type-Checking
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,

    // Additional Checks
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "allowUnusedLabels": false,
    "allowUnreachableCode": false,

    // Module Resolution
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "resolveJsonModule": true,
    "forceConsistentCasingInFileNames": true,

    // Emit
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "removeComments": false,

    // Interop Constraints
    "isolatedModules": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts", "**/*.spec.ts"]
}
```

### Configuration for Libraries

**`tsconfig.json` for library projects**:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "declaration": true,
    "declarationMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,

    // Library-specific
    "composite": true,
    "incremental": true,
    "stripInternal": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

## Type Safety Best Practices

### Avoid `any` - Use Proper Types

```typescript
// Bad - loses type safety
function processData(data: any): any {
  return data.value;
}

// Good - specific types
function processData(data: { value: string }): string {
  return data.value;
}

// Good - generic for flexibility with type safety
function processData<T extends { value: string }>(data: T): string {
  return data.value;
}

// Good - unknown for truly unknown types
function processData(data: unknown): string {
  if (typeof data === "object" && data !== null && "value" in data) {
    return String(data.value);
  }
  throw new Error("Invalid data");
}
```

### Use Type Guards

```typescript
// User-defined type guard
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value &&
    typeof (value as User).id === "number" &&
    typeof (value as User).name === "string"
  );
}

// Usage
function processValue(value: unknown): string {
  if (isString(value)) {
    return value.toUpperCase();  // Type-safe
  }
  throw new Error("Value must be string");
}
```

### Use Discriminated Unions

```typescript
// Good - discriminated union for type-safe states
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
    default:
      // Exhaustiveness check
      const _exhaustive: never = response;
      throw new Error(`Unhandled case: ${_exhaustive}`);
  }
}
```

### Avoid Type Assertions

```typescript
// Bad - type assertion bypasses type safety
const input = document.getElementById("input") as HTMLInputElement;
input.value = "text";  // Could fail at runtime

// Good - type guard
const input = document.getElementById("input");
if (input instanceof HTMLInputElement) {
  input.value = "text";  // Type-safe
}

// Bad - double assertion
const value = someValue as unknown as SomeType;

// Good - validation with type guard
function isSomeType(value: unknown): value is SomeType {
  // Validate at runtime
  return (
    typeof value === "object" &&
    value !== null &&
    // ... validate properties
  );
}

const value = someValue;
if (isSomeType(value)) {
  // Use value safely
}
```

### Use `unknown` Instead of `any`

```typescript
// Bad - any loses type safety
function parseJSON(json: string): any {
  return JSON.parse(json);
}

// Good - unknown requires type checking
function parseJSON(json: string): unknown {
  return JSON.parse(json);
}

// Usage with type guard
const data = parseJSON(jsonString);
if (isUser(data)) {
  console.log(data.name);  // Type-safe
}
```

### Prefer `const` Assertions

```typescript
// Good - const assertion for literal types
const config = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
  retries: 3,
} as const;

// Type: { readonly apiUrl: "https://api.example.com"; readonly timeout: 5000; readonly retries: 3 }

// Good - const assertion for arrays
const roles = ["admin", "editor", "viewer"] as const;
type Role = typeof roles[number];  // "admin" | "editor" | "viewer"
```

## Error Handling

### Custom Error Hierarchy

```typescript
// Base error class
class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string = "UNKNOWN_ERROR",
    public readonly statusCode: number = 500,
    public readonly metadata?: Record<string, unknown>
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Validation error
class ValidationError extends AppError {
  constructor(
    message: string,
    public readonly field?: string,
    metadata?: Record<string, unknown>
  ) {
    super(message, "VALIDATION_ERROR", 400, metadata);
  }
}

// Not found error
class NotFoundError extends AppError {
  constructor(
    public readonly resource: string,
    public readonly id: number | string
  ) {
    super(
      `${resource} with id ${id} not found`,
      "NOT_FOUND",
      404,
      { resource, id }
    );
  }
}

// Database error
class DatabaseError extends AppError {
  constructor(
    message: string,
    public readonly originalError: Error
  ) {
    super(message, "DATABASE_ERROR", 500, {
      originalMessage: originalError.message,
    });
  }
}
```

### Type-Safe Error Handling

```typescript
// Result type pattern
type Result<T, E = Error> =
  | { success: true; value: T }
  | { success: false; error: E };

function divide(a: number, b: number): Result<number, string> {
  if (b === 0) {
    return { success: false, error: "Division by zero" };
  }
  return { success: true, value: a / b };
}

// Usage
const result = divide(10, 2);
if (result.success) {
  console.log(result.value);  // Type-safe access
} else {
  console.error(result.error);  // Type-safe access
}
```

### Async Error Handling

```typescript
// Good - proper async error handling with types
async function fetchUser(userId: number): Promise<User> {
  try {
    const response = await fetch(`/api/users/${userId}`);

    if (!response.ok) {
      throw new AppError(
        `Failed to fetch user: ${response.statusText}`,
        "FETCH_ERROR",
        response.status
      );
    }

    const data: unknown = await response.json();

    if (!isUser(data)) {
      throw new ValidationError("Invalid user data");
    }

    return data;
  } catch (error) {
    if (error instanceof AppError) {
      throw error;
    }

    throw new AppError(
      "Unexpected error fetching user",
      "INTERNAL_ERROR",
      500,
      { originalError: error }
    );
  }
}
```

## Data Validation

### Use Zod for Runtime Validation

**Zod provides type safety and runtime validation**:

```typescript
import { z } from "zod";

// Define schema
const UserSchema = z.object({
  id: z.number().int().positive(),
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional(),
  role: z.enum(["admin", "editor", "viewer"]),
  metadata: z.record(z.string(), z.unknown()).optional(),
});

// Extract TypeScript type from schema
type User = z.infer<typeof UserSchema>;

// Validate data
function validateUser(data: unknown): User {
  return UserSchema.parse(data);  // Throws ZodError on failure
}

// Safe parse (returns Result-like object)
function safeValidateUser(data: unknown): Result<User, z.ZodError> {
  const result = UserSchema.safeParse(data);

  if (result.success) {
    return { success: true, value: result.data };
  } else {
    return { success: false, error: result.error };
  }
}
```

### Complex Validation Schemas

```typescript
// Nested objects
const AddressSchema = z.object({
  street: z.string(),
  city: z.string(),
  zipCode: z.string().regex(/^\d{5}$/),
});

const UserWithAddressSchema = UserSchema.extend({
  address: AddressSchema,
});

// Refinements for custom validation
const PasswordSchema = z
  .string()
  .min(8)
  .refine(
    (password) => /[A-Z]/.test(password),
    "Password must contain uppercase letter"
  )
  .refine(
    (password) => /[0-9]/.test(password),
    "Password must contain number"
  );

// Transforms
const DateSchema = z.string().transform((str) => new Date(str));

// Discriminated unions
const EventSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("click"), x: z.number(), y: z.number() }),
  z.object({ type: z.literal("keypress"), key: z.string() }),
]);
```

### Validation Best Practices

- **Validate at boundaries**: Always validate external input
- **Use schema validation**: Zod, io-ts, or similar libraries
- **Provide clear error messages**: Help users understand validation failures
- **Type and runtime safety**: Use schemas that provide both

## Testing Strategy

### Jest with TypeScript

**Project setup**:

```bash
npm install --save-dev jest ts-jest @types/jest
npx ts-jest config:init
```

**`jest.config.js`**:

```javascript
module.exports = {
  preset: "ts-jest",
  testEnvironment: "node",
  roots: ["<rootDir>/src", "<rootDir>/tests"],
  testMatch: ["**/__tests__/**/*.ts", "**/?(*.)+(spec|test).ts"],
  collectCoverageFrom: [
    "src/**/*.ts",
    "!src/**/*.d.ts",
    "!src/**/*.test.ts",
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
};
```

### Writing Typed Tests

```typescript
import { describe, test, expect, beforeEach } from "@jest/globals";
import { UserService } from "../services/userService";
import type { User, CreateUserData } from "../types";

describe("UserService", () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
  });

  test("creates user with valid data", async () => {
    const userData: CreateUserData = {
      name: "Alice",
      email: "alice@example.com",
    };

    const user: User = await service.createUser(userData);

    expect(user.name).toBe("Alice");
    expect(user.email).toBe("alice@example.com");
    expect(user.id).toBeDefined();
  });

  test("throws ValidationError for invalid email", async () => {
    const userData: CreateUserData = {
      name: "Bob",
      email: "invalid-email",
    };

    await expect(service.createUser(userData)).rejects.toThrow(
      ValidationError
    );
  });
});
```

### Mocking with Types

```typescript
import { jest } from "@jest/globals";
import type { UserRepository } from "../repositories/userRepository";

// Create typed mock
const mockUserRepository: jest.Mocked<UserRepository> = {
  findById: jest.fn(),
  findAll: jest.fn(),
  create: jest.fn(),
  update: jest.fn(),
  delete: jest.fn(),
};

describe("UserService with mocks", () => {
  test("fetches user from repository", async () => {
    const mockUser: User = {
      id: 1,
      name: "Alice",
      email: "alice@example.com",
    };

    mockUserRepository.findById.mockResolvedValue(mockUser);

    const service = new UserService(mockUserRepository);
    const user = await service.getUser(1);

    expect(user).toEqual(mockUser);
    expect(mockUserRepository.findById).toHaveBeenCalledWith(1);
  });
});
```

### Testing Async Code

```typescript
describe("async operations", () => {
  test("resolves with correct data", async () => {
    const result = await fetchData(123);
    expect(result).toEqual({ id: 123, name: "Test" });
  });

  test("rejects with typed error", async () => {
    await expect(fetchData(-1)).rejects.toThrow(ValidationError);
  });

  test("handles concurrent operations", async () => {
    const results = await Promise.all([
      fetchData(1),
      fetchData(2),
      fetchData(3),
    ]);

    expect(results).toHaveLength(3);
    results.forEach((result) => {
      expect(result).toHaveProperty("id");
      expect(result).toHaveProperty("name");
    });
  });
});
```

## Linting & Code Quality

### ESLint Configuration for TypeScript

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
    // TypeScript-specific rules
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-floating-promises": "error",
    "@typescript-eslint/no-misused-promises": "error",
    "@typescript-eslint/await-thenable": "error",
    "@typescript-eslint/prefer-nullish-coalescing": "warn",
    "@typescript-eslint/prefer-optional-chain": "warn",
    "@typescript-eslint/strict-boolean-expressions": "error",
    "@typescript-eslint/no-non-null-assertion": "error",
    "@typescript-eslint/consistent-type-imports": "warn",
    "@typescript-eslint/consistent-type-definitions": ["error", "interface"],

    // General rules
    "no-console": "warn",
    "prefer-const": "error",
  },
};
```

### Mechanical vs Complex Fixes

**Mechanical fixes (safe to auto-fix)**:
- `@typescript-eslint/no-unused-vars` - Remove unused variables
- `@typescript-eslint/prefer-nullish-coalescing` - Use `??` instead of `||`
- `@typescript-eslint/prefer-optional-chain` - Use `?.` for chaining
- `@typescript-eslint/consistent-type-imports` - Use `import type`

**Complex fixes (requires analysis)**:
- `@typescript-eslint/no-explicit-any` - Replace `any` with proper types
- `@typescript-eslint/no-floating-promises` - Handle promise rejections
- `@typescript-eslint/strict-boolean-expressions` - Fix implicit boolean coercion
- `@typescript-eslint/no-non-null-assertion` - Remove `!` assertions

## Advanced Type Patterns

### Mapped Types

```typescript
// Make all properties optional
type Partial<T> = {
  [P in keyof T]?: T[P];
};

// Make all properties required
type Required<T> = {
  [P in keyof T]-?: T[P];
};

// Make all properties readonly
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};

// Custom mapped type
type Nullable<T> = {
  [P in keyof T]: T[P] | null;
};
```

### Conditional Types

```typescript
// Extract return type of function
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

// Extract array element type
type ArrayElement<T> = T extends (infer E)[] ? E : never;

// Conditional type example
type IsString<T> = T extends string ? "yes" : "no";

type Test1 = IsString<string>;  // "yes"
type Test2 = IsString<number>;  // "no"
```

### Template Literal Types

```typescript
// Event names
type EventName = "click" | "focus" | "blur";
type EventHandler = `on${Capitalize<EventName>}`;
// Type: "onClick" | "onFocus" | "onBlur"

// API routes
type Resource = "users" | "posts" | "comments";
type HTTPMethod = "GET" | "POST" | "PUT" | "DELETE";
type APIRoute = `/${Resource}`;
type APIEndpoint = `${HTTPMethod} ${APIRoute}`;
```

### Branded Types

```typescript
// Branded type for type safety
type Brand<T, TBrand> = T & { __brand: TBrand };

type UserId = Brand<number, "UserId">;
type PostId = Brand<number, "PostId">;

function createUserId(id: number): UserId {
  return id as UserId;
}

function createPostId(id: number): PostId {
  return id as PostId;
}

function getUser(id: UserId): User {
  // Implementation
}

const userId = createUserId(1);
const postId = createPostId(1);

getUser(userId);  // OK
getUser(postId);  // Error: Type 'PostId' is not assignable to type 'UserId'
```

## Performance Optimization

### Type Performance

```typescript
// Bad - complex union type
type BadType =
  | Type1 | Type2 | Type3 | Type4 | Type5
  | Type6 | Type7 | Type8 | Type9 | Type10;

// Good - use discriminated union
type GoodType =
  | { kind: "group1"; value: Type1 | Type2 | Type3 }
  | { kind: "group2"; value: Type4 | Type5 | Type6 }
  | { kind: "group3"; value: Type7 | Type8 | Type9 };
```

### Efficient Data Structures

```typescript
// Good - use Map for frequent lookups
const userCache = new Map<number, User>();

function getUser(id: number): User | undefined {
  if (userCache.has(id)) {
    return userCache.get(id);
  }

  const user = fetchUserFromDatabase(id);
  userCache.set(id, user);
  return user;
}

// Good - use Set for uniqueness checks
const activeUsers = new Set<number>();

function isUserActive(userId: number): boolean {
  return activeUsers.has(userId);
}
```

## Security Best Practices

### Input Validation

```typescript
// Good - validate with Zod
import { z } from "zod";

const LoginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

type LoginData = z.infer<typeof LoginSchema>;

function login(data: unknown): LoginData {
  return LoginSchema.parse(data);  // Validates at runtime
}
```

### Authentication

```typescript
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

// Hash passwords
async function hashPassword(password: string): Promise<string> {
  const saltRounds = 12;
  return bcrypt.hash(password, saltRounds);
}

// Verify passwords
async function verifyPassword(
  password: string,
  hashedPassword: string
): Promise<boolean> {
  return bcrypt.compare(password, hashedPassword);
}

// JWT payload type
interface JWTPayload {
  userId: number;
  email: string;
}

// Generate JWT
function generateToken(payload: JWTPayload): string {
  const secret = process.env.JWT_SECRET;
  if (!secret) {
    throw new Error("JWT_SECRET not configured");
  }

  return jwt.sign(payload, secret, { expiresIn: "24h" });
}

// Verify JWT
function verifyToken(token: string): JWTPayload {
  const secret = process.env.JWT_SECRET;
  if (!secret) {
    throw new Error("JWT_SECRET not configured");
  }

  return jwt.verify(token, secret) as JWTPayload;
}
```

## Project Structure

**Recommended structure**:

```
myproject/
├── package.json              # Project configuration
├── package-lock.json         # Dependency lock file
├── tsconfig.json             # TypeScript configuration
├── tsconfig.build.json       # Build-specific TS config
├── .eslintrc.js              # ESLint configuration
├── .prettierrc               # Prettier configuration
├── jest.config.js            # Jest configuration
├── README.md                 # Project documentation
├── .gitignore                # Git ignore file
├── .env.example              # Environment variables template
├── src/
│   ├── index.ts              # Application entry point
│   ├── types/                # Type definitions
│   │   ├── index.ts
│   │   ├── user.ts
│   │   └── api.ts
│   ├── config/               # Configuration
│   │   ├── database.ts
│   │   └── server.ts
│   ├── controllers/          # Request handlers
│   │   ├── userController.ts
│   │   └── authController.ts
│   ├── services/             # Business logic
│   │   ├── userService.ts
│   │   └── authService.ts
│   ├── repositories/         # Data access layer
│   │   ├── userRepository.ts
│   │   └── postRepository.ts
│   ├── models/               # Data models
│   │   ├── User.ts
│   │   └── Post.ts
│   ├── middleware/           # Express middleware
│   │   ├── auth.ts
│   │   └── validation.ts
│   ├── routes/               # Route definitions
│   │   ├── users.ts
│   │   └── auth.ts
│   ├── utils/                # Utility functions
│   │   ├── logger.ts
│   │   └── helpers.ts
│   └── errors/               # Custom error classes
│       └── index.ts
├── tests/                    # Tests
│   ├── setup.ts
│   ├── controllers/
│   ├── services/
│   └── utils/
└── dist/                     # Compiled output
```

## Context7 Integration

Always use Context7 MCP server for current documentation when developing TypeScript projects:

### Key Libraries

- `/microsoft/TypeScript` - TypeScript language documentation
- `/nodejs/node` - Node.js runtime documentation
- `/expressjs/express` - Web framework
- `/prisma/prisma` - Modern ORM
- `/colinhacks/zod` - Schema validation
- `/facebook/jest` - Testing framework
- `/eslint/eslint` - Linting tool
- `/prettier/prettier` - Code formatter

### Example Usage

```
Create an Express.js application with TypeScript, Prisma ORM, Zod validation, and JWT authentication.
Include proper type safety, async patterns, and error handling.
use context7 /microsoft/TypeScript /expressjs/express /prisma/prisma /colinhacks/zod
```

## Summary

- **Strict TypeScript**: Enable all strict compiler options
- **Type safety**: Avoid `any`, use proper types and type guards
- **Validation**: Use Zod for runtime validation and type inference
- **Testing**: >70% coverage with typed tests
- **Error handling**: Custom error classes with type guards
- **Linting**: ESLint with TypeScript-specific rules
- **Modern patterns**: Discriminated unions, branded types, template literals
- **Security**: Validate input, hash passwords, use JWT
- **Performance**: Efficient data structures, optimized types
- **Clean architecture**: Separate concerns, clear layers

These practices ensure robust, type-safe, maintainable, and secure TypeScript applications.
