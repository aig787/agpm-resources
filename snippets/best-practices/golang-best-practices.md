# Go Best Practices

This document defines technical best practices for Go development, covering tools, patterns, testing, security, and performance optimization.

## Core Principles

1. **Idiomatic Go**: Write code that follows Go conventions and standard library patterns
2. **Zero Warnings Policy**: All code must pass linting without warnings
3. **Error Handling**: Implement proper error handling and propagation
4. **Clean Architecture**: Separate concerns with clear architectural layers
5. **Test Coverage**: Maintain >70% test coverage
6. **Security First**: Follow security best practices from the start
7. **Performance Awareness**: Consider performance implications in design decisions

## Mandatory Completion Checklist

Before considering any Go code complete, you MUST:

1. ✅ Run formatter (`gofmt -w .` and `goimports -w .`)
2. ✅ Run linter (`golangci-lint run`)
3. ✅ Run static analysis (`go vet ./...`)
4. ✅ Run tests (`go test ./...`)
5. ✅ Verify test coverage (`go test -cover ./...` - target >70%)
6. ✅ Verify all dependencies are properly declared (`go mod tidy`)
7. ✅ Check for race conditions (`go test -race ./...`)

## Development Tools

### Package Management: Go Modules (Standard)

**Use Go modules for dependency management**:

```bash
# Initialize new module
go mod init myapp

# Add dependencies
go get github.com/gin-gonic/gin
go get github.com/lib/pq

# Add dev dependencies
go get github.com/golang/mock/gomock
go get golang.org/x/tools/cmd/goimports

# Update dependencies
go get -u ./...
go mod tidy

# Run commands
go run main.go
go test ./...
go build -o myapp ./cmd/myapp

# Manage dependencies
go list -m all
go mod why github.com/gin-gonic/gin
```

### Dependency Best Practices

- **Use semantic versioning**: Understand version constraints
- **Pin critical dependencies**: Use `go get` with specific versions when needed
- **Keep dependencies updated**: Regularly review and update
- **Security auditing**: Use `go list -m -u all` to check for updates
- **Minimal dependencies**: Prefer standard library solutions when possible
- **Document dependency choices**: Explain why specific packages are required

### Go Version Management
```bash
# Use gvm for managing Go versions
go install golang.org/dl/gotip@latest
gotip download

# Or use g (version manager)
go install github.com/voidint/g@latest
g install 1.21.0
g use 1.21.0

# Check Go version
go version
```

## Error Handling

### Error Design Patterns

**Use structured error types**:

```go
// Custom error with context
type AppError struct {
    Code    string
    Message string
    Cause   error
}

func (e *AppError) Error() string {
    if e.Cause != nil {
        return fmt.Sprintf("%s: %s (%v)", e.Code, e.Message, e.Cause)
    }
    return fmt.Sprintf("%s: %s", e.Code, e.Message)
}

func (e *AppError) Unwrap() error {
    return e.Cause
}

// Error constructors
func NewValidationError(field, message string) *AppError {
    return &AppError{
        Code:    "VALIDATION_ERROR",
        Message: fmt.Sprintf("%s: %s", field, message),
    }
}

func NewDatabaseError(cause error) *AppError {
    return &AppError{
        Code:    "DATABASE_ERROR",
        Message: "database operation failed",
        Cause:   cause,
    }
}
```

**Error wrapping and propagation**:

```go
func GetUser(id int) (*User, error) {
    if id <= 0 {
        return nil, NewValidationError("id", "must be positive")
    }
    
    user, err := db.FindUser(id)
    if err != nil {
        return nil, NewDatabaseError(err)
    }
    if user == nil {
        return nil, NewNotFoundError("user", id)
    }
    return user, nil
}

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
```

### Sentinel Errors
```go
var (
    ErrUserNotFound    = errors.New("user not found")
    ErrInvalidInput    = errors.New("invalid input")
    ErrUnauthorized    = errors.New("unauthorized access")
    ErrRateLimitExceeded = errors.New("rate limit exceeded")
)

// Usage with errors.Is
func HandleError(err error) {
    if errors.Is(err, ErrUserNotFound) {
        // Handle not found
    } else if errors.Is(err, ErrUnauthorized) {
        // Handle unauthorized
    }
}
```

### Error Handling Best Practices

- **Handle errors immediately**: Don't defer error handling
- **Wrap errors with context**: Use `fmt.Errorf` with `%w` verb
- **Use structured errors**: Create custom error types for different domains
- **Log errors at appropriate levels**: Debug for expected errors, Error for unexpected
- **Return errors from goroutines**: Use channels or sync.WaitGroup
- **Don't ignore errors**: Always handle or return errors

## Testing Strategy

### Testing Framework: Standard Testing + Testify

**Project structure**:

```
myproject/
├── cmd/
│   └── myapp/
│       └── main.go
├── internal/
│   ├── user/
│   │   ├── user.go
│   │   └── user_test.go
│   └── auth/
│       ├── auth.go
│       └── auth_test.go
├── pkg/
│   └── utils/
│       ├── utils.go
│       └── utils_test.go
├── test/
│   ├── testdata/
│   └── mocks/
├── go.mod
├── go.sum
└── Makefile
```

### Writing Tests

**Basic test**:

```go
func TestCalculateTotal(t *testing.T) {
    tests := []struct {
        name     string
        items    []float64
        taxRate  float64
        expected float64
        wantErr  bool
    }{
        {
            name:     "simple calculation",
            items:    []float64{10.0, 20.0, 30.0},
            taxRate:  0.08,
            expected: 64.8,
            wantErr:  false,
        },
        {
            name:     "negative tax rate",
            items:    []float64{10.0},
            taxRate:  -0.1,
            expected: 0,
            wantErr:  true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := CalculateTotal(tt.items, tt.taxRate)
            if (err != nil) != tt.wantErr {
                t.Errorf("CalculateTotal() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if !tt.wantErr && result != tt.expected {
                t.Errorf("CalculateTotal() = %v, want %v", result, tt.expected)
            }
        })
    }
}
```

**Using testify for assertions**:

```go
import (
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    "github.com/stretchr/testify/suite"
)

func TestUserCreate(t *testing.T) {
    // Use require for fatal assertions
    require.NotNil(t, db)
    
    user := &User{
        Name:  "John Doe",
        Email: "john@example.com",
    }
    
    err := userRepo.Create(user)
    require.NoError(t, err)
    assert.NotZero(t, user.ID)
    assert.Equal(t, "John Doe", user.Name)
}
```

**Test suites**:

```go
type UserServiceTestSuite struct {
    suite.Suite
    service *UserService
    mockDB  *MockDatabase
}

func (suite *UserServiceTestSuite) SetupTest() {
    suite.mockDB = NewMockDatabase(suite.T())
    suite.service = NewUserService(suite.mockDB)
}

func (suite *UserServiceTestSuite) TestCreateUser() {
    user := &User{Name: "John", Email: "john@example.com"}
    
    suite.mockDB.EXPECT().
        CreateUser(user).
        Return(nil).
        Times(1)
    
    err := suite.service.CreateUser(user)
    suite.NoError(err)
}

func TestUserServiceTestSuite(t *testing.T) {
    suite.Run(t, new(UserServiceTestSuite))
}
```

### Mocking with gomock

```go
//go:generate go run github.com/golang/mock/mockgen -destination=mocks/database.go -package=mocks myapp/internal Database

func TestUserService_GetUser(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()
    
    mockDB := mocks.NewMockDatabase(ctrl)
    service := NewUserService(mockDB)
    
    expectedUser := &User{ID: 1, Name: "John", Email: "john@example.com"}
    
    mockDB.EXPECT().
        GetUser(1).
        Return(expectedUser, nil).
        Times(1)
    
    user, err := service.GetUser(1)
    
    assert.NoError(t, err)
    assert.Equal(t, expectedUser, user)
}
```

### Testing Best Practices

- **Aim for >70% coverage**: Use `go test -cover ./...`
- **Test isolation**: Each test should be independent
- **Use table-driven tests**: For multiple test cases
- **Test edge cases**: Empty inputs, nil values, boundary conditions
- **Use subtests**: For related test cases with `t.Run()`
- **Mock external dependencies**: Use interfaces and mocking frameworks
- **Test concurrency**: Use `-race` flag to detect race conditions

### Integration Testing

```go
// test/integration_test.go
//go:build integration

package test

import (
    "testing"
    "myapp/internal"
)

func TestDatabaseIntegration(t *testing.T) {
    db := setupTestDatabase(t)
    defer cleanupTestDatabase(t, db)
    
    userRepo := internal.NewUserRepository(db)
    
    user := &User{Name: "Test User", Email: "test@example.com"}
    err := userRepo.Create(user)
    require.NoError(t, err)
    
    retrieved, err := userRepo.Get(user.ID)
    require.NoError(t, err)
    assert.Equal(t, user.Name, retrieved.Name)
}
```

## Linting & Code Quality

### golangci-lint Configuration

**`.golangci.yml`**:

```yaml
run:
  timeout: 5m
  tests: true
  skip-dirs:
    - vendor
    - testdata

linters:
  enable:
    - gofmt
    - goimports
    - govet
    - errcheck
    - staticcheck
    - unused
    - gosimple
    - ineffassign
    - misspell
    - unconvert
    - unparam
    - nakedret
    - prealloc
    - gocritic
    - gosec
    - goconst
    - gocyclo
    - dupl
    - gochecknoinits
    - gomnd
    - gomoddirectives
    - gomodguard
    - goprintffuncname
    - nolintlint
    - rowserrcheck
    - sqlclosecheck
    - bodyclose
    - noctx
    - exportloopref

linters-settings:
  gofmt:
    simplify: true
  goimports:
    local-prefixes: myapp
  errcheck:
    check-type-assertions: true
    check-blank: true
    ignore: fmt:.*,io/ioutil:^Read.*
  gocyclo:
    min-complexity: 15
  dupl:
    threshold: 100
  goconst:
    min-len: 3
    min-occurrences: 3
  gocritic:
    enabled-tags:
      - diagnostic
      - experimental
      - opinionated
      - performance
      - style
    disabled-checks:
      - dupImport
      - ifElseChain
      - octalLiteral
      - whyNoLint
      - wrapperFunc
  gomnd:
    settings:
      mnd:
        checks: argument,case,condition,operation,return,assign

issues:
  exclude-use-default: false
  max-issues-per-linter: 0
  max-same-issues: 0
  exclude-rules:
    - path: _test\.go
      linters:
        - gomnd
        - goconst
        - gocyclo
    - path: test/
      linters:
        - gosec
        - errcheck
```

### Linting Categories

**Mechanical fixes (safe to auto-fix)**:

- **gofmt**: Code formatting issues
- **goimports**: Import organization
- **misspell**: Spelling errors
- **unconvert**: Unnecessary type conversions
- **ineffassign**: Ineffective assignments

**Complex fixes (requires analysis)**:

- **gosec**: Security issues - review carefully
- **gocritic**: Code quality suggestions - evaluate impact
- **gocyclo**: Cyclomatic complexity - refactor complex functions
- **dupl**: Code duplication - consider refactoring
- **errcheck**: Unchecked errors - handle appropriately

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
      - id: check-merge-conflict

  - repo: https://github.com/pre-commit/mirrors-golangci-lint
    rev: v1.54.2
    hooks:
      - id: golangci-lint

  - repo: local
    hooks:
      - id: go-mod-tidy
        name: go mod tidy
        entry: go mod tidy
        language: system
        files: (go\.mod|go\.sum)$
        pass_filenames: false

      - id: go-test
        name: go test
        entry: go test ./...
        language: system
        pass_filenames: false
```

## Concurrency Best Practices

### Goroutine Management

**Use worker pools**:

```go
func ProcessItems(items []Item, numWorkers int) error {
    jobs := make(chan Item, len(items))
    results := make(chan error, len(items))
    
    // Start workers
    for i := 0; i < numWorkers; i++ {
        go func() {
            for item := range jobs {
                if err := processItem(item); err != nil {
                    results <- err
                }
            }
        }()
    }
    
    // Send jobs
    for _, item := range items {
        jobs <- item
    }
    close(jobs)
    
    // Collect results
    for i := 0; i < len(items); i++ {
        if err := <-results; err != nil {
            return err
        }
    }
    
    return nil
}
```

**Use context for cancellation**:

```go
func ProcessWithTimeout(ctx context.Context, data []byte) error {
    ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
    defer cancel()
    
    resultChan := make(chan []byte, 1)
    errChan := make(chan error, 1)
    
    go func() {
        result, err := processData(data)
        if err != nil {
            errChan <- err
            return
        }
        resultChan <- result
    }()
    
    select {
    case result := <-resultChan:
        handleResult(result)
        return nil
    case err := <-errChan:
        return err
    case <-ctx.Done():
        return ctx.Err()
    }
}
```

### Channel Patterns

**Use buffered channels appropriately**:

```go
// Good - buffered channel for throughput
func WorkerPool(jobs <-chan Job, results chan<- Result) {
    for job := range jobs {
        result := processJob(job)
        results <- result
    }
}

// Avoid - unbuffered channel can cause deadlock
func BadExample() {
    ch := make(chan int)
    ch <- 1  // This will block forever if no receiver
}
```

**Use select for non-blocking operations**:

```go
func HandleRequests(requests <-chan Request) {
    for {
        select {
        case req := <-requests:
            handleRequest(req)
        case <-time.After(5 * time.Second):
            log.Println("No requests received in 5 seconds")
        case <-ctx.Done():
            log.Println("Shutting down")
            return
        }
    }
}
```

### Synchronization

**Use mutex for shared state**:

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
```

**Use sync.Once for initialization**:

```go
var (
    instance *Service
    once     sync.Once
)

func GetInstance() *Service {
    once.Do(func() {
        instance = &Service{
            // initialization
        }
    })
    return instance
}
```

### Concurrency Guidelines

- **Prefer channels over shared memory**: "Do not communicate by sharing memory; instead, share memory by communicating"
- **Use context for cancellation**: Always pass context to long-running operations
- **Avoid goroutine leaks**: Ensure all goroutines can exit
- **Use race detector**: Run tests with `-race` flag
- **Be careful with closures**: Capture variables correctly in goroutines
- **Use worker pools**: Limit concurrent goroutines for resource management

## Database Best Practices

### Database Drivers

**Use modern database drivers**:

```go
// PostgreSQL
import (
    "github.com/lib/pq"
    "database/sql"
)

func NewDB(dsn string) (*sql.DB, error) {
    db, err := sql.Open("postgres", dsn)
    if err != nil {
        return nil, err
    }
    
    // Configure connection pool
    db.SetMaxOpenConns(25)
    db.SetMaxIdleConns(5)
    db.SetConnMaxLifetime(5 * time.Minute)
    
    return db, nil
}
```

### Query Patterns

**Use prepared statements**:

```go
func (r *UserRepository) GetByID(id int) (*User, error) {
    const query = `
        SELECT id, name, email, created_at 
        FROM users 
        WHERE id = $1
    `
    
    var user User
    err := r.db.QueryRow(query, id).Scan(
        &user.ID,
        &user.Name,
        &user.Email,
        &user.CreatedAt,
    )
    
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, ErrUserNotFound
        }
        return nil, fmt.Errorf("get user by id: %w", err)
    }
    
    return &user, nil
}
```

**Use transactions**:

```go
func (s *UserService) CreateUserWithProfile(user *User, profile *Profile) error {
    tx, err := s.db.Begin()
    if err != nil {
        return fmt.Errorf("begin transaction: %w", err)
    }
    defer tx.Rollback()
    
    // Create user
    if err := s.userRepo.CreateWithTx(tx, user); err != nil {
        return fmt.Errorf("create user: %w", err)
    }
    
    // Create profile
    profile.UserID = user.ID
    if err := s.profileRepo.CreateWithTx(tx, profile); err != nil {
        return fmt.Errorf("create profile: %w", err)
    }
    
    return tx.Commit()
}
```

### ORM Usage

**Use GORM for complex applications**:

```go
import (
    "gorm.io/gorm"
    "gorm.io/driver/postgres"
)

type User struct {
    ID        uint           `gorm:"primaryKey"`
    Name      string         `gorm:"not null"`
    Email     string         `gorm:"uniqueIndex;not null"`
    CreatedAt time.Time      `gorm:"autoCreateTime"`
    UpdatedAt time.Time      `gorm:"autoUpdateTime"`
    DeletedAt gorm.DeletedAt `gorm:"index"`
    Profile   Profile        `gorm:"foreignKey:UserID"`
}

func NewDB(dsn string) (*gorm.DB, error) {
    db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
        Logger: logger.Default.LogMode(logger.Info),
    })
    if err != nil {
        return nil, err
    }
    
    sqlDB, err := db.DB()
    if err != nil {
        return nil, err
    }
    
    sqlDB.SetMaxOpenConns(25)
    sqlDB.SetMaxIdleConns(5)
    
    return db, nil
}
```

### Database Guidelines

- **Use connection pooling**: Configure appropriate pool sizes
- **Handle transactions properly**: Always commit or rollback
- **Use prepared statements**: For security and performance
- **Implement proper indexing**: Based on query patterns
- **Use migrations**: Track schema changes with tools like golang-migrate
- **Monitor query performance**: Use logging and metrics
- **Handle connection errors**: Implement retry logic where appropriate

## Security Best Practices

### Input Validation

**Validate all external input**:

```go
type CreateUserRequest struct {
    Name  string `json:"name" validate:"required,min=1,max=100"`
    Email string `json:"email" validate:"required,email"`
    Age   int    `json:"age" validate:"gte=0,lte=150"`
}

func (s *UserService) CreateUser(req *CreateUserRequest) (*User, error) {
    if err := s.validator.Struct(req); err != nil {
        return nil, NewValidationError("request", err.Error())
    }
    
    // Additional business logic validation
    if strings.Contains(req.Name, "admin") {
        return nil, NewValidationError("name", "cannot contain 'admin'")
    }
    
    user := &User{
        Name: req.Name,
        Email: req.Email,
        Age: req.Age,
    }
    
    return s.repo.Create(user)
}
```

### Password Security

**Use proper password hashing**:

```go
import "golang.org/x/crypto/bcrypt"

func HashPassword(password string) (string, error) {
    bytes, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
    return string(bytes), err
}

func CheckPassword(password, hash string) bool {
    err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
    return err == nil
}
```

### JWT Authentication

```go
import "github.com/golang-jwt/jwt/v5"

type Claims struct {
    UserID int    `json:"user_id"`
    Email  string `json:"email"`
    jwt.RegisteredClaims
}

func GenerateToken(userID int, email string, secret string) (string, error) {
    claims := &Claims{
        UserID: userID,
        Email:  email,
        RegisteredClaims: jwt.RegisteredClaims{
            ExpiresAt: jwt.NewNumericDate(time.Now().Add(24 * time.Hour)),
            IssuedAt:  jwt.NewNumericDate(time.Now()),
        },
    }
    
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    return token.SignedString([]byte(secret))
}
```

### Security Guidelines

- **Validate all input**: Never trust external data
- **Use parameterized queries**: Prevent SQL injection
- **Implement authentication & authorization**: JWT, OAuth2, etc.
- **Enable HTTPS**: Always use TLS in production
- **Implement rate limiting**: Prevent abuse
- **Don't log sensitive data**: Passwords, tokens, API keys
- **Use secure headers**: Implement CSP, HSTS, etc.
- **Regular security audits**: Use `gosec` linter and security scanning
- **Keep dependencies updated**: Address security vulnerabilities
- **Use environment variables**: For secrets and configuration

```go
// Good - use environment variables
func GetDBConfig() *DBConfig {
    return &DBConfig{
        Host:     os.Getenv("DB_HOST"),
        Port:     os.Getenv("DB_PORT"),
        User:     os.Getenv("DB_USER"),
        Password: os.Getenv("DB_PASSWORD"),
        Database: os.Getenv("DB_NAME"),
    }
}

// Avoid - hardcoded credentials
func GetDBConfigBad() *DBConfig {
    return &DBConfig{
        Host:     "localhost",
        Password: "hardcoded-password",  // Bad!
    }
}
```

## Performance Optimization

### Profiling

**Use pprof for profiling**:

```go
import (
    _ "net/http/pprof"
    "net/http"
)

func main() {
    // Enable pprof
    go func() {
        log.Println(http.ListenAndServe("localhost:6060", nil))
    }()
    
    // Application code
}
```

```bash
# CPU profiling
go tool pprof http://localhost:6060/debug/pprof/profile

# Memory profiling
go tool pprof http://localhost:6060/debug/pprof/heap

# Goroutine profiling
go tool pprof http://localhost:6060/debug/pprof/goroutine
```

### Memory Management

**Use object pooling for frequently allocated objects**:

```go
var bufferPool = sync.Pool{
    New: func() interface{} {
        return make([]byte, 0, 1024)
    },
}

func ProcessData(data []byte) {
    buf := bufferPool.Get().([]byte)
    defer bufferPool.Put(buf[:0]) // Reset length but keep capacity
    
    // Use buffer
    buf = append(buf, data...)
    processData(buf)
}
```

**Avoid memory leaks**:

```go
// Good - proper cleanup
func ProcessWithTimeout() error {
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel() // Always call cancel
    
    return doWork(ctx)
}

// Avoid - potential memory leak
func BadExample() error {
    ctx, _ := context.WithTimeout(context.Background(), 30*time.Second)
    // Forgot to call cancel!
    return doWork(ctx)
}
```

### Performance Guidelines

- **Profile before optimizing**: Use pprof to identify bottlenecks
- **Use sync.Pool**: For frequently allocated objects
- **Avoid unnecessary allocations**: Reuse buffers and objects
- **Use efficient algorithms**: Choose appropriate data structures
- **Implement caching**: Redis or in-memory for frequently accessed data
- **Use connection pooling**: For database and HTTP connections
- **Batch operations**: Reduce round trips to database/API
- **Consider streaming**: For large data processing
- **Monitor performance**: Use metrics and logging

## Project Structure

**Recommended structure**:

```
myproject/
├── cmd/
│   ├── myapp/
│   │   └── main.go              # Application entry point
│   └── migration/
│       └── main.go              # Database migration tool
├── internal/
│   ├── auth/
│   │   ├── auth.go
│   │   ├── middleware.go
│   │   └── auth_test.go
│   ├── user/
│   │   ├── user.go
│   │   ├── repository.go
│   │   ├── service.go
│   │   └── user_test.go
│   └── config/
│       ├── config.go
│       └── config_test.go
├── pkg/
│   ├── logger/
│   │   ├── logger.go
│   │   └── logger_test.go
│   └── utils/
│       ├── utils.go
│       └── utils_test.go
├── api/
│   ├── openapi/
│   │   └── spec.yaml
│   └── proto/
│       └── user.proto
├── web/
│   ├── static/
│   └── templates/
├── scripts/
│   ├── build.sh
│   └── deploy.sh
├── deployments/
│   ├── docker/
│   │   └── Dockerfile
│   └── k8s/
├── test/
│   ├── integration/
│   ├── mocks/
│   └── testdata/
├── docs/
│   ├── api.md
│   └── deployment.md
├── go.mod
├── go.sum
├── Makefile
├── README.md
└── .gitignore
```

### Makefile

```makefile
.PHONY: build test lint clean docker

# Variables
APP_NAME=myapp
VERSION=$(shell git describe --tags --always --dirty)
LDFLAGS=-ldflags "-X main.version=$(VERSION)"

# Build
build:
	go build $(LDFLAGS) -o bin/$(APP_NAME) ./cmd/$(APP_NAME)

# Test
test:
	go test -v -race -cover ./...

test-integration:
	go test -v -race -tags=integration ./test/integration/...

# Lint
lint:
	golangci-lint run

# Format
fmt:
	goimports -w .
	gofmt -s -w .

# Clean
clean:
	rm -rf bin/

# Docker
docker:
	docker build -t $(APP_NAME):$(VERSION) .

# Dependencies
deps:
	go mod tidy
	go mod verify

# Security
security:
	gosec ./...

# Profile
profile:
	go tool pprof http://localhost:6060/debug/pprof/profile
```

## CI/CD Integration

### GitHub Actions

**`.github/workflows/ci.yml`**:

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        go-version: [1.20, 1.21]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Go
      uses: actions/setup-go@v4
      with:
        go-version: ${{ matrix.go-version }}
    
    - name: Cache Go modules
      uses: actions/cache@v3
      with:
        path: ~/go/pkg/mod
        key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
        restore-keys: |
          ${{ runner.os }}-go-
    
    - name: Install dependencies
      run: go mod download
    
    - name: Run tests
      run: go test -v -race -cover ./...
    
    - name: Run linter
      uses: golangci/golangci-lint-action@v3
      with:
        version: latest
    
    - name: Run security check
      run: |
        go install github.com/securecodewarrior/gosec/v2/cmd/gosec@latest
        gosec ./...
    
    - name: Build
      run: go build -v ./...
```

### CI Pipeline Steps

1. **Setup Go environment**: Install appropriate Go version
2. **Cache dependencies**: Speed up builds with module caching
3. **Install dependencies**: `go mod download`
4. **Run tests**: `go test -v -race -cover ./...`
5. **Run linter**: `golangci-lint run`
6. **Security scanning**: `gosec ./...`
7. **Build application**: `go build -v ./...`
8. **Upload artifacts**: Store binaries and test results

## Context7 Integration

Always use Context7 MCP server for current documentation when developing Go projects:

### Key Libraries

- `/golang/go` - Go language documentation
- `/gin-gonic/gin` - HTTP web framework
- `/lib/pq` - PostgreSQL driver
- `/gorm-io/gorm` - ORM library
- `/golang-jwt/jwt` - JWT implementation
- `/stretchr/testify` - Testing framework
- `/golang-migrate/migrate` - Database migration tool
- `/uber-go/zap` - Structured logging
- `/golang-mock/gomock` - Mocking framework

### Example Usage

```
Create a Go web service using Gin framework with JWT authentication,
PostgreSQL database with GORM, and proper testing with testify.
Include middleware, error handling, and API documentation.
use context7 /gin-gonic/gin /gorm-io/gorm /golang-jwt/jwt /stretchr/testify
```

## Summary

- **Use modern tools**: `go modules`, `golangci-lint`, `testify`, `gomock`
- **Test thoroughly**: >70% coverage, unit + integration tests, race detection
- **Handle errors properly**: Structured errors, wrapping, immediate handling
- **Write concurrent code safely**: Goroutines, channels, proper synchronization
- **Secure by default**: Input validation, authentication, encryption
- **Follow clean architecture**: Separate concerns, clear layers
- **Optimize when needed**: Profile first, then optimize
- **Automate quality checks**: CI/CD, pre-commit hooks
- **Keep dependencies updated**: Security and features

These practices ensure robust, maintainable, and secure Go applications.