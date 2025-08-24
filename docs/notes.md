# Vitals Tracker CLI - Notes

## Day 1: Input & Data Structure

**Goals**  
- Define which patient vitals to track (BP, HR, Temp, O₂)  
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
	4.	“Enter temperature (°C):”
	5.	“Enter oxygen saturation (%):”  
3. Validate numerical ranges for each vital sign (safe ranges to enforce):
	- Systolic BP: 50–250
    - Diastolic BP: 30–150
	- Heart Rate: 30–220
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