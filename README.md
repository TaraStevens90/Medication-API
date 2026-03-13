## README.md — Clinical Data Reconciliation Engine
A full‑stack mini EHR integration project for medication reconciliation and data quality validation.

## Introduction Video
[▶Click here to download introduction video](./Project%20Video.mp4)

This short video introduces who I am, my background in healthcare, and why this project was meaningful to me.

## Overview
This project implements a clinical data reconciliation engine that resolves conflicting medication information across multiple healthcare systems. It uses a hybrid approach combining:
• 	deterministic scoring logic
• 	AI‑powered clinical reasoning
• 	data quality validation
• 	clinician‑friendly frontend visualization
The system ingests conflicting medication records, evaluates reliability, analyzes patient context, and produces a reconciled “most likely truth” with confidence scoring and human‑readable reasoning.
(This project was built as part of the Full Stack Developer – EHR Integration Intern Take‑Home Assessment.)

## Screenshots

### Clinical Reconciliation Dashboard
Frontend view of the clinician‑friendly dashboard used to visualize reconciled medication data.
![Clinical Reconciliation Dashboard](./Demo%20Screenshots/Clinical%20Reconciliation%20Dashboard.png)

### Data Quality Report
Frontend data quality validation results for a patient’s medication list.
![Data Quality Report](./Demo%20Screenshots/Data%20Quality%20Report.png)

### Swagger UI
Interactive API with endpoints.
![Swagger UI](./Demo%20Screenshots/Swagger%20UI.png)

### Reconcile Medication Endpoint
Example of the backend reconciliation endpoint in action.
![Reconcile Medication](./Demo%20Screenshots/Reconcile%20Medication.png)

### Validate Data Quality Endpoint
Example of the `/validate/data-quality` endpoint response.
![Validate Data Quality](./Demo%20Screenshots/Validate%20Data%20Quality.png)

### Passed Reconciliation Tests
All unit tests running successfully.
![Passed Reconciliation Tests](./Demo%20Screenshots/Passed%20Reconciliation%20Tests.png)

### Project Folder Layout
A quick look at the organized project structure.
![Folder Layout](./Demo%20Screenshots/Folder%20Layout.png)

## Features

Backend (FastAPI)
• 	Medication reconciliation with confidence scoring
• 	AI‑generated clinical reasoning
• 	Data quality validation with breakdown + issues
• 	Safety checks for implausible or dangerous data
• 	API key authentication
• 	20‑test regression suite (unit tests)
• 	Clean, modular architecture

Frontend (HTML/JS)
• 	Clinician‑friendly dashboard
• 	Reconciliation results display
• 	Data quality scoring with red/yellow/green indicators
• 	Confidence score visualization
• 	Approve/Reject suggestion interaction
• 	Clear reasoning and recommended actions

AI Integration
• 	OpenAI‑powered reasoning
• 	Implausible data detection
• 	Natural‑language explanations
• 	Prompt engineering with guardrails
• 	Error handling and fallback logic

## Architecture Overview
┌──────────────────────────┐
│        Frontend          │
│  HTML + JS Dashboard     │
│  - Displays results      │
│  - Approve/Reject UI     │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│         Backend          │
│        FastAPI           │
│  - Reconcile endpoint    │
│  - Data quality scoring  │
│  - Validation + errors   │
│  - API key auth          │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│      AI Reasoning        │
│      OpenAI API          │
│  - Clinical reasoning    │
│  - Safety checks         │
│  - Implausible data      │
└──────────────────────────┘

## Environment Variables
Create a file in the project root:   OPENAI_API_KEY=your_openai_key_here
A .env_example file is included for reference.

## API Authentication
All backend requests require a simple header‑based API key:
x-api-key:       mysecretkey
This key is intentionally simple and included for evaluation purposes.

## AI Integration & Prompt Engineering
OpenAI was chosen because it provides reliable structured reasoning, strong safety controls, and predictable JSON‑style outputs.
This project uses OpenAI to enhance deterministic logic with contextual clinical reasoning.
What the LLM does
• 	Explains reconciliation decisions
• 	Identifies implausible data
• 	Provides clinician‑friendly reasoning
• 	Suggests follow‑up actions
• 	Performs safety checks

Prompt Engineering Strategy
• 	Structured JSON input
• 	Explicit instructions
• 	Guardrails to reduce hallucinations
• 	Deterministic scaffolding (LLM only handles reasoning)
• 	Fallback responses on errors

Error Handling
• 	All API calls wrapped in try/except
• 	Graceful fallback if the LLM is unavailable
• 	Validation of returned fields

Caching (Design Decision)
Caching was not implemented due to low request volume.
With more time, Redis or in‑memory TTL caching would be added.

## API Endpoints
1️. POST /api/reconcile/medication
Reconciles conflicting medication records.
Input:

{
  "patient_context": {...},
  "sources": [...]
}

Output:
• 	reconciled medication
• 	confidence score
• 	reasoning
• 	recommended actions
• 	safety check

2️. POST /api/validate/data-quality
Evaluates data quality across multiple dimensions.
Output includes:
• 	overall score
• 	breakdown (completeness, accuracy, timeliness, plausibility)
• 	issues detected

## Additional Endpoints (Bonus Features)
These are not required by the assignment but included to enhance usability:
•  /api/reconcile/medication/by-id
•  /api/patient/{patient_id}/medications
•  /api/patient/{patient_id}/reconcile
These endpoints support dataset exploration and patient‑specific workflows.

## Testing
This project includes 20 unit tests covering:
•  medication normalization
•  scoring logic
•  conflict detection
•  data quality evaluation
•  safety checks
•  endpoint behavior

Run tests with:   pytest -v   or   python -m unittest discover -v

## Running the Application
Backend use command:         uvicorn main:app --reload

Frontend use command:        python -m http.server 5500
Then open index.html in your browser with:  http://127.0.0.1:5500/frontend/index.html
The frontend communicates with the backend via fetch requests.

## Key Design Decisions
• Hybrid AI + deterministic logic
    LLM handles reasoning; backend handles scoring and validation.
• Simple API key auth
    Lightweight and appropriate for a take‑home project.
• No database
    In‑memory data keeps the project simple and focused.
• Modular architecture
    Separation of concerns:
        • models
        • services
        • utils
        • routes
        • tests
• Clinician‑friendly UI
    Prioritized clarity over design complexity.

## Future Improvements
With additional time, I would expand the project in the following areas to increase performance, reliability, and clinical realism:
1. Redis Caching for LLM Responses
Caching previous AI responses would reduce repeated calls to the LLM when the same patient data is reconciled multiple times. 
This improves speed and reduces API usage.

2. Docker Containerization
Packaging the backend and frontend into Docker containers would make the application easier to deploy and run consistently across environments.

3. Deployment to Vercel/Railway
Hosting the frontend and backend on lightweight cloud platforms would allow reviewers to interact with the system live without running it locally.

4. More Advanced Clinical Rules
The current logic is intentionally simple. With more time, I would add deeper clinical rules such as drug–disease interactions, renal dosing adjustments, and allergy cross-checking.

5. Medication Name Normalization (RxNorm)
Different systems describe medications differently. Integrating RxNorm would standardize medication names and strengths to improve matching accuracy.

6. Webhook Support for Real-Time Updates
Webhooks would allow external systems (like pharmacies or clinics) to notify the engine when new data arrives, triggering automatic reconciliation.

7. Role-Based Authentication
Adding user roles (clinician, pharmacist, admin) would make the system more secure and more aligned with real healthcare environments.

8. Expanded Test Coverage
Although the project already includes 20 unit tests, I would add integration tests and more edge-case scenarios to further strengthen reliability.

## Time Spent
Approximately 24 hours.

## Test Data
Synthetic EHR data is included in the repository for evaluation.

## Final Notes
This project demonstrates:
• full‑stack development
• clinical data reasoning
• AI integration
• clean architecture
• strong testing discipline
• user‑friendly design
It is built to be clear, maintainable, and easy for evaluators to run.
