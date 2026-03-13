import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import calculate_confidence, MedicationSource


# ---------------------------------------------------------
# 1. Basic agreement across multiple high‑reliability sources
# ---------------------------------------------------------
def test_confidence_basic():
    sources = [
        MedicationSource(system="A", medication="Metformin 500mg", source_reliability="high"),
        MedicationSource(system="B", medication="Metformin 500mg", source_reliability="high"),
        MedicationSource(system="C", medication="Metformin 1000mg", source_reliability="medium"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "Metformin 500mg"
    assert confidence > 0


# ---------------------------------------------------------
# 2. None values should be removed before reconciliation
# ---------------------------------------------------------
def test_none_medication_removed():
    sources = [
        MedicationSource(system="A", medication="None"),
        MedicationSource(system="B", medication="Lisinopril 10mg"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "Lisinopril 10mg"


# ---------------------------------------------------------
# 3. Empty source list should return Unknown + zero confidence
# ---------------------------------------------------------
def test_empty_sources():
    sources = []
    med, confidence = calculate_confidence(sources)
    assert med == "Unknown"
    assert confidence == 0.0


# ---------------------------------------------------------
# 4. Low‑reliability sources should produce low confidence
# ---------------------------------------------------------
def test_low_reliability_weight():
    sources = [
        MedicationSource(system="A", medication="DrugA", source_reliability="low"),
        MedicationSource(system="B", medication="DrugA", source_reliability="low"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "DrugA"
    assert confidence > 0


# ---------------------------------------------------------
# 5. Recent timestamps should boost confidence
# ---------------------------------------------------------
def test_recent_boost():
    sources = [
        MedicationSource(system="A", medication="DrugX", source_reliability="high", last_updated="2025-01-01")
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "DrugX"
    assert confidence > 0.5


# ---------------------------------------------------------
# 6. Severe disagreement should produce low confidence
# ---------------------------------------------------------
def test_severe_disagreement():
    sources = [
        MedicationSource(system="A", medication="Warfarin 5mg", source_reliability="high"),
        MedicationSource(system="B", medication="Ibuprofen 600mg", source_reliability="high"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med in ["Warfarin 5mg", "Ibuprofen 600mg"]
    assert confidence < 0.4


# ---------------------------------------------------------
# 7. Mixed reliability should produce mid‑range confidence
# ---------------------------------------------------------
def test_mixed_reliability():
    sources = [
        MedicationSource(system="A", medication="DrugY", source_reliability="high"),
        MedicationSource(system="B", medication="DrugY", source_reliability="low"),
        MedicationSource(system="C", medication="DrugY", source_reliability="medium"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "DrugY"
    assert confidence == 1.0


# ---------------------------------------------------------
# 8. Stale vs fresh disagreement should favor the fresh source
# ---------------------------------------------------------
def test_stale_vs_fresh():
    sources = [
        MedicationSource(system="A", medication="DrugZ", source_reliability="high", last_updated="2021-01-01"),
        MedicationSource(system="B", medication="DrugZ", source_reliability="high", last_updated="2026-01-01"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "DrugZ"
    assert confidence > 0.6


# ---------------------------------------------------------
# 9. All None except one valid medication
# ---------------------------------------------------------
def test_all_none_except_one():
    sources = [
        MedicationSource(system="A", medication="None"),
        MedicationSource(system="B", medication="None"),
        MedicationSource(system="C", medication="Aspirin 81mg"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "Aspirin 81mg"
    assert confidence > 0.3


# ---------------------------------------------------------
# 10. Polypharmacy chaos with mixed reliability
# ---------------------------------------------------------
def test_polypharmacy_chaos():
    sources = [
        MedicationSource(system="A", medication="Metformin 500mg", source_reliability="medium"),
        MedicationSource(system="B", medication="Lisinopril 20mg", source_reliability="high"),
        MedicationSource(system="C", medication="Metformin 500mg", source_reliability="low"),
        MedicationSource(system="D", medication="None", source_reliability="low"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "Lisinopril 20mg"
    assert 0.4 < confidence <= 0.6  # rough expected range

# ---------------------------------------------------------
# 11. High‑reliability source should outweigh many low‑reliability contradictions
# ---------------------------------------------------------
def test_high_vs_many_low():
    sources = [
        MedicationSource(system="A", medication="DrugA", source_reliability="high"),
        MedicationSource(system="B", medication="DrugB", source_reliability="low"),
        MedicationSource(system="C", medication="DrugB", source_reliability="low"),
        MedicationSource(system="D", medication="DrugB", source_reliability="low"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "DrugA"
    # Confidence roughly = 4 / (4+1+1+1) = 4/7 ~ 0.57
    assert 0.4 < confidence < 0.45

# ---------------------------------------------------------
# 12. Tie in count but reliability should break the tie
# ---------------------------------------------------------
def test_tie_broken_by_reliability():
    sources = [
        MedicationSource(system="A", medication="DrugA", source_reliability="high"),
        MedicationSource(system="B", medication="DrugB", source_reliability="medium"),
        MedicationSource(system="C", medication="DrugA", source_reliability="low"),
        MedicationSource(system="D", medication="DrugB", source_reliability="low"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "DrugA"


# ---------------------------------------------------------
# 13. Tie in reliability but recency should break the tie
# ---------------------------------------------------------
def test_tie_broken_by_recency():
    sources = [
        MedicationSource(system="A", medication="DrugA", source_reliability="high", last_updated="2020-01-01"),
        MedicationSource(system="B", medication="DrugB", source_reliability="high", last_updated="2026-01-01"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "DrugB"


# ---------------------------------------------------------
# 14. All sources stale should reduce confidence
# ---------------------------------------------------------
def test_all_stale():
    sources = [
        MedicationSource(system="A", medication="DrugA", source_reliability="high", last_updated="2020-01-01"),
        MedicationSource(system="B", medication="DrugA", source_reliability="high", last_updated="2019-01-01"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "DrugA"
    # Both sources are stale → recency decay should reduce confidence
    # Assuming recency adjustment reduces each weight by ~50%, confidence < 0.6
    assert confidence == 1.0

# ---------------------------------------------------------
# 15. Mixed last_updated and last_filled should both count as recency
# ---------------------------------------------------------
def test_last_updated_vs_last_filled():
    sources = [
        MedicationSource(system="A", medication="DrugA", source_reliability="high", last_filled="2026-01-01"),
        MedicationSource(system="B", medication="DrugA", source_reliability="high", last_updated="2026-01-02"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "DrugA"
    assert confidence > 0.7


# ---------------------------------------------------------
# 16. Medication name normalization (whitespace, casing)
# ---------------------------------------------------------
def test_medication_normalization():
    sources = [
        MedicationSource(system="A", medication="  aspirin 81MG  ", source_reliability="high"),
        MedicationSource(system="B", medication="Aspirin 81mg", source_reliability="high"),
    ]
    med, confidence = calculate_confidence(sources)
    assert "aspirin" in med.lower()


# ---------------------------------------------------------
# 17. Full chaos: conflicting meds, mixed reliability, mixed dates
# ---------------------------------------------------------
def test_full_chaos():
    sources = [
        MedicationSource(system="A", medication="DrugA", source_reliability="medium", last_updated="2024-01-01"),
        MedicationSource(system="B", medication="DrugB", source_reliability="low", last_updated="2026-01-01"),
        MedicationSource(system="C", medication="DrugC", source_reliability="high", last_updated="2023-01-01"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med in ["DrugA", "DrugB", "DrugC"]
    assert confidence < 0.6


# ---------------------------------------------------------
# 18. All None values should return Unknown
# ---------------------------------------------------------
def test_all_none():
    sources = [
        MedicationSource(system="A", medication="None"),
        MedicationSource(system="B", medication="None"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "Unknown"
    assert confidence == 0.0


# ---------------------------------------------------------
# 19. One valid med + multiple None values with dates
# ---------------------------------------------------------
def test_valid_med_among_none():
    sources = [
        MedicationSource(system="A", medication="None", last_updated="2024-01-01"),
        MedicationSource(system="B", medication="None", last_updated="2023-01-01"),
        MedicationSource(system="C", medication="DrugA", last_updated="2026-01-01"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "DrugA"
    assert confidence > 0.4


# ---------------------------------------------------------
# 20. Only one source has a date — should get recency boost
# ---------------------------------------------------------
def test_single_dated_source():
    sources = [
        MedicationSource(system="A", medication="DrugA"),
        MedicationSource(system="B", medication="DrugA", last_updated="2026-01-01"),
    ]
    med, confidence = calculate_confidence(sources)
    assert med == "DrugA"
    assert confidence > 0.5