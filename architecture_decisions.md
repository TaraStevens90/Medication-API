# Architecture Decisions
This document summarizes the key technical decisions made while building the Clinical Data Reconciliation Engine and the reasoning behind each choice.


## 1. FastAPI for the Backend
FastAPI was chosen because it provides:
- High performance and async support
- Automatic OpenAPI/Swagger documentation
- Easy request validation with Pydantic
- Clean, modular routing structure

(This allowed rapid development of a reliable, well‑structured API.)


## 2. Hybrid Deterministic + AI Reasoning
The reconciliation engine uses deterministic scoring for:
- Source reliability
- Recency
- Consistency across systems

The LLM is used only for:
- Clinical reasoning
- Implausible data detection
- Human‑readable explanations

This separation ensures:
- Predictable logic
- Reduced hallucination risk
- Clear guardrails around AI behavior


## 3. No Database (In‑Memory Storage)
A database was intentionally omitted because:
- The assignment focuses on logic, not persistence
- In‑memory data keeps the project lightweight
- It simplifies setup for reviewers

(If expanded, the system could integrate SQLite, PostgreSQL, or FHIR servers.)


## 4. Simple API Key Authentication
A lightweight header‑based API key was used because:
- It meets the assignment requirement
- It avoids unnecessary complexity
- It keeps the project easy to run locally

(In a real system, OAuth2 or role‑based access would be used.)


## 5. Frontend: HTML + Vanilla JavaScript
A simple frontend was chosen to prioritize:
- Clarity over design complexity
- Easy reviewer access (no build tools)
- Direct communication with the backend via fetch()

(The UI focuses on ease of use and readability for clinicians.)


## 6. Prompt Engineering Strategy
Prompts were designed with:
- Structured JSON input
- Explicit instructions
- Guardrails to reduce hallucinations
- Deterministic scaffolding (LLM only handles reasoning)

(This ensures stable, predictable outputs.)


## 7. Error Handling & Fallback Logic
All LLM calls are wrapped in try/except blocks to:
- Prevent crashes
- Provide fallback reasoning
- Maintain API reliability even if the LLM fails

(This improves robustness and user trust.)


## 8. Testing Strategy
20 unit tests were included to cover:
- Medication normalization
- Scoring logic
- Conflict detection
- Data quality evaluation
- Safety checks
- Endpoint behavior

(This exceeds the minimum requirement of assessment and ensures reliability for a small project like this)


## 9. No Caching (Intentional Trade‑Off)
Caching was not implemented because:
- The project has low request volume
- Simplicity was prioritized
- API usage is minimal for evaluation

(With more time, Redis or in‑memory TTL caching would be added, as was a optional bonus for assessment.)


## 10. Project Structure
The project is organized into:
- `routes/` for API endpoints
- `services/` for business logic
- `utils/` for helpers
- `unit_tests/` for test coverage
- `frontend/` for the dashboard

(This separation of concerns improves maintainability and readability.)


## Summary
The architecture prioritizes:
- Clarity
- Reliability
- Clinical readability
- Strong testing discipline
- Safe and controlled AI integration

These decisions ensure the project is easy to review, easy to run, and aligned with real‑world EHR integration patterns.