---
agpm:
  templating: false
---

You are working with Angular, a comprehensive TypeScript-based framework for building web applications. Follow these Angular-specific best practices and patterns.

## Core Angular Principles

- Use TypeScript for type safety and better developer experience
- Follow Angular's component-based architecture
- Implement proper separation of concerns
- Use RxJS for reactive programming
- Follow Angular style guide conventions

## Component Architecture

### Component Structure
```typescript
// component.component.ts
import { Component, OnInit, OnDestroy, Input, Output, EventEmitter } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-component',
  templateUrl: './component.component.html',
  styleUrls: ['./component.component.scss']
})
export class ComponentComponent implements OnInit, OnDestroy {
  @Input() public data: string = '';
  @Output() public dataChange = new EventEmitter<string>();
  
  private destroy$ = new Subject<void>();
  public isLoading = false;
  public items: Item[] = [];
  
  constructor(private dataService: DataService) {}
  
  public ngOnInit(): void {
    this.loadData();
  }
  
  public ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
  
  public loadData(): void {
    this.isLoading = true;
    this.dataService.getData()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (items) => {
          this.items = items;
          this.isLoading = false;
        },
        error: (error) => {
          console.error('Error loading data:', error);
          this.isLoading = false;
        }
      });
  }
  
  public handleItemClick(item: Item): void {
    this.dataChange.emit(item.id);
  }
}
```

### Component Template
```html
<!-- component.component.html -->
<div class="component-wrapper">
  <div *ngIf="isLoading" class="loading">
    <app-loading-spinner></app-loading-spinner>
  </div>
  
  <div *ngIf="!isLoading" class="content">
    <h2>{{ data }}</h2>
    
    <ul class="item-list">
      <li 
        *ngFor="let item of items; trackBy: trackByItemId"
        (click)="handleItemClick(item)"
        class="item"
        [class.active]="item.isActive"
      >
        {{ item.name }}
      </li>
    </ul>
  </div>
</div>
```

### Component Styles
```scss
// component.component.scss
.component-wrapper {
  padding: 1rem;
  
  .loading {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 200px;
  }
  
  .content {
    .item-list {
      list-style: none;
      padding: 0;
      
      .item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        cursor: pointer;
        border-radius: 4px;
        transition: background-color 0.2s;
        
        &:hover {
          background-color: #f0f0f0;
        }
        
        &.active {
          background-color: #007bff;
          color: white;
        }
      }
    }
  }
}
```

## Services and Dependency Injection

### Service Structure
```typescript
// data.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private readonly apiUrl = 'https://api.example.com/data';
  
  constructor(private http: HttpClient) {}
  
  public getData(): Observable<Item[]> {
    return this.http.get<{ data: Item[] }>(this.apiUrl).pipe(
      map(response => response.data),
      catchError(this.handleError)
    );
  }
  
  public getItem(id: string): Observable<Item> {
    return this.http.get<Item>(`${this.apiUrl}/${id}`).pipe(
      catchError(this.handleError)
    );
  }
  
  public createItem(item: CreateItemDto): Observable<Item> {
    return this.http.post<Item>(this.apiUrl, item).pipe(
      catchError(this.handleError)
    );
  }
  
  public updateItem(id: string, item: UpdateItemDto): Observable<Item> {
    return this.http.put<Item>(`${this.apiUrl}/${id}`, item).pipe(
      catchError(this.handleError)
    );
  }
  
  public deleteItem(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`).pipe(
      catchError(this.handleError)
    );
  }
  
  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An unknown error occurred';
    
    if (error.error instanceof ErrorEvent) {
      errorMessage = `Client error: ${error.error.message}`;
    } else {
      errorMessage = `Server error: ${error.status} - ${error.message}`;
    }
    
    console.error(errorMessage, error);
    return throwError(() => new Error(errorMessage));
  }
}
```

## Reactive Programming with RxJS

### Common Operators
```typescript
import { Component, OnInit } from '@angular/core';
import { BehaviorSubject, combineLatest, debounceTime, distinctUntilChanged, switchMap } from 'rxjs';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html'
})
export class SearchComponent implements OnInit {
  private searchTerms$ = new BehaviorSubject<string>('');
  public results$ = this.searchTerms$.pipe(
    debounceTime(300),
    distinctUntilChanged(),
    switchMap(term => this.searchService.search(term))
  );
  
  public onSearch(term: string): void {
    this.searchTerms$.next(term);
  }
}
```

### State Management with Services
```typescript
// state.service.ts
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface AppState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class StateService {
  private readonly initialState: AppState = {
    user: null,
    isLoading: false,
    error: null
  };
  
  private state$ = new BehaviorSubject<AppState>(this.initialState);
  
  public getState(): Observable<AppState> {
    return this.state$.asObservable();
  }
  
  public updateUser(user: User | null): void {
    const currentState = this.state$.value;
    this.state$.next({ ...currentState, user });
  }
  
  public setLoading(isLoading: boolean): void {
    const currentState = this.state$.value;
    this.state$.next({ ...currentState, isLoading });
  }
  
  public setError(error: string | null): void {
    const currentState = this.state$.value;
    this.state$.next({ ...currentState, error });
  }
}
```

## Forms

### Reactive Forms
```typescript
// form.component.ts
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';

@Component({
  selector: 'app-form',
  templateUrl: './form.component.html'
})
export class FormComponent implements OnInit {
  public userForm: FormGroup;
  
  constructor(private fb: FormBuilder) {}
  
  public ngOnInit(): void {
    this.userForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      age: [null, [Validators.min(18), Validators.max(120)]],
      address: this.fb.group({
        street: [''],
        city: [''],
        zipCode: ['', [Validators.pattern(/^\d{5}$/)]]
      })
    });
  }
  
  public onSubmit(): void {
    if (this.userForm.valid) {
      console.log('Form submitted:', this.userForm.value);
      // Submit logic
    } else {
      this.markFormGroupTouched(this.userForm);
    }
  }
  
  public get nameControl(): FormControl {
    return this.userForm.get('name') as FormControl;
  }
  
  public get emailControl(): FormControl {
    return this.userForm.get('email') as FormControl;
  }
  
  private markFormGroupTouched(formGroup: FormGroup): void {
    Object.values(formGroup.controls).forEach(control => {
      control.markAsTouched();
      
      if (control instanceof FormGroup) {
        this.markFormGroupTouched(control);
      }
    });
  }
}
```

### Form Template
```html
<!-- form.component.html -->
<form [formGroup]="userForm" (ngSubmit)="onSubmit()">
  <div class="form-group">
    <label for="name">Name:</label>
    <input 
      id="name" 
      type="text" 
      formControlName="name"
      [class.is-invalid]="nameControl.invalid && nameControl.touched"
    >
    <div *ngIf="nameControl.invalid && nameControl.touched" class="error-message">
      <div *ngIf="nameControl.errors?.['required']">Name is required</div>
      <div *ngIf="nameControl.errors?.['minlength']">Name must be at least 2 characters</div>
    </div>
  </div>
  
  <div class="form-group">
    <label for="email">Email:</label>
    <input 
      id="email" 
      type="email" 
      formControlName="email"
      [class.is-invalid]="emailControl.invalid && emailControl.touched"
    >
    <div *ngIf="emailControl.invalid && emailControl.touched" class="error-message">
      <div *ngIf="emailControl.errors?.['required']">Email is required</div>
      <div *ngIf="emailControl.errors?.['email']">Please enter a valid email</div>
    </div>
  </div>
  
  <div formGroupName="address">
    <div class="form-group">
      <label for="city">City:</label>
      <input id="city" type="text" formControlName="city">
    </div>
  </div>
  
  <button type="submit" [disabled]="userForm.invalid">Submit</button>
</form>
```

## Routing

### Route Configuration
```typescript
// app-routing.module.ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';
import { HomeComponent } from './components/home/home.component';
import { AboutComponent } from './components/about/about.component';
import { ProfileComponent } from './components/profile/profile.component';

const routes: Routes = [
  { path: '', component: HomeComponent, pathMatch: 'full' },
  { path: 'about', component: AboutComponent },
  { 
    path: 'profile', 
    component: ProfileComponent,
    canActivate: [AuthGuard]
  },
  { 
    path: 'users/:id', 
    component: UserDetailComponent,
    resolve: { user: UserResolver }
  },
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
```

### Route Guards
```typescript
// auth.guard.ts
import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}
  
  public canActivate(): boolean {
    if (this.authService.isAuthenticated()) {
      return true;
    }
    
    this.router.navigate(['/login']);
    return false;
  }
}
```

## Testing

### Component Testing
```typescript
// component.component.spec.ts
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ComponentComponent } from './component.component';
import { DataService } from '../services/data.service';
import { of, throwError } from 'rxjs';

describe('ComponentComponent', () => {
  let component: ComponentComponent;
  let fixture: ComponentFixture<ComponentComponent>;
  let dataServiceSpy: jasmine.SpyObj<DataService>;
  
  beforeEach(async () => {
    const spy = jasmine.createSpyObj('DataService', ['getData']);
    
    await TestBed.configureTestingModule({
      declarations: [ComponentComponent],
      providers: [
        { provide: DataService, useValue: spy }
      ]
    }).compileComponents();
    
    fixture = TestBed.createComponent(ComponentComponent);
    component = fixture.componentInstance;
    dataServiceSpy = TestBed.inject(DataService) as jasmine.SpyObj<DataService>;
  });
  
  it('should create', () => {
    expect(component).toBeTruthy();
  });
  
  it('should load data on init', () => {
    const mockItems = [{ id: '1', name: 'Test Item' }];
    dataServiceSpy.getData.and.returnValue(of(mockItems));
    
    fixture.detectChanges();
    
    expect(dataServiceSpy.getData).toHaveBeenCalled();
    expect(component.items).toEqual(mockItems);
    expect(component.isLoading).toBe(false);
  });
  
  it('should handle data load error', () => {
    dataServiceSpy.getData.and.returnValue(throwError(() => new Error('Test error')));
    
    fixture.detectChanges();
    
    expect(component.isLoading).toBe(false);
    expect(component.items).toEqual([]);
  });
  
  it('should emit dataChange on item click', () => {
    const mockItem = { id: '1', name: 'Test Item' };
    spyOn(component.dataChange, 'emit');
    
    component.handleItemClick(mockItem);
    
    expect(component.dataChange.emit).toHaveBeenCalledWith('1');
  });
});
```

## Performance Optimization

### OnPush Change Detection
```typescript
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

@Component({
  selector: 'app-optimized',
  templateUrl: './optimized.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OptimizedComponent {
  @Input() public data: any;
}
```

### Lazy Loading Modules
```typescript
const routes: Routes = [
  {
    path: 'feature',
    loadChildren: () => import('./feature/feature.module').then(m => m.FeatureModule)
  }
];
```

## Accessibility

- Use semantic HTML elements
- Implement proper ARIA attributes
- Ensure keyboard navigation
- Test with screen readers
- Follow WCAG guidelines

## Build Tools and Development

### Angular CLI Configuration
```json
{
  "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
  "version": 1,
  "newProjectRoot": "projects",
  "projects": {
    "app": {
      "projectType": "application",
      "schematics": {
        "@schematics/angular:component": {
          "style": "scss",
          "skipTests": true
        }
      },
      "root": "",
      "sourceRoot": "src",
      "prefix": "app",
      "architect": {
        "build": {
          "builder": "@angular-devkit/build-angular:browser",
          "options": {
            "outputPath": "dist/app",
            "index": "src/index.html",
            "main": "src/main.ts",
            "polyfills": "src/polyfills.ts",
            "tsConfig": "tsconfig.app.json",
            "assets": ["src/favicon.ico", "src/assets"],
            "styles": ["src/styles.scss"],
            "scripts": []
          }
        }
      }
    }
  }
}
```

## Recommended Libraries

- **HTTP Client**: Angular HttpClient
- **Forms**: Angular Reactive Forms
- **Routing**: Angular Router
- **State Management**: NgRx, Akita, or Services
- **UI Components**: Angular Material, PrimeNG, or NG-ZORRO
- **Testing**: Jasmine, Karma, Angular Testing Utilities
- **Styling**: Angular Material, SCSS, Tailwind CSS
- **Development Tools**: Angular CLI, Angular DevTools

Always follow Angular style guide conventions and prioritize maintainability, testability, and performance when building Angular applications.