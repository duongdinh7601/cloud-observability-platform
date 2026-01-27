# Frontend Dashboard

The frontend is a **Next.js + TypeScript** application for the Cloud Observability Platform.  
It provides a production-style dashboard to **browse, filter, and inspect log data** collected by backend services.

This frontend is designed as a **client-first observability UI**, similar in spirit to tools like Datadog or Kibana, with a strong focus on usability, performance, and maintainable architecture.

---

## Features

- Display logs in a structured, readable list
- Cursor-based pagination with “Load more”
- Filter logs by:
  - Severity level (select input)
  - Service name (debounced text search)
- URL-synced filters (shareable & refresh-safe)
- Skeleton loading states (no layout shift)
- Friendly error and empty states with recovery actions
- Colored severity badges for fast scanning
- Relative timestamps with full timestamp tooltip
- Copy-to-clipboard action for log messages
- Modular, reusable UI components

---

## Tech Stack

- **Next.js (App Router)** for routing and rendering
- **React + TypeScript** for component-driven UI with strong type safety
- **Tailwind CSS** for utility-first styling
- **shadcn/ui** for accessible, composable UI primitives
- **TanStack Query (React Query)** for client-side data fetching, caching, and pagination
- **Fetch API** for communicating with backend services

---

## Architecture & Design Principles

- **Client-first rendering** for interactive dashboards
- **Clear separation of concerns**:
  - Page components orchestrate data and state
  - Presentational components render UI only
- **Query-driven state** (filters and pagination are part of the query key)
- **Environment-agnostic configuration** (API base URL via environment variables)
- **Production-minded UX patterns** (debounce, skeletons, recovery actions)

---

## Folder Structure

frontend/
```graphql
├── src/
│   ├── app/                  # Next.js App Router pages & layouts
│   │   ├── layout.tsx         # Global app layout (AppShell)
│   │   ├── page.tsx           # Home page
│   │   └── logs/
│   │       └── page.tsx       # Logs dashboard
│   ├── components/            # Reusable UI components
│   │   ├── log-row.tsx
│   │   ├── log-list.tsx
│   │   ├── log-filters.tsx
│   │   └── ui/                # shadcn/ui components
│   ├── lib/
│   │   ├── api/               # Typed API clients
│   │   └── use-debounced-value.ts
│   └── styles/
│       └── globals.css
├── public/                    # Static assets
├── package.json
├── tsconfig.json
└── README.md
```

---

## Setup Instructions

### Prerequisites
- Node.js 18+
- npm

1. Navigate to the frontend folder:
```bash
cd frontend
```
2. Install dependencies:
```bash
npm install
```
3. Start the development server:
```bash
npm run dev
```
The app will run on `http://localhost:3000` and connect to the backend API.

---

## Notes

- Designed to be **modular and scalable**
- Built with real-world dashboard patterns (pagination, filters, URL sync)
- Intended to be containerized alongside backend services
- Integrates with the Log Service via REST APIs (`GET /logs`, `POST /logs`)

---

## Future Improvements

- Time range filter (start / end timestamp)
- Log level aggregation & charts
- Live log streaming
- Metrics and alert dashboards
- Authentication & role-based access



