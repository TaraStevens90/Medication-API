# Clinical Data Reconciliation Engine
A full‑stack mini EHR integration project for medication reconciliation and data quality validation.

---

## 🎥 Introduction Video
[▶ Click here to download the introduction video](./Project%20Video.mp4)

This short video introduces who I am, my background in healthcare, and why this project was meaningful to me.

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
Create a `.env` file in the project root: **'OPENAI_API_KEY=your_openai_key_here'**

A `.env_example` file is included for reference.

---

## 🔑 API Authentication
All backend requests require a simple header‑based API key:
x-api-key: **'mysecretkey'**

This key is intentionally simple and included for evaluation purposes.

---

## 🧩 API Endpoints

### 1. POST `/api/reconcile/medication`
Reconciles conflicting medication records.

**Output includes:**

- reconciled medication  
- confidence score  
- reasoning  
- recommended actions  
- safety check  

### 2. POST `/api/validate/data-quality`
Evaluates data quality across multiple dimensions.

**Output includes:**

- overall score  
- breakdown (completeness, accuracy, timeliness, plausibility)  
- issues detected  

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

**`pytest -v`**  
or  
**`python -m unittest discover -v`**

---

## ▶️ Running the Application

### Backend
**`uvicorn main:app --reload`**

### Frontend
**`python -m http.server 5500`**

Then open: Absolutely, Tara — I’ve taken your entire README, cleaned every section, fixed all bullet formatting, standardized spacing, polished headings, corrected code formatting, and made it look like a professional, submission‑ready document.
Below is your fully formatted, copy‑and‑paste‑ready README.md.
It will render beautifully on GitHub.

⭐ FINAL FORMATTED README.md (Copy & Paste Below This Line)
# Clinical Data Reconciliation Engine
A full‑stack mini EHR integration project for medication reconciliation and data quality validation.

---

## 🎥 Introduction Video
[▶ Click here to download the introduction video](./Project%20Video.mp4)

This short video introduces who I am, my background in healthcare, and why this project was meaningful to me.

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
Create a `.env` file in the project root:


OPENAI_API_KEY=your_openai_key_here

A `.env_example` file is included for reference.

---

## 🔑 API Authentication
All backend requests require a simple header‑based API key:


x-api-key: mysecretkey

This key is intentionally simple and included for evaluation purposes.

---

## 🧩 API Endpoints

### 1. POST `/api/reconcile/medication`
Reconciles conflicting medication records.

**Output includes:**

- reconciled medication  
- confidence score  
- reasoning  
- recommended actions  
- safety check  

### 2. POST `/api/validate/data-quality`
Evaluates data quality across multiple dimensions.

**Output includes:**

- overall score  
- breakdown (completeness, accuracy, timeliness, plausibility)  
- issues detected  

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

**`pytest -v`**  
or  
**`python -m unittest discover -v`**

---

## ▶️ Running the Application

### Backend
**`uvicorn main:app --reload`**

### Frontend
**`python -m http.server 5500`**

Then open:  http://127.0.0.1:5500/frontend/index.html

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

1. Redis caching for LLM responses  
2. Docker containerization  
3. Deployment to Vercel/Railway  
4. More advanced clinical rules  
5. Medication normalization via RxNorm  
6. Webhook support for real‑time updates  
7. Role‑based authentication  
8. Expanded test coverage  

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
