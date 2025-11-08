---
agpm:
  version: "1.1.0"
---
# Go Style Guide

This document defines the code style standards for Go projects. It covers formatting, naming conventions, types, imports, and documentation style.

## Code Formatting

### Line Length
- **Maximum line length**: 100 characters (enforced by `gofmt`)
- **Break long lines** at logical points for readability
- Use `gofmt` and `goimports` for automatic formatting

### Indentation
- **Use tabs** for indentation (Go standard)
- **Never use spaces** for indentation
- `gofmt` handles this automatically

### Whitespace
- **One blank line** between top-level function and method definitions
- **No blank lines** between consecutive imports
- **One blank line** at end of file
- **No trailing whitespace** on any line
- **Spaces around operators**: `x = y + z`, not `x=y+z`
- **No spaces** inside brackets: `[1, 2, 3]`, not `[ 1, 2, 3 ]`
- **Spaces after commas**: `func(a, b, c)`, not `func(a,b,c)`

### Braces and Control Structures
- **Opening brace on same line**: `if condition {`
- **No semicolons** at end of lines (except for specific cases)
- **Always use braces** for control structures, even single statements

```go
// Good
if condition {
    doSomething()
}

// Avoid
if condition 
    doSomething()

// Also avoid
if condition { doSomething() }
```

### String Quotes
- **Use double quotes** for strings: `"hello"`
- **Use backticks** for raw strings when helpful: `` `path\to\file` ``
- **Be consistent** within a project

## Naming Conventions

### Variables and Functions
- **Use `camelCase`** for variables and functions (exported names start with capital)
- **Use descriptive names** that convey intent
- **Avoid single-letter names** except in:
  - Loop counters: `for i := 0; i < 10; i++`
  - Common mathematical variables: `x, y, z`
  - Short function parameters: `func(s string)`

**Examples**:
```go
// Good
userCount := 10
func calculateTotal(items []float64) float64 {
    // implementation
}

// Avoid
uc := 10
func calcTot(items []float64) float64 {
    // implementation
}
```

### Package Names
- **Use short, lowercase names**: `http`, `json`, `strings`
- **No underscores or mixed caps**: `user_service` → `userservice`
- **Make names unique**: Avoid common names like `util`, `common`
- **Use singular form**: `user` not `users` (unless package contains multiple user types)

**Examples**:
```go
// Good
package user
package auth
package database

// Avoid
package users
package utils
package common
```

### Constants
- **Use `camelCase`** for constants (exported constants start with capital)
- **Group related constants** with `iota` when appropriate
- **Use descriptive names** that explain the purpose

**Examples**:
```go
// Good
const (
    MaxConnections = 100
    DefaultTimeout = 30 * time.Second
    APIBaseURL     = "https://api.example.com"
)

// Using iota for enums
const (
    StatusPending Status = iota
    StatusActive
    StatusInactive
)
```

### Interfaces
- **Use `-er` suffix** for interfaces with single methods: `Reader`, `Writer`
- **Use descriptive names** for interfaces with multiple methods
- **Keep interfaces small** and focused

**Examples**:
```go
// Good - single method
type Reader interface {
    Read([]byte) (int, error)
}

// Good - multiple methods
type UserStore interface {
    Create(user *User) error
    Get(id int) (*User, error)
    Update(user *User) error
    Delete(id int) error
}

// Avoid - vague interface name
type Interface interface {
    DoSomething()
}
```

### Structs and Types
- **Use `PascalCase`** for type names (exported types start with capital)
- **Use nouns** for type names
- **Use clear, descriptive names**

**Examples**:
```go
// Good
type User struct {
    ID       int
    Name     string
    Email    string
    Active   bool
}

type HTTPResponse struct {
    StatusCode int
    Body       []byte
    Headers    map[string]string
}

// Avoid
type user struct {
    id   int
    name string
}

type Http_Response struct {
    status_code int
}
```

### Exported vs Unexported
- **Exported names** start with capital letter: `User`, `GetName()`
- **Unexported names** start with lowercase letter: `user`, `getName()`
- **Export only what's needed** for the public API

**Examples**:
```go
type User struct {
    ID       int       // Exported
    name     string    // Unexported
    Email    string    // Exported
    password string    // Unexported
}

func (u *User) GetName() string {  // Exported method
    return u.name
}

func (u *User) validate() error {  // Unexported method
    // validation logic
}
```

### Boolean Names
- **Prefix with `Is`, `Has`, or `Can`** for clarity
- **Use affirmative names**

**Examples**:
```go
// Good
isActive := true
hasPermission := false
canEdit := true

// Avoid
active := true     // ambiguous
noPermission := true  // negative naming
```

### Receiver Names
- **Use 1-2 letter abbreviations** that are consistent across methods
- **Don't use `this` or `self`**
- **Be consistent** within the same type

**Examples**:
```go
// Good
func (u *User) GetName() string {
    return u.name
}

func (s *Server) Start() error {
    // implementation
}

// Avoid
func (this *User) GetName() string {
    return this.name
}

func (self *Server) Start() error {
    // implementation
}
```

## Type Definitions

### Basic Types
- **Use descriptive type names** for domain-specific concepts
- **Create type aliases** for clarity when needed
- **Use `type` declarations** for semantic meaning

```go
// Good
type UserID int
type Email string
type Timestamp time.Time

func GetUser(id UserID) (*User, error) {
    // implementation
}

// Using custom types
type Temperature float64

func (t Temperature) Celsius() float64 {
    return float64(t)
}
```

### Struct Composition
- **Use embedding** for composition over inheritance
- **Prefer explicit field names** when embedding for clarity
- **Use interfaces** for behavior abstraction

```go
// Good - embedding
type User struct {
    Person  // Embedded struct
    Email   string
    Active  bool
}

type Person struct {
    Name string
    Age  int
}

// Good - explicit embedding
type User struct {
    Person Person  `json:"person"`
    Email  string  `json:"email"`
    Active bool    `json:"active"`
}
```

### Error Types
- **Implement `error` interface** for custom errors
- **Use fmt.Errorf** for simple errors
- **Create custom error types** for structured errors

```go
// Simple error
func validateUser(u *User) error {
    if u.Name == "" {
        return fmt.Errorf("user name cannot be empty")
    }
    return nil
}

// Custom error type
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %s", e.Field, e.Message)
}
```

## Import Organization

### Import Grouping
Organize imports in two distinct groups with one blank line between each:

1. **Standard library imports**
2. **Third-party and local imports**

Within each group, sort imports alphabetically.

### Import Style
- **One import per line** for clarity:
  ```go
  // Good
  import "fmt"
  import "os"
  
  // Avoid
  import (
      "fmt"
      "os"
  )
  ```

- **Group imports from same package**:
  ```go
  import (
      "context"
      "fmt"
      "time"
  )
  ```

- **Use absolute imports** (Go standard):
  ```go
  import (
      "github.com/gin-gonic/gin"
      "myapp/internal/models"
      "myapp/pkg/utils"
  )
  ```

- **Avoid unused imports**: `goimports` handles this automatically

### Import Example
```go
import (
    "context"
    "fmt"
    "time"

    "github.com/gin-gonic/gin"
    "github.com/lib/pq"
    "go.uber.org/zap"

    "myapp/internal/models"
    "myapp/pkg/config"
    "myapp/pkg/utils"
)
```

### Import Aliases
- **Use aliases** to resolve naming conflicts
- **Use descriptive aliases** for clarity
- **Avoid unnecessary aliases**

```go
import (
    "fmt"
    sql "database/sql"  // Alias to avoid conflict
    psql "github.com/lib/pq"  // Descriptive alias
)
```

## Documentation Style

### Godoc Format
- **Use `/** */` for package documentation**
- **Use `// ` for function, type, and method documentation**
- **First line**: Brief summary (one line, present tense)
- **Blank line** after summary if there's more content
- **Detailed description**: Multi-paragraph explanation if needed

### Package Documentation
Place at the top of every Go file (typically in a file named `doc.go` or the main file):

```go
// Package user provides functionality for user management including
// registration, authentication, and profile management.
//
// This package implements the core business logic for user operations
// and integrates with the database layer for persistence.
package user
```

### Function Documentation
```go
// CalculateTotal computes the sum of all item prices including tax.
//
// It takes a slice of item prices and applies the given tax rate.
// The tax rate should be provided as a decimal (e.g., 0.08 for 8%).
//
// Parameters:
//   - items: Slice of item prices
//   - taxRate: Tax rate as a decimal
//
// Returns:
//   - Total cost with tax applied
//   - Error if tax rate is negative
//
// Example:
//   items := []float64{10.0, 20.0, 30.0}
//   total, err := CalculateTotal(items, 0.08)
//   if err != nil {
//       log.Fatal(err)
//   }
//   fmt.Printf("Total: %.2f\n", total)
func CalculateTotal(items []float64, taxRate float64) (float64, error) {
    if taxRate < 0 {
        return 0, fmt.Errorf("tax rate cannot be negative")
    }
    
    subtotal := 0.0
    for _, price := range items {
        subtotal += price
    }
    return subtotal * (1 + taxRate), nil
}
```

### Type Documentation
```go
// User represents a user account in the system.
//
// It contains personal information, authentication details,
// and account status. The ID field is automatically assigned
// when the user is created.
type User struct {
    ID       int       `json:"id" db:"id"`
    Name     string    `json:"name" db:"name"`
    Email    string    `json:"email" db:"email"`
    Password string    `json:"-" db:"password"` // Hidden from JSON
    Active   bool      `json:"active" db:"active"`
    Created  time.Time `json:"created" db:"created"`
}
```

### Method Documentation
```go
// GetName returns the user's full name.
//
// It combines the first and last name fields with a space
// between them. If the name is empty, it returns "Unknown".
func (u *User) GetName() string {
    if u.Name == "" {
        return "Unknown"
    }
    return u.Name
}

// Validate checks if the user data is valid.
//
// It verifies that required fields are present and valid.
// Returns a ValidationError if any field is invalid.
func (u *User) Validate() error {
    if u.Name == "" {
        return &ValidationError{Field: "name", Message: "cannot be empty"}
    }
    if u.Email == "" {
        return &ValidationError{Field: "email", Message: "cannot be empty"}
    }
    return nil
}
```

### Interface Documentation
```go
// UserStore defines the interface for user data persistence.
//
// It provides methods for creating, retrieving, updating, and
// deleting user records. Implementations should handle database
// operations and return appropriate errors.
type UserStore interface {
    // Create saves a new user to the database.
    Create(user *User) error
    
    // Get retrieves a user by ID.
    // Returns nil if user not found.
    Get(id int) (*User, error)
    
    // Update modifies an existing user.
    Update(user *User) error
    
    // Delete removes a user by ID.
    Delete(id int) error
}
```

### Short Documentation
For simple functions, a one-line comment is sufficient:

```go
// Return the username for the given user ID.
func GetUsername(userID int) string {
    // implementation
}

// Default timeout duration in seconds.
const DefaultTimeout = 30
```

## Comments

### Inline Comments
- **Use sparingly**: Code should be self-documenting
- **Place on separate line** above the code when possible
- **Use for complex logic** that isn't obvious
- **Update comments** when code changes

```go
// Good - explains non-obvious logic
// Apply 10% discount for orders over $100, otherwise 5%
discount := 0.10
if total > 100 {
    discount = 0.05
}

// Avoid - stating the obvious
// Set x to 5
x := 5
```

### Block Comments
- **Use for complex algorithms** or business logic
- **Keep updated** with code changes
- **Indent to match** the code they describe

```go
// Check if user has permission to access this resource.
// Permission is granted if:
// 1. User is an admin
// 2. User owns the resource
// 3. Resource is marked as public
if user.IsAdmin || resource.OwnerID == user.ID || resource.IsPublic {
    grantAccess()
}
```

### TODO Comments
- **Use TODO** for future improvements:
  ```go
  // TODO: Add caching for better performance
  // TODO: Implement proper error handling
  ```

- **Include context** when helpful:
  ```go
  // TODO(john): Add validation for email format
  // TODO: Bug #123 - Handle edge case for empty slices
  ```

## Error Handling

### Error Patterns
```go
// Custom error types
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %s", e.Field, e.Message)
}

type DatabaseError struct {
    Query   string
    Original error
}

func (e *DatabaseError) Error() string {
    return fmt.Sprintf("database error in query %s: %v", e.Query, e.Original)
}

func (e *DatabaseError) Unwrap() error {
    return e.Original
}
```

### Error Handling Best Practices
```go
// Good - handle errors immediately
func GetUser(id int) (*User, error) {
    user, err := db.GetUser(id)
    if err != nil {
        return nil, fmt.Errorf("failed to get user %d: %w", id, err)
    }
    return user, nil
}

// Good - use error wrapping
func ProcessUser(id int) error {
    user, err := GetUser(id)
    if err != nil {
        return fmt.Errorf("process user failed: %w", err)
    }
    
    if err := validateUser(user); err != nil {
        return fmt.Errorf("validation failed: %w", err)
    }
    
    return nil
}

// Avoid - ignoring errors
func BadExample() {
    data, _ := os.ReadFile("file.txt")  // Don't ignore errors!
    fmt.Println(string(data))
}
```

### Sentinel Errors
```go
var (
    ErrUserNotFound = errors.New("user not found")
    ErrInvalidInput = errors.New("invalid input")
    ErrUnauthorized = errors.New("unauthorized access")
)

func GetUser(id int) (*User, error) {
    if id <= 0 {
        return nil, ErrInvalidInput
    }
    
    user, err := db.FindUser(id)
    if err != nil {
        return nil, err
    }
    if user == nil {
        return nil, ErrUserNotFound
    }
    return user, nil
}
```

## Concurrency Patterns

### Goroutines
```go
// Good - use wait groups for synchronization
func ProcessUsers(users []User) error {
    var wg sync.WaitGroup
    errChan := make(chan error, len(users))
    
    for _, user := range users {
        wg.Add(1)
        go func(u User) {
            defer wg.Done()
            if err := processUser(u); err != nil {
                errChan <- err
            }
        }(user)
    }
    
    wg.Wait()
    close(errChan)
    
    for err := range errChan {
        if err != nil {
            return err
        }
    }
    return nil
}

// Avoid - goroutine leaks
func BadExample() {
    go func() {
        // This goroutine might never exit
        for {
            time.Sleep(time.Second)
        }
    }()
}
```

### Channels
```go
// Good - use channels for communication
func Worker(id int, jobs <-chan Job, results chan<- Result) {
    for job := range jobs {
        result := processJob(job)
        results <- result
    }
}

func StartWorkers(numWorkers int) {
    jobs := make(chan Job, 100)
    results := make(chan Result, 100)
    
    for i := 0; i < numWorkers; i++ {
        go Worker(i, jobs, results)
    }
    
    // Send jobs
    for _, job := range jobList {
        jobs <- job
    }
    close(jobs)
    
    // Collect results
    for i := 0; i < len(jobList); i++ {
        result := <-results
        handleResult(result)
    }
}
```

### Mutex and Sync
```go
type SafeCounter struct {
    mu    sync.RWMutex
    count int
}

func (c *SafeCounter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

func (c *SafeCounter) Value() int {
    c.mu.RLock()
    defer c.mu.RUnlock()
    return c.count
}

// Good - use sync.Once for initialization
var (
    instance *Service
    once     sync.Once
)

func GetInstance() *Service {
    once.Do(func() {
        instance = &Service{}
    })
    return instance
}
```

## Code Organization

### File Organization
1. **Package documentation** (if not in separate doc.go)
2. **Imports** (standard → third-party/local)
3. **Constants**
4. **Variables**
5. **Types and interfaces**
6. **Functions and methods**

### Struct Organization
1. **Struct documentation**
2. **Exported fields**
3. **Unexported fields**

**Example**:
```go
package user

import (
    "fmt"
    "time"
)

const (
    MaxNameLength = 100
    MinAge        = 0
    MaxAge        = 150
)

var (
    ErrUserNotFound = fmt.Errorf("user not found")
    ErrInvalidAge   = fmt.Errorf("invalid age")
)

// User represents a user account in the system.
type User struct {
    ID        int       `json:"id" db:"id"`
    Name      string    `json:"name" db:"name"`
    Email     string    `json:"email" db:"email"`
    Age       int       `json:"age" db:"age"`
    active    bool      `json:"-" db:"active"`  // Unexported
    createdAt time.Time `json:"created_at" db:"created_at"`
}

// NewUser creates a new user with the given name and email.
func NewUser(name, email string, age int) *User {
    return &User{
        Name:      name,
        Email:     email,
        Age:       age,
        active:    true,
        createdAt: time.Now(),
    }
}

// GetName returns the user's name.
func (u *User) GetName() string {
    return u.Name
}

// validate checks if the user data is valid.
func (u *User) validate() error {
    if len(u.Name) > MaxNameLength {
        return fmt.Errorf("name too long")
    }
    if u.Age < MinAge || u.Age > MaxAge {
        return ErrInvalidAge
    }
    return nil
}
```

## Formatting and Linting Tools

### gofmt and goimports
```bash
# Format all Go files
gofmt -w .

# Format and organize imports
goimports -w .

# Check formatting without modifying
gofmt -d .
goimports -d .
```

### golint
```bash
# Run linter
golint ./...

# Check specific package
golint ./internal/user
```

### go vet
```bash
# Run static analysis
go vet ./...

# Check specific issues
go vet -shadow ./...
```

### golangci-lint (Recommended)
**`.golangci.yml`**:
```yaml
run:
  timeout: 5m
  tests: true

linters:
  enable:
    - gofmt
    - goimports
    - govet
    - errcheck
    - staticcheck
    - unused
    - gosimple
    - structcheck
    - varcheck
    - ineffassign
    - deadcode
    - misspell
    - unconvert
    - unparam
    - nakedret
    - prealloc
    - scopelint
    - gocritic

linters-settings:
  gofmt:
    simplify: true
  goimports:
    local-prefixes: myapp
  errcheck:
    check-type-assertions: true
    check-blank: true
  gocyclo:
    min-complexity: 15
  dupl:
    threshold: 100
  goconst:
    min-len: 3
    min-occurrences: 3

issues:
  exclude-use-default: false
  max-issues-per-linter: 0
  max-same-issues: 0
```

### Pre-commit Hooks
**`.pre-commit-config.yaml`**:
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/pre-commit/mirrors-golangci-lint
    rev: v1.54.2
    hooks:
      - id: golangci-lint
```

## Summary

- **Formatting**: Use `gofmt` and `goimports`, 100 char lines, tab indentation
- **Naming**: `camelCase` for functions/variables, `PascalCase` for types, lowercase packages
- **Types**: Create descriptive types, use composition, implement error interface
- **Imports**: Group in stdlib → third-party/local, sort alphabetically
- **Error Handling**: Use error wrapping, custom error types, handle immediately
- **Concurrency**: Use goroutines with wait groups, channels for communication, mutex for synchronization
- **Documentation**: Godoc format with examples, clear parameter descriptions
- **Tools**: `gofmt`, `goimports`, `golangci-lint`, `go vet` for code quality

This style guide ensures consistent, readable, and maintainable Go code across all projects.