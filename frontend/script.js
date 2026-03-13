// Configuration
  const apiBase = "http://127.0.0.1:8000";
  const apiKey = "mysecretkey";

// DOM Helper
  const get = id => document.getElementById(id);

// UI Update Functions
  function updateConfidenceBar(score) {
    const percent = Math.round(score * 100);
    const bar = get("confidenceBar");
    const label = bar.querySelector(".bar-label");

    let colorClass = "green";
    if (score < 0.5) colorClass = "red";
    else if (score < 0.8) colorClass = "yellow";

    bar.className = `bar ${colorClass}`;
    bar.style.width = percent + "%";
    label.textContent = percent + "%";
  }

  function updateSafetyCheck(status, reason) {
    let colorClass = "-";
    if (status.includes("PASSED")) colorClass = "green";
    else if (status.includes("WARNING")) colorClass = "yellow";
    else if (status.includes("FAILED")) colorClass = "red";

    const text = reason ? `${status} - ${reason}` : status;
    get("safety").innerHTML = `<span class="status-box ${colorClass}">${text}</span>`;
  }

  function updateActions(actions) {
    const ul = get("actionsList");
    ul.innerHTML = "";
    actions.forEach(act => {
      const li = document.createElement("li");
      li.textContent = act;
      ul.appendChild(li);
    });
  }

// API Call: Reconciliation
  async function handleReconcile() {
    const patientId = get("patientId").value.trim();
    if (!patientId) return alert("Please enter a patient ID.");

    try {
      const res = await fetch(`${apiBase}/api/reconcile/medication/by-id`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": apiKey
        },
        body: JSON.stringify({ patient_id: patientId })
      });

      if (!res.ok) {
        const errorText = await res.text();
        console.error("Fetch failed:", errorText);
        throw new Error(res.statusText);
      }

      const data = await res.json();
      const reconciled = data.reconciled_medication;

// Display reconciled medication
  get("truth").textContent = reconciled.truth;
  get("reasoning").textContent = reconciled.reasoning;
  updateConfidenceBar(reconciled.confidence);
  updateActions(reconciled.recommended_actions);
  updateSafetyCheck(reconciled.clinical_safety_check, reconciled.safety_reason);

// Display all medication sources
  const medsList = get("medicationsList");
  medsList.innerHTML = "";
  data.all_medications.forEach(med => {
    const li = document.createElement("li");
    li.textContent = `${med.medication} (Source: ${med.system}${med.source_reliability ? ", Reliability: " + med.source_reliability : ""}${med.last_updated ? ", Updated: " + med.last_updated : ""})`;
    medsList.appendChild(li);
  });

  } catch (err) {
    console.error(err);
    alert("Error fetching reconciliation.");
  }
}

// API Call: Data Quality
  async function handleDataQuality() {
    const patientId = get("patientId").value.trim();
    if (!patientId) return alert("Please enter a patient ID.");

// Hide the section before loading new results
  get("dataQualitySection").style.display = "none";

  try {
    // Fetch stored medications
    const patientRes = await fetch(`${apiBase}/api/patient/${patientId}/medications`, {
      headers: { "x-api-key": apiKey }
    });

    if (!patientRes.ok) throw new Error(patientRes.statusText);
    const rawMeds = await patientRes.json();
    const meds = rawMeds.map(m => m.medication);

    const record = {
      demographics: { name: "John Doe", dob: "1955-03-15", gender: "M" },
      medications: meds,
      allergies: [],
      conditions: ["Type 2 Diabetes"],
      vital_signs: { blood_pressure: "120/80", heart_rate: 70 },
      last_updated: "2025-01-01"
    };

    const res = await fetch(`${apiBase}/api/validate/data-quality`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey
      },
      body: JSON.stringify(record)
    });

    if (!res.ok) {
      const errorText = await res.text();
      console.error("Data quality fetch failed:", errorText);
      throw new Error(res.statusText);
    }

    const data = await res.json();

// Reveal the section
  get("dataQualitySection").style.display = "block";

// Update Overall Score
  let color = "green";
  if (data.overall_score < 70) color = "yellow";
  if (data.overall_score < 50) color = "red";
  get("qualityScore").innerHTML = `<span class="${color}">${data.overall_score}</span>`;

// Update Breakdown Table
  const b = data.breakdown;
  get("dq-completeness").textContent = b.completeness ?? "-";
  get("dq-accuracy").textContent = b.accuracy ?? "-";
  get("dq-timeliness").textContent = b.timeliness ?? "-";
  get("dq-plausibility").textContent = b.clinical_plausibility ?? "-";
  get("dq-consistency").textContent = b.consistency ?? "-";
  get("dq-conflict").textContent = b.conflict_severity ?? "-";
  get("dq-diversity").textContent = b.medication_diversity ?? "-";

// Update Issues List
  const issuesList = get("issuesList");
  issuesList.innerHTML = "";
  data.issues_detected.forEach(issue => {
    const li = document.createElement("li");
    li.textContent = `${issue.field}: ${issue.issue} (${issue.severity})`;
    issuesList.appendChild(li);
  });

  } catch (err) {
    console.error(err);
    alert("Error fetching data quality.");
  }
}

// Hide Data Quality section whenever the patient ID changes
  get("patientId").addEventListener("input", () => {
    get("dataQualitySection").style.display = "none";
  });

// Decision Buttons
function approveSuggestion() {
  get("decisionStatus").textContent = "Suggestion approved.";
}

function rejectSuggestion() {
  get("decisionStatus").textContent = "Suggestion rejected.";
}

// Copy Reasoning Button
  function copyReasoning() {
    const text = get("reasoning").textContent;
    navigator.clipboard.writeText(text)
      .then(() => alert("Reasoning copied to clipboard."))
      .catch(() => alert("Failed to copy reasoning."));
  }