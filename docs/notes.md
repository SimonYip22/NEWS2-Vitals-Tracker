# Vitals Tracker CLI - Notes

## Day 1: Input & Data Structure

**Goals**  
- Define which patient vitals to track (BP, HR, RR, Temp, O₂)  
- Implement robust input handling  
- Store patient data efficiently  

**Goals Explanation**  
- Track essential vitals for monitoring patient status  
- Ensure inputs are validated to avoid incorrect data  
- Use data structures that allow easy retrieval and future computation (alerts, trend visualization)  

**Plan / Thoughts**  
1. Create a Python dictionary keyed by patient ID for each set of vitals:
    - Choose names (keys) you’ll use consistently (e.g., "blood_pressure", "systolic", "diastolic", "heart_rate", "temperature", "oxygen_saturation").
    - Decide data types: BP as integers; HR as integer; Temp as float; O₂ as integer.
    - Nest BP inside a parent BP key so you don’t lose which number is which.
2. Prompt the user for each vital using `input()`, plan UX:
	1.	“Enter systolic BP (mmHg):”
	2.	“Enter diastolic BP (mmHg):”
	3.	“Enter heart rate (bpm):”
	4.  "Enter respiratory rate (bpm):"
	5.	“Enter temperature (°C):”
	6.	“Enter oxygen saturation (%):”  
3. Validate numerical ranges for each vital sign (safe ranges to enforce):
	- Systolic BP: 50–250
    - Diastolic BP: 30–150
	- Heart Rate: 30–220
	- Respiratory Rate: 5-60
	- Temperature (°C): 30.0–45.0
	- Oxygen Saturation (%): 50–100
4. Plan modular validation loop:
    - Show a prompt → try converting to the right type → if conversion fails or it’s out of range, show a helpful message and ask again → else return the value
    - Loop through each vital, validating and mapping to the dictionary.
    - One reusable function in your file can handle: prompt text, type (int/float), and min/max
5. Store each patient entry as a dictionary inside a list to allow multiple patient tracking  
    1.	Ask for systolic, validate.
	2.	Ask for diastolic, validate.
	3.	Ask for heart rate, validate.
	4. Ask for respiratory rate, validate.
	4.	Ask for temperature, validate.
	5.	Ask for oxygen saturation, validate.
	6.	Construct reading dict using the exact keys I chose in Task 1.
6. Manual test cases (run cases):
    1.  Happy path: 120 / 80, 72, 37.0, 98 → Should accept and print.
	2.	Bad type: “abc” for HR → Should reprompt, then accept a valid number.
	3.	Out of range: 500 for HR → Should reprompt.
	4.	Edge case: Minimum/maximum allowed values → Should accept.
7. Add a repeat loop to allow multiple sets of inputs for testing:
	- After printing the reading, ask: “Record another? (y/n)” and loop the whole collection.
	- If you do this, you’re ready for Day 2 (alerts and thresholds).

**Reflection**  
- Learned how to break a problem into modular functions.
- Understood try/except for input validation and numeric conversion.
- Practiced mapping user input to nested data structures.
- Realized the value of reusing functions instead of repeating code.
- Encountered challenges with loops, nested dictionaries, and type handling—but overcame them by thinking logically about what each step should do.

**Implement on day 2**
How we’ll use this on Day 2:
- Add alert thresholds (e.g., HR > 120, Temp ≥ 38.0).
- Program will flag abnormal values immediately after input or in a summary.
- Sketch CSV/JSON persistence and prep for trend visualization.



## Day 2: Tiered Alert Logic (based on NEWS2 ranges)

**Goals**
- Move beyond binary abnormal/normal flags by implementing tiered alerts (normal, mild, moderate, severe) for each vital sign.
- Implement conditional checks to flag abnormal readings
- Display clear alert messages for abnormal vitals immediately and/or in summary
- Make the program clinically interpretable by aligning thresholds with NEWS2 scoring ranges.
- Begin planning for persistence (CSV/JSON) and trend visualization

**Goals Explanation**
- Normal ranges are essential for deciding whether a patient’s reading is safe or concerning.
- Automated checks improve usability by instantly highlighting risks.
- Alerts must be informative but not overwhelming, balancing clinical accuracy with readability.
- Persistence and visualization prep ensures today’s work will connect seamlessly to future trend monitoring.
- Binary alerts (just “normal vs abnormal”) don’t differentiate between mild and life-threatening deviations.
- NEWS2 provides a validated framework for stratifying vitals into clinically meaningful severity levels.
- This improves the program’s realism, usability, and future scalability.


**Plan/Thoughts**
1.	Define thresholds for each vital, assign severity levels (Normal, Mild, Moderate, Severe) mapped from NEWS2 scores (0–3):
	- Systolic BP: Normal 111–219; Mild Alert 101–110, Moderate Alert 91–100, Severe Alert ≤90 or ≥220
	- Diastolic BP: Normal 60–90; Alert <60 or >90. High Alert <50 or ≥110. Not included in scoring just “⚠️ clinically abnormal” 
	- Heart Rate: Normal 51–90; Mild Alert 41–50 or 91–110, Moderate Alert 111–130, Severe Alert ≤40 or ≥131
	- Respiratory rate: Normal 12-20: Mild Alert 21-24, Moderate Alert 9-11, Severe Alert ≤8 or ≥25
	- Temperature (°C): Normal 36.1–38.0; Mild Alert 35.1–36.0 or 38.1–39.0, Moderate Alert ≥39.1, Severe Alert ≤35.0
	- Oxygen Saturation (%): Normal ≥96; Mild Alert 94–95, Moderate Alert 92–93, Severe Alert ≤91
	- Level of Consciousness: Normal "Yes"; Severe Alert "No/Unsure"
2.	Write a reusable function user_inputs():
	- Collects all vital inputs in a local dictionary instead of modifying a global dictionary.
	- Includes validation for numeric ranges (validate_input()), loops for error handling, and clear prompts.
	- Handles nested vitals like blood pressure (systolic and diastolic) separately.
	- Collects Level of Consciousness with specific yes/no/unsure validation.
	- Challenge: Needed multiple loops and careful indentation to handle nested inputs and validation.
3.	Write reusable function check_alert(vital_name, value):
	- Determines alert level for a single vital using defined thresholds.
	- Handles both simple tuples and lists of ranges (for severities that have two ranges).
	- Challenge: Learning tuple unpacking in loops and handling None as open-ended min/max values.
	- Amendment: Added type check for list vs tuple ranges to avoid logic errors.
4.	Write helper function get_alert_message(alert_level, alert_messages):
	- Returns a user-friendly message for the given alert level.
	- Returns default unknown alert message if no match is found.
	- Improvement: Simplified with if alert_level in alert_messages for readability.
5.	Implement main loop:
	- Iterates through all vitals in the dictionary returned from user_inputs().
	- Handles nested vitals (blood pressure) with a sub-loop.
	- Prints each reading along with its corresponding alert message.
	- Allows repeating input sessions without modifying the reference/global dictionary.
	- Challenge: Multi-level loops + dictionary iteration was mentally heavy, required careful attention to variable names and indentation.

**Reflection**
- Conceptual difficulty: Nested dictionaries, multiple loops, tuple vs list handling, None as a range boundary.
- Debugging/Amendments:
	- Changed user_inputs() to return a local dictionary rather than modifying the global vitals dictionary.
	- Learned to map blood pressure’s nested structure correctly into a dictionary (patient_vitals["Blood pressure"] = {"systolic": systolic, "diastolic": diastolic}).
	- Added robust input validation loops for both numbers and categorical inputs (yes/no/unsure for consciousness).
	- Adjusted check_alert() to handle multiple ranges and avoid errors when ranges were lists of tuples.
	- Separated alert computation (check_alert) from message display (get_alert_message) for modularity.
- Cognitive load: Multiple loops and function calls were challenging; visualizing the flow of data helped.
- Key learning points:
	- Modular design improves readability and makes debugging easier.
	- Tiered alert logic requires careful mapping from real-world clinical thresholds to code.
	- Returning local dictionaries is safer than modifying global state, and avoids accidental overwrites.
	- Clear separation between input collection, validation, and alert computation simplifies future extension (CSV logging, visualization).
- By the end of the day, the program:
	- Collects vitals in a reusable local dictionary.
	- Validates inputs robustly.
	- Computes alert levels correctly for all vitals.
	- Displays clear, clinically relevant alert messages.
	- Can be repeated for multiple patient entries without losing data.


**Next Steps/Day 3 Prep**
- Implement storage of multiple vitals readings in a session log.
- Start designing CSV/JSON persistence and timestamping.
- Consider plotting trends and highlighting worst alerts over time.
- Review unit tests and edge cases (boundary values, multiple simultaneous alerts).