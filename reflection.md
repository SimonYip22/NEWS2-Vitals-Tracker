# Final Reflection — Clinically-Informed Vitals Tracker CLI

## Project Overview

This project implements a **comprehensive Python-based CLI tool** for patient vitals monitoring, integrating **real-time NEWS2 scoring**, **tiered clinical alerts**, and **trend visualisation** using ASCII and Matplotlib charts. The system tracks multiple vital signs, assigns **unique patient IDs** for anonymisation, and stores historical data in **CSV files**, enabling secure longitudinal tracking while adhering to **data privacy standards (GDPR)**.

The scoring, alert logic, and trend visualisations were **designed using clinical reasoning**, ensuring outputs are not just computationally correct but **reflect real-world prioritisation and interpretation of vital signs by clinicians**. This makes the tool **clinically interpretable and relevant**, something a generic CS-focused developer could not replicate without healthcare expertise.

Key technical achievements include **nested dictionary handling, modular architecture, robust input validation, CSV data persistence, ASCII/Matplotlib trend plotting, and clinically-informed alert logic**, collectively demonstrating both programming and clinical insight.

---

## Design Choices

- **CLI Focus**: Command-line interface chosen for rapid prototyping and clarity, while emulating clinical workflows.
- **Patient ID Anonymisation**: Unique IDs decouple patient identity from vitals, supporting GDPR-compliant longitudinal tracking.
- **Tiered Alert Logic**: NEWS2 scoring reflects clinical escalation thresholds (Normal → Mild → Moderate → Severe).
- **Dual Plotting Strategy**: ASCII charts for quick monitoring; Matplotlib plots for professional, portfolio-ready visualisation.
- **Modular Architecture**: Input, validation, scoring, alerting, and plotting separated for maintainability, testing, and future integration.
- **CSV-Based Persistence**: Chosen for tabular time-series data, enabling easy inspection, debugging, and trend plotting.

---

## Technical Learning Outcomes

- **Python Programming**:
    - Developed modular functions (`user_inputs`, `validate_input`, `save_to_csv`, `load_from_csv`, `plot_ascii`, `plot_matplotlib`) to separate concerns and ensure maintainability.
    - Used nested dictionaries for structured storage of patient vitals; flattened them for CSV compatibility.
    - Applied loops, conditionals, and list comprehensions for validation, scoring, and plotting.

- **Clinical Logic Implementation**:
    - Implemented **tiered NEWS2 scoring** per standard clinical guidelines, for vitals (Normal → Mild → Moderate → Severe), including exception handling for overlapping thresholds.
    - Designed alert messages and thresholds to reflect actionable clinical insights.
    - Integrated systolic/diastolic BP handling, scoring systolic while flagging diastolic, consistent with clinical prioritisation.

- **Data Handling & Privacy**:
    - Assigned **unique patient IDs** to anonymise data, aligning with GDPR and healthcare data protection requirements.
    - Stored historical readings in CSV with careful header management to prevent KeyErrors and ensure consistent data loading..
    - Ensured type consistency (str → float/int conversions) for both calculations and plotting.

- **Visualisation & UX**:
    - ASCII charts for lightweight, terminal-based trend analysis, normalising values to proportional bar lengths.
    - Matplotlib plots for dual-axis trends (vitals + NEWS2), formatted timestamps, and data markers.
    - CLI improved for readability: right-aligned numbers, horizontal separators, and intuitive prompts.

- **Testing & Debugging**:
    - Resolved CSV header mismatches and patient ID KeyErrors.
    - Corrected string-to-float conversion issues for plotting.
    - Fixed alert logic overlaps for diastolic BP.
    - Handled edge cases: missing readings, min/max values, and invalid input types.


---

## Challenges & Solutions

- **Nested Dictionaries**: Flattened vitals for CSV and plotting while preserving clinical interpretation of systolic/diastolic BP.
- **Alert Threshold Overlaps**: Adjusted ranges to prevent misclassification and runtime errors.
- **Type Conversion Issues**: Ensured numeric conversions for both plotting and calculations.
- **Data Privacy & Anonymisation**: Integrated unique patient IDs to comply with GDPR and clinical standards.
- **Timestamp Formatting**: Required careful handling to avoid overlapping x-axis labels in Matplotlib plots.
- **CSV Header Management**: Prepending headers to historical CSV files ensured existing patient data could be loaded safely.
- **User Input Validation**: Loops and type checking for numeric/categorical inputs, including Level of Consciousness.
- **CLI UX Design**: Aligned output formatting, separators, and prompts to clearly display clinically meaningful trends.


---

## Future Improvements

- **Predictive Analytics**: Integrate ML models for early detection of patient deterioration.
- **EHR Integration**: Automated input/output from electronic health records for real-time monitoring.
- **Web/GUI Front-End**: Interactive dashboards for hospitals or telemedicine applications.
- **Automated Notifications**: Trigger alerts for moderate/severe NEWS2 scores in real-time.
- **Expanded Vitals & Metrics**: Include additional physiological markers and composite scoring for more granular monitoring.
- **Unit Testing Enhancements**: Extend automated tests for edge cases, plotting consistency, and CSV integrity.
- **Enhanced Data Analytics**: Aggregate population-level statistics and trends for research or clinical auditing.

---

## Key Takeaways

1. **Clinically-informed design** ensures scoring, alerts, and trend visualisation reflect real-world medical reasoning.
2. **Integration of programming and clinical logic** demonstrates the ability to bridge Python development with healthcare expertise.
3. **Complex CLI architecture** effectively manages input, scoring, secure data persistence, and visualisation.
4. **Modular design and testing** are essential for maintainable, scalable healthcare software.
5. **Robust and privacy-conscious data handling** ensures GDPR-compliant longitudinal tracking.
6. **Extensive debugging and edge-case handling** prepares the tool for diverse patient datasets and user inputs.
7. **Portfolio-ready visualisations**, both ASCII and Matplotlib trendshighlight usability, interpretation, and professional presentation.
8. **Modular, extensible architecture** lays the foundation for AI/ML integration and front-end development.