from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class DrugAnalysis(BaseModel):
    """Structured output for LLM drug analysis"""
    interaction_severity: str  # Major, Moderate, Minor, None, Unknown
    contraindications: List[str] = []
    age_restrictions: List[str] = []
    dosage_forms: List[str] = []
    description: str = ""
    common_interactions: List[str] = []
    therapeutic_class: str = ""
    monitoring_required: List[str] = []

class DrugInfo(BaseModel):
    name: str
    description: str
    source_url: str = ""
    interaction_severity: Optional[str] = None
    contraindications: List[str] = []
    age_restrictions: List[str] = []
    dosage_forms: List[str] = []
    common_interactions: List[str] = []
    therapeutic_class: str = ""
    monitoring_required: List[str] = []

class ExtractedDrugInfo(BaseModel):
    drug_name: str
    dosage_amount: str = ""
    dosage_unit: str = ""
    frequency: str = ""
    route: str = ""
    duration: str = ""
    special_instructions: str = ""

class ResearchState(BaseModel):
    query: str
    extracted_drugs: List[str] = []  # Drugs extracted from medical text
    drug_info: List[DrugInfo] = []
    search_results: List[Dict[str, Any]] = []
    extracted_drug_details: List[ExtractedDrugInfo] = []
    analysis: Optional[str] = None
    interactions: List[Dict[str, Any]] = []
    dosage_recommendations: List[Dict[str, Any]] = []
    alternatives: List[Dict[str, Any]] = []
