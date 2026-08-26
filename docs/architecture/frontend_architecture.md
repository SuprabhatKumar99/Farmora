# Frontend Architecture

the frontend should be a **modular React + TypeScript application** that communicates with the Spring Boot backend through REST APIs and WebSockets.

```text
                         ┌─────────────────────┐
                         │       USER          │
                         │   Web Browser       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   React Application │
                         │    TypeScript       │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
       │ UI / Views   │      │ State Mgmt   │      │ API Layer    │
       │ Tailwind CSS │      │ Zustand      │      │ Axios        │
       │ shadcn/ui    │      │ TanStack     │      │ REST         │
       └──────────────┘      │ Query        │      │ WebSocket    │
                             └──────────────┘      └──────┬───────┘
                                                         │
                                                         ▼
                                              ┌────────────────────┐
                                              │ Spring Boot Backend│
                                              └────────────────────┘
```

## 1. Frontend Technology Stack

| Category       | Technology                     |
| -------------- | ------------------------------ |
| Framework      | **React.js**                   |
| Language       | **TypeScript**                 |
| Build Tool     | **Vite**                       |
| CSS            | **Tailwind CSS**               |
| UI Components  | **shadcn/ui**                  |
| Routing        | **React Router**               |
| Server State   | **TanStack Query**             |
| Client State   | **Zustand**                    |
| API Client     | **Axios**                      |
| Forms          | **React Hook Form**            |
| Validation     | **Zod**                        |
| Charts         | **Recharts**                   |
| Maps           | **React Leaflet + Leaflet**    |
| Icons          | **Lucide React**               |
| Notifications  | **Sonner**                     |
| Real-time      | **WebSocket / STOMP**          |
| Authentication | JWT + HttpOnly Cookies         |
| Testing        | Vitest + React Testing Library |
| E2E Testing    | Playwright                     |

---

# 2. Frontend Layered Architecture

```text
┌───────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                    │
│                                                           │
│ Pages • Layouts • Components • Forms • Tables • Charts   │
└───────────────────────────┬───────────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────┐
│                     FEATURE LAYER                          │
│                                                           │
│ Auth • Dashboard • Detection • Reports • Alerts • Users  │
└───────────────────────────┬───────────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────┐
│                      STATE LAYER                           │
│                                                           │
│ Zustand              TanStack Query                       │
│ Client State         Server/API State                     │
└───────────────────────────┬───────────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────┐
│                     SERVICE LAYER                          │
│                                                           │
│ Axios • API Services • WebSocket • Auth Interceptors     │
└───────────────────────────┬───────────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────┐
│                     BACKEND API                            │
│                                                           │
│                  Spring Boot Backend                       │
└───────────────────────────────────────────────────────────┘
```

---

# 3. Recommended Folder Structure

```text
frontend/
│
├── public/
│   ├── favicon.svg
│   ├── logo.svg
│   └── assets/
│
├── src/
│   │
│   ├── app/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   │
│   │   ├── router/
│   │   │   ├── AppRouter.tsx
│   │   │   ├── ProtectedRoute.tsx
│   │   │   └── RoleRoute.tsx
│   │   │
│   │   └── providers/
│   │       ├── QueryProvider.tsx
│   │       ├── ThemeProvider.tsx
│   │       └── WebSocketProvider.tsx
│   │
│   ├── components/
│   │   ├── ui/
│   │   ├── layout/
│   │   ├── common/
│   │   ├── charts/
│   │   ├── tables/
│   │   ├── maps/
│   │   └── media/
│   │
│   ├── features/
│   │   │
│   │   ├── auth/
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   ├── hooks/
│   │   │   ├── services/
│   │   │   ├── schemas/
│   │   │   └── types.ts
│   │   │
│   │   ├── dashboard/
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   ├── hooks/
│   │   │   └── types.ts
│   │   │
│   │   ├── detection/
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   ├── hooks/
│   │   │   ├── services/
│   │   │   └── types.ts
│   │   │
│   │   ├── reports/
│   │   ├── alerts/
│   │   ├── analytics/
│   │   ├── users/
│   │   ├── cameras/
│   │   └── settings/
│   │
│   ├── services/
│   │   ├── api/
│   │   │   ├── axios.ts
│   │   │   ├── authApi.ts
│   │   │   ├── detectionApi.ts
│   │   │   ├── reportApi.ts
│   │   │   ├── alertApi.ts
│   │   │   └── userApi.ts
│   │   │
│   │   └── websocket/
│   │       ├── client.ts
│   │       ├── events.ts
│   │       └── handlers.ts
│   │
│   ├── store/
│   │   ├── authStore.ts
│   │   ├── uiStore.ts
│   │   └── filterStore.ts
│   │
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useDebounce.ts
│   │   ├── useWebSocket.ts
│   │   └── useMediaQuery.ts
│   │
│   ├── types/
│   │   ├── api.ts
│   │   ├── user.ts
│   │   ├── detection.ts
│   │   └── report.ts
│   │
│   ├── utils/
│   │   ├── formatters.ts
│   │   ├── validators.ts
│   │   ├── permissions.ts
│   │   └── constants.ts
│   │
│   ├── styles/
│   │   └── globals.css
│   │
│   └── config/
│       └── env.ts
│
├── .env
├── .env.production
├── Dockerfile
├── nginx.conf
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.ts
```

---

# 4. Feature-Based Architecture

Instead of putting everything into generic folders, keep functionality inside **features**.

For example:

```text
features/
│
├── auth/
├── dashboard/
├── detection/
├── reports/
├── alerts/
├── analytics/
├── cameras/
└── users/
```

Each feature owns its:

```text
components
pages
hooks
services
schemas
types
```

This makes the application easier to scale.

---

# 5. Application Pages

A recommended navigation structure:

```text
                    APPLICATION
                         │
       ┌─────────────────┼──────────────────┐
       │                 │                  │
    AUTHENTICATION     DASHBOARD         SETTINGS
       │                 │                  │
       ├─ Login          ├─ Overview        ├─ Profile
       ├─ Register       ├─ Live Status     ├─ Preferences
       └─ Forgot         ├─ Statistics      └─ Security
                         │
              ┌──────────┼───────────┐
              │          │           │
          DETECTION    REPORTS     ALERTS
              │          │           │
              ├─ Upload  ├─ Generate ├─ Active
              ├─ Live    ├─ History  ├─ History
              ├─ History └─ Export   └─ Details
              └─ Details
```

---

# 6. Dashboard Architecture

The dashboard should be composed of reusable widgets rather than one huge component.

```text
Dashboard
│
├── Header
│
├── KPI Cards
│   ├── Total Detections
│   ├── Active Alerts
│   ├── Processing Jobs
│   └── System Status
│
├── Detection Statistics
│   └── Recharts
│
├── Live Detection
│   ├── Camera Feed
│   ├── Bounding Boxes
│   └── Detection Metadata
│
├── Geographic View
│   └── Leaflet Map
│
├── Recent Detections
│   └── Data Table
│
└── Recent Alerts
```

---

# 7. AI Detection UI

The detection interface is one of the most important frontend modules.

```text
                Detection Page
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
    Upload         Camera        Video
     Image          Feed         Upload
       │             │             │
       └─────────────┼─────────────┘
                     ▼
              Spring Boot API
                     │
                     ▼
                  AI Engine
                     │
                     ▼
               Detection Result
                     │
                     ▼
              Frontend Renderer
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   Bounding Box   Confidence    Metadata
```

The frontend should render:

* Bounding boxes
* Object labels
* Confidence score
* Detection count
* Processing time
* Model version
* Timestamp
* Location
* Detection status

---

# 8. Real-Time Architecture

For live detection and alerts, use WebSockets.

```text
Spring Boot
     │
     │ WebSocket
     ▼
WebSocket Client
     │
     ▼
React Context / Hook
     │
     ▼
Zustand
     │
     ├───────────────┐
     ▼               ▼
Dashboard        Alert Panel
     │
     ▼
Detection UI
```

Example event:

```text
detection.completed
        │
        ▼
WebSocket
        │
        ▼
useWebSocket()
        │
        ▼
detectionStore
        │
        ├── Dashboard
        ├── Live Detection
        └── Notification
```

---

# 9. State Management

Don't put everything into Zustand.

Use **TanStack Query for server data** and **Zustand for client/UI state**.

### TanStack Query

Use for:

```text
Users
Detections
Reports
Alerts
Analytics
Camera data
API responses
```

### Zustand

Use for:

```text
Authentication state
Sidebar state
Theme
Selected camera
Filters
Modal state
UI preferences
```

Architecture:

```text
                  STATE
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
    Server State         Client State
          │                   │
          ▼                   ▼
 TanStack Query           Zustand
          │                   │
          ▼                   ▼
    Backend API          UI / Session
```

---

# 10. API Layer

Create one centralized Axios instance.

```text
services/
└── api/
    ├── axios.ts
    ├── authApi.ts
    ├── detectionApi.ts
    ├── reportApi.ts
    ├── alertApi.ts
    └── userApi.ts
```

Flow:

```text
React Component
      │
      ▼
Custom Hook
      │
      ▼
TanStack Query
      │
      ▼
API Service
      │
      ▼
Axios
      │
      ▼
Spring Boot
```

The component should **not directly call Axios**.

---

# 11. Authentication Architecture

```text
Login Page
    │
    ▼
authApi.login()
    │
    ▼
Spring Security
    │
    ▼
JWT / Session Cookie
    │
    ▼
Auth Store
    │
    ▼
Protected Routes
```

Route protection:

```text
/                   → Redirect
/login              → Public
/dashboard          → Authenticated
/detection          → Authenticated
/reports            → Authenticated
/admin/users        → ADMIN only
/settings           → Authenticated
```

Use role-based route guards:

```text
ProtectedRoute
      │
      ▼
Authenticated?
   │       │
  No      Yes
   │       │
 Login    Role Check
           │
       ┌───┴───┐
      Pass    Fail
       │        │
       ▼        ▼
     Page      403
```

---

# 12. UI Design System

Tailwind CSS + shadcn/ui should provide a consistent design system.

```text
Design System
│
├── Colors
├── Typography
├── Spacing
├── Border Radius
├── Shadows
├── Buttons
├── Inputs
├── Cards
├── Dialogs
├── Dropdowns
├── Tables
├── Tabs
├── Badges
├── Tooltips
└── Toasts
```

Keep all reusable primitives in:

```text
components/ui/
```

Feature-specific components should stay inside their feature.

---

# 13. Responsive Architecture

The frontend should support:

```text
Desktop
Tablet
Mobile
```

Use Tailwind responsive utilities:

```text
Mobile-first
    ↓
sm
    ↓
md
    ↓
lg
    ↓
xl
    ↓
2xl
```

For the main dashboard:

```text
Desktop
┌────────┬──────────────────────────┐
│ Sidebar│ Dashboard                │
│        │ ┌────┬────┬────┬────┐    │
│        │ │ KPI│ KPI│ KPI│ KPI│    │
│        │ └────┴────┴────┴────┘    │
│        │ ┌────────────┬─────────┐  │
│        │ │ Detection  │ Alerts  │  │
│        │ │ Chart      │         │  │
│        │ └────────────┴─────────┘  │
└────────┴──────────────────────────┘
```

Mobile:

```text
┌────────────────────┐
│ Header       ☰     │
├────────────────────┤
│ KPI                │
├────────────────────┤
│ Detection          │
├────────────────────┤
│ Alerts             │
├────────────────────┤
│ Recent Activity    │
└────────────────────┘
```

---

# 14. Error Handling

Centralized error handling:

```text
Backend
   │
   ▼
Axios
   │
   ▼
Response Interceptor
   │
   ├── 401 → Logout/Login
   ├── 403 → Permission Error
   ├── 404 → Not Found
   ├── 422 → Validation Error
   ├── 429 → Rate Limited
   └── 500 → Server Error
             │
             ▼
          Toast/UI
```

Use an error boundary around major application sections so one component failure doesn't bring down the entire application.

---

# 15. Performance Architecture

Important optimizations:

### Code splitting

```text
React.lazy()
Suspense
```

Load large features only when required.

### API caching

TanStack Query handles:

```text
Caching
Refetching
Deduplication
Background updates
Pagination
Retry
```

### Large tables

Use virtualization for large datasets.

### Images/videos

Use:

```text
Lazy loading
Compression
Thumbnail generation
Progressive loading
```

### Dashboard

Don't request every widget independently on every render; use query caching and appropriate stale times.

---

# 16. Frontend Security

Implement:

```text
HTTPS
JWT / HttpOnly cookies
RBAC
Input validation
XSS protection
CSRF protection where applicable
CSP
Secure headers
Rate limiting
File type validation
File size validation
```

For uploads:

```text
User
 │
 ▼
Frontend validation
 │
 ├── File type
 ├── File size
 └── Extension
 │
 ▼
Backend validation
 │
 ▼
Object Storage
```

**Never trust frontend validation alone.**

---

# 17. Testing Architecture

```text
                    TESTING
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
     Unit Tests   Integration      E2E Tests
        │              │              │
      Vitest      React Testing    Playwright
                    Library
```

Test:

* Components
* Hooks
* API services
* Authentication
* Route guards
* Forms
* Detection rendering
* Dashboard
* Upload flow
* Real-time alerts
* Responsive layouts

---

# 18. Frontend Docker Architecture

Production build:

```text
React Source
     │
     ▼
Node.js Build
     │
     ▼
npm run build
     │
     ▼
dist/
     │
     ▼
Nginx Container
     │
     ▼
Kubernetes
```

Recommended multi-stage Docker build:

```text
Stage 1
Node.js
   │
   └── Build React

Stage 2
Nginx
   │
   └── Serve dist/
```

This keeps the production image lightweight.

---

# 19. Frontend → Backend Communication

```text
                    FRONTEND
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
       REST API                 WebSocket
          │                         │
          │                         │
          ▼                         ▼
    Spring Boot API           Spring Boot
          │                         │
          │                         │
          ▼                         ▼
 PostgreSQL/Redis/Kafka       Real-time Events
```

### REST

Use for:

```text
Login
CRUD
Upload
Reports
History
Analytics
User management
Settings
```

### WebSocket

Use for:

```text
Live detections
AI processing status
Alerts
Notifications
Camera status
Job progress
```

---

# 20. Final Frontend Architecture

```text
┌───────────────────────────────────────────────────────────────┐
│                         BROWSER                               │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    REACT + TYPESCRIPT                   │  │
│  │                                                         │  │
│  │  ┌───────────────┐      ┌───────────────────────────┐  │  │
│  │  │    ROUTER     │      │       PRESENTATION        │  │  │
│  │  │ React Router  │─────►│ Tailwind + shadcn/ui      │  │  │
│  │  └───────────────┘      └─────────────┬─────────────┘  │  │
│  │                                       │                │  │
│  │                         ┌─────────────▼─────────────┐  │  │
│  │                         │         FEATURES          │  │  │
│  │                         │                           │  │  │
│  │                         │ Auth                      │  │  │
│  │                         │ Dashboard                 │  │  │
│  │                         │ Detection                 │  │  │
│  │                         │ Reports                   │  │  │
│  │                         │ Alerts                    │  │  │
│  │                         │ Analytics                 │  │  │
│  │                         │ Cameras                   │  │  │
│  │                         │ Users                     │  │  │
│  │                         └─────────────┬─────────────┘  │  │
│  │                                       │                │  │
│  │              ┌────────────────────────┴────────────┐  │  │
│  │              │                                     │  │  │
│  │              ▼                                     ▼  │  │
│  │       ┌──────────────┐                    ┌───────────┐│  │
│  │       │ TanStack     │                    │  Zustand  ││  │
│  │       │ Query        │                    │           ││  │
│  │       └──────┬───────┘                    └───────────┘│  │
│  │              │                                        │  │
│  │              ▼                                        │  │
│  │       ┌──────────────┐                    ┌───────────┐│  │
│  │       │    Axios     │                    │ WebSocket ││  │
│  │       └──────┬───────┘                    └─────┬─────┘│  │
│  └──────────────┼──────────────────────────────────┼──────┘  │
└─────────────────┼──────────────────────────────────┼─────────┘
                  │                                  │
                HTTPS                            WebSocket
                  │                                  │
                  └──────────────┬───────────────────┘
                                 ▼
                     ┌────────────────────────┐
                     │     SPRING BOOT API    │
                     └────────────────────────┘
```

### Recommended principle

**Keep the frontend feature-driven, strongly typed, API-driven, and independent of backend implementation details.**

The most important separation is:

**React UI → Feature Logic → State Management → API/WebSocket Services → Spring Boot**

