---
agpm:
  version: "1.0.0"
  templating: false
---
You are working with Vue.js, a progressive JavaScript framework for building user interfaces. Follow these Vue-specific best practices and patterns.

## Core Vue Principles

- Use the Composition API as the default approach
- Implement proper component composition and reusability
- Follow the single responsibility principle for components
- Use TypeScript for type safety and better developer experience

## Component Architecture

### Component Structure
```vue
<template>
  <div class="component-wrapper">
    <!-- Template content -->
    <button @click="handleClick">{{ buttonText }}</button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';

// Props definition
interface Props {
  initialCount?: number;
  title: string;
}

const props = withDefaults(defineProps<Props>(), {
  initialCount: 0
});

// Emits definition
interface Emits {
  update: [value: number];
  click: [event: MouseEvent];
}

const emit = defineEmits<Emits>();

// Reactive state
const count = ref(props.initialCount);
const isLoading = ref(false);

// Computed properties
const buttonText = computed(() => `Count: ${count.value}`);

// Methods
const handleClick = (event: MouseEvent) => {
  count.value++;
  emit('update', count.value);
  emit('click', event);
};

// Watchers
watch(count, (newValue, oldValue) => {
  console.log(`Count changed from ${oldValue} to ${newValue}`);
});

// Lifecycle hooks
onMounted(() => {
  console.log('Component mounted');
});
</script>

<style scoped>
.component-wrapper {
  /* Component-specific styles */
}
</style>
```

### Composables
```typescript
// useCounter.ts
import { ref, computed } from 'vue';

export interface UseCounterReturn {
  count: Ref<number>;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
  isEven: ComputedRef<boolean>;
}

export function useCounter(initialValue = 0): UseCounterReturn {
  const count = ref(initialValue);
  
  const increment = () => {
    count.value++;
  };
  
  const decrement = () => {
    count.value--;
  };
  
  const reset = () => {
    count.value = initialValue;
  };
  
  const isEven = computed(() => count.value % 2 === 0);
  
  return {
    count,
    increment,
    decrement,
    reset,
    isEven
  };
}
```

## State Management

### Local State
- Use `ref` and `reactive` for local state
- Use `computed` for derived state
- Use `watch` and `watchEffect` for side effects

### Global State with Pinia
```typescript
// stores/counter.ts
import { defineStore } from 'pinia';

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
    name: 'Counter Store'
  }),
  
  getters: {
    doubleCount: (state) => state.count * 2,
    isEven: (state) => state.count % 2 === 0
  },
  
  actions: {
    increment() {
      this.count++;
    },
    
    decrement() {
      this.count--;
    },
    
    reset() {
      this.count = 0;
    },
    
    async fetchCount() {
      // Async action
      const response = await fetch('/api/count');
      this.count = await response.json();
    }
  }
});
```

## Performance Optimization

### Computed Properties
```typescript
// Expensive calculations should be computed
const expensiveValue = computed(() => {
  return heavyCalculation(props.data);
});
```

### Lazy Loading Components
```vue
<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

const LazyComponent = defineAsyncComponent(() => 
  import('./LazyComponent.vue')
);
</script>

<template>
  <Suspense>
    <LazyComponent />
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>
```

### v-memo Directive
```vue
<template>
  <!-- Only re-render when item.id changes -->
  <div v-for="item in items" :key="item.id" v-memo="[item.id]">
    {{ item.name }}
  </div>
</template>
```

## Styling Approaches

### Scoped CSS
```vue
<style scoped>
.component {
  /* Scoped styles */
}
</style>
```

### CSS Modules
```vue
<template>
  <div :class="$style.container">
    <!-- Content -->
  </div>
</template>

<style module>
.container {
  /* Module styles */
}
</style>
```

### Tailwind CSS
```vue
<template>
  <div class="flex items-center justify-between p-4">
    <!-- Content -->
  </div>
</template>
```

## Testing

### Component Testing with Vue Test Utils
```typescript
import { mount } from '@vue/test-utils';
import Component from './Component.vue';

describe('Component', () => {
  it('renders correctly', () => {
    const wrapper = mount(Component, {
      props: {
        title: 'Test Title'
      }
    });
    
    expect(wrapper.text()).toContain('Test Title');
  });
  
  it('handles interactions', async () => {
    const wrapper = mount(Component);
    
    await wrapper.find('button').trigger('click');
    
    expect(wrapper.emitted()).toHaveProperty('click');
  });
  
  it('updates state correctly', async () => {
    const wrapper = mount(Component);
    
    await wrapper.find('button').trigger('click');
    
    expect(wrapper.vm.count).toBe(1);
  });
});
```

### Composable Testing
```typescript
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { count } = useCounter();
    
    expect(count.value).toBe(0);
  });
  
  it('increments correctly', () => {
    const { count, increment } = useCounter(5);
    
    increment();
    
    expect(count.value).toBe(6);
  });
});
```

## Common Patterns

### Conditional Rendering
```vue
<template>
  <div>
    <div v-if="condition">Show when true</div>
    <div v-else-if="otherCondition">Show when other is true</div>
    <div v-else>Show when false</div>
    
    <div v-show="isVisible">Toggle visibility</div>
  </div>
</template>
```

### List Rendering
```vue
<template>
  <ul>
    <li v-for="item in items" :key="item.id">
      {{ item.name }}
    </li>
  </ul>
  
  <!-- With index -->
  <ul>
    <li v-for="(item, index) in items" :key="item.id">
      {{ index }}: {{ item.name }}
    </li>
  </ul>
</template>
```

### Forms
```vue
<template>
  <form @submit.prevent="handleSubmit">
    <input
      v-model="formData.name"
      type="text"
      placeholder="Name"
      required
    />
    <input
      v-model="formData.email"
      type="email"
      placeholder="Email"
      required
    />
    <button type="submit" :disabled="isSubmitting">
      {{ isSubmitting ? 'Submitting...' : 'Submit' }}
    </button>
  </form>
</template>

<script setup lang="ts">
interface FormData {
  name: string;
  email: string;
}

const formData = ref<FormData>({
  name: '',
  email: ''
});

const isSubmitting = ref(false);

const handleSubmit = async () => {
  isSubmitting.value = true;
  try {
    // Submit logic
    await submitForm(formData.value);
  } finally {
    isSubmitting.value = false;
  }
};
</script>
```

## Error Handling

### Error Boundaries
```vue
<!-- ErrorBoundary.vue -->
<template>
  <div v-if="error" class="error-boundary">
    <h2>Something went wrong</h2>
    <p>{{ error.message }}</p>
    <button @click="resetError">Try again</button>
  </div>
  <slot v-else />
</template>

<script setup lang="ts">
import { ref, onErrorCaptured } from 'vue';

const error = ref<Error | null>(null);

onErrorCaptured((err) => {
  error.value = err;
  return false; // Prevent error from propagating
});

const resetError = () => {
  error.value = null;
};
</script>
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
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
});
```

### TypeScript Configuration
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

## Recommended Libraries

- **Routing**: Vue Router
- **State Management**: Pinia
- **HTTP Client**: Axios or Fetch API
- **Form Handling**: VeeValidate
- **UI Components**: Vuetify, Element Plus, or PrimeVue
- **Styling**: Tailwind CSS, SCSS
- **Testing**: Vue Test Utils, Vitest
- **Development Tools**: Vue DevTools

Always prioritize component reusability, performance, and accessibility when building Vue applications.