# Clinical Data Reconciliation Engine
A full‑stack mini EHR integration project for medication reconciliation and data quality validation.

---

## 🎥 Introduction Video
[▶ Click here to download the introduction video](./Project%20Video.mp4)

This short video introduces who I am, my background in healthcare, and why this project was meaningful to me.

## Medication API Demo Video
[▶ Click here to download the introduction video](./Medication_API_Demo.mp4)

This demo shows part of the script, the Swagger interface, how the endpoints work, and a walkthrough of all the buttons and features in the front‑end.

---

## 📌 Overview
This project implements a clinical data reconciliation engine that resolves conflicting medication information across multiple healthcare systems. It uses a hybrid approach combining:

- deterministic scoring logic  
- AI‑powered clinical reasoning  
- data quality validation  
- clinician‑friendly frontend visualization  

The system ingests conflicting medication records, evaluates reliability, analyzes patient context, and produces a reconciled “most likely truth” with confidence scoring and human‑readable reasoning.

*(This project was built as part of the Full Stack Developer – EHR Integration Intern Take‑Home Assessment.)*

---

## 🖼️ Screenshots

### Clinical Reconciliation Dashboard
![Clinical Reconciliation Dashboard](./Demo%20Screenshots/Clinical%20Reconciliation%20Dashboard.png)

### Data Quality Report
![Data Quality Report](./Demo%20Screenshots/Data%20Quality%20Report.png)

### Swagger UI
![Swagger UI](./Demo%20Screenshots/Swagger%20UI.png)

### Reconcile Medication Endpoint
![Reconcile Medication](./Demo%20Screenshots/Reconcile%20Medication.png)

### Validate Data Quality Endpoint
![Validate Data Quality](./Demo%20Screenshots/Validate%20Data%20Quality.png)

### Passed Reconciliation Tests
![Passed Reconciliation Tests](./Demo%20Screenshots/Passed%20Reconciliation%20Tests.png)

### Project Folder Layout
![Folder Layout](./Demo%20Screenshots/Folder%20Layout.png)

---

## 🚀 Features

### Backend (FastAPI)

- Medication reconciliation with confidence scoring  
- AI‑generated clinical reasoning  
- Data quality validation with breakdown + issues  
- Safety checks for implausible or dangerous data  
- API key authentication  
- 20‑test regression suite (unit tests)  
- Clean, modular architecture  

### Frontend (HTML/JS)

- Clinician‑friendly dashboard  
- Reconciliation results display  
- Data quality scoring with red/yellow/green indicators  
- Confidence score visualization  
- Approve/Reject suggestion interaction  
- Clear reasoning and recommended actions  

### AI Integration

- OpenAI‑powered reasoning  
- Implausible data detection  
- Natural‑language explanations  
- Prompt engineering with guardrails  
- Error handling and fallback logic  

---

## 🧠 AI Integration & Prompt Engineering

### What the LLM Does

- Explains reconciliation decisions  
- Identifies implausible data  
- Provides clinician‑friendly reasoning  
- Suggests follow‑up actions  
- Performs safety checks  

### Prompt Engineering Strategy

- Structured JSON input  
- Explicit instructions  
- Guardrails to reduce hallucinations  
- Deterministic scaffolding (LLM only handles reasoning)  
- Fallback responses on errors  

### Error Handling

- All API calls wrapped in try/except  
- Graceful fallback if the LLM is unavailable  
- Validation of returned fields  

---

## 🔐 Environment Variables
Create a `.env` file in the project root: **OPENAI_API_KEY=your_openai_key_here**

A `.env_example` file is included for reference.

---

## 🔑 API Authentication
All backend requests require a simple header‑based API key:
x-api-key: **mysecretkey**

This key is intentionally simple and included for evaluation purposes.

---

## 🧩 API Endpoints

### 1. POST /api/reconcile/medication
Reconciles conflicting medication records.

### Sample Input
```json
{
  "sources": [
    {
      "system": "A",
      "medication": "Metformin 500mg",
      "source_reliability": "high",
      "last_updated": "2026-03-01",
      "last_filled": "2026-02-28"
    },
    {
      "system": "B",
      "medication": "Metformin 500mg",
      "source_reliability": "medium",
      "last_updated": "2026-02-15",
      "last_filled": "2026-02-14"
    },
    {
      "system": "C",
      "medication": "Lisinopril 20mg",
      "source_reliability": "low",
      "last_updated": "2025-12-01",
      "last_filled": "2025-12-01"
    }
  ]
}
```

**Output includes:**

- reconciled medication  
- confidence score  
- reasoning  
- recommended actions  
- safety check

### Sample Output
```json
{
  "all_medications": [
    {
      "system": "A",
      "medication": "Metformin 500mg",
      "last_updated": "2026-03-01",
      "last_filled": "2026-02-28",
      "source_reliability": "high"
    },
    {
      "system": "B",
      "medication": "Metformin 500mg",
      "last_updated": "2026-02-15",
      "last_filled": "2026-02-14",
      "source_reliability": "medium"
    },
    {
      "system": "C",
      "medication": "Lisinopril 20mg",
      "last_updated": "2025-12-01",
      "last_filled": "2025-12-01",
      "source_reliability": "low"
    }
  ],
  "reconciled_medication": {
    "truth": "Metformin 500mg",
    "confidence": 0.74,
    "reasoning": "The reconciled medication, Metformin 500mg, is the most likely correct choice due to its high reliability from source A, which was last updated on March 1, 2026, indicating it reflects the most current information. Additionally, both sources A and B confirm the same dosage of Metformin, providing consistency across reliable sources, while the lower reliability and older update of source C for Lisinopril diminishes its credibility in this context.",
    "recommended_actions": [
      "Verify with sources that Metformin 500mg is correct"
    ],
    "clinical_safety_check": "WARNING",
    "safety_reason": "Duplicate medications detected across sources; Multiple dosage variants of the same medication detected"
  }
}
```

### 2. POST /api/validate/data-quality
Evaluates data quality across multiple dimensions.

### Sample Input:
```JSON
{
  "system": "Epic",
  "medication": "Metformin 500mg",
  "source_reliability": "high",
  "last_updated": "2026-01-02",
  "last_filled": null
}
```

**Output includes:**

- overall score  
- breakdown (completeness, accuracy, timeliness, plausibility)  
- issues detected

```JSON
{
  "overall_score": 71,
  "breakdown": {
    "completeness": 60,
    "accuracy": 100,
    "timeliness": 100,
    "clinical_plausibility": 100,
    "consistency": 100,
    "conflict_severity": 0,
    "medication_diversity": 40
  },
  "issues_detected": [
    {
      "field": "allergies",
      "issue": "No allergies documented - likely incomplete",
      "severity": "medium"
    },
    {
      "field": "medications",
      "issue": "No medications listed",
      "severity": "high"
    }
  ]
}
```

---

## ➕ Additional Endpoints (Bonus Features)

- `/api/reconcile/medication/by-id`  
- `/api/patient/{patient_id}/medications`  
- `/api/patient/{patient_id}/reconcile`  

These endpoints support dataset exploration and patient‑specific workflows.

---

## 🧪 Testing

This project includes 20 unit tests covering:

- medication normalization  
- scoring logic  
- conflict detection  
- data quality evaluation  
- safety checks  
- endpoint behavior  

Run tests with:

**pytest -v**  
or  
**python -m unittest discover -v**

---

## ▶️ Running the Application

### Backend
**uvicorn main:app --reload**

### Frontend
**python -m http.server 5500**

Then open: http://127.0.0.1:5500/frontend/index.html


The frontend communicates with the backend via fetch requests.

---

## 🏗️ Key Design Decisions

- **Hybrid AI + deterministic logic**  
  LLM handles reasoning; backend handles scoring and validation.

- **Simple API key auth**  
  Lightweight and appropriate for a take‑home project.

- **No database**  
  In‑memory data keeps the project simple and focused.

- **Modular architecture**  
  Separation of concerns across models, services, utils, routes, and tests.

- **Clinician‑friendly UI**  
  Prioritized clarity over design complexity.

---

## 🔮 Future Improvements

With additional time, I would expand the project in the following areas to increase performance, reliability, and clinical realism. Each improvement is chosen to address a real limitation or scalability concern in the current design.

### 1. Redis Caching for LLM Responses
Right now, every reconciliation request triggers a new LLM call, even when the same patient data is processed repeatedly. LLM calls are the slowest and most expensive part of the system.

**Why this matters:**
- Reduces repeated LLM calls for identical inputs  
- Improves response time and user experience  
- Lowers API usage costs  
- Makes the system more scalable under load  

**Trade‑off:**  
Requires cache invalidation logic when patient data changes.

---

### 2. Docker Containerization
The backend and frontend currently require manual setup. Docker would package them into reproducible containers.

**Why this matters:**
- Ensures consistent environments across machines  
- Simplifies onboarding for reviewers or teammates  
- Enables one‑command startup for the entire stack  
- Prepares the project for cloud deployment  

**Trade‑off:**  
Adds initial setup complexity but pays off in deployment reliability.

---

### 3. Deployment to Vercel or Railway
The project currently runs locally only. Deploying it would allow reviewers to interact with the system instantly in a browser.

**Why this matters:**
- Zero‑setup demo experience  
- More realistic “production‑like” environment  
- Easier sharing with stakeholders  
- Demonstrates deployment skills  

**Trade‑off:**  
Requires configuring environment variables, CORS, and rate‑limiting for the LLM.

---

### 4. More Advanced Clinical Rules
The current logic is intentionally simple to keep the project focused. Real EHR systems use complex rule engines.

**Why this matters:**
- Increases clinical realism  
- Reduces reliance on the LLM for basic checks  
- Improves safety and accuracy  
- Supports more nuanced medication decisions  

Examples of rules to add:
- Drug–disease interactions  
- Renal dosing adjustments  
- Allergy cross‑checking  

**Trade‑off:**  
More rules require more maintenance and more extensive testing.

---

### 5. Medication Name Normalization (RxNorm)
Different systems describe medications differently (e.g., “Metoprolol Tartrate 25mg” vs “Metoprolol 25 mg tablet”). Without normalization, matching accuracy is limited.

**Why this matters:**
- Standardizes medication names and strengths  
- Improves matching across sources  
- Increases reconciliation accuracy  
- Aligns with real‑world EHR practices  

**Trade‑off:**  
Requires integrating external APIs or maintaining local datasets.

---

### 6. Webhook Support for Real‑Time Updates
The system currently reconciles only when manually triggered. Real EHR systems react to new data automatically.

**Why this matters:**
- Enables real‑time medication updates  
- Supports event‑driven workflows  
- Makes the system more clinically realistic  
- Reduces manual refreshes or polling  

**Trade‑off:**  
Requires secure endpoints and event‑handling logic.

---

### 7. Role‑Based Authentication
The current API key is intentionally simple for evaluation. Real systems require different permissions for clinicians, pharmacists, and admins.

**Why this matters:**
- Improves security  
- Supports more realistic user workflows  
- Allows restricting sensitive actions  
- Enables auditability and accountability  

**Trade‑off:**  
Adds complexity to authentication and user management.

---

### 8. Expanded Test Coverage
The project already includes 20 unit tests, but as the system grows, more tests are needed to prevent regressions.

**Why this matters:**
- Increases reliability  
- Provides confidence during refactoring  
- Covers more edge cases  
- Strengthens long‑term maintainability  

**Trade‑off:**  
More tests require ongoing maintenance as logic evolves.

---

## 🧪 Test Data
Synthetic EHR data is included in the repository for evaluation.

---

## 📝 Final Notes
This project demonstrates:

- full‑stack development  
- clinical data reasoning  
- AI integration  
- clean architecture  
- strong testing discipline  
- user‑friendly design  

It is built to be clear, maintainable, and easy for evaluators to run.

---

## ⏱️ Time Spent
Approximately 24 hours.

