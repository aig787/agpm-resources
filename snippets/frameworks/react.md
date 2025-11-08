---
agpm:
  version: "1.1.0"
  templating: true
---
You are working with React, a popular JavaScript library for building user interfaces. Follow these React-specific best practices and patterns.

## Core React Principles

- Use functional components with hooks as the default approach
- Implement proper component composition and reusability
- Follow the single responsibility principle for components
- Use TypeScript for type safety and better developer experience

## Component Architecture

### Component Structure
```typescript
interface ComponentProps {
  // Define prop types here
}

const Component: React.FC<ComponentProps> = ({ prop1, prop2 }) => {
  // Hooks and state management
  const [state, setState] = useState<Type>(initialValue);
  
  // Effects and side effects
  useEffect(() => {
    // Side effect logic
    return () => {
      // Cleanup
    };
  }, [dependencies]);
  
  // Event handlers
  const handleClick = useCallback(() => {
    // Handler logic
  }, [dependencies]);
  
  // Render logic
  return (
    <div className="component-wrapper">
      {/* JSX content */}
    </div>
  );
};

export default Component;
```

### Custom Hooks
```typescript
interface UseCustomHookReturn {
  // Return type definition
}

const useCustomHook = (param: Type): UseCustomHookReturn => {
  // Hook logic
  return {
    // Return values
  };
};

export default useCustomHook;
```

## State Management

### Local State
- Use `useState` for simple local state
- Use `useReducer` for complex state logic
- Consider `useContext` for prop drilling avoidance

### Global State
- Use Zustand for simple global state
- Use Redux Toolkit for complex state management
- Consider React Query/TanStack Query for server state

## Performance Optimization

### Memoization
- Use `React.memo` for component memoization
- Use `useMemo` for expensive calculations
- Use `useCallback` for function references

### Code Splitting
```typescript
const LazyComponent = React.lazy(() => import('./LazyComponent'));

// Usage with Suspense
<Suspense fallback={<Loading />}>
  <LazyComponent />
</Suspense>
```

## Styling Approaches

### CSS Modules
```typescript
import styles from './Component.module.css';

const Component = () => (
  <div className={styles.container}>
    {/* Content */}
  </div>
);
```

### Styled Components
```typescript
import styled from 'styled-components';

const StyledContainer = styled.div`
  /* CSS styles */
`;

const Component = () => (
  <StyledContainer>
    {/* Content */}
  </StyledContainer>
);
```

### Tailwind CSS
```typescript
const Component = () => (
  <div className="flex items-center justify-between p-4">
    {/* Content */}
  </div>
);
```

## Testing

### Component Testing
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import Component from './Component';

describe('Component', () => {
  it('renders correctly', () => {
    render(<Component prop="value" />);
    expect(screen.getByText('expected text')).toBeInTheDocument();
  });
  
  it('handles interactions', () => {
    const handleClick = jest.fn();
    render(<Component onClick={handleClick} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalled();
  });
});
```

### Hook Testing
```typescript
import { renderHook, act } from '@testing-library/react';
import useCustomHook from './useCustomHook';

describe('useCustomHook', () => {
  it('returns expected values', () => {
    const { result } = renderHook(() => useCustomHook('param'));
    
    expect(result.current.value).toBe('expected');
  });
  
  it('handles state updates', () => {
    const { result } = renderHook(() => useCustomHook('param'));
    
    act(() => {
      result.current.updateValue('new value');
    });
    
    expect(result.current.value).toBe('new value');
  });
});
```

## Common Patterns

### Conditional Rendering
```typescript
const Component = ({ condition, children }) => (
  <div>
    {condition && <ConditionalComponent />}
    {condition ? <TrueComponent /> : <FalseComponent />}
    {children}
  </div>
);
```

### Lists and Keys
```typescript
const ListComponent = ({ items }) => (
  <ul>
    {items.map((item) => (
      <ListItem key={item.id} item={item} />
    ))}
  </ul>
);
```

### Forms
```typescript
const FormComponent = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: ''
  });
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Submit logic
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        name="name"
        value={formData.name}
        onChange={handleChange}
      />
      <input
        name="email"
        value={formData.email}
        onChange={handleChange}
      />
      <button type="submit">Submit</button>
    </form>
  );
};
```

## Error Handling

### Error Boundaries
```typescript
class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }
  
  static getDerivedStateFromError(error: Error) {
    return { hasError: true };
  }
  
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    
    return this.props.children;
  }
}
```

## Accessibility

- Use semantic HTML elements
- Implement proper ARIA attributes
- Ensure keyboard navigation
- Test with screen readers
- Follow WCAG guidelines

## Build Tools and Development

### Vite Configuration
```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': '/src',
    },
  },
});
```

### ESLint Configuration
```json
{
  "extends": [
    "react-app",
    "react-app/jest",
    "@typescript-eslint/recommended"
  ],
  "rules": {
    "react-hooks/exhaustive-deps": "warn",
    "@typescript-eslint/no-unused-vars": "error"
  }
}
```

## Recommended Libraries

- **Routing**: React Router
- **HTTP Client**: Axios or Fetch API
- **Form Handling**: React Hook Form
- **UI Components**: Material-UI, Ant Design, or Chakra UI
- **Styling**: Styled Components, Emotion, or Tailwind CSS
- **Testing**: React Testing Library, Jest
- **State Management**: Zustand, Redux Toolkit, or React Query
- **Development Tools**: React DevTools, Redux DevTools

Always prioritize component reusability, performance, and accessibility when building React applications.