# Frontend Dashboard

The frontend is a **React + TypeScript application** for the Cloud Observability Platform.  
It provides a user interface to view, filter, and visualize log entries collected by the backend services.

---

## Features

- Display logs in tables with sorting and pagination  
- Filter logs by timestamp, severity, and service name  
- Responsive and modular UI components  
- Connects to backend API (`POST /logs`, `GET /logs`)  
- Designed for future visualization of metrics and alerts  

---

## Tech Stack

- **React** for building UI components  
- **TypeScript** for type safety and maintainability  
- **Axios** (or fetch) for API requests  
- **React Router** for multi-page navigation (if needed)  
- **CSS / Tailwind / Chakra UI** (your choice for styling)  

---

## Folder Structure

frontend/
├── src/ # React application source code
│ ├── components/ # Reusable UI components
│ ├── pages/ # Pages / views
│ ├── services/ # API service calls
│ └── App.tsx # Root component
├── public/ # Static assets
├── package.json
├── tsconfig.json
└── README.md

---

## Setup Instructions

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
npm start
```
The app will run on `http://localhost:3000` and connect ot the backend API.

---

## Notes

- Designed to be **modular and scalable**
- Can be containerized with Docker for local or production deployment
- Integrates with the Log Service backend via REST APIs
- Future improvements: charts, metrics visualization, and alert notifications
