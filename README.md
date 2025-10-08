# 💊 AI-Medical-Prescription-Verification System

A secure and intelligent system leveraging advanced Artificial Intelligence (AI) to automate the reading, interpretation, and clinical verification of medical prescriptions, significantly reducing dispensing errors and enhancing patient safety.

## 🌟 Overview

The traditional process of verifying prescriptions is prone to human error, particularly with illegible handwriting or complex drug-drug and drug-allergy interactions. This system addresses this critical challenge by using a multi-stage AI pipeline to ensure every prescription is **accurate, safe, and clinically appropriate** for the individual patient.

It acts as a **Real-Time Clinical Decision Support (CDS) tool** for pharmacists and healthcare professionals.

## ✨ Key Features

| Feature | Description | Technical Core |
| :--- | :--- | :--- |
| **Multimodal Extraction** | Accurately extracts text from digital, printed, and handwritten prescription images (including Sig codes). | OCR (Tesseract/PaliGemma), CNN for Handwriting Recognition (HWR). |
| **NLP Interpretation** | Parses and standardizes unstructured text into structured data (Drug Name, Dosage, Frequency, Route, Duration). | Named Entity Recognition (NER), Custom fine-tuned LLMs (e.g., MedGemma). |
| **Real-Time Safety Check**| Instantly flags critical errors against patient history and drug databases. | Rule-Based Systems, Predictive Analytics, Drug-Drug Interaction (DDI) API. |
| **Interaction & Allergy Alerts** | Detects potential adverse effects based on the patient's existing medication list and known allergies. | Clinical Decision Support Engine (CDSE) Integration. |
| **Dosage Validation** | Verifies that the prescribed dosage and frequency are within safe clinical guidelines (adjusted for age, weight, and renal function). | Parameterized Algorithms. |
| **Structured Output** | Provides a clear, color-coded report detailing the prescription, detected entities, and any verification alerts. | JSON/FHIR formatting. |
| **Audit Logging** | Compliant logging of all verification steps, decisions, and human overrides for regulatory and quality assurance purposes. | Secure Database (PostgreSQL/MongoDB). |

## 🏗️ Technical Architecture

The system follows a layered microservices architecture to ensure modularity, scalability, and compliance.

1.  **Input/Capture Layer:**
    * **Source:** Image Upload (e.g., JPEG, PNG, PDF), or direct EHR/e-Prescription feed.
    * **Component:** API Gateway for secure ingestion and patient anonymization.

2.  **Perception Layer (AI Core):**
    * **Image Processing:** Pre-processing (Noise Reduction, Contrast Enhancement).
    * **Text Extraction:** Utilizes OCR/HWR models to convert images into raw text.
    * **Text Analysis (NLP):** An LLM (e.g., fine-tuned Gemini/MedGemma) performs Entity Extraction (Drug name, quantity, dosage form, instructions).
    * **Output:** Structured JSON object (`Prescription_Data.json`).

3.  **Reasoning & Verification Layer:**
    * **Clinical Data Integration:** Secure connection (FHIR API) to Patient Medication Record (PMR) or Electronic Health Record (EHR) systems to fetch patient context (Allergies, Vitals, Comorbidities).
    * **Decision Engine:** Cross-references extracted data against:
        * Drug Master Database (NDC/RxNorm).
        * Interaction Checker.
        * Clinical Guidelines (Dosage ranges).
    * **Output:** `Verification_Report.json` (includes confidence scores and risk flags).

4.  **Interaction Layer:**
    * **Interface:** Web UI/API endpoint for displaying results.
    * **Features:** Color-coded discrepancy visualization, Pharmacist Override functionality, and Alert prioritization.

## 🛠️ Installation & Setup

### Prerequisites

* Python 3.10+
* Docker & Docker Compose (Recommended for deployment)
* Access to a **Clinical Drug Database API** (e.g., FDB, Medispan - *Note: License required*)
* LLM API Key (for the NLP module)

### Local Setup (using Docker Compose)

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/AI-Prescription-Verification.git](https://github.com/yourusername/AI-Prescription-Verification.git)
    cd AI-Prescription-Verification
    ```

2.  **Configure Environment:**
    Create a `.env` file in the root directory and add your keys/credentials:
    ```ini
    # .env file content
    LLM_API_KEY="your_llm_api_key"
    DRUG_DB_API_URL="[https://api.drugdatabase.com/v1](https://api.drugdatabase.com/v1)"
    EHR_FHIR_ENDPOINT="[https://fhir.ehr-system.com/r4](https://fhir.ehr-system.com/r4)"
    SECRET_KEY="your_secure_django_secret_key"
    ```

3.  **Build and Run Services:**
    ```bash
    docker-compose up --build -d
    ```

4.  **Access the Application:**
    The system will be available at `http://localhost:8000`.

## 🚀 Usage

The primary interface is a secure web portal.

### Workflow

1.  **Input:** User (e.g., Pharmacy Technician) uploads an image or text from a new prescription.
2.  **Processing:** The system extracts structured data and performs safety checks.
3.  **Review:** A **Verification Dashboard** displays the results:
    * ✅ **Green Light:** Verified, no significant alerts.
    * ⚠️ **Yellow Flag:** Minor warning (e.g., slightly high dosage for weight, needs review).
    * 🚨 **Red Alert:** Critical safety issue (e.g., Drug-Allergy interaction, toxic dosage, requires immediate pharmacist intervention).
4.  **Action:** Pharmacist reviews and either approves the prescription or contacts the prescriber.

## 🔒 Security & Compliance

***Disclaimer: This is a high-level overview. A production system requires exhaustive security measures.***

* **Data Encryption:** All data in transit (TLS 1.3) and at rest (AES-256) is encrypted.
* **Access Control:** Role-Based Access Control (RBAC) is enforced.
* **Compliance:** Designed with consideration for HIPAA (US), GDPR (EU), and other relevant data privacy regulations. Patient Health Information (PHI) handling adheres to strict isolation and anonymization protocols.

## 🤝 Contributing

We welcome contributions to improve the accuracy of our models and the robustness of the system. Please see `CONTRIBUTING.md` for details on our code of conduct and submission process.

## 📄 License

This project is licensed under the **Apache 2.0 License** - see the `LICENSE` file for details.

## 📞 Contact

* **Project Lead:** [Your Name/Team Name]
* **Email:** [your.contact@email.com]
* **Issues:** [Link to GitHub Issues]
