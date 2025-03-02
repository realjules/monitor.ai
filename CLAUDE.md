# ML Platform Development Guide

## Build & Run Commands
- Python API services: `docker-compose up [service-name]`
- Frontend: `cd services/frontend && npm run dev`
- Build frontend: `cd services/frontend && npm run build`
- Lint frontend: `cd services/frontend && npm run lint`
- Run single test: No test command found, need to implement testing

## Code Style Guidelines
- Python: Follow PEP 8 conventions with 4-space indentation
- TypeScript/React: 
  - Use TypeScript with strict typing (no 'any' unless necessary)
  - Functional components with React hooks preferred
  - Use ESM imports (import/export syntax)
  - Group imports: React first, then external libraries, then internal components/utils

## Error Handling
- Python: Use try/except blocks for expected errors, raise specific exceptions
- Frontend: Use error boundaries and proper async/await error handling

## Naming Conventions
- Python: snake_case for variables/functions, PascalCase for classes
- TypeScript: camelCase for variables/functions, PascalCase for components/classes
- Files: Descriptive names reflecting purpose, not implementation

## Project Structure
- Core services in `/core` directory
- Frontend in `/services/frontend`
- Infrastructure config in `/infrastructure`
- Docker compose for local development