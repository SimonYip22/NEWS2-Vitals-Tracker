#global dictionary of vitals for reference
vitals  = {
    "Blood pressure": {"systolic": None, "diastolic": None},

    "Heart rate": None,

    "Respiratory rate": None,

    "Temperature": None,

    "Oxygen saturations": None, 

    "Level of consciousness (fully awake and responsive?)": None,
}

thresholds = {
    "systolic": {"Normal": (111, 219), "Mild Alert": (101, 110), "Moderate Alert": (91, 100), "Severe Alert": [(None, 90), (220, None)]},
    
    "diastolic": {"Normal": (60, 90), "Alert": [(None, 59), (91, None)], "High Alert": [(None, 49), (110, None)]},

    "Heart rate": {"Normal": (51, 90), "Mild Alert": (41, 50), "Moderate Alert": (111, 130), "Severe Alert": [(None, 40), (131, None)]},
                   
    "Respiratory rate": {"Normal": (12, 20), "Mild Alert": (21, 24), "Moderate Alert": (9, 11), "Severe Alert": [(None, 8),(25, None)]},
                         
	"Temperature": {"Normal": (36.1, 38.0), "Mild Alert": [(35.1, 36.0), (38.1, 39.0)], "Moderate Alert": (39.1, None), "Severe Alert": (None, 35.0)},
	
    "Oxygen Saturations": {"Normal": (96, None), "Mild Alert": (94, 95), "Moderate Alert": (92, 93), "Severe Alert": (None, 91)},
	
    "Level of Consciousness (fully awake and responsive?)": {"Normal": "Yes", "Severe Alert": "No/Unsure"}
}

alert_messages = {
    "Normal": "Normal",

    "Mild Alert": "⚠️ Mild Alert! → Continue monitoring",

    "Moderate Alert": "⚠️⚠️ Moderate Alert!! → Consider escalation",

    "Severe Alert": "⚠️⚠️⚠️ Severe Alert!!! → Seek emergency help",

    "Alert": "⚠️ Clinically abnormal",

    "High Alert": "⚠️ Clinically abnormal"
}


#helper function for validating the users input
#modular function because does one thing, promting for input, converting in to a data type, and validating it, and it can be reused for any vital sign
def validate_input(prompt, min_value, max_value, data_type=int):
    while True: #loop until a valid input is entered
            try: #for handling potentiel ValueError
                value = data_type(input(prompt))
                if min_value <= value <= max_value: #is the input number within an acceptable range?
                    return value #if so, then the loop ends
                else:
                    print(f"Value must be between {min_value} and {max_value}. Please enter again.") #if outside of range, ask to enter again
            except ValueError:
                print("Invalid input. Please enter a number.") #if the input is not an integar, ValueError is thrown and will print this


#function for asking for patient inputs and mapping to dictionary
def user_inputs():
    patient_vitals = {} #local dictionary so we do not have to directly change the global vitals dictionary
    print("Please enter patient vital signs\n")
    
    #Blood pressure requires two values
    print("Enter blood pressure (systolic/diastolic):")
    systolic = validate_input("  Systolic (mmHg): ", 50, 250)
    diastolic = validate_input("  Diastolic (mmHg): ", 30, 150)
    patient_vitals["Blood pressure"] = {"systolic": systolic, "diastolic": diastolic} #Map inputs to local dictionary

    #Other vitals
    patient_vitals["Heart rate"] = validate_input("\nEnter heart rate (bpm): ", 30, 220)
    patient_vitals["Respiratory rate"] = validate_input("\nEnter respiratory rate (bpm): ", 5, 60)
    patient_vitals["Temperature"] = validate_input("\nEnter temperature (°C): ", 30, 45, float)
    patient_vitals["Oxygen saturations"] = validate_input("\nEnter oxygen saturations (%): ", 50, 100)


    #Level of consciousness needs if/elif/else for more than 2 options or need to validate inputs
    while True: #loop will continue to ask for a valid response that can be entered into dictionary
        loc = input("\nIs the person fully awake and responsive? (yes/no/unsure): ").strip().lower()
        if loc in ["yes", "y"]:
            patient_vitals["Level of consciousness (fully awake and responsive?)"] = "Yes"
            break
        elif loc in ["no", "n", "unsure"]: #explicitly checks for negative/uncertain responses 
            patient_vitals["Level of consciousness (fully awake and responsive?)"] = "No/Unsure"
            break
        else: #catches mistakes 
            print("Invalid input. Please enter either yes, no, or unsure.")
    
    return patient_vitals


#Checks which alert level the value belongs to
def check_alert(vital_name, value):
    vital_thresholds = thresholds[vital_name] #vital name is the key, value is the vital ranges (vital_thresholds is a dictionary of alert levels)

    for alert_level, level_range in vital_thresholds.items(): #looping through the ranges in the dictionary of alert levels
                                                              # alert_level = "Normal", "Mild Alert", ...
                                                              # level_range = (min, max) or [(min1,max1),(min2,max2)]
        if isinstance(level_range, list) #checking whether the range is either a tuple (min, max) or a list of tuples [(min1,max1),(min2,max2)]
            for min_val, max_val in level_range: #loop through each tuple in the list, tuple unpacking so you don't need to manually index
                if (min_val is None or value >= min_val) and (max_val is None or value <= max_val): # value is inside this range
                    return alert_level
        else: #if the range is a simple tuple
            min_val, max_val = level_range #defining the values in the tuple
            if (min_val is None or value >= min_val) and (max_val is None or value <= max_val):
                return alert_level #Once a match is found, the function immediately returns the corresponding alert level


#helper function to get alert message 
def get_alert_message(alert_level, alert_messages): #takes two inputs, the alert level, the dictionary mapping alert levels to the messages
    if alert_level in alert_messages: #checks to see if the alert level string is a key in the dictionary
        return alert_messages[alert_level] #if the alert level is in the alert_messages dictionary, then the alert message will be the one corresponding to the alert level key
    else:
        return f"⚠️ Unknown level: {alert_level}" #if potentially the alert level does not map to one in the messages dictionary, then it will return an automatic unknown message


while True:
    current_vitals = user_inputs()
    print("Here are the vital signs you have entered: ", current_vitals)

    for vital, user_value in current_vitals.items(): #loop through key-value pairs in dictionary of current user vitals
        
        if isinstance(user_value, dict): #is this a dictionary? This is to account for the nested dictionary for blood pressure.
            for bp_type, bp_value in user_value.items(): #loop through both systolic and diastolic bp in the nested dictionary
                alert_level = check_alert(bp_type, bp_value) #return the alert level for both
                alert_message = get_alert_message(alert_level, alert_messages) #alert message comes from helper function
                print(f"{vital} ({bp_type}): {bp_value} → {alert_message}")
        else: 
            alert_level = check_alert(vital, user_value) #if the value isnt a dictionary and is just a number, then we do not need to do a loop as there is no nested dictioanry
            alert_message = get_alert_message(alert_level, alert_messages)
            print(f"{vital}: {user_value} → {alert_message}")

    
    repeat = input("Record another set of values? (y/n): ").lower() #Allows recording multiple sets of vitals in one session
    if repeat != 'y': #loop breaks if user declines recording another set of vitals
        print("Goodbye!")
        break