# 🧪 Sample Runs - Clinically-Informed Vitals Tracker (CLI, Matplotlib and v2 FastAPI)

---

This document logs **test runs** illustrating how the tool handles user input, vital sign scoring, alert generation, and trend visualisation. Examples are separated by **CLI interactions (terminal-based app)** and **FastAPI endpoints (programmatic access)**, showing both the workflow for end-users and API consumers. Each example reflects **clinically-informed scoring and alerts**, ensuring outputs are interpretable and actionable.

---

## EXAMPLE 1: NORMAL READING

```bash
Patient vitals Monitoring App
=============================
1. Add new reading
2. View past readings
3. View trends
4. Exit

Select an option (1/2/3/4): 1

=== Enter Patient Vitals ===

Please enter patient vital signs

Enter blood pressure (systolic/diastolic):
  Systolic (mmHg): 120
  Diastolic (mmHg): 80

Enter heart rate (bpm): 75

Enter respiratory rate (bpm): 16

Enter temperature (°C): 37

Enter oxygen saturations (%): 98

Is the person fully awake and responsive? (yes/no/unsure): yes

Vitals recorded successfully!

Blood pressure (systolic): 120 → Normal (Score: 0)
Blood pressure (diastolic): 80 → Normal (Not scored)
Heart rate: 75 → Normal (Score: 0)
Respiratory rate: 16 → Normal (Score: 0)
Temperature: 37.0 → Normal (Score: 0)
Oxygen saturations: 98 → Normal (Score: 0)
Level of consciousness (fully awake and responsive?): Yes → Normal (Score: 0)
Total NEWS2 score: 0
Please enter full name: simon yip
Please enter date of birth (dd/mm/yy): 26/11/00
Existing patient found: ID 1
Add another reading? (y/n): y
```

---

## EXAMPLE 2: MILD ALERT

```bash
=== Enter Patient Vitals ===

Please enter patient vital signs

Enter blood pressure (systolic/diastolic):
  Systolic (mmHg): 110
  Diastolic (mmHg): 75

Enter heart rate (bpm): 95

Enter respiratory rate (bpm): 22

Enter temperature (°C): 38.5

Enter oxygen saturations (%): 95

Is the person fully awake and responsive? (yes/no/unsure): yes

Vitals recorded successfully!

Blood pressure (systolic): 110 → ⚠️ Mild Alert! → Continue monitoring (Score: 1)
Blood pressure (diastolic): 75 → Normal (Not scored)
Warning: No alert level matched Heart rate = 95
Heart rate: 95 → Normal (Score: 0)
Respiratory rate: 22 → ⚠️ Mild Alert! → Continue monitoring (Score: 1)
Temperature: 38.5 → ⚠️ Mild Alert! → Continue monitoring (Score: 1)
Oxygen saturations: 95 → ⚠️ Mild Alert! → Continue monitoring (Score: 1)
Level of consciousness (fully awake and responsive?): Yes → Normal (Score: 0)
Total NEWS2 score: 4
Please enter full name: simon yip
Please enter date of birth (dd/mm/yy): 26/11/00
Existing patient found: ID 1
Add another reading? (y/n): y
```

---

## EXAMPLE 3: MODERATE ALERT

```bash
=== Enter Patient Vitals ===

Please enter patient vital signs

Enter blood pressure (systolic/diastolic):
  Systolic (mmHg): 100
  Diastolic (mmHg): 70

Enter heart rate (bpm): 115

Enter respiratory rate (bpm): 25

Enter temperature (°C): 39.2

Enter oxygen saturations (%): 93

Is the person fully awake and responsive? (yes/no/unsure): yes

Vitals recorded successfully!

Blood pressure (systolic): 100 → ⚠️⚠️ Moderate Alert!! → Consider escalation (Score: 2)
Blood pressure (diastolic): 70 → Normal (Not scored)
Heart rate: 115 → ⚠️⚠️ Moderate Alert!! → Consider escalation (Score: 2)
Respiratory rate: 25 → ⚠️⚠️⚠️ Severe Alert!!! → Seek emergency help (Score: 3)
Temperature: 39.2 → ⚠️⚠️ Moderate Alert!! → Consider escalation (Score: 2)
Oxygen saturations: 93 → ⚠️⚠️ Moderate Alert!! → Consider escalation (Score: 2)
Level of consciousness (fully awake and responsive?): Yes → Normal (Score: 0)
Total NEWS2 score: 11
Please enter full name: simon yip
Please enter date of birth (dd/mm/yy): 26/11/00
Existing patient found: ID 1
Add another reading? (y/n): y
```

---

## EXAMPLE 4: SEVERE ALERT

```bash
=== Enter Patient Vitals ===

Please enter patient vital signs

Enter blood pressure (systolic/diastolic):
  Systolic (mmHg): 85
  Diastolic (mmHg): 55

Enter heart rate (bpm): 135

Enter respiratory rate (bpm): 28

Enter temperature (°C): 34.5

Enter oxygen saturations (%): 89

Is the person fully awake and responsive? (yes/no/unsure): no

Vitals recorded successfully!

Blood pressure (systolic): 85 → ⚠️⚠️⚠️ Severe Alert!!! → Seek emergency help (Score: 3)
Blood pressure (diastolic): 55 → ⚠️ Clinically abnormal (Not scored)
Heart rate: 135 → ⚠️⚠️⚠️ Severe Alert!!! → Seek emergency help (Score: 3)
Respiratory rate: 28 → ⚠️⚠️⚠️ Severe Alert!!! → Seek emergency help (Score: 3)
Temperature: 34.5 → ⚠️⚠️⚠️ Severe Alert!!! → Seek emergency help (Score: 3)
Oxygen saturations: 89 → ⚠️⚠️⚠️ Severe Alert!!! → Seek emergency help (Score: 3)
Level of consciousness (fully awake and responsive?): No/Unsure → ⚠️⚠️⚠️ Severe Alert!!! → Seek emergency help (Score: 3)
Total NEWS2 score: 18
Please enter full name: simon yip
Please enter date of birth (dd/mm/yy): 26/11/00
Existing patient found: ID 1
Add another reading? (y/n): n
```

---

## EXAMPLE 5: VIEWING PAST READINGS

```bash
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

--- 

## EXAMPLE 6: VIEWING TRENDS (ASCII)

```bash
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

---

## EXAMPLE 7: VIEWING TRENDS (MATPLOTLIB)

```bash
View another patient's trend? (y/n): y
Enter full name: simon yip
Please enter date of birth (dd/mm/yy): 26/11/00
Patient found. ID: 1. Retrieving vitals...
View trends as (1) ASCII or (2) matplotlib? 2
```

Matplotlib trend plots for patient Simon Yip (ID 1) successfully generated on 28/08/2025, and saved as 'Vitals-tracker-matplotlib.png'.
Plots include: news2_score, bp_systolic, bp_diastolic, heart_rate, respiratory_rate, temperature, oxygen_sats.

---

## EXAMPLE 8: v2 API ENDPOINTS

### Verify API Running

GET /Root
Response: 
```json
{"message": "Clinically-Informed Vitals Tracker API is running"}
```

### Add vitals via API

POST /add_vitals/
Curl:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/add_vitals/?patient_name=John%20Doe&dob=01%2F01%2F00' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "Blood pressure": {"systolic": 150, "diastolic": 100},
  "Heart rate": 120,
  "Respiratory rate": 28,
  "Temperature": 39.0,
  "Oxygen saturations": 88,
  "Level of consciousness (fully awake and responsive?)": "No"
}'
```
Response:
```json
{
  "patient_id": "1",
  "total_news2_score": 12,
  "alerts": {
    "Blood pressure": {
      "systolic": {
        "value": 150,
        "level": "Normal",
        "score": 0,
        "message": "Normal"
      },
      "diastolic": {
        "value": 100,
        "level": "Alert",
        "score": null,
        "message": "⚠️ Clinically abnormal"
      }
    },
    "Heart rate": {
      "value": 120,
      "level": "Moderate Alert",
      "score": 2,
      "message": "⚠️⚠️ Moderate Alert!! → Consider escalation"
    },
    "Respiratory rate": {
      "value": 28,
      "level": "Severe Alert",
      "score": 3,
      "message": "⚠️⚠️⚠️ Severe Alert!!! → Seek emergency help"
    },
    "Temperature": {
      "value": 39,
      "level": "Mild Alert",
      "score": 1,
      "message": "⚠️ Mild Alert! → Continue monitoring"
    },
    "Oxygen saturations": {
      "value": 88,
      "level": "Severe Alert",
      "score": 3,
      "message": "⚠️⚠️⚠️ Severe Alert!!! → Seek emergency help"
    },
    "Level of consciousness (fully awake and responsive?)": {
      "value": "No",
      "level": "Severe Alert",
      "score": 3,
      "message": "⚠️⚠️⚠️ Severe Alert!!! → Seek emergency help"
    }
  }
}
```

### Fetch past readings via API
GET /patient/1
Response:
```json
[
  {
    "patient_id": "1",
    "timestamp": "2025-09-09T19:08:16.423473",
    "news2_score": "0",
    "bp_systolic": "120",
    "bp_diastolic": "80",
    "heart_rate": "75",
    "respiratory_rate": "18",
    "temperature": "37.0",
    "oxygen_sats": "98",
    "loc": "Yes"
  },
  {
    "patient_id": "1",
    "timestamp": "2025-09-09T19:35:44.425752",
    "news2_score": "4",
    "bp_systolic": "108",
    "bp_diastolic": "78",
    "heart_rate": "105",
    "respiratory_rate": "22",
    "temperature": "38.5",
    "oxygen_sats": "95",
    "loc": "Yes"
  },
  {
    "patient_id": "1",
    "timestamp": "2025-09-09T19:56:03.020282",
    "news2_score": "14",
    "bp_systolic": "92",
    "bp_diastolic": "85",
    "heart_rate": "125",
    "respiratory_rate": "26",
    "temperature": "39.5",
    "oxygen_sats": "92",
    "loc": "No"
  },
  {
    "patient_id": "1",
    "timestamp": "2025-09-09T20:11:20.915030",
    "news2_score": "12",
    "bp_systolic": "150",
    "bp_diastolic": "100",
    "heart_rate": "120",
    "respiratory_rate": "28",
    "temperature": "39.0",
    "oxygen_sats": "88",
    "loc": "No"
  }
]
```

### Get trends via PNG of matplotlib plot 

GET /trends/1/png
Response:
Binary image file

### Get trends via JSON
GET /trends/1/json
```json
Response:
[
  {
    "patient_id": "1",
    "timestamp": "2025-09-09T19:08:16.423473",
    "news2_score": "0",
    "bp_systolic": "120",
    "bp_diastolic": "80",
    "heart_rate": "75",
    "respiratory_rate": "18",
    "temperature": "37.0",
    "oxygen_sats": "98",
    "loc": "Yes"
  },
  {
    "patient_id": "1",
    "timestamp": "2025-09-09T19:35:44.425752",
    "news2_score": "4",
    "bp_systolic": "108",
    "bp_diastolic": "78",
    "heart_rate": "105",
    "respiratory_rate": "22",
    "temperature": "38.5",
    "oxygen_sats": "95",
    "loc": "Yes"
  },
  {
    "patient_id": "1",
    "timestamp": "2025-09-09T19:56:03.020282",
    "news2_score": "14",
    "bp_systolic": "92",
    "bp_diastolic": "85",
    "heart_rate": "125",
    "respiratory_rate": "26",
    "temperature": "39.5",
    "oxygen_sats": "92",
    "loc": "No"
  },
  {
    "patient_id": "1",
    "timestamp": "2025-09-09T20:11:20.915030",
    "news2_score": "12",
    "bp_systolic": "150",
    "bp_diastolic": "100",
    "heart_rate": "120",
    "respiratory_rate": "28",
    "temperature": "39.0",
    "oxygen_sats": "88",
    "loc": "No"
  }
]
```

---