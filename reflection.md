# Final Reflection — Clinically-Informed Vitals Tracker CLI & API

## Project Overview

Monitoring patient vitals in real time is a cornerstone of acute care. This project delivers a **comprehensive patient vitals monitoring system**, combining a **Python-based CLI** with a **FastAPI backend**, demonstrating both **clinical insight** and **professional-grade deployment skills**. The tool tracks multiple vital signs, calculates **NEWS2 scores**, generates **tiered clinical alerts**, and visualises trends via **ASCII and Matplotlib charts**. Patient data is stored in **CSV files** with **unique IDs** for **GDPR-compliant** longitudinal tracking.

The system was designed with **clinically-informed logic**: scoring, alert thresholds, and trend visualisations reflect **real-world prioritisation by healthcare professionals**, producing outputs that are **interpretable, actionable, and portfolio-ready**.

With **v2 FastAPI deployment live on Render** ([https://vitals-tracker-cli.onrender.com/docs](https://vitals-tracker-cli.onrender.com/docs)), users can access the API remotely, test endpoints, and retrieve JSON outputs for automated workflows. **GitHub Actions CI/CD** ensures that live endpoints remain reliable, validating `/Root`, `/add_vitals/`, `/patient/{id}`, and `/trends/{id}` endpoints continuously.

This tool lays the foundation for future integration into the **Early Warning System (EWS) project**, enabling **real-time clinical monitoring** and potential **AI/ML enhancements**.

Key technical achievements include **nested dictionary handling, modular CLI architecture, robust input validation, CSV persistence, dual visualisation pipelines, clinically-informed alert logic, and API integration with live deployment**, showcasing the combination of **software engineering and irreplaceable clinical insight**.

---

## CLI vs FastAPI: Skills Showcase

| Feature | CLI (v1) | FastAPI (v2 - Live on Render) |
|---------|-----------|-------------------------------|
| **User Interaction** | Command-line prompts, numeric & categorical inputs | JSON-based API requests (`GET /Root`, `POST /add_vitals/`, `GET /patient/{patient_id}`, `GET /trends/{patient_id}/png/`, `GET /trends/{patient_id}/json/`) |
| **Data Entry** | Manual typing via terminal | Scriptable input via HTTP requests or Swagger UI |
| **Visualisation** | ASCII bar charts; Matplotlib plots saved locally | API returns JSON data; Matplotlib plots generated on server as PNG |
| **Alerts & Scoring** | NEWS2 scoring, tiered alerts printed to console | NEWS2 scoring calculated server-side; alerts included in structured JSON response |
| **Persistence** | CSV storage with unique patient IDs | CSV storage leveraged for backend; data retrieval via endpoints |
| **Testing & CI/CD** | Manual verification of CLI workflows | Automated endpoint validation using GitHub Actions, ensuring production-readiness |
| **Clinical Insight** | Direct feedback to clinician user | Enables integration into EHRs, dashboards, or telemedicine apps |

---

## Design Choices

- **Clinician–Technologist Insight**: Encodes tacit clinical reasoning into scoring, alert messages, and trend interpretation.
- **Dual Interaction Modes (CLI vs API)**: CLI for rapid prototyping and clinical simulation; FastAPI for **live deployment, remote access, and integration potential**.
- **Tiered Alert Logic**: NEWS2 scoring thresholds (Normal → Mild → Moderate → Severe) with clear escalation advice.
- **Unique Patient IDs & GDPR Compliance**: Supports **GDPR-compliant longitudinal tracking** while anonymising sensitive data.
- **Dual Visualisation**: ASCII charts for immediate, lightweight terminal feedback; Matplotlib plots for professional, portfolio-ready visualisations.
- **Modular & Extensible Architecture**: Separation of input, validation, scoring, alerting, plotting, and persistence enables maintainable, testable, and extensible code for **future EWS integration**.  
- **CSV-Based Persistence**: Chosen for simplicity, compatibility, and inspection; ensures reproducible trend plotting.

---

## Technical Learning Outcomes

- **Python Programming**:
    - Modular functions (`user_inputs`, `validate_input`, `save_to_csv`, `load_from_csv`, `plot_ascii`, `plot_matplotlib`) for maintainability.
    - Nested dictionaries for structured vitals; flattened for CSV and plotting.
    - Loops, conditionals, and list comprehensions for validation, scoring, and plotting.
- **Clinical Logic Implementation**:
    - Implemented **tiered NEWS2 scoring** per clinical guidelines, including edge-case handling for overlapping thresholds.
    - Designed **alert messages and prioritisation logic**, including systolic vs diastolic BP handling.
    - Ensured outputs are **clinically interpretable**, not just algorithmically correct.
- **Data Handling & Privacy**:
    - Unique patient IDs anonymise data for longitudinal tracking, type-consistent CSV storage, GDPR alignment.
    - CSV storage maintains type consistency and prevents runtime errors, supporting **secure trend analysis**.
- **Visualisation & UX**:
    - ASCII trend charts for quick terminal feedback with normalised bar lengths.
    - Matplotlib plots with dual axes, formatted timestamps, and markers for portfolio presentation.
    - CLI output design (alignment, separators, prompts) ensures **readable and clinically meaningful data display**.
- **FastAPI & Live Deployment**:
    - Endpoints: `/Root`, `/add_vitals/`, `/patient/{id}`, `/trends/{id}/json`, `/trends/{id}/png`.
    - Live on Render: [https://vitals-tracker-cli.onrender.com/docs](https://vitals-tracker-cli.onrender.com/docs)
    - Swagger UI provides professional interface for testing and exploration.
    - Enables remote testing, reproducibility, and backend integration.
- **Testing & CI/CD**:
    - Automated GitHub Actions workflow validates both CLI functions and live API endpoints on push and weekly schedule.
    - Edge case testing for CSV persistence, alert logic, and plotting correctness.
    - Ensures **production-grade reliability** with multi-vital data inputs.

---

## Challenges & Solutions

- **Nested Dictionaries & CSV Flattening**: Preserved clinical semantics while enabling tabular storage and plotting.
- **Alert Threshold Overlaps**: Adjusted thresholds for systolic/diastolic BP to prevent misclassification.
- **Type Conversion & Input Validation**: Loops and type-checks for numeric and categorical inputs. Ensured numeric conversions for plotting and calculation; handled missing or extreme readings.
- **Timestamp Management**: Ensured non-overlapping axes in Matplotlib plots.
- **Data Privacy & GDPR**: Unique IDs and CSV management preserve confidentiality.
- **CLI UX**: Aligned output formatting, separators, and prompts for clarity and ease of interpretation.
- **FastAPI & Deployment**: Ensured modular separation from CLI; implemented CI/CD for live validation.

---

## Future Improvements

- **Integration with EWS Project**: Modular architecture and API backend ready to feed into hospital-wide Early Warning System.
- **Predictive Analytics**: ML models for patient deterioration detection.
- **EHR Integration**: Automatic input/output with electronic health records for real-time monitoring.
- **Web/GUI Front-End**: Interactive dashboards or Streamlit interfaces for hospitals, telemedicine, or mobile deployment.
- **Automated Notifications**: Trigger alerts for moderate/severe NEWS2 scores in real-time via SMS, email, or internal hospital messaging.
- **Expanded Vitals & Metrics**: Include additional physiological markers and composite scoring. 
- **Enhanced Unit Testing**: Cover edge cases, plotting consistency, CSV integrity.
- **Population Analytics**: Aggregate trends across patients for research or clinical auditing.  

---

## Key Takeaways

1. **Clinically-informed design** ensures NEWS2 scoring, alerts, and trends reflect real-world medical reasoning and prioritisation.
2. **Dual-mode interaction (CLI vs API)** demonstrates both rapid prototyping and production-ready backend skills.
3. **Live FastAPI deployment on Render** demonstrates production-ready deployment and professional portfolio impact.
4. **CI/CD validation with GitHub Actions** guarantee reliability for live multi-vital API endpoints.  
5. **Modular, maintainable architecture** enables future EWS integration and AI/ML extensions.
6. **Complex clinical data handling and trend visualisation** demonstrates irreplaceable clinician–technologist expertise.
7. **Portfolio-ready outputs** (ASCII + Matplotlib + JSON API) showcase usability, interpretability, and deployment.
8. **Bridges programming, clinical reasoning, and backend deployment**, highlighting the unique skill set for healthcare technology roles.

This project demonstrates the convergence of **advanced Python programming, clinical reasoning, data engineering, visualisation, API deployment, and live production CI/CD**, positioning the developer as an **irreplaceable clinician–technologist** capable of building healthcare tools with real-world impact.

---