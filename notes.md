# Vitals Tracker CLI - Notes

## Day 1: Input & Data Structure

### Goals 
- Define which patient vitals to track (BP, HR, RR, Temp, O₂)  
- Implement robust input handling  
- Store patient data efficiently  

### Goals Explanation
- Track essential vitals for monitoring patient status  
- Ensure inputs are validated to avoid incorrect data  
- Use data structures that allow easy retrieval and future computation (alerts, trend visualization)  

### Plan / Thoughts 
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

### Reflection  
- Learned how to break a problem into modular functions.
- Understood try/except for input validation and numeric conversion.
- Practiced mapping user input to nested data structures.
- Realized the value of reusing functions instead of repeating code.
- Encountered challenges with loops, nested dictionaries, and type handling—but overcame them by thinking logically about what each step should do.

### Implement on day 2
How we’ll use this on Day 2:
- Add alert thresholds (e.g., HR > 120, Temp ≥ 38.0).
- Program will flag abnormal values immediately after input or in a summary.
- Sketch CSV/JSON persistence and prep for trend visualization.


---


## Day 2: Tiered Alert Logic (based on NEWS2 ranges)

### Goals
- Move beyond binary abnormal/normal flags by implementing tiered alerts (normal, mild, moderate, severe) for each vital sign.
- Implement conditional checks to flag abnormal readings
- Display clear alert messages for abnormal vitals immediately and/or in summary
- Make the program clinically interpretable by aligning thresholds with NEWS2 scoring ranges.
- Begin planning for persistence (CSV/JSON) and trend visualization

### Goals Explanation
- Normal ranges are essential for deciding whether a patient’s reading is safe or concerning.
- Automated checks improve usability by instantly highlighting risks.
- Alerts must be informative but not overwhelming, balancing clinical accuracy with readability.
- Persistence and visualization prep ensures today’s work will connect seamlessly to future trend monitoring.
- Binary alerts (just “normal vs abnormal”) don’t differentiate between mild and life-threatening deviations.
- NEWS2 provides a validated framework for stratifying vitals into clinically meaningful severity levels.
- This improves the program’s realism, usability, and future scalability.


### Plan/Thoughts
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

### Reflection
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


### Next Steps/Day 3 Prep
- Implement storage of multiple vitals readings in a session log.
- Start designing CSV/JSON persistence and timestamping.
- Consider plotting trends and highlighting worst alerts over time.
- Review unit tests and edge cases (boundary values, multiple simultaneous alerts).


---


## Day 3: Data Persistence (CSV/JSON) & NEWS2 Scoring Implementation

### Goals 
1.	Enable saving patient vitals into persistent storage.
2.	Implement NEWS2 scoring for each set of vitals.
3.	Allow retrieval of historical patient data.
4.	Handle nested vitals (blood pressure) and selective scoring.
5.	Test reading, writing, and calculations for reliability.

### Goals Explanation  
- **Persistence** ensures vitals are stored even after program exit.
- **NEWS2 scoring** converts alerts into a numeric score, allowing trend analysis.
- **Nested vitals handling** (BP systolic/diastolic) ensures correct scoring and display.
- **Historical retrieval** allows trend analysis, forming the foundation for visualisation.  
- **Testing** guarantees data is stored/retrieved correctly without corruption.  

### Plan / Thoughts  
- Why CSV (not JSON)?
	- Vitals are tabular, time-series data, making CSV the natural choice. Rows = measurements, columns = vital signs
	- Easy to open in Excel/Sheets for quick checks
	- Directly supported by pandas/matplotlib for plotting
	- Lightweight, human-readable
	- JSON is better for nested/complex data, but here CSV keeps things simple, efficient, and visualisation-ready.
	- Use **CSV** for human-readable storage, **JSON** for structured data.  
- Main helper functions implemented:
	- validate_input(prompt, min_value, max_value, data_type=int) → ensures valid numeric input for any vital.
	- user_inputs() → collects all patient vitals, including nested BP, and returns as dictionary.
	- check_alert(vital_name, value) → determines alert level based on thresholds.
	- get_alert_message(alert_level, alert_messages) → maps alert levels to human-readable messages.
	- flatten_vitals(patient_vitals) → converts nested dictionary (BP) to flat dictionary for CSV.
	- get_or_create_patient_id() → tracks multiple patients, assigns new IDs, or returns existing ID.
	- save_to_csv(patient_vitals, total_score, filename="vitals.csv") → stores vitals, patient ID, timestamp, and total NEWS2 score.
	- load_from_csv(patient_id, filename="vitals.csv") → retrieves historical vitals for a given patient.
	- print_patient_vitals(patient_id) → prints last few entries for a patient in a readable format.
	- find_patient_id() → allows user to locate patient ID via name + DOB.
- NEWS2 scoring:
	- Alert levels mapped to numeric scores: "Normal": 0, "Mild Alert": 1, "Moderate Alert": 2, "Severe Alert": 3.
	- Only systolic BP counted in total score; diastolic printed but not scored.
- Flatten nested dictionaries for CSV storage (bp_systolic, bp_diastolic).
- Added patient mapping (get_or_create_patient_id) to track multiple patients.
- Main menu CLI supports adding new readings and viewing past readings.
	- Option 1: Add new reading (with NEWS2 scoring, printing, saving).
	- Option 2: View past readings.
	- Option 3: Exit.
- Error handling: missing keys, invalid input, and proper CSV writing/reading.

### Reflections  
- Successfully implemented persistence using CSV.
- NEWS2 scoring and alert messages integrated with live input.
- Nested dictionary handling and flattening solved for CSV compatibility.
- Debugging took significant time due to code flow and scoring logic placement.
- Now have a fully working CLI system for input, scoring, and historical tracking.
- Took ~7-8 hours, longer than expected due to debugging and restructuring.


### Next Steps / Day 4 Prep  
- Focus: **Visualisation** of historical data.  
- Options:  
  - **ASCII charts** (fast, lightweight).  
  - **Matplotlib plots** (professional, portfolio-ready).  
- Ensure time/date stamps are included for trend plotting.  
- Decide which vitals are most useful to visualise (e.g., HR, BP, Temp).
- Consider plotting NEWS2 scores over time alongside vitals.
- Prepare sample_run.txt and test.py after full project is stable.


---


## Day 4: Trend Visualisation (ASCII/matplotlib)

### Goals
1.	Implement visualisation of historical patient data.
2.	Provide two approaches: ASCII charts (lightweight) and matplotlib charts (portfolio-ready).
3.	Display time-series trends for key vitals (HR, RR, Temp, SpO₂, BP systolic).
4.	Allow NEWS2 scores to be plotted alongside vitals for severity tracking.
5.	Test visualisation with sample patient datasets.
6.	Format timestamps for readability in plots (including day, month, year, time).
7.	Improve user experience with clearer CLI prompts, spacing, and separators.

### Goals Explanation
- ASCII charts: Quick, dependency-free way to visualise trends directly in the terminal. Good for simple testing and debugging.
- Matplotlib charts: Industry-standard plotting for clean, professional, publication-ready visuals. Essential for portfolio demonstration.
- Vital trend tracking: Clinicians need to see how a patient’s vitals evolve over time, not just single values.
- NEWS2 score plots: Helps highlight deterioration or improvement. Graphical context adds clinical meaning to numeric scores.
- Timestamp formatting: Improves readability and avoids overlapping x-axis labels in plots.
- Testing with sample data: Ensures system works with both small and larger datasets, avoids runtime errors in real use.
- UX improvements: Added horizontal dividers and spacing for easier reading of multiple vitals in CLI.

### Plan / Thoughts
- Implementation order:
	1.	Load patient history from CSV.
	2.	Extract relevant columns (timestamp, HR, RR, Temp, SpO₂, BP systolic, NEWS2).
	3.	Build ASCII chart function for quick terminal trend view.
	4.	Implement matplotlib visualisation for polished plots.
	5.	Integrate timestamp formatting using matplotlib.dates.DateFormatter("%d-%b-%y %H:%M").
	6.	Ensure both plotting functions handle missing or insufficient data (<2 readings).
- ASCII chart options:
	- Use a fixed-width proportional scale (e.g., # marks) for trends.
	- Normalises values between min and max for each vital.
	- Includes timestamp and actual numeric value for reference.
	- Divider line ("-" * 60) for clarity between readings.
	- Suitable for text-only environments, quick previews.
- Matplotlib:
	- Line plots for each vital with markers at each data point.
	- Dual-axis for vitals + NEWS2 score to show correlation.
	- Combined legend for clarity.
	- Rotation of x-axis labels and tight_layout() to prevent overlap.
- Design choices:
	- Only plot systolic BP (matches NEWS2 scoring rules).
	- Diastolic BP included in ASCII charts but marked as non-scoring.
	- Handle missing values gracefully (skip or set default).
- Testing strategy:
	- Dummy dataset with 10–15 readings per patient.
	- Independent testing of plot_ascii and plot_matplotlib.
	- Check timestamp alignment, value normalization, and correct labelling.


### Additions / Changes Made Today
- Added horizontal separators ("-" * 70) after each CLI output line for improved readability.
- Aligned numeric outputs using right-alignment (:>3 for most vitals, :>5 for temperature) to make columns visually consistent.
- Added timestamp formatting in Matplotlib to show day-month-year-hour:minute (%d-%b-%y %H:%M).
- Updated CLI prompts for clarity (e.g., Add another reading? (y/n)), spacing, and messages confirming patient vitals saved.
- Implemented dual plotting for NEWS2 scores alongside vitals in Matplotlib.
- Added checks for patients with insufficient readings to prevent plotting errors.
- Flattened nested dictionaries for CSV compatibility and smooth integration with plotting functions.
- Improved handling of Level of Consciousness input in CLI with validation (yes/no/unsure) and mapping to Yes/No/Unsure.

### Difficulties / Debugging / Extra Challenges
- Nested dictionaries for blood pressure: Needed special handling to flatten for CSV and plotting.
- Timestamp formatting in Matplotlib: Required importing matplotlib.dates and using DateFormatter to avoid overlapping labels.
- Handling min=max in ASCII plots: Added conditional to avoid division by zero when all readings for a vital are equal.
- Dual-axis plotting: Combining NEWS2 score with vitals required separate axes (twinx) and merging legends.
- CLI alignment issues: Right-aligning numeric values and leaving text like loc unaligned required careful formatting with :>3 and :>5.
- Input validation: Validating floats (temperature) vs integers (other vitals) needed separate handling in validate_input.
- ASCII plot normalization and scaling: Normalised values proportionally to plot_width to make trends visually interpretable.
- Flattened vitals for CSV/plotting: Ensured that nested vitals were flattened consistently for smooth integration with ASCII and Matplotlib.
- Debugging CSV read/write: Ensuring patient ID mapping worked correctly and new readings appended properly.
- Mental fatigue: Iterative testing and correcting minor formatting and plotting bugs was draining; required external help for timestamp formatting and final alignment.

### Enhancements from Sample Run Preparation
- Created a comprehensive sample_run.txt demonstrating all scenarios: normal, mild, moderate, severe alerts, past readings, ASCII trends, and Matplotlib trends.
- CSV header issues: Earlier patient_id KeyError required prepending correct CSV headers to existing files to ensure historical data could be loaded.
- Type conversion for ASCII plotting: Values read from CSV were strings; converting to float for plotting fixed TypeError: unsupported operand type(s) for -: 'str' and 'str'.
- Timestamp formatting in Matplotlib: Required importing matplotlib.dates and using DateFormatter to avoid overlapping x-axis labels.
- Diastolic BP alert threshold overlap: Original alert tuples for diastolic BP had overlapping ranges, which caused some normal values (e.g., 75 mmHg) to not match any tuple, resulting in runtime errors. Fixed by adjusting the thresholds and implementing a failsafe to return 0 (Normal) when no tuple matches.

### Reflections
- Persistence paid off: CLI input, CSV storage, ASCII and Matplotlib visualisation now work seamlessly.
- ASCII charts are useful for quick terminal checks; Matplotlib plots are polished and suitable for portfolio showcase.
- Data persistence and trend visualisation make the tool clinically interpretable.
- Debugging timestamp formatting and dual-axis plotting was unexpectedly tricky.
- UX improvements in CLI (spacing, dividers, clear prompts) greatly improved readability and usability.


---

