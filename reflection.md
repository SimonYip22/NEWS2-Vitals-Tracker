# Final Reflection

## Project Overview

This project implements a **comprehensive Python-based CLI tool** for patient vitals monitoring, integrating **real-time NEWS2 scoring**, **tiered clinical alerts**, and **trend visualisation** using both ASCII and Matplotlib charts. The system tracks multiple vital signs, assigns **unique patient IDs** for anonymisation, and stores historical data in **CSV files**, enabling secure longitudinal tracking while adhering to **data privacy standards (GDPR)**.

Key technical achievements include **nested dictionary handling, modular architecture, robust input validation, CSV data persistence, ASCII/Matplotlib trend plotting, and clinical alert logic**, which together demonstrate both computational and healthcare domain expertise.

---

## Technical Learning Outcomes

Throughout the project, I developed both technical and conceptual skills:

- **Python Programming**:
    - Implemented modular functions (`user_inputs`, `validate_input`, `save_to_csv`, `load_from_csv`, `plot_ascii`, `plot_matplotlib`) for separation of concerns and maintainability.
    - Used nested dictionaries for structured vital sign storage and flattened them for CSV compatibility.
    - Applied list comprehensions, loops, and conditional logic for data validation, alert scoring, and plotting.

- **Clinical Logic Implementation**:
    - Implemented **tiered NEWS2 scoring** for vitals (Normal → Mild → Moderate → Severe), including exception handling for overlapping thresholds.
    - Automated alert messages for each vital sign, with special handling for nested BP values (systolic scored, diastolic flagged but not scored).

- **Data Handling & Privacy**:
    - Assigned **unique patient IDs** to anonymise data, aligning with GDPR and healthcare data protection requirements.
    - Stored historical readings in CSV with careful header management to prevent KeyErrors.
    - Ensured type consistency (str → float/int conversions) for both calculations and plotting.

- **Visualisation & UX**:
    - ASCII charts for terminal-based trend analysis, normalising values to proportional bar lengths.
    - Matplotlib plots with dual-axis for vitals + NEWS2, formatted timestamps, and data markers for clear presentation.
    - Improved CLI usability via right-aligned numeric outputs, horizontal separators, and clear prompts.

- **Testing & Debugging**:
    - Resolved CSV header mismatches and patient ID KeyErrors.
    - Corrected string-to-float conversion issues for plotting.
    - Fixed alert logic overlaps for diastolic BP.
    - Handled edge cases: missing readings, min=max values, and invalid input types.

---

## Design Choices

- **CLI Focus**: Command-line interface chosen for simplicity, rapid iteration, and suitability for both testing and clinical demonstration.
- **Patient ID Anonymisation**: Unique IDs decouple patient identity from data, enabling safe storage and analysis.
- **Tiered Alert Logic**: NEWS2 framework applied to multiple vitals with automated messages for clinical interpretation.
- **Dual Plotting Strategy**: ASCII for lightweight CLI checks, Matplotlib for portfolio-quality visualisation.
- **Modular Architecture**: Each functional component (input, validation, scoring, persistence, plotting) separated to improve maintainability and extensibility.
- **CSV-Based Persistence**: Chosen for tabular time-series data, enabling easy inspection, debugging, and plotting integration.

---

## Challenges & Solutions

- **Nested Dictionaries**: Flattened BP readings for CSV and plotting; maintained systolic/diastolic distinction.
- **Alert Overlaps**: Adjusted diastolic BP ranges to prevent misclassification and runtime errors.
- **Type Conversion for Plots**: Converted CSV string values to float for calculations and ASCII/Matplotlib plotting.
- **Data Privacy**: Integrated anonymised patient IDs to comply with GDPR and clinical data handling standards.
- **Timestamp Handling**: Required careful formatting to avoid overlapping x-axis labels in Matplotlib.
- **CSV Header Management**: Prepending headers to historical CSV files ensured existing patient data could be loaded safely.
- **User Input Validation**: Loops and type checking prevented incorrect numeric or categorical input, including Level of Consciousness.
- **CLI UX**: Designed readable outputs with alignment, separators, and prompts for multiple readings/trends.

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

1. **Integration of clinical logic and technical programming**: Demonstrates ability to bridge Python development with real-world medical reasoning.
2. **Complex CLI architecture** can effectively handle clinical logic, secure data management, and visualisation.
3. **Modular design and testing** are essential for maintainable, scalable healthcare software.
4. **Robust and privacy-conscious design**: Patient ID anonymisation ensures GDPR-compliant longitudinal data storage.
5. **Extensive debugging and edge-case handling**: Prepared for diverse patient datasets and user inputs.
6. **Portfolio-ready visualisations**: Both ASCII and Matplotlib trends highlight usability and professional presentation.
7. **Extensible architecture**: Modular functions and clear separation of concerns provide a strong foundation for AI/ML and front-end extensions.