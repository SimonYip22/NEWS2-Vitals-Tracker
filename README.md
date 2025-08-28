# Vitals Tracker CLI
**Python | CLI Tool | NEWS2 Scoring | ASCII & Matplotlib Visualisation**

![Python](https://img.shields.io/badge/python-3.13-blue)
![Build Status](https://img.shields.io/github/actions/workflow/status/SimonYip22/vitals-tracker-cli/python-tests.yml?branch=main)
![License](https://img.shields.io/badge/license-MIT-green)
![Release](https://img.shields.io/github/v/release/SimonYip22/vitals-tracker-cli)
![Issues](https://img.shields.io/github/issues/SimonYip22/vitals-tracker-cli)
![Forks](https://img.shields.io/github/forks/SimonYip22/vitals-tracker-cli)
![Stars](https://img.shields.io/github/stars/SimonYip22/vitals-tracker-cli)
![Contributors](https://img.shields.io/github/contributors/SimonYip22/vitals-tracker-cli)

A complex **Python-based command-line interface (CLI) tool** for comprehensive patient vitals tracking, **real-time NEWS2 scoring,** and trend visualisation. Supports **ASCII charts** for lightweight terminal-based monitoring and **Matplotlib plots** for professional, portfolio-ready visualisations. Implements robust CSV-based data persistence with patient mapping and strong input validation for clinical reliability.

---


## TL;DR

- Enter patient vitals (BP, HR, RR, Temp, O₂, Level of Consciousness).
- Automatic **NEWS2 scoring** with **tiered alerts (Normal → Severe)**.
- Persist historical data in CSV for multiple patients.
- Retrieve past readings or plot trends in **ASCII or Matplotlib**.
- Modular, maintainable code for further integration or AI/ML expansion.

---


## Features

- **Full patient vitals capture**: Systolic/Diastolic BP, Heart Rate, Respiratory Rate, Temperature, Oxygen Saturations, Level of Consciousness.
- **NEWS2 scoring integrated with tiered alert levels**: Normal, Mild, Moderate, Severe.
- **Patient ID anonymisation**: Unique IDs ensure GDPR-compliant data handling
- **Data persistence**: Stores historical readings in CSV (vitals.csv) with patient mapping (patient_mapping.csv).
- **Trend visualisation**:
    - ASCII charts for lightweight CLI monitoring.
    - Matplotlib charts with dual-axis (vitals + NEWS2 score) for professional visualisation.
- **Robust input validation**: Ensures safe ranges, correct data types, and consistent nested data structures.
- **Comprehensive error handling**:
    - Fixed CSV header issues to avoid KeyErrors.
    - Type conversion for plotting prevents string/float errors.
    - Adjusted diastolic BP alert ranges to prevent overlapping thresholds.
- **Sample run included**: Demonstrates all alert scenarios, past readings, and plotting outputs.

---


## Technical Highlights

- Nested dictionary flattening for CSV compatibility and smooth plotting.
- **ASCII normalisation**: Values scaled proportionally to fixed-width bars for quick interpretation.
- **Matplotlib dual-axis plotting**: Overlay NEWS2 scores with vitals over time.
- **Timestamp formatting**: ISO timestamps converted and formatted for readability in plots.
- **Failsafes and edge-case handling**:
    - Minimum/maximum values handled in ASCII plots.
    - Alert thresholds with default 0 if no match found.

---


## Architecture & Implementation

**Key Components**
1.	**Data Persistence**
	- **save_to_csv()**: Writes flattened vitals with patient ID, timestamp, and NEWS2 score.
	- **load_from_csv()**: Retrieves historical readings for a given patient.
2.	**Patient Management**
	- **get_or_create_patient_id()**: Maps multiple patients to unique IDs. Patient ID anonymisation ensure GDPR-compliant data handling
	- **find_patient_id()**: CLI interface to locate patient ID via full name + DOB.
3.	**Input & Validation**
	- **user_inputs()**: Collects vitals in nested dictionary form.
	- **validate_input()**: Ensures numeric values are within safe clinical ranges.
	- Level of Consciousness handled as categorical input (Yes/No/Unsure).
4.	**Alert & Scoring**
	- **check_alert()**: Determines tiered alert level per NEWS2.
	- **get_alert_message()**: Converts alert level to user-friendly message.
	- **Scores summed for total NEWS2**; systolic BP counts in total, diastolic printed only.
5.	**Display**
    - **print_patient_vitals()**: Prints last 5 historical readings with alignment for readability.
	- **plot_ascii()**: ASCII-based trend visualisation for lightweight terminal output.
	- **plot_matplotlib()**: Professional Matplotlib plots with dual-axis for vitals + NEWS2.
6.	**CLI Loop**
    - **Options**: Add Reading, View Past Readings, View Trends, Exit.
    - Nested loops for multiple readings, plotting options, and patient queries.

---


## Future Improvements

- **AI/ML Integration**: Predictive models for deterioration, anomaly detection.
- **Web or GUI Front-End**: Interactive dashboards for hospitals or telemedicine.
- **EHR Integration**: Directly pull/push patient vitals for automated trend analysis.
- **Alerts & Notifications**: Automated escalation for moderate/severe NEWS2 scores.

---


## Quick Start

**Clone and run**:

```bash
git clone https://github.com/SimonYip22/vitals-tracker-cli.git
cd vitals-tracker-cli
python3 vitals_tracker.py
```

- Follow CLI prompts to add readings, view past vitals, or plot trends.
- Select ASCII for lightweight monitoring or Matplotlib for portfolio-ready visuals.

---


## Matplotlib Plot Example

![Vitals Tracker Matplotlib Plot](vitals-tracker-matplotlib.png)

- **The included `vitals-tracker-matplotlib.png` demonstrates a sample patient's vitals trends over time. It includes**:
    - **Line plots for key vital signs**: Systolic BP, Heart Rate, Respiratory Rate, Temperature, and Oxygen Saturations.
    - **Dual-axis plotting**: Vitals on the primary y-axis and NEWS2 scores on the secondary y-axis (red dashed line).
    - Markers at each data point for clarity.
    - Formatted timestamps on the x-axis for readability.
- This PNG exemplifies the professional plotting capabilities of the CLI tool and can be used in portfolio showcases or presentations to illustrate the trend visualisation functionality.

---


## Example session

```text
Patient vitals Monitoring App
=============================
1. Add new reading
2. View past readings
3. View trends
4. Exit

Select an option (1/2/3/4): 1
=== Enter Patient Vitals ===
Systolic BP (mmHg): 120
Diastolic BP (mmHg): 80
Heart Rate (bpm): 75
Respiratory Rate (bpm): 16
Temperature (°C): 37
Oxygen Saturation (%): 98
Fully awake and responsive? (Yes/No/Unsure): Yes
Vitals recorded successfully!
Total NEWS2 score: 0
```

```text
Patient vitals Monitoring App
=============================
1. Add new reading
2. View past readings
3. View trends
4. Exit

Select an option (1/2/3/4): 2
Enter full name: simon yip
Please enter date of birth (dd/mm/yy): 26/11/00
Patient found. ID: 1. Retrieving vitals...

Vitals for patient 1:

Patient has 4 recorded vital sign entries. Showing the last 4:
2025-08-28T00:11:30.266959 | BP: 120/ 80 mmHg | HR:  75 bpm | RR:  16 bpm | Temp:    37 °C | O2 sats:  98 % | Awake and fully responsive?: Yes | 
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2025-08-28T00:11:55.336599 | BP: 110/ 75 mmHg | HR:  95 bpm | RR:  22 bpm | Temp:  38.5 °C | O2 sats:  95 % | Awake and fully responsive?: Yes | 
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2025-08-28T00:12:25.660340 | BP: 100/ 70 mmHg | HR: 115 bpm | RR:  25 bpm | Temp:  39.2 °C | O2 sats:  93 % | Awake and fully responsive?: Yes | 
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2025-08-28T00:12:55.637678 | BP:  85/ 55 mmHg | HR: 135 bpm | RR:  28 bpm | Temp:  34.5 °C | O2 sats:  89 % | Awake and fully responsive?: No/Unsure | 
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
View another past reading? (y/n): n
```

```text
Patient vitals Monitoring App
=============================
1. Add new reading
2. View past readings
3. View trends
4. Exit

Select an option (1/2/3/4): 3
Enter full name: simon yip
Please enter date of birth (dd/mm/yy): 26/11/00
Patient found. ID: 1. Retrieving vitals...
View trends as (1) ASCII or (2) matplotlib? 1

news2_score trends:
2025-08-28T00:11:30.266959 |   0.0 | 

------------------------------------------------------------
2025-08-28T00:11:55.336599 |   4.0 | ###########

------------------------------------------------------------
2025-08-28T00:12:25.660340 |  11.0 | ##############################

------------------------------------------------------------
2025-08-28T00:12:55.637678 |  18.0 | ##################################################

------------------------------------------------------------

bp_systolic trends:
2025-08-28T00:11:30.266959 | 120.0 | ##################################################

------------------------------------------------------------
2025-08-28T00:11:55.336599 | 110.0 | ###################################

------------------------------------------------------------
2025-08-28T00:12:25.660340 | 100.0 | #####################

------------------------------------------------------------
2025-08-28T00:12:55.637678 |  85.0 | 

------------------------------------------------------------

bp_diastolic trends:
2025-08-28T00:11:30.266959 |  80.0 | ##################################################

------------------------------------------------------------
2025-08-28T00:11:55.336599 |  75.0 | ########################################

------------------------------------------------------------
2025-08-28T00:12:25.660340 |  70.0 | ##############################

------------------------------------------------------------
2025-08-28T00:12:55.637678 |  55.0 | 

------------------------------------------------------------

heart_rate trends:
2025-08-28T00:11:30.266959 |  75.0 | 

------------------------------------------------------------
2025-08-28T00:11:55.336599 |  95.0 | ################

------------------------------------------------------------
2025-08-28T00:12:25.660340 | 115.0 | #################################

------------------------------------------------------------
2025-08-28T00:12:55.637678 | 135.0 | ##################################################

------------------------------------------------------------

respiratory_rate trends:
2025-08-28T00:11:30.266959 |  16.0 | 

------------------------------------------------------------
2025-08-28T00:11:55.336599 |  22.0 | #########################

------------------------------------------------------------
2025-08-28T00:12:25.660340 |  25.0 | #####################################

------------------------------------------------------------
2025-08-28T00:12:55.637678 |  28.0 | ##################################################

------------------------------------------------------------

temperature trends:
2025-08-28T00:11:30.266959 |  37.0 | ##########################

------------------------------------------------------------
2025-08-28T00:11:55.336599 |  38.5 | ##########################################

------------------------------------------------------------
2025-08-28T00:12:25.660340 |  39.2 | ##################################################

------------------------------------------------------------
2025-08-28T00:12:55.637678 |  34.5 | 

------------------------------------------------------------

oxygen_sats trends:
2025-08-28T00:11:30.266959 |  98.0 | ##################################################

------------------------------------------------------------
2025-08-28T00:11:55.336599 |  95.0 | #################################

------------------------------------------------------------
2025-08-28T00:12:25.660340 |  93.0 | ######################

------------------------------------------------------------
2025-08-28T00:12:55.637678 |  89.0 | 

------------------------------------------------------------
```

- Full sample_run.txt included demonstrating normal → severe alerts, past readings, ASCII trends, and Matplotlib plots.

---


## Project Structure

```text
vitals-tracker-cli/
├── 01_miscellaneous/
├── notes.md
├── patient_mapping.csv
├── README.md
├── reflection.md
├── requirements.txt
├── sample_run.txt
├── test_vitals_tracker.py
├── vitals_tracker.py
├── vitals-tracker-matplotlib.png
├── vitals.csv
```

**Explanations**:
- **01_miscellaneous/** — Misc files, helper notes.
- **notes.md** — Daily development logs
- **patient_mapping.csv** — Maps patient names + DOB to IDs.
- **README.md** — Project documentation
- **reflection.md** - Final project reflection
- **requirements.txt** - Required matplotlib 
- **sample_run.txt** — Demonstrates all scenarios.
- **test_vitals_tracker.py** — Automated unit tests.
- **vitals_tracker.py** — Main CLI program.
- **vitals-tracker-matplotlib.png** — Example Matplotlib output.
- **vitals.csv** — Historical patient readings.

---


## Running Tests

```bash
pytest -v
```

**Tests include**:
- Validation of input ranges and data types.
- Correct alert level assignment for all vitals.
- Flattening nested dictionaries for CSV storage.
- ASCII & Matplotlib plotting functions with sample datasets.

---


## Disclaimer
- Educational and portfolio purposes only.
- Not a substitute for professional medical advice.
- For emergency concerns, contact NHS 111 or 999 immediately.