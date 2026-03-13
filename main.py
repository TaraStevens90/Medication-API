""" Mini Clinical Data Reconciliation Engine
This FastAPI service simulates a clinical decision support system used in modern Electronic Health Records (EHRs).

The system reconciles conflicting medication records coming from multiple healthcare systems such as:
• Hospital EHR
• Pharmacy systems
• Patient portals
• Insurance data feeds

As healthcare data is often inconsistent, the system determines the most likely correct medication using:
1. Source reliability weighting
2. Recency of updates
3. Agreement across multiple systems
4. AI generated clinical reasoning

The API returns:
• reconciled medication ("truth")
• confidence score
• AI reasoning explanation
• recommended verification actions
• clinical safety check

The goal is to simulate how real clinical data platforms detect and resolve conflicting patient medication records.

Prepared by Tara Stevens """

# Standard Library Imports
import os
import logging
from datetime import datetime
from typing import Any, List, Dict, Optional, Tuple

# Third-Party Library Imports
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Local Application Imports
from test_db import test_db

# Logging Configuration
# Logging is used instead of print statements to provide structured debugging and monitoring. In production systems,
# logs help track API usage, system errors, and clinical reconciliation decisions.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Environment Configuration
# Load environment variables such as the API key from a .env file.
# This prevents sensitive credentials from being hard-coded.
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# OpenAI Client Initialization
# The AI client is used to generate clinical reasoning explanations for reconciliation decisions. 
# If the OpenAI package is not installed, the system falls back to rule-based reasoning.
try:
    from openai import OpenAI
    client = OpenAI(api_key=openai_key)
except ImportError:
    logger.warning("OpenAI SDK not installed — AI reasoning disabled.")
    client = None

# API Key Authentication
# Simple header-based API key authentication.
# In production healthcare systems, this ensures that only authorized clients can access patient data.
API_KEY = API_KEY = os.getenv("API_KEY", "mysecretkey")  # Default only for dev/testing

def api_key_auth(x_api_key: str = Header(...)):
    """
    Validates the provided API key against the server's secret.

    Args:
        x_api_key (str): API key provided in request headers.

    Raises:
        HTTPException: 401 Unauthorized if the key is invalid.
    """
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# FastAPI Application Initialization
app = FastAPI(
title="Mini Clinical Data Reconciliation Engine",
description="""
A simulated clinical decision support system for resolving conflicting medication records across healthcare systems.

### **Data Sources Included**
- Electronic Health Records (EHR)
- Pharmacy systems
- Patient portals
- Insurance claims systems

### **Key Capabilities**
- Medication reconciliation
- Confidence scoring
- AI-generated clinical reasoning
- Clinical safety validation
- Healthcare data quality scoring

This project simulates core functions used in real healthcare interoperability and clinical decision support platforms.
""",
version="1.0"
)

# Middleware Configuration
# CORS middleware allows requests from different origins. 
# # Best practice in roduction is to restrict `allow_origins` to trusted domains only.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI Response Cache
# Stores previously generated AI explanations to:
#   • Reduce API costs
#   • Improve performance
#   • Avoid hitting API rate limits
# Cache key format: medication + patient context + sources
ai_cache = {}

# Pydantic Models
# These define the data structures used for input validation, API responses, and internal calculations. 
# Using Pydantic ensures type safety, automatic validation, and serialization.

# Medication Models
class MedicationSource(BaseModel):
    """Represents a single source reporting a patient's medication."""
    system: str
    medication: str
    last_updated: Optional[str] = None
    last_filled: Optional[str] = None
    source_reliability: Optional[str] = "medium"

class MedicationSourceOutput(BaseModel):
    """Output representation of a medication source for API responses."""
    system: str
    medication: str
    last_updated: Optional[str] = None
    last_filled: Optional[str] = None
    source_reliability: Optional[str] = "medium"

class ReconcileInput(BaseModel):
    """Input structure for medication reconciliation API."""
    patient_context: Optional['PatientContext'] = None
    sources: List[MedicationSource]

class ReconciliationResult(BaseModel):
    """Core result of a reconciliation process."""
    truth: str
    confidence: float
    reasoning: str
    recommended_actions: List[str]
    clinical_safety_check: str
    safety_reason: Optional[str] = None

class MedicationReconciliationResponse(BaseModel):
    """Full reconciliation response including all sources and the reconciled result."""
    all_medications: List[MedicationSourceOutput]
    reconciled_medication: ReconciliationResult

# Patient Models
class PatientContext(BaseModel):
    """Contextual patient information to assist AI reasoning."""
    age: int
    conditions: List[str] = Field(default_factory=list)
    recent_labs: Optional[Dict[str, float]] = None

class PatientRecord(BaseModel):
    """Represents a patient's complete medical record."""
    demographics: Dict[str, Any] = Field(default_factory=dict)
    medications: List[str] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)
    conditions: List[str] = Field(default_factory=list)
    vital_signs: Dict[str, Any] = Field(default_factory=dict)
    last_updated: Optional[str] = None
    
class DataQualityOutput(BaseModel):
    """Output of data quality assessment for a patient record."""
    completeness: int
    accuracy: int
    timeliness: int
    clinical_plausibility: int
    consistency: int
    conflict_severity: int
    medication_diversity: int

class DataQualityResponse(BaseModel):
    overall_score: int
    breakdown: DataQualityOutput
    issues_detected: List[Dict[str, str]]

class PatientIDInput(BaseModel):
    """Input structure for APIs that require a patient ID."""
    patient_id: str

# Helper Functions and Constants
# These functions simulate key logic used in clinical data reconciliation systems: 
# parsing dates, normalizing medication, names, and calculating confidence scores.

# Date Parsing
def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Safely parse a date string in YYYY-MM-DD format."""

    if not date_str:
        return None

    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

# System Reliability
# Trust levels used for scoring medication sources.
SYSTEM_RELIABILITY: Dict[str, str] = {
    "EHR": "high",
    "PHARMACY": "high",
    "INSURANCE": "medium",
    "PATIENT_PORTAL": "low",
    "Unknown": "medium"
}

# Medication Normalization
def normalize_medication_name(med_name: str) -> str:
    """
    Standardize a medication name by lowercasing and removing spaces.

    Args:
        med_name (str): Raw medication name from the source.

    Returns:
        str: Normalized string for consistent comparison.
    """
    return med_name.strip().lower().replace(" ", "")

# Confidence Calculation
def calculate_confidence(meds_list: List[MedicationSource]) -> Tuple[str, float]:
    """
    Determine the most likely correct medication and compute a confidence score.

    Algorithm:
        1. Assign points based on source reliability:
               high   = 3
               medium = 2
               low    = 1
        2. Add a recency bonus (+1) if last updated/fill < 30 days.
        3. Normalize medication names for consistent scoring.
        4. Select the medication with the highest total score.
        5. Convert the score into a relative confidence value.

    Args:
        meds_list (List[MedicationSource]): Medication entries from different sources.

    Returns:
        Tuple[str, float]: Most likely medication name and confidence (0 to 1).
    """
    weights = {"high": 4, "medium": 2, "low": 1}
    med_scores: Dict[str, int] = {}

    for s in meds_list:
        if s.medication.strip().lower() == "none":
            continue

        # Determine reliability
        reliability = s.source_reliability or SYSTEM_RELIABILITY.get(s.system, "medium")
        score = weights.get(reliability.lower(), 2)

        # Recency bonus
        date_field = s.last_updated or s.last_filled
        if date_field:
            parsed = parse_date(date_field)
            if parsed:
                delta = (datetime.now() - parsed).days
                if delta < 30:
                    score += 1

        # Normalize medication for consistent scoring
        normalized_med = normalize_medication_name(s.medication)
        med_scores[normalized_med] = med_scores.get(normalized_med, 0) + score

    if not med_scores:
        return "Unknown", 0.0

    # Identify top-scoring medication
    top_med_normalized = max(
    med_scores,
    key=lambda m: (
        med_scores[m],
        max(
            [
                parse_date(s.last_updated or s.last_filled) or datetime.min
                for s in meds_list
                if normalize_medication_name(s.medication) == m
            ],
            default=datetime.min,
        ),
    ),
)


    # Retrieve original medication name from sources
    top_med = next(
        s.medication for s in meds_list
        if normalize_medication_name(s.medication) == top_med_normalized
    )

    total_score = sum(med_scores.values())
    unique_meds = len(med_scores)

    # Penalize disagreement across sources
    if unique_meds > 1:
        disagreement_penalty = 0.15 * (unique_meds - 1)
    else:
        disagreement_penalty = 0

    confidence = (med_scores[top_med_normalized] / total_score) - disagreement_penalty
    confidence = max(confidence, 0)

    return top_med, round(confidence, 2)

def generate_ai_reasoning(
    patient_context: Optional[PatientContext],
    sources: List[MedicationSource],
    med: str
) -> str:
    """
    Generate AI-based clinical reasoning for a reconciled medication.

    Args:
        patient_context (Optional[PatientContext]):
            Patient data including age, conditions, and recent labs.
        sources (List[MedicationSource]):
            Medication entries from different systems, including reliability
            and timestamps.
        med (str):
            The medication determined to be the most likely correct result
            after reconciliation.

    Returns:
        str:
            A natural-language explanation describing why the selected
            medication is most likely correct, referencing reliability,
            recency, and agreement across systems.

    Notes:
        - Uses a simple in-memory cache placeholder to avoid repeated API calls
          for identical inputs (not fully implemented).
        - Falls back to a default reasoning string if the OpenAI client is
          unavailable.
        - Produces explainable output similar to clinician-style rationale.
    """

    # Fallback if OpenAI client is unavailable
    if client is None:
        logger.warning("OpenAI client not available. Using default reasoning fallback.")
        return "AI reasoning unavailable. Decision based on reliability and recency."

    logger.info("Generating AI reasoning for reconciliation result")
    logger.debug("Medication: %s", med)
    logger.debug("Sources: %s", sources)

    # Generate a cache key to prevent redundant API calls
    cache_key = f"{med}-{str(patient_context)}-{str(sources)}"
    if cache_key in ai_cache:
        logger.debug("Using cached AI reasoning")
        return ai_cache[cache_key]

    # Build patient context string for the prompt
    context_str = ""
    if patient_context:
        context_str = (
            f"Patient Age: {patient_context.age}\n"
            f"Conditions: {patient_context.conditions}\n"
            f"Recent Labs: {patient_context.recent_labs}"
        )

    # Build medication sources string for the prompt
    sources_str = "\n".join([
        f"{s.system}: {s.medication}, reliability={s.source_reliability}, "
        f"updated={s.last_updated or s.last_filled}"
        for s in sources
    ])

    # The AI is asked to justify the reconciliation decision using clinician-like criteria:
    #   • reliability of each data source
    #   • recency of medication updates
    #   • agreement across multiple systems
    # Produces explainable output rather than a black-box prediction.
    
    prompt = f"""You are a clinical decision support AI assisting with medication reconciliation.

    Patient Context:
    {context_str}

    Medication Sources:
    {sources_str}

    Reconciled Medication: {med}

    Explain why this medication is the most likely correct one. Respond in 2 to 3 sentences using clear, confident clinical language.
    Highlight reliability, recency, and consistency across sources."""

    try:
        # Modern OpenAI API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a clinical decision support AI."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=150
        )

        # Extract reasoning text
        reasoning = response.choices[0].message.content.strip()

        # Cache the result
        ai_cache[cache_key] = reasoning
        logger.debug("AI reasoning generated and cached")
        return reasoning

    except Exception as e:
        logger.warning("OpenAI reasoning failed: %s", repr(e))
        return "AI reasoning unavailable. Decision based on reliability and recency."

def detect_clinical_risks(medications: List[str]) -> str:
    """
    Detect potential clinical risks in a list of medications.

    Args:
        medications (List[str]):
            A list of medication names (including doses) from different sources.

    Returns:
        str:
            A summary of detected risks, or a message indicating that no major
            risks were found.

    Notes:
        - Checks for duplicate medications across sources.
        - Detects dosage conflicts (same drug, different strengths).
        - Can be extended to include allergy conflicts or drug–drug interactions.
        - Normalizes medication names to improve detection accuracy.
    """
    logger.info("Checking clinical risks for medications: %s", medications)
    risks = []

    # Normalize medications for consistent comparison
    normalized_meds = [m.lower() for m in medications]

    # Detect exact duplicates
    if len(normalized_meds) != len(set(normalized_meds)):
        risks.append("Duplicate medications detected across sources")
        logger.debug("Duplicate medications detected")

    # Detect dosage conflicts (same drug name, different dosages)
    # Assumes first word is drug name; can be enhanced with proper parsing
    drug_names = [m.split()[0].lower() for m in medications]
    if len(drug_names) != len(set(drug_names)):
        risks.append("Multiple dosage variants of the same medication detected")
        logger.debug("Dosage conflicts detected for: %s", set([d for d in drug_names if drug_names.count(d) > 1]))

    if not risks:
        logger.info("No major medication risks detected")
        return "No major medication risks detected"

    risk_summary = "; ".join(risks)
    logger.info("Clinical risks detected: %s", risk_summary)
    return risk_summary

@app.post(
    "/api/reconcile/medication",
    response_model=MedicationReconciliationResponse,
    dependencies=[Depends(api_key_auth)],
    summary="Reconcile medication records from multiple systems",
    description="""
Analyzes conflicting medication records from different healthcare sources and determines the most likely correct medication.

### Reconciliation Algorithm Considers:
- Source reliability
- Recency of updates
- Agreement across systems

### AI Reasoning
An AI model then generates a clinical explanation describing why the selected medication is most likely correct.
"""
)
def reconcile_medications(input_data: ReconcileInput) -> MedicationReconciliationResponse:
    """Reconcile medication records using reliability, recency, and AI reasoning."""

    # Compute reconciled medication and confidence
    med, confidence = calculate_confidence(input_data.sources)

    # Generate AI reasoning
    reasoning = generate_ai_reasoning(input_data.patient_context, input_data.sources, med)

    # Recommended actions for clinicians
    actions = [f"Verify with sources that {med} is correct"]

    # Detect potential clinical risks
    meds_list = [s.medication for s in input_data.sources if s.medication.lower() != "none"]
    risk_message = detect_clinical_risks(meds_list)

    # Determine clinical safety status
    clinical_check = "PASSED"
    if med.lower() == "none":
        clinical_check = "FAILED"
    elif "Duplicate" in risk_message or "dosage" in risk_message:
        clinical_check = "WARNING"

    # Convert sources to output model
    sources_output = [
        MedicationSourceOutput(
            system=s.system,
            medication=s.medication,
            last_updated=s.last_updated,
            last_filled=s.last_filled,
            source_reliability=s.source_reliability
        )
        for s in input_data.sources
    ]

    logger.info(
        "Medication reconciliation completed: %s, Confidence: %.2f, Risk: %s",
        med, confidence, clinical_check
    )

    # Return full response including all sources and reconciled result
    return MedicationReconciliationResponse(
        all_medications=sources_output,
        reconciled_medication=ReconciliationResult(
            truth=med,
            confidence=confidence,
            reasoning=reasoning,
            recommended_actions=actions,
            clinical_safety_check=clinical_check,
            safety_reason=risk_message
        )
    )

@app.post(
    "/api/reconcile/medication/by-id",
    response_model=MedicationReconciliationResponse,
    dependencies=[Depends(api_key_auth)],
    summary="Reconcile medications for a specific patient",
    description="""
Retrieves medication records for a patient and determines the most likely accurate medication across multiple sources.

### How it works
- Fetches all medication entries for the given patient ID
- Identifies the most common medication across sources
- Calculates a confidence score based on agreement
- Generates AI reasoning to explain the selection
- Performs a clinical safety check for duplicates or dosage conflicts
"""
)
def reconcile_by_patient_id(input_data: PatientIDInput) -> MedicationReconciliationResponse:
    """Reconcile medications for a specific patient by ID."""
    logger.info("Reconciling medications for patient ID: %s", input_data.patient_id)
    patient = test_db.get(input_data.patient_id)

    if not patient:
        logger.warning("Patient ID %s not found", input_data.patient_id)
        return MedicationReconciliationResponse(
            all_medications=[],
            reconciled_medication=ReconciliationResult(
                truth="Unknown",
                confidence=0.0,
                reasoning="Patient not found",
                recommended_actions=[],
                clinical_safety_check="FAILED",
                safety_reason=None
            )
        )

    records = patient.get("medications", [])

    # Safely convert records to MedicationSource objects
    sources = []
    for r in records:
        if isinstance(r, dict):
            sources.append(MedicationSource(
                system=r.get("system", "Unknown"),
                medication=r.get("medication", "Unknown"),
                last_updated=r.get("last_updated"),
                last_filled=r.get("last_filled"),
                source_reliability=r.get("source_reliability", "medium")
        ))
        elif isinstance(r, str) and r.lower() != "none":
            sources.append(MedicationSource(
                system="Unknown",
                medication=r,
                last_updated=None,
                last_filled=None,
                source_reliability="medium"
        ))

    if not sources:
        logger.warning("No valid medications found for patient ID %s", input_data.patient_id)
        return MedicationReconciliationResponse(
            all_medications=[],
            reconciled_medication=ReconciliationResult(
                truth="None",
                confidence=0.0,
                reasoning="No valid medications found",
                recommended_actions=[],
                clinical_safety_check="FAILED",
                safety_reason=None
            )
        )

    # Main reconciliation logic
    med, confidence = calculate_confidence(sources)
    reasoning = generate_ai_reasoning(None, sources, med)
    actions = [f"Verify with sources that {med} is correct"]

    meds_list = [s.medication for s in sources if s.medication.lower() != "none"]
    risk_message = detect_clinical_risks(meds_list)

    clinical_check = "PASSED"
    if med.lower() == "none":
        clinical_check = "FAILED"
    elif "Duplicate" in risk_message or "dosage" in risk_message:
        clinical_check = "WARNING"

    # Convert sources to output model
    sources_output = [
        MedicationSourceOutput(
            system=s.system,
            medication=s.medication,
            last_updated=s.last_updated,
            last_filled=s.last_filled,
            source_reliability=s.source_reliability
        )
        for s in sources
    ]

    logger.info(
        "Medication reconciliation completed for patient ID %s: %s, Confidence: %.2f, Risk: %s",
        input_data.patient_id, med, confidence, clinical_check
    )

    return MedicationReconciliationResponse(
        all_medications=sources_output,
        reconciled_medication=ReconciliationResult(
            truth=med,
            confidence=round(confidence, 2),
            reasoning=reasoning,
            recommended_actions=actions,
            clinical_safety_check=clinical_check,
            safety_reason=risk_message
        )
    )


# Helper: reconcile a plain list of records
def reconcile_medication_records(records: List[Dict[str, str]]) -> MedicationReconciliationResponse:
    """Reconciles a list of medication records and evaluates clinical risk."""
    sources = [MedicationSource(**r) for r in records if r.get("medication", "").lower() != "none"]

    if not sources:
        return MedicationReconciliationResponse(
            all_medications=[],
            reconciled_medication=ReconciliationResult(
                truth="None",
                confidence=0.0,
                reasoning="No valid medications found",
                recommended_actions=[],
                clinical_safety_check="FAILED",
                safety_reason=None
            )
        )

    return reconcile_medications(ReconcileInput(patient_context=None, sources=sources))

# Get all medications for a specific patient
@app.get(
    "/api/patient/{patient_id}/medications",
    response_model=List[Dict],
    dependencies=[Depends(api_key_auth)],
    summary="Retrieve all medication records for a patient",
    description="""
Returns all stored medication records for a specific patient.

### What this endpoint does
- Looks up the patient in the test database
- Retrieves all medication entries associated with the patient ID
- Returns the raw medication list exactly as stored
- Does **not** perform reconciliation or AI reasoning

### When to use this endpoint
Use this GET endpoint when you want to view a patient's medication history **without** running the reconciliation engine.
"""
)
def get_patient_medications(patient_id: str):
    patient = test_db.get(patient_id)
    return patient.get("medications", [])


@app.get(
    "/api/patient/{patient_id}/reconcile",
    response_model=MedicationReconciliationResponse,
    dependencies=[Depends(api_key_auth)],
    summary="Reconcile medications for a patient (GET)",
    description="""
Retrieves a patient's stored medication records and performs reconciliation.

### What this endpoint does
- Looks up the patient in the test database
- Retrieves all medication entries associated with the patient ID
- Runs the reconciliation engine on the stored records
- Returns the most likely correct medication, confidence score, AI reasoning, and safety checks

### When to use this endpoint
Use this GET endpoint when you want to reconcile medications **based on data already stored** for a patient, without sending a request body.
"""
)
def reconcile_patient(patient_id: str) -> MedicationReconciliationResponse:
    patient = test_db.get(patient_id)

    if not patient:
        return MedicationReconciliationResponse(
            all_medications=[],
            reconciled_medication=ReconciliationResult(
                truth="Unknown",
                confidence=0.0,
                reasoning="Patient not found",
                recommended_actions=[],
                clinical_safety_check="FAILED",
                safety_reason=None
            )
        )

    records = patient.get("medications", [])

    # Safely convert records to MedicationSource objects
    sources = []
    for r in records:
        if isinstance(r, dict):
            sources.append(MedicationSource(
                system=r.get("system", "Unknown"),
                medication=r.get("medication", "none"),
                last_updated=r.get("last_updated"),
                last_filled=r.get("last_filled"),
                source_reliability=r.get("source_reliability", "medium")
            ))
        elif isinstance(r, str) and r.lower() != "none":
            sources.append(MedicationSource(system="Unknown", medication=r))

    # Filter out invalid "none" medications
    sources = [s for s in sources if s.medication.lower() != "none"]

    if not sources:
        return MedicationReconciliationResponse(
            all_medications=[],
            reconciled_medication=ReconciliationResult(
                truth="None",
                confidence=0.0,
                reasoning="No valid medications found",
                recommended_actions=[],
                clinical_safety_check="FAILED",
                safety_reason=None
            )
        )

    # Reuse the main reconciliation logic
    return reconcile_medications(ReconcileInput(patient_context=None, sources=sources))

# Data Quality Validation Engine
# Evaluates the reliability and completeness of a patient clinical record.
# This simulates real-world data quality monitoring used in healthcare interoperability platforms.

@app.post(
    "/api/validate/data-quality",
    response_model=DataQualityResponse,
    dependencies=[Depends(api_key_auth)],
    summary="Evaluate healthcare data quality",
    description="""
Evaluates the quality of a patient clinical record across four key dimensions.

### Data Quality Dimensions
- **Completeness** — Are required fields present (e.g., medications, allergies)?
- **Accuracy** — Are values correctly formatted and valid?
- **Timeliness** — Is the data recent and up to date?
- **Clinical Plausibility** — Are physiological values realistic for a human patient?
- **Consistency** — Do values agree across systems, or are there contradictions?
- **Conflict Severity** — How significant are disagreements between sources?
- **Medication Diversity Score** — Measures variation in medication entries to detect unusual or conflicting patterns.

### What this endpoint does
- Analyzes the patient record for missing or incomplete fields  
- Validates formatting and structure of vital signs  
- Checks whether the record is outdated  
- Flags physiologically impossible or unsafe values  
- Returns a structured score and list of issues detected

This endpoint simulates real-world healthcare data quality validation used in clinical systems.
"""
)
def validate_data_quality(record: PatientRecord) -> DataQualityOutput:
    """
    Evaluate patient record quality and identify potential issues across multiple
    data quality dimensions.

    Args:
        record (PatientRecord):
            A structured patient record containing demographics, medications,
            allergies, conditions, vital signs, and a last_updated timestamp.

    Returns:
        DataQualityOutput:
            An object containing:
            - overall_score (int): Aggregate score from 0–100.
            - breakdown (dict): Individual scores for each data quality dimension.
            - issues_detected (List[dict]): List of detected issues with severity levels.
    """

    # Initialize scores (100 = perfect)
    breakdown = {
        "completeness": 100,
        "accuracy": 100,
        "timeliness": 100,
        "clinical_plausibility": 100,
        "consistency": 100,
        "conflict_severity": 0,   # lower is better
        "medication_diversity": 100
    }
    issues = []

    # Completeness Checks
    if not record.allergies:
        breakdown["completeness"] -= 20
        issues.append({
            "field": "allergies",
            "issue": "No allergies documented - likely incomplete",
            "severity": "medium"
        })

    if not record.medications:
        breakdown["completeness"] -= 20
        issues.append({
            "field": "medications",
            "issue": "No medications listed",
            "severity": "high"
        })

    # Accuracy & Clinical Plausibility Checks
    bp = record.vital_signs.get("blood_pressure")
    if bp:
        try:
            systolic, diastolic = map(int, bp.split("/"))
            if systolic > 250 or diastolic > 150:
                breakdown["clinical_plausibility"] -= 40
                issues.append({
                    "field": "vital_signs.blood_pressure",
                    "issue": f"Blood pressure {bp} is physiologically implausible",
                    "severity": "high"
                })
        except ValueError:
            breakdown["accuracy"] -= 10
            issues.append({
                "field": "vital_signs.blood_pressure",
                "issue": "Blood pressure format invalid",
                "severity": "medium"
            })

    # Timeliness Check
    try:
        last_updated = datetime.strptime(record.last_updated, "%Y-%m-%d")
        days_old = (datetime.now() - last_updated).days
        if days_old > 180:
            breakdown["timeliness"] -= 30
            issues.append({
                "field": "last_updated",
                "issue": f"Data is {days_old} days old",
                "severity": "medium"
            })
    except (ValueError, TypeError):
        breakdown["timeliness"] -= 20
        issues.append({
            "field": "last_updated",
            "issue": "Invalid date format",
            "severity": "medium"
        })

 
    # Consistency
    normalized = [m.strip().lower() for m in record.medications]
    unique_meds = set(normalized)

    if len(unique_meds) <= 1:
        breakdown["consistency"] = 100
    elif len(unique_meds) == 2:
        breakdown["consistency"] = 70
    else:
        breakdown["consistency"] = 40
        issues.append({
            "field": "medications",
            "issue": "Multiple conflicting medication names",
            "severity": "medium"
        })

    # Conflict Severity
    if len(unique_meds) <= 1:
        breakdown["conflict_severity"] = 0
    elif len(unique_meds) == 2:
        breakdown["conflict_severity"] = 40
    else:
        breakdown["conflict_severity"] = 80

    # Medication Variety Score
    med_count = len(record.medications)
    if med_count >= 5:
        breakdown["medication_diversity"] = 100
    elif med_count >= 3:
        breakdown["medication_diversity"] = 80
    elif med_count == 2:
        breakdown["medication_diversity"] = 60
    else:
        breakdown["medication_diversity"] = 40

    # Overall Score
    overall_score = sum(breakdown.values()) // len(breakdown)

    return DataQualityResponse(
        overall_score=overall_score,
        breakdown=DataQualityOutput(**breakdown),
        issues_detected=issues
    )