import csv #to read/write CSV files.
import os #to check if the file exists (so we know whether to write headers).
from pathlib import Path #Path is a convenient way to work with file paths. It lets you check if a file exists, create directories, or manipulate paths in a clean, platform-independent way.
from datetime import datetime #to timestamp each entry automatically.

#patient ID mapping file setup, we are keeping a record of patients
mapping_file = 'patient_mapping.csv' #file name 
if not Path(mapping_file).exists(): #creates a Path object for patient_mapping.csv if it doesn't exist, so only runs once to create the file and aloso write the first line
    with open(mapping_file, 'w', newline='') as f: #opens file for writing 'w'
                                                   #newline='' prevents extra blank lines in CSVs on some platforms
                                                   #with ... as f: is a context manager, which automatically closes the file after the block runs so no need for f.close().
        writer = csv.DictWriter(f, fieldnames=['patient_id','patient_name','dob']) #csv.DictWriter writes dictionaries to CSV, maps each dictionary key to a column in the CSV.
                                                                                   #fieldnames defines the column headers and the order of columns
                                                                                   #tells python that a dictionary will be written into the CSV with these keys
        writer.writeheader() #writes the first row of the CSV (patient_id,patient_name,dob), only runs if the file doesn't exist yet 
                             #after this, the file is ready to store patient mapping rows

#function to get patient ID, either return an existing ID already in the CSV, or create a new ID if it doesn't exist
def get_or_create_patient_id():
    patient_name = input("Please enter full name: ").strip().lower() #get patient info, name and dob
    dob = input("Please enter your date of birth (dd/mm/yy): ").strip()

    #read existing patients by turning CSV rows into dictionary for fast access 
    patient_map = {} #create dictionary to store the data in CSV
    with open(mapping_file, 'r', newline='') as f: #opens CSV file in read 'r' mode
        reader = csv.DictReader(f) #csv.DictReader(f) → Reads CSV rows as a python dictionary (row['patient_name'], etc.). key = fieldnames, values = cell values for that row
        for row in reader: #loops through each row and builds a dictionary mapping ID 
            patient_map[row['patient_id']] = (row['patient_name'], row['dob']) #in patient_map, key is the patient ID, value is a tuple including name and dob. Example: '1': ('simon yip', '01/01/1995')

    #check if patient exists by looping through the dictionary we created
    for patient_id, (name, existing_dob) in patient_map.items(): #loop through patient_map dictionary items
        if name == patient_name and existing_dob == dob: #if both name and dob match inputs, patient already exists (names can be the same but wont have same dob)
            print(f"Existing patient found: ID {patient_id}") #prints message saying the patient already exists in the symptom
            return patient_id #return existing patient ID

    #assign new ID if patient doesn't exist
    if patient_map: #if any patients already exist. Empty collections evaluate as False, non-empty collections as True. Same as: if len(patient_map) > 0:
        new_id = str(max(int(patient_id) for patient_id in patient_map.keys()) + 1) #turn all patient ID into integars, find the max integar which will be the most recent ID, then add 1 to it and turn it back into a string, this will be the new patient ID
    else: #if there are no patients yet
        new_id = '1' #first patient ID is 1

    #append new patient to the CSV
    with open(mapping_file, 'a', newline='') as f: #open file in append mode 'a', doesn't erase existing file like 'w' would, 'a' adds at the end. When you open the CSV in append mode, you need a writer object to format the dictionary correctly into a CSV row.
        writer = csv.DictWriter(f, fieldnames=['patient_id','patient_name','dob']) #use DictWriter to write Python dictionaries into CSV rows. fieldnames maps dictionary keys to csv columns, and values mapped into cells
        writer.writerow({'patient_id': new_id, 'patient_name': patient_name, 'dob': dob}) #.writerow writes a dictionary as one new row
                                                                                          #the new ID, patient name and dob will be entered as a new row

    print(f"New patient added: ID {new_id}") #prints confirmation to user
    return new_id #returns newly assigned ID, which can use to tag their vital signs 

# CSV schema: defines the columns in the CSV file
CSVNAMES = [  
    "patient_id", #optional identifier, lets track multiple patients
    "timestamp", #captures when reading was taken, ensures chronological order when analysing trends 
    "news2_score" #total news2 score
    "bp_systolic",
    "bp_diastolic",
    "heart_rate",
    "respiratory_rate",
    "temperature",
    "oxygen_sats",
    "loc", # "Yes" or "No/Unsure"
]

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

alert_scores = {
    "Normal": 0,
    "Mild Alert": 1,
    "Moderate Alert": 2,
    "Severe Alert": 3
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




#produces a flat dictionary instead of nested dictionary to enter into CSV columns as they don't accept nested dictionaries
def flatten_vitals(patient_vitals):
    flat_vitals = {}

    if "Blood pressure" in patient_vitals: #nested dictionary items get recorded into flat dictionary 
        flat_vitals["bp_systolic"] = patient_vitals["Blood pressure"]["systolic"] 
        flat_vitals["bp_diastolic"] = patient_vitals["Blood pressure"]["diastolic"]

    #.get so if value doesn’t exist (maybe a bug or incomplete input), it returns None instead of crashing program.
    flat_vitals["heart_rate"] = patient_vitals.get("Heart rate")
    flat_vitals["respiratory_rate"] = patient_vitals.get("Respiratory rate")
    flat_vitals["temperature"] = patient_vitals.get("Temperature")
    flat_vitals["oxygen_sats"] = patient_vitals.get("Oxygen saturations")
    flat_vitals["loc"] = patient_vitals.get("Level of consciousness (fully awake and responsive?)")
    
    return flat_vitals #new dictionary created for CSV



#function to store input vitals into csv file, which will store all vital sign readings, patient ID, and timestamp
def save_to_csv(patient_vitals, total_score, filename="vitals.csv"):
    flat_vitals = flatten_vitals(patient_vitals) #flatten the vitals dictionary 
    
    # Add a timestamp and patient ID for multiple patients
    flat_vitals["patient_id"] = get_or_create_patient_id()  #calls function to either return existing ID or create new ID, ensures each reading is linked to a patient
    flat_vitals["timestamp"] = datetime.now().isoformat() #gets current date and time the moment the fucntion runs, converts the timetsamp to a standard string suitable for CSV
    #add total NEWS2 score 
    flat_vitals["news2_score"] = total_score

    with open(filename, 'a', newline='') as f: #append the vitals csv file, adds rows without overwriting existing data
        writer = csv.DictWriter(f, fieldnames=CSVNAMES) #map dictionary keys defined in CSVNAMES to CSV column headers in fieldnames.
        writer.writerow(flat_vitals) #write a single row with the flat_vitals dictionary

while True: #loop to keep asking for another set of readings, vitals.csv will append new readings. 
    patient_vitals = user_inputs()
    save_to_csv(patient_vitals)
    if input("Add another reading? (y/n): ").strip().lower() != 'y':
        break



#function to return saved vitals from vitals.csv as a list of dictionaries
def load_from_csv(patient_id, filename="vitals.csv"):
    with open(filename, 'r', newline='') as f: #open vitals.csv in read mode
        reader = csv.DictReader(f) #Reads each line of the CSV and converts it into a dictionary.
        return [row for row in reader if row['patient_id'] == patient_id] #loops over all rows in the dictionry, filters so you only keep rows where the patient_id stored in the CSV matches the one you passed in
                                                                          #You get a list of dictionaries, one for every matching row.
                                                                          #If a patient has multiple vitals saved over time, you’ll get all their readings back.

#function prints recorded vitals neatly based on patient ID
def print_patient_vitals(patient_id): 
    patient_vitals = load_from_csv(patient_id) #calls csv reader which filters rows by patient_id, so returns a list of dictionaries that match the patient id

    if not patient_vitals: #checks whether length of list is >0
        print(f"No data found for patient {patient_id}") #if list empty, stop here and tell the user no data exists
        return

    print(f"\nVitals for patient {patient_id}:\n") #print header before looping through each row
    
    num_to_show = min(5, len(patient_vitals))  #len(patient_vitals) counts how many vital sign entries the patient has in total
                                               #min(..) picks the smaller number between 5 and the total entries.
    print(f"Patient has {len(patient_vitals)} recorded vital sign entries. Showing the last {num_to_show}:") #summary message shows how many entries, and then how many entries will be printed
    
    for row in patient_vitals[-num_to_show:]: #loops through each dictionary in the list (one vitals set = one row)
                                              # [-num_to_show:] does not reverse the order, just slices the last num_to_show elements, keeping their original order.
        print( 
            f"{row['timestamp']} | "
            f"BP: {row['bp_systolic']}/{row['bp_diastolic']} mmHg | "
            f"HR: {row['heart_rate']} bpm | "
            f"RR: {row['respiratory_rate']} bpm | "
            f"Temp: {row['temperature']} °C | "
            f"O2 sats: {row['oxygen_sats']} % | "
            f"Awake and fully responsive?: {row['loc']} | "
        )
    #prints a nicely formatted line showing all values in a readbale way

#function for finding patient ID when a patient wants to view past readings in the main menu
def find_patient_id():
    while True: #loops to keep asking for a name and dob until it finds a patient ID that matches
        patient_name = input("Enter full name: ").strip().lower()
        dob = input("Enter date of birth (dd/mm/yyyy): ").strip()

        matches = [] #list of matching patient ID
        with open(mapping_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['patient_name'] == patient_name and row['dob'] == dob:
                    matches.append(row['patient_id']) #add the corresponding patient id if the input name and dob matches 

        if not matches:
            print("No matching patient found. Please try again") #if there is no matching patient id in the csv file, this is printed
            continue
        elif len(matches) == 1: #if there is a patient id in the matches list
            print(f"Patient found. ID: {matches[0]}. Retrieving vitals...") #print the patient id for them to enter 
            return matches[0] #returns the string 

#while loop for continuous input, text-based interface
while True:
    print("\nPatient vitals Monitoring App")
    print("1. Add new reading")
    print("2. View past readings")
    print("3. Exit")

    choice = input("Select an option (1/2/3): ").strip()

    if choice == "1":
        while True: #loop for multiple readings without leaving main menu 
            patient_vitals = user_inputs()
            
            total_score = 0 #score counter for NEWS2 total for each set of vitals

            for vital, user_value in patient_vitals.items(): #loop through key-value pairs in dictionary of current user vitals
                if isinstance(user_value, dict): #is this a dictionary? This is to account for the nested dictionary for blood pressure.
                    for bp_type, bp_value in user_value.items(): #loop through both systolic and diastolic bp in the nested dictionary
                        alert_level = check_alert(bp_type, bp_value) #return the alert level for both
                        alert_message = get_alert_message(alert_level, alert_messages) #alert message comes from helper function
                        
                        if bp_type == "systolic": #only include systolic in the score
                            score = alert_scores[alert_level]
                            total_score += score
                            print(f"{vital} ({bp_type}): {bp_value} → {alert_message} (Score: {score})")
                        else: #diastolic
                            print(f"{vital} ({bp_type}): {bp_value} → {alert_message} (Not scored)")
                else: 
                    alert_level = check_alert(vital, user_value) #if the value isnt a dictionary and is just a number, then we do not need to do a loop as there is no nested dictioanry
                    alert_message = get_alert_message(alert_level, alert_messages)
                    score = alert_scores[alert_level]
                    total_score += score
                    print(f"{vital}: {user_value} → {alert_message} (Score: {score})")
            
            print(f"Total NEWS2 score: {total_score}")

            save_to_csv(patient_vitals, total_score) #enters all patient vitals and the newly calculated NEWS2 score into the csv function

            another_reading = input("Add another reading? (y/n): ").strip().lower()
            if another_reading != 'y':
                break #exit inner loop, return to main menu

    elif choice == "2":
        while True:
            patient_id = find_patient_id() #calls find_patient_id
            print_patient_vitals(patient_id) #prints findings for the patient id
            another_past_reading = input("View another past reading? (y/n): ").strip().lower()
            if another_past_reading != 'y':
                break

    elif choice == "3":
        print("Exiting program. Goodbye!")
        break
    else:
        print("Invalid option, please try again.")

