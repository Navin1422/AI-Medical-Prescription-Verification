from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from .models import ResearchState, DrugInfo, DrugAnalysis, ExtractedDrugInfo
from .firecrawl import FirecrawlService
from .prompts import DrugAnalysisPrompts
import os
import json
import re

class Workflow:
    def __init__(self):
        self.firecrawl = FirecrawlService()
        # Use OpenRouter-compatible ChatOpenAI config
        self.llm = ChatOpenAI(
            model="deepseek/deepseek-chat-v3-0324:free",
            temperature=0.1,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        self.prompts = DrugAnalysisPrompts()
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(ResearchState)
        graph.add_node("extract_drugs", self._extract_drugs_step)
        graph.add_node("research_drugs", self._research_drugs_step)
        graph.add_node("analyze_interactions", self._analyze_interactions_step)
        graph.add_node("generate_recommendations", self._generate_recommendations_step)
        
        graph.set_entry_point("extract_drugs")
        graph.add_edge("extract_drugs", "research_drugs")
        graph.add_edge("research_drugs", "analyze_interactions")
        graph.add_edge("analyze_interactions", "generate_recommendations")
        graph.add_edge("generate_recommendations", END)
        
        return graph.compile()

    def _extract_drugs_step(self, state: ResearchState) -> Dict[str, Any]:
        print(f"🔍 Extracting drug information from: {state.query}")
        
        # Check if query contains drug names or medical text
        if self._contains_medical_text(state.query):
            # Extract structured drug info using NLP
            messages = [
                SystemMessage(content=self.prompts.NLP_EXTRACTION_SYSTEM),
                HumanMessage(content=self.prompts.nlp_extraction_user(state.query))
            ]
            
            try:
                response = self.llm.invoke(messages)
                # Parse JSON response for structured drug info
                extracted_details = self._parse_drug_details(response.content)
                drug_names = [detail.drug_name for detail in extracted_details]
                
                return {
                    "extracted_drugs": drug_names,
                    "extracted_drug_details": extracted_details
                }
            except Exception as e:
                print(f"NLP extraction error: {e}")
                # Fallback to simple drug name extraction
                drug_names = self._extract_drug_names_simple(state.query)
                return {"extracted_drugs": drug_names}
        else:
            # Search for drug information based on query
            search_results = self.firecrawl.search_drug_info(state.query, num_results=3)
            
            all_content = ""
            for result in search_results.data if hasattr(search_results, 'data') else []:
                url = result.get("url", "")
                scraped = self.firecrawl.scrape_medical_page(url)
                if scraped:
                    all_content += scraped.markdown[:1500] + "\n\n"
            
            # Extract drug names from search results
            messages = [
                SystemMessage(content=self.prompts.DRUG_EXTRACTION_SYSTEM),
                HumanMessage(content=self.prompts.drug_extraction_user(state.query, all_content))
            ]
            
            try:
                response = self.llm.invoke(messages)
                drug_names = [
                    name.strip()
                    for name in response.content.strip().split("\n")
                    if name.strip()
                ]
                
                print(f"Extracted drugs: {', '.join(drug_names[:5])}")
                return {"extracted_drugs": drug_names}
            except Exception as e:
                print(f"Drug extraction error: {e}")
                return {"extracted_drugs": []}

    def _research_drugs_step(self, state: ResearchState) -> Dict[str, Any]:
        extracted_drugs = getattr(state, "extracted_drugs", [])
        if not extracted_drugs:
            print("⚠️ No extracted drugs found")
            return {"drug_info": []}
        
        print(f"🔬 Researching specific drugs: {', '.join(extracted_drugs[:5])}")
        
        drug_info_list = []
        for drug_name in extracted_drugs[:5]:  # Limit to 5 drugs
            # Search for specific drug information
            drug_search_results = self.firecrawl.search_drug_interactions(drug_name, num_results=2)
            
            if drug_search_results and hasattr(drug_search_results, 'data') and drug_search_results.data:
                result = drug_search_results.data[0]
                url = result.get("url", "")
                
                drug_info = DrugInfo(
                    name=drug_name,
                    description="",
                    source_url=url
                )
                
                # Scrape detailed drug information
                scraped = self.firecrawl.scrape_medical_page(url)
                if scraped:
                    content = scraped.markdown
                    analysis = self._analyze_drug_content(drug_name, content)
                    
                    drug_info.interaction_severity = analysis.interaction_severity
                    drug_info.contraindications = analysis.contraindications
                    drug_info.age_restrictions = analysis.age_restrictions
                    drug_info.dosage_forms = analysis.dosage_forms
                    drug_info.description = analysis.description
                    drug_info.common_interactions = analysis.common_interactions
                    drug_info.therapeutic_class = analysis.therapeutic_class
                    drug_info.monitoring_required = analysis.monitoring_required
                
                drug_info_list.append(drug_info)
        
        return {"drug_info": drug_info_list}

    def _analyze_interactions_step(self, state: ResearchState) -> Dict[str, Any]:
        print("🔍 Analyzing drug interactions")
        
        drug_info_list = getattr(state, "drug_info", [])
        if len(drug_info_list) < 2:
            return {
                "interactions": [],
                "dosage_recommendations": self._generate_dosage_recommendations(drug_info_list),
                "alternatives": []
            }
        
        interactions = []
        # Check interactions between all drug pairs
        for i, drug1 in enumerate(drug_info_list):
            for drug2 in drug_info_list[i+1:]:
                interaction_data = {
                    "drug_pair": f"{drug1.name} + {drug2.name}",
                    "interaction_severity": self._assess_interaction_severity(drug1, drug2),
                    "notes": f"Monitor for interactions between {drug1.therapeutic_class} and {drug2.therapeutic_class}"
                }
                interactions.append(interaction_data)
        
        dosage_recommendations = self._generate_dosage_recommendations(drug_info_list)
        alternatives = self._generate_alternatives(drug_info_list)
        
        return {
            "interactions": interactions,
            "dosage_recommendations": dosage_recommendations,
            "alternatives": alternatives
        }

    def _generate_recommendations_step(self, state: ResearchState) -> Dict[str, Any]:
        print("📝 Generating clinical recommendations")
        
        # Compile all analysis data
        drug_data = {
            "drugs": [drug.dict() for drug in getattr(state, "drug_info", [])],
            "interactions": getattr(state, "interactions", []),
            "dosage_recommendations": getattr(state, "dosage_recommendations", []),
            "alternatives": getattr(state, "alternatives", [])
        }
        
        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompts.recommendations_user(state.query, json.dumps(drug_data)))
        ]
        
        try:
            response = self.llm.invoke(messages)
            return {"analysis": response.content}
        except Exception as e:
            print(f"Recommendation generation error: {e}")
            return {"analysis": "Unable to generate recommendations due to processing error."}

    def _analyze_drug_content(self, drug_name: str, content: str) -> DrugAnalysis:
        """Analyze drug content using structured output"""
        structured_llm = self.llm.with_structured_output(DrugAnalysis)
        
        messages = [
            SystemMessage(content=self.prompts.DRUG_INTERACTION_SYSTEM),
            HumanMessage(content=self.prompts.drug_interaction_user(drug_name, content))
        ]
        
        try:
            analysis = structured_llm.invoke(messages)
            return analysis
        except Exception as e:
            print(f"Drug analysis error: {e}")
            return DrugAnalysis(
                interaction_severity="Unknown",
                contraindications=[],
                age_restrictions=[],
                dosage_forms=[],
                description="Analysis failed",
                common_interactions=[],
                therapeutic_class="Unknown",
                monitoring_required=[]
            )

    def _contains_medical_text(self, text: str) -> bool:
        """Check if text contains medical/prescription information"""
        medical_patterns = [
            r'\d+\s*mg', r'\d+\s*mcg', r'\d+\s*ml',
            r'take\s+\d+', r'twice\s+daily', r'once\s+daily',
            r'tablet', r'capsule', r'injection'
        ]
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in medical_patterns)

    def _parse_drug_details(self, response_content: str) -> List[ExtractedDrugInfo]:
        """Parse structured drug information from LLM response"""
        try:
            # Try to parse JSON response
            if '{' in response_content:
                json_str = response_content[response_content.find('{'):response_content.rfind('}')+1]
                drug_data = json.loads(json_str)
                
                if isinstance(drug_data, list):
                    return [ExtractedDrugInfo(**item) for item in drug_data]
                else:
                    return [ExtractedDrugInfo(**drug_data)]
            else:
                return []
        except Exception as e:
            print(f"JSON parsing error: {e}")
            return []

    def _extract_drug_names_simple(self, text: str) -> List[str]:
        """Simple drug name extraction fallback"""
        # This is a basic implementation - in reality, you'd use medical NER
        common_drugs = [
            'aspirin', 'ibuprofen', 'acetaminophen', 'metformin', 'lisinopril',
            'atorvastatin', 'omeprazole', 'warfarin', 'insulin', 'prednisone'
        ]
        found_drugs = []
        text_lower = text.lower()
        for drug in common_drugs:
            if drug in text_lower:
                found_drugs.append(drug.title())
        return found_drugs

    def _assess_interaction_severity(self, drug1: DrugInfo, drug2: DrugInfo) -> str:
        """Assess interaction severity between two drugs"""
        # Simple heuristic - in practice, use drug interaction databases
        if drug1.interaction_severity == "Major" or drug2.interaction_severity == "Major":
            return "Major"
        elif drug1.interaction_severity == "Moderate" or drug2.interaction_severity == "Moderate":
            return "Moderate"
        else:
            return "Minor"

    def _generate_dosage_recommendations(self, drug_info_list: List[DrugInfo]) -> List[Dict[str, Any]]:
        """Generate dosage recommendations for drugs"""
        recommendations = []
        for drug in drug_info_list:
            rec = {
                "drug_name": drug.name,
                "recommended_dose": "Follow prescriber instructions",
                "notes": "Standard dosing applies unless contraindicated"
            }
            if drug.age_restrictions:
                rec["notes"] = f"Age restrictions: {', '.join(drug.age_restrictions)}"
            recommendations.append(rec)
        return recommendations

    def _generate_alternatives(self, drug_info_list: List[DrugInfo]) -> List[Dict[str, Any]]:
        """Generate alternative medication suggestions"""
        alternatives = []
        for drug in drug_info_list:
            if drug.contraindications:
                alt = {
                    "drug_name": f"Alternative to {drug.name}",
                    "dose": "As prescribed",
                    "reason": f"Consider due to contraindications: {', '.join(drug.contraindications[:2])}"
                }
                alternatives.append(alt)
        return alternatives

    def run(self, query: str) -> ResearchState:
        initial_state = ResearchState(query=query)
        final_state = self.workflow.invoke(initial_state)
        return ResearchState(**final_state)
