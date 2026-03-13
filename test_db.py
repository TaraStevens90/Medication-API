test_db = {
    # CLEAN — high confidence, PASSED
    "P001": {
        "name": "Alice Johnson",
        "medications": [
            {"patient_id": "P001", "system": "Hospital EHR", "medication": "Aspirin 81mg", "last_updated": "2026-02-10", "source_reliability": "high"},
            {"patient_id": "P001", "system": "Pharmacy", "medication": "Aspirin 81mg", "last_filled": "2026-02-12", "source_reliability": "high"}
        ]
    },

    # MILD DOSE MISMATCH — WARNING
    "P002": {
        "name": "Brian Smith",
        "medications": [
            {"patient_id": "P002", "system": "Hospital EHR", "medication": "Metformin 500mg", "last_updated": "2025-12-01", "source_reliability": "high"},
            {"patient_id": "P002", "system": "Pharmacy", "medication": "Metformin 1000mg", "last_filled": "2026-01-15", "source_reliability": "medium"}
        ]
    },

    # LOW CONFIDENCE — single source, stale
    "P003": {
        "name": "Harold Whitman",
        "medications": [
            {"patient_id": "P003", "system": "Clinic System", "medication": "Aspirin 81mg", "last_updated": "2022-11-10", "source_reliability": "medium"}
        ]
    },

    # FAILED — dangerous contradiction (Warfarin + Ibuprofen)
    "P004": {
        "name": "Grant Holloway",
        "medications": [
            {"patient_id": "P004", "system": "Hospital EHR", "medication": "Warfarin 5mg", "last_updated": "2026-01-20", "source_reliability": "high"},
            {"patient_id": "P004", "system": "Pharmacy", "medication": "Warfarin 10mg", "last_filled": "2026-02-01", "source_reliability": "high"},
            {"patient_id": "P004", "system": "Clinic System", "medication": "Ibuprofen 600mg", "last_updated": "2026-01-15", "source_reliability": "medium"}
        ]
    },

    # CLEAN MULTI-SOURCE — PASSED
    "P005": {
        "name": "Arianna Steele",
        "medications": [
            {"patient_id": "P005", "system": "Hospital EHR", "medication": "Levothyroxine 75mcg", "last_updated": "2026-01-15", "source_reliability": "high"},
            {"patient_id": "P005", "system": "Pharmacy", "medication": "Levothyroxine 75mcg", "last_filled": "2026-01-20", "source_reliability": "high"},
            {"patient_id": "P005", "system": "Clinic System", "medication": "Levothyroxine 75mcg", "last_updated": "2026-01-10", "source_reliability": "medium"}
        ]
    },

    # CHAOTIC — 5 sources, mixed reliability, conflicting doses
    "P006": {
        "name": "Silas Brennan",
        "medications": [
            {"patient_id": "P006", "system": "Hospital EHR", "medication": "Lisinopril 10mg", "last_updated": "2026-02-01", "source_reliability": "high"},
            {"patient_id": "P006", "system": "Pharmacy", "medication": "Lisinopril 40mg", "last_filled": "2026-02-05", "source_reliability": "medium"},
            {"patient_id": "P006", "system": "Clinic System", "medication": "Lisinopril 20mg", "last_updated": "2025-12-10", "source_reliability": "medium"},
            {"patient_id": "P006", "system": "Patient Portal", "medication": "None", "last_updated": "2024-01-01", "source_reliability": "low"},
            {"patient_id": "P006", "system": "Specialist System", "medication": "Lisinopril 10mg", "last_updated": "2026-02-02", "source_reliability": "high"}
        ]
    },

    # CLEAN SINGLE MED — PASSED
    "P007": {
        "name": "Lorelai Chen",
        "medications": [
            {"patient_id": "P007", "system": "Pharmacy", "medication": "Omeprazole 20mg", "last_filled": "2026-02-10", "source_reliability": "high"}
        ]
    },

    # FAILED — insulin type mismatch
    "P008": {
        "name": "Tanner Briggs",
        "medications": [
            {"patient_id": "P008", "system": "Hospital EHR", "medication": "Insulin Glargine", "last_updated": "2026-01-10", "source_reliability": "high"},
            {"patient_id": "P008", "system": "Pharmacy", "medication": "Insulin Lispro", "last_filled": "2026-01-12", "source_reliability": "high"},
            {"patient_id": "P008", "system": "Clinic System", "medication": "Metformin 500mg", "last_updated": "2025-12-01", "source_reliability": "medium"}
        ]
    },

    # WARNING — stale + mild mismatch
    "P009": {
        "name": "Camila Duarte",
        "medications": [
            {"patient_id": "P009", "system": "Patient Portal", "medication": "Aspirin 81mg", "last_updated": "2022-01-01", "source_reliability": "low"},
            {"patient_id": "P009", "system": "Clinic System", "medication": "Aspirin 81mg", "last_updated": "2023-05-10", "source_reliability": "medium"}
        ]
    },

    # CLEAN — PASSED
    "P010": {
        "name": "Eden Walsh",
        "medications": [
            {"patient_id": "P010", "system": "Hospital EHR", "medication": "Amlodipine 5mg", "last_updated": "2026-02-10", "source_reliability": "high"},
            {"patient_id": "P010", "system": "Pharmacy", "medication": "Amlodipine 5mg", "last_filled": "2026-02-12", "source_reliability": "high"}
        ]
    },

    # MEDIUM CONFIDENCE — 3 sources, mild mismatch
    "P011": {
        "name": "Chloe Adams",
        "medications": [
            {"patient_id": "P011", "system": "Hospital EHR", "medication": "Amlodipine 5mg", "last_updated": "2025-01-22", "source_reliability": "high"},
            {"patient_id": "P011", "system": "Pharmacy", "medication": "Amlodipine 10mg", "last_filled": "2025-01-25", "source_reliability": "medium"},
            {"patient_id": "P011", "system": "Patient Portal", "medication": "None", "last_updated": "2025-01-10", "source_reliability": "low"}
        ]
    },

    # CLEAN — PASSED
    "P012": {
        "name": "Marcus Hill",
        "medications": [
            {"patient_id": "P012", "system": "Hospital EHR", "medication": "Gabapentin 300mg", "last_updated": "2025-02-01", "source_reliability": "high"},
            {"patient_id": "P012", "system": "Pharmacy", "medication": "Gabapentin 300mg", "last_filled": "2025-02-03", "source_reliability": "high"}
        ]
    },

    # WARNING — stale + mismatch
    "P013": {
        "name": "Samantha Ortiz",
        "medications": [
            {"patient_id": "P013", "system": "Clinic System", "medication": "Fluoxetine 20mg", "last_updated": "2025-01-28", "source_reliability": "medium"},
            {"patient_id": "P013", "system": "Pharmacy", "medication": "Fluoxetine 20mg", "last_filled": "2025-02-02", "source_reliability": "high"},
            {"patient_id": "P013", "system": "Hospital EHR", "medication": "None", "last_updated": "2025-01-15", "source_reliability": "low"}
        ]
    },

    # FAILED — Atorvastatin 20 vs 40
    "P014": {
        "name": "Derek Wilson",
        "medications": [
            {"patient_id": "P014", "system": "Hospital EHR", "medication": "Atorvastatin 40mg", "last_updated": "2025-01-18", "source_reliability": "high"},
            {"patient_id": "P014", "system": "Pharmacy", "medication": "Atorvastatin 20mg", "last_filled": "2025-01-22", "source_reliability": "medium"},
            {"patient_id": "P014", "system": "Patient Portal", "medication": "Atorvastatin 40mg", "last_updated": "2025-01-12", "source_reliability": "low"}
        ]
    },

    # CLEAN — PASSED
    "P015": {
        "name": "Grace Kim",
        "medications": [
            {"patient_id": "P015", "system": "Clinic System", "medication": "Montelukast 10mg", "last_updated": "2025-02-05", "source_reliability": "medium"},
            {"patient_id": "P015", "system": "Pharmacy", "medication": "Montelukast 10mg", "last_filled": "2025-02-07", "source_reliability": "high"}
        ]
    },

    # HIGH VARIATION — 3 sources, mixed reliability
    "P016": {
        "name": "Henry Foster",
        "medications": [
            {"patient_id": "P016", "system": "Hospital EHR", "medication": "Insulin Glargine", "last_updated": "2025-02-10", "source_reliability": "high"},
            {"patient_id": "P016", "system": "Pharmacy", "medication": "Insulin Glargine", "last_filled": "2025-02-12", "source_reliability": "high"},
            {"patient_id": "P016", "system": "Clinic System", "medication": "Metformin 500mg", "last_updated": "2025-01-30", "source_reliability": "medium"}
        ]
    },

    # LOW CONFIDENCE — 2 low-reliability sources
    "P017": {
        "name": "Callie Monroe",
        "medications": [
            {"patient_id": "P017", "system": "Patient Portal", "medication": "Aspirin 325mg", "last_updated": "2023-01-01", "source_reliability": "low"},
            {"patient_id": "P017", "system": "Clinic System", "medication": "Aspirin 81mg", "last_updated": "2023-02-01", "source_reliability": "low"}
        ]
    },

    # FAILED — 3 sources, all disagree
    "P018": {
        "name": "Mara Ellington",
        "medications": [
            {"patient_id": "P018", "system": "Hospital EHR", "medication": "Insulin Glargine", "last_updated": "2024-01-10", "source_reliability": "medium"},
            {"patient_id": "P018", "system": "Pharmacy", "medication": "Warfarin 5mg", "last_filled": "2025-01-12", "source_reliability": "medium"},
            {"patient_id": "P018", "system": "Clinic System", "medication": "Sertraline 50mg", "last_updated": "2023-10-01", "source_reliability": "low"}
        ]
    },

    # CLEAN — PASSED
    "P019": {
        "name": "Holly Barrett",
        "medications": [
            {"patient_id": "P019", "system": "Hospital EHR", "medication": "Levothyroxine 50mcg", "last_updated": "2021-01-01", "source_reliability": "medium"},
            {"patient_id": "P019", "system": "Pharmacy", "medication": "Levothyroxine 50mcg", "last_filled": "2021-02-01", "source_reliability": "medium"}
        ]
    },

    # WARNING — stale + mismatch
    "P020": {
        "name": "Ronan Blake",
        "medications": [
            {"patient_id": "P020", "system": "Hospital EHR", "medication": "Metformin 500mg", "source_reliability": "medium"},
            {"patient_id": "P020", "system": "Pharmacy", "medication": "Lisinopril 20mg", "last_filled": "2022-05-01", "source_reliability": "medium"}
        ]
    },
    # CLEAN — PASSED
    "P021": {
        "name": "Eden Walsh",
        "medications": [
            {"patient_id": "P021", "system": "Hospital EHR", "medication": "Aspirin 81mg", "last_updated": "2026-02-10", "source_reliability": "high"},
            {"patient_id": "P021", "system": "Pharmacy", "medication": "Aspirin 81mg", "last_filled": "2026-02-12", "source_reliability": "high"}
        ]
    },

    # WARNING — mild mismatch
    "P022": {
        "name": "Trevor Simmons",
        "medications": [
            {"patient_id": "P022", "system": "Hospital EHR", "medication": "Metformin 500mg", "last_updated": "2025-01-15", "source_reliability": "high"},
            {"patient_id": "P022", "system": "Pharmacy", "medication": "Metformin 500mg", "last_filled": "2025-01-28", "source_reliability": "high"},
            {"patient_id": "P022", "system": "Patient Portal", "medication": "None", "last_updated": "2025-01-10", "source_reliability": "low"}
        ]
    },

    # FAILED — conflicting meds
    "P023": {
        "name": "Ariana Flores",
        "medications": [
            {"patient_id": "P023", "system": "Clinic System", "medication": "Sertraline 25mg", "last_updated": "2025-02-05", "source_reliability": "medium"},
            {"patient_id": "P023", "system": "Pharmacy", "medication": "Sertraline 50mg", "last_filled": "2025-02-07", "source_reliability": "high"},
            {"patient_id": "P023", "system": "Hospital EHR", "medication": "None", "last_updated": "2025-01-22", "source_reliability": "low"}
        ]
    },

    # CLEAN — PASSED
    "P024": {
        "name": "Gavin Brooks",
        "medications": [
            {"patient_id": "P024", "system": "Hospital EHR", "medication": "Lisinopril 20mg", "last_updated": "2025-01-30", "source_reliability": "high"},
            {"patient_id": "P024", "system": "Pharmacy", "medication": "Lisinopril 20mg", "last_filled": "2025-02-01", "source_reliability": "high"}
        ]
    },

    # HIGH VARIATION — 4 sources, mixed reliability
    "P025": {
        "name": "Maya Singh",
        "medications": [
            {"patient_id": "P025", "system": "Pharmacy", "medication": "Levothyroxine 50mcg", "last_filled": "2025-02-02", "source_reliability": "high"},
            {"patient_id": "P025", "system": "Hospital EHR", "medication": "Levothyroxine 75mcg", "last_updated": "2025-01-25", "source_reliability": "medium"}
        ]
    },

    # HIGH AGREEMENT — same medication, different timestamps
    "P026": {
        "name": "Owen Parker",
        "medications": [
            {"patient_id": "P026", "system": "Clinic System", "medication": "Albuterol Inhaler", "last_updated": "2025-02-10", "source_reliability": "medium"},
            {"patient_id": "P026", "system": "Pharmacy", "medication": "Albuterol Inhaler", "last_filled": "2025-02-12", "source_reliability": "high"}
        ]
    },

    # DOSE CONFLICT — high vs low dose, mixed recency
    "P027": {
        "name": "Lily Bennett",
        "medications": [
            {"patient_id": "P027", "system": "Hospital EHR", "medication": "Amlodipine 10mg", "last_updated": "2024-09-12", "source_reliability": "high"},
            {"patient_id": "P027", "system": "Pharmacy", "medication": "Amlodipine 5mg", "last_filled": "2025-02-20", "source_reliability": "medium"}
        ]
    },

    # MIXED SOURCES — two agreeing, one 'None' low-reliability source
    "P028": {
        "name": "Ethan Wallace",
        "medications": [
            {"patient_id": "P028", "system": "Pharmacy", "medication": "Omeprazole 20mg", "last_filled": "2025-02-03", "source_reliability": "high"},
            {"patient_id": "P028", "system": "Hospital EHR", "medication": "Omeprazole 20mg", "last_updated": "2025-01-28", "source_reliability": "high"},
            {"patient_id": "P028", "system": "Clinic System", "medication": "None", "last_updated": "2025-01-12", "source_reliability": "low"}
        ]
    },

    # CONFLICTING MEDICATIONS — two high-reliability agree, one medium disagrees
    "P029": {
        "name": "Sofia Ramirez",
        "medications": [
            {"patient_id": "P029", "system": "Hospital EHR", "medication": "Warfarin 5mg", "last_updated": "2025-01-22", "source_reliability": "high"},
            {"patient_id": "P029", "system": "Pharmacy", "medication": "Warfarin 5mg", "last_filled": "2025-01-25", "source_reliability": "high"},
            {"patient_id": "P029", "system": "Clinic System", "medication": "Aspirin 81mg", "last_updated": "2025-01-15", "source_reliability": "medium"}
        ]
    },

    # PARTIAL AGREEMENT — two agree, one conflicting high-reliability source
    "P030": {
        "name": "Caleb Foster",
        "medications": [
            {"patient_id": "P030", "system": "Clinic System", "medication": "Hydrochlorothiazide 25mg", "last_updated": "2025-02-08", "source_reliability": "medium"},
            {"patient_id": "P030", "system": "Pharmacy", "medication": "Hydrochlorothiazide 25mg", "last_filled": "2025-02-10", "source_reliability": "high"},
            {"patient_id": "P030", "system": "Hospital EHR", "medication": "Lisinopril 20mg", "last_updated": "2025-01-30", "source_reliability": "high"}
        ]
    },

    # LOW CONFIDENCE — single stale source
    "P031": {
        "name": "Harper Mills",
        "medications": [
            {"patient_id": "P031", "system": "Clinic System", "medication": "Aspirin 81mg", "last_updated": "2022-03-01", "source_reliability": "medium"}
        ]
    },

    # FAILED — 3 sources, all disagree
    "P032": {
        "name": "Julian Scott",
        "medications": [
            {"patient_id": "P032", "system": "Hospital EHR", "medication": "Metformin 1000mg", "last_updated": "2025-01-18", "source_reliability": "high"},
            {"patient_id": "P032", "system": "Pharmacy", "medication": "Lisinopril 20mg", "last_filled": "2025-01-28", "source_reliability": "medium"},
            {"patient_id": "P032", "system": "Patient Portal", "medication": "None", "last_updated": "2024-01-10", "source_reliability": "low"}
        ]
    },

    # CLEAN — PASSED
    "P033": {
        "name": "Elena Brooks",
        "medications": [
            {"patient_id": "P033", "system": "Pharmacy", "medication": "Sertraline 50mg", "last_filled": "2026-02-05", "source_reliability": "high"},
            {"patient_id": "P033", "system": "Hospital EHR", "medication": "Sertraline 50mg", "last_updated": "2026-02-03", "source_reliability": "high"}
        ]
    },

    # WARNING — mild mismatch + stale
    "P034": {
        "name": "Miles Carter",
        "medications": [
            {"patient_id": "P034", "system": "Hospital EHR", "medication": "Atorvastatin 20mg", "last_updated": "2025-01-30", "source_reliability": "high"},
            {"patient_id": "P034", "system": "Pharmacy", "medication": "Atorvastatin 40mg", "last_filled": "2025-02-01", "source_reliability": "medium"}
        ]
    },

    # CLEAN — PASSED
    "P035": {
        "name": "Zoe Ramirez",
        "medications": [
            {"patient_id": "P035", "system": "Pharmacy", "medication": "Levothyroxine 75mcg", "last_filled": "2026-02-04", "source_reliability": "high"},
            {"patient_id": "P035", "system": "Hospital EHR", "medication": "Levothyroxine 75mcg", "last_updated": "2026-02-01", "source_reliability": "high"}
        ]
    },

    # CHAOTIC — 4 sources, conflicting meds
    "P036": {
        "name": "Adrian Foster",
        "medications": [
            {"patient_id": "P036", "system": "Clinic System", "medication": "Albuterol Inhaler", "last_updated": "2025-02-12", "source_reliability": "medium"},
            {"patient_id": "P036", "system": "Pharmacy", "medication": "Prednisone 20mg", "last_filled": "2025-02-14", "source_reliability": "medium"},
            {"patient_id": "P036", "system": "Hospital EHR", "medication": "Prednisone 10mg", "last_updated": "2025-01-28", "source_reliability": "high"},
            {"patient_id": "P036", "system": "Patient Portal", "medication": "None", "last_updated": "2024-05-01", "source_reliability": "low"}
        ]
    },

    # CLEAN — PASSED
    "P037": {
        "name": "Nora Ellis",
        "medications": [
            {"patient_id": "P037", "system": "Hospital EHR", "medication": "Amlodipine 5mg", "last_updated": "2026-01-22", "source_reliability": "high"},
            {"patient_id": "P037", "system": "Pharmacy", "medication": "Amlodipine 5mg", "last_filled": "2026-01-25", "source_reliability": "high"}
        ]
    },

    # FAILED — Omeprazole 20 vs 40 + None
    "P038": {
        "name": "Xavier Hunt",
        "medications": [
            {"patient_id": "P038", "system": "Pharmacy", "medication": "Omeprazole 40mg", "last_filled": "2026-02-06", "source_reliability": "high"},
            {"patient_id": "P038", "system": "Hospital EHR", "medication": "Omeprazole 20mg", "last_updated": "2026-01-28", "source_reliability": "medium"},
            {"patient_id": "P038", "system": "Clinic System", "medication": "None", "last_updated": "2025-01-10", "source_reliability": "low"}
        ]
    },

    # CLEAN — PASSED
    "P039": {
        "name": "Penelope Ward",
        "medications": [
            {"patient_id": "P039", "system": "Hospital EHR", "medication": "Warfarin 5mg", "last_updated": "2025-01-20", "source_reliability": "high"},
            {"patient_id": "P039", "system": "Pharmacy", "medication": "Warfarin 5mg", "last_filled": "2025-01-23", "source_reliability": "high"}
        ]
    },

    # WARNING — mild mismatch
    "P040": {
        "name": "Leo Armstrong",
        "medications": [
            {"patient_id": "P040", "system": "Clinic System", "medication": "Hydrochlorothiazide 25mg", "last_updated": "2025-02-08", "source_reliability": "medium"},
            {"patient_id": "P040", "system": "Pharmacy", "medication": "Hydrochlorothiazide 12.5mg", "last_filled": "2025-02-10", "source_reliability": "high"}
        ]
    },
    # LOW CONFIDENCE — 2 low-reliability sources
    "P041": {
        "name": "Aubrey Daniels",
        "medications": [
            {"patient_id": "P041", "system": "Patient Portal", "medication": "Aspirin 81mg", "last_updated": "2023-01-10", "source_reliability": "low"},
            {"patient_id": "P041", "system": "Clinic System", "medication": "Aspirin 325mg", "last_updated": "2023-02-01", "source_reliability": "low"}
        ]
    },

    # FAILED — 5 sources, all disagree
    "P042": {
        "name": "Riley Thompson",
        "medications": [
            {"patient_id": "P042", "system": "Hospital EHR", "medication": "Metformin 500mg", "last_updated": "2025-01-22", "source_reliability": "high"},
            {"patient_id": "P042", "system": "Pharmacy", "medication": "Warfarin 5mg", "last_filled": "2025-01-28", "source_reliability": "medium"},
            {"patient_id": "P042", "system": "Clinic System", "medication": "Sertraline 50mg", "last_updated": "2024-01-10", "source_reliability": "medium"},
            {"patient_id": "P042", "system": "Specialist System", "medication": "Prednisone 20mg", "last_updated": "2025-11-01", "source_reliability": "medium"},
            {"patient_id": "P042", "system": "Patient Portal", "medication": "None", "last_updated": "2023-05-01", "source_reliability": "low"}
        ]
    },

    # CLEAN — PASSED
    "P043": {
        "name": "Gabriella Ruiz",
        "medications": [
            {"patient_id": "P043", "system": "Pharmacy", "medication": "Sertraline 50mg", "last_filled": "2026-02-08", "source_reliability": "high"},
            {"patient_id": "P043", "system": "Hospital EHR", "medication": "Sertraline 50mg", "last_updated": "2026-02-06", "source_reliability": "high"}
        ]
    },

    # WARNING — stale + mismatch
    "P044": {
        "name": "Dominic Hayes",
        "medications": [
            {"patient_id": "P044", "system": "Hospital EHR", "medication": "Atorvastatin 20mg", "last_updated": "2024-11-20", "source_reliability": "high"},
            {"patient_id": "P044", "system": "Pharmacy", "medication": "Atorvastatin 40mg", "last_filled": "2025-01-05", "source_reliability": "medium"}
        ]
    },

    # CLEAN — PASSED
    "P045": {
        "name": "Stella Nguyen",
        "medications": [
            {"patient_id": "P045", "system": "Pharmacy", "medication": "Levothyroxine 88mcg", "last_filled": "2026-02-03", "source_reliability": "high"},
            {"patient_id": "P045", "system": "Hospital EHR", "medication": "Levothyroxine 88mcg", "last_updated": "2026-01-25", "source_reliability": "high"}
        ]
    },

    # CHAOTIC — 4 sources, conflicting meds
    "P046": {
        "name": "Wyatt Coleman",
        "medications": [
            {"patient_id": "P046", "system": "Clinic System", "medication": "Albuterol Inhaler", "last_updated": "2025-02-14", "source_reliability": "medium"},
            {"patient_id": "P046", "system": "Pharmacy", "medication": "Albuterol Inhaler", "last_filled": "2025-02-15", "source_reliability": "high"},
            {"patient_id": "P046", "system": "Hospital EHR", "medication": "Prednisone 10mg", "last_updated": "2025-01-28", "source_reliability": "high"},
            {"patient_id": "P046", "system": "Patient Portal", "medication": "None", "last_updated": "2024-05-01", "source_reliability": "low"}
        ]
    },

    # CLEAN — PASSED
    "P047": {
        "name": "Madeline Foster",
        "medications": [
            {"patient_id": "P047", "system": "Hospital EHR", "medication": "Amlodipine 5mg", "last_updated": "2025-01-22", "source_reliability": "high"},
            {"patient_id": "P047", "system": "Pharmacy", "medication": "Amlodipine 5mg", "last_filled": "2025-01-25", "source_reliability": "high"}
        ]
    },

    # FAILED — conflicting doses + None
    "P048": {
        "name": "Ezekiel Barrett",
        "medications": [
            {"patient_id": "P048", "system": "Pharmacy", "medication": "Omeprazole 40mg", "last_filled": "2026-02-06", "source_reliability": "high"},
            {"patient_id": "P048", "system": "Hospital EHR", "medication": "Omeprazole 20mg", "last_updated": "2026-01-28", "source_reliability": "medium"},
            {"patient_id": "P048", "system": "Clinic System", "medication": "None", "last_updated": "2025-01-10", "source_reliability": "low"}
        ]
    },

    # CLEAN — PASSED
    "P049": {
        "name": "Valentina Cruz",
        "medications": [
            {"patient_id": "P049", "system": "Hospital EHR", "medication": "Warfarin 5mg", "last_updated": "2025-01-20", "source_reliability": "high"},
            {"patient_id": "P049", "system": "Pharmacy", "medication": "Warfarin 5mg", "last_filled": "2025-01-23", "source_reliability": "high"}
        ]
    },

    # LOW CONFIDENCE — single source, stale
    "P050": {
        "name": "Carter Jennings",
        "medications": [
            {"patient_id": "P050", "system": "Clinic System", "medication": "Lisinopril 10mg", "last_updated": "2022-01-01", "source_reliability": "medium"}
        ]
    }
}
   

    