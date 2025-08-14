# prompts.py

class DrugAnalysisPrompts:
    """Collection of prompts for analyzing drug interactions, dosages, and alternative medications"""

    # Drug extraction prompts
    DRUG_EXTRACTION_SYSTEM = """You are a medical information researcher. Extract specific drug names, dosages, and medical information from healthcare documents.

Focus on actual pharmaceutical products, medications, and therapeutic substances that are clinically used."""

    @staticmethod
    def drug_extraction_user(query: str, content: str) -> str:
        return f"""Query: {query}

Medical Content: {content}

Extract a list of specific drug/medication names mentioned in this content that are relevant to "{query}".

Rules:
- Only include actual pharmaceutical product names, not generic medical terms
- Focus on drugs that clinicians can prescribe/administer
- Include both brand names and generic names where mentioned
- Include dosage information if available
- Limit to the 10 most relevant medications
- Return drug names with dosage info if available, one per line

Example format:
Aspirin 325mg
Metformin 500mg
Lisinopril 10mg
Atorvastatin 20mg
Warfarin 5mg"""

    # Drug interaction analysis prompts
    DRUG_INTERACTION_SYSTEM = """You are analyzing pharmaceutical drugs and their interactions.

Focus on extracting information relevant to healthcare providers and pharmacists.

Pay special attention to drug interactions, contraindications, side effects, and dosage recommendations."""

    @staticmethod
    def drug_interaction_user(drug_name: str, content: str) -> str:
        return f"""Drug: {drug_name}

Medical Database Content: {content[:2500]}

Analyze this content from a clinical perspective and provide:

- interaction_severity: One of "Major", "Moderate", "Minor", "None", or "Unknown"
- contraindications: List of conditions or patient groups where this drug should be avoided
- age_restrictions: Specific age groups with restrictions (pediatric, geriatric, etc.)
- dosage_forms: Available forms (tablet, injection, liquid, etc.)
- description: Brief 1-sentence description of the drug's primary therapeutic use
- common_interactions: List of other drugs that commonly interact with this medication
- therapeutic_class: Drug classification (e.g., ACE inhibitor, beta-blocker, antibiotic)
- monitoring_required: Special monitoring or lab tests required during treatment

Focus on clinical safety, drug interactions, and patient-specific considerations."""

    # NLP drug information extraction prompts
    NLP_EXTRACTION_SYSTEM = """You are a medical NLP specialist extracting structured drug information from unstructured text.

Parse medical text to identify drug names, dosages, frequencies, and administration details."""

    @staticmethod
    def nlp_extraction_user(medical_text: str) -> str:
        return f"""Medical Text: {medical_text}

Extract structured drug information from this unstructured medical text:

Identify and structure:
- drug_name: Exact medication name (generic or brand)
- dosage_amount: Numerical dose (e.g., 500, 10, 0.25)
- dosage_unit: Unit of measurement (mg, mcg, ml, tablets)
- frequency: How often taken (daily, BID, TID, PRN, etc.)
- route: Method of administration (oral, IV, IM, topical)
- duration: Length of treatment if mentioned
- special_instructions: Any specific timing or food requirements

Return in JSON format for each drug found:
{
  "drug_name": "Metformin",
  "dosage_amount": "500",
  "dosage_unit": "mg",
  "frequency": "twice daily",
  "route": "oral",
  "duration": "ongoing",
  "special_instructions": "take with meals"
}"""

    # Age-specific dosage prompts
    AGE_DOSAGE_SYSTEM = """You are a clinical pharmacist specializing in age-appropriate drug dosing.

Provide dosage recommendations based on patient age, weight, and safety profiles."""

    @staticmethod
    def age_dosage_user(drug_name: str, patient_age: str, patient_weight: str = None) -> str:
        return f"""Drug: {drug_name}
Patient Age: {patient_age}
Patient Weight: {patient_weight if patient_weight else "Not provided"}

Provide age-appropriate dosage recommendations:

Consider:
- pediatric_dosing: Specific dosing for children if applicable
- geriatric_considerations: Adjustments needed for elderly patients
- weight_based_dosing: If dosing should be calculated by weight
- renal_adjustments: Kidney function considerations by age group
- hepatic_adjustments: Liver function considerations by age group
- contraindications_by_age: Age groups where drug is contraindicated
- monitoring_requirements: Special monitoring needed for this age group
- alternative_formulations: Age-appropriate drug forms (liquid vs tablet)

Provide specific mg/kg or standard doses with frequency recommendations."""

    # Alternative medication prompts
    ALTERNATIVE_MEDICATION_SYSTEM = """You are a clinical pharmacist providing alternative medication recommendations.

Suggest safer or equivalent drugs when interactions or contraindications are identified."""

    @staticmethod
    def alternative_medication_user(primary_drug: str, contraindication_reason: str, patient_profile: str) -> str:
        return f"""Primary Drug: {primary_drug}
Contraindication Reason: {contraindication_reason}
Patient Profile: {patient_profile}

Suggest alternative medications that:

- therapeutic_alternatives: Drugs in same class with similar efficacy
- mechanism_alternatives: Different mechanism but same therapeutic outcome  
- safety_profile: Better safety profile for this patient
- interaction_potential: Lower interaction risk with patient's other medications
- cost_considerations: Generic or more affordable options
- administration_advantages: Easier dosing or better compliance
- contraindication_avoidance: Specifically addresses the identified concern

For each alternative provide:
- Drug name and typical dose
- Why it's a suitable alternative
- Any remaining precautions
- Efficacy comparison to original drug

Rank alternatives by safety and efficacy for this patient profile."""

    # Drug safety analysis prompts
    SAFETY_ANALYSIS_SYSTEM = """You are analyzing drug safety profiles and risk assessment.

Focus on identifying potential hazards, contraindications, and safety monitoring requirements."""

    @staticmethod
    def safety_analysis_user(drug_combination: str, patient_data: str) -> str:
        return f"""Drug Combination: {drug_combination}
Patient Data: {patient_data}

Perform comprehensive safety analysis:

- interaction_risk_level: Overall risk level (High/Medium/Low/None)
- specific_interactions: Detailed interaction mechanisms
- clinical_significance: Real-world impact on patient care
- monitoring_protocol: Required lab tests, vital signs, symptoms to watch
- timeline_considerations: When interactions might occur (immediate, days, weeks)
- severity_outcomes: Potential consequences if interaction occurs
- mitigation_strategies: How to safely use combination if benefits outweigh risks
- patient_counseling_points: Key safety information for patient education

Provide evidence-based risk assessment with clinical recommendations."""

    # Recommendation synthesis prompts
    RECOMMENDATIONS_SYSTEM = """You are a senior clinical pharmacist providing comprehensive drug therapy recommendations.

Synthesize all drug analysis data into actionable clinical recommendations."""

    @staticmethod
    def recommendations_user(query: str, drug_analysis_data: str) -> str:
        return f"""Clinical Query: {query}

Drug Analysis Data: {drug_analysis_data}

Provide comprehensive clinical recommendations (5-6 sentences) covering:

- Primary safety concern and risk level
- Recommended dosage adjustments if needed
- Most suitable alternative if contraindicated
- Key monitoring requirements
- Patient counseling priorities
- Follow-up recommendations

Be clinically accurate and include specific actionable steps for healthcare providers."""
