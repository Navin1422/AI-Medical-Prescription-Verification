# main.py

from dotenv import load_dotenv
from src.workflow import Workflow

load_dotenv()

def main():
    workflow = Workflow()
    print("Drug Interaction & Dosage Analysis Agent")

    while True:
        user_input = input("\n🔍 Enter drugs, patient age, or 'quit' to exit: ").strip()
        if user_input.lower() in {"quit", "exit"}:
            break
        if not user_input:
            continue

        # Example: workflow.run might accept structured queries like:
        # {"mode": "interaction", "drugs": ["A", "B"], "age": "65"}
        result = workflow.run(user_input)

        print(f"\n📊 Analysis Results for: {user_input}")
        print("=" * 60)

        if hasattr(result, "interactions"):
            print("⚠️ Drug Interactions:")
            for inter in result.interactions:
                print(f" • {inter['drug_pair']}: Severity={inter['interaction_severity']}, Notes={inter.get('notes', '—')}")

        if hasattr(result, "dosage"):
            print("\n💊 Dosage Recommendations:")
            print(f" • {result.dosage['drug_name']}: {result.dosage['recommended_dose']} ({result.dosage.get('notes', 'standard dosing')})")

        if hasattr(result, "alternatives"):
            print("\n🔄 Alternative Medications:")
            for alt in result.alternatives:
                print(f" • {alt['drug_name']} {alt['dose']}: {alt['reason']}")

        if hasattr(result, "extracted_info"):
            print("\n🧾 NLP-Extracted Drug Info:")
            for info in result.extracted_info:
                print(f" • {info}")

        if hasattr(result, "recommendations"):
            print("\n📝 Clinical Recommendations:")
            print(result.recommendations)

        print()

if __name__ == "__main__":
    main()
