# Call Analysis Application

A Streamlit-based application to analyze call conversations between debt collection agents and borrowers. The project evaluates compliance and call metrics, including profanity detection, privacy violations, and call quality metrics such as overtalk and silence.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Implementation Details](#implementation-details)
- [Visualization](#visualization)

---

## Project Overview
This project analyzes YAML/JSON conversation files and performs the following tasks:

1. **Profanity Detection**
   - Detects profane language used by agents and borrowers.
   - Supports pattern matching using Regex and machine learning approaches.

2. **Privacy and Compliance Violation**
   - Identifies sensitive information shared without proper verification (e.g., balance, account details).
   - Supports pattern matching (Regex) and LLM prompt-based approaches.

3. **Call Quality Metrics Analysis**
   - Calculates overtalk (simultaneous speaking) percentage per call.
   - Calculates silence percentage per call.
   - Visualizes these metrics for comparative analysis.

---

## Features
- Streamlit application with a user-friendly interface.
- File upload support for JSON or YAML conversation files.
- Dropdowns to select **entity type** and **analysis approach**.
- Conditional NLTK resource downloads for cloud deployment.
- Visualizations for call quality metrics (overtalk and silence percentages).

---


## Installation

1. Clone the repository:

```bash
git clone https://github.com/AdetGupta/call_analysis_app.git
cd call_analysis_app
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage

Run the Streamlit application:

```bash
streamlit run app/Home.py
```

1. Upload a JSON or YAML conversation file on the **Upload & Analyze** page (`1_📁_Analyze_File.py`).
2. Select the entity to analyze: Profanity or Privacy & Compliance Violation.
3. Select the approach: Pattern Matching, Machine Learning, or LLM.
4. Click **Analyze** to get results.
5. Optionally, check **Show File** to display the conversation content.
6. Switch to the **Visualizations** page (`2_📊_Visualizations.py`) to view charts for silence and overtalk metrics across calls.

---

## Implementation Details

- **Data Processing:** `app/data_processing/processor.py` parses conversation files and prepares them for analysis.
- **Profanity Detection:**  
  - Pattern Matching: `app/detections/profanity/pattern.py`  
  - Machine Learning: `app/detections/profanity/ml.py`
- **Privacy & Compliance Violation Detection:**  
  - Pattern Matching: `app/detections/privacy_violation/pattern.py`  
  - LLM-based detection: `app/detections/privacy_violation/llm.py`
- **Call Quality Metrics:** `app/metrics/call_quality.py` calculates overtalk and silence percentages.
- **Visualizations:** `app/visualizations/plots.py` generates charts for metrics.

---



