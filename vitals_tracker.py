import csv #to read/write CSV files.
import os #to check if the file exists (so we know whether to write headers).
from pathlib import Path #Path is a convenient way to work with file paths. It lets you check if a file exists, create directories, or manipulate paths in a clean, platform-independent way.
from datetime import datetime #to timestamp each entry automatically.
import matplotlib.pyplot as plt #import external library matplotlib and name it plt
import matplotlib.dates as mdates #formats the x-axis dates nicely in the matplotlib

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

#function for making sure dob is valid
def get_valid_dob():
    while True:
        dob_input = input("Please enter date of birth (dd/mm/yy): ").strip()
        try:
            dob = datetime.strptime(dob_input, "%d/%m/%y").date()
            return dob.strftime("%d/%m/%y")  # consistently store as dd/mm/yy
        except ValueError:
            print("Invalid format. Please enter the date in dd/mm/yy format (e.g., 26/11/00).")


#function to get patient ID, either return an existing ID already in the CSV, or create a new ID if it doesn't exist
def get_or_create_patient_id():
    patient_name = input("Please enter full name: ").strip().lower() #get patient info, name and dob
    dob = get_valid_dob()

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
    "news2_score", #total news2 score
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
    "bp_systolic": {"Normal": (111, 219), "Mild Alert": (101, 110), "Moderate Alert": (91, 100), "Severe Alert": [(None, 90), (220, None)]},
    
    "bp_diastolic": {"Normal": (60, 90), "Alert": [(50, 59), (91, 109)], "High Alert": [(None, 49), (110, None)]},

    "Heart rate": {"Normal": (51, 90), "Mild Alert": (41, 50), "Moderate Alert": (111, 130), "Severe Alert": [(None, 40), (131, None)]},
                   
    "Respiratory rate": {"Normal": (12, 20), "Mild Alert": (21, 24), "Moderate Alert": (9, 11), "Severe Alert": [(None, 8),(25, None)]},
                         
	"Temperature": {"Normal": (36.1, 38.0), "Mild Alert": [(35.1, 36.0), (38.1, 39.0)], "Moderate Alert": (39.1, None), "Severe Alert": (None, 35.0)},
	
    "Oxygen saturations": {"Normal": (96, None), "Mild Alert": (94, 95), "Moderate Alert": (92, 93), "Severe Alert": (None, 91)},
	
    "Level of consciousness (fully awake and responsive?)": {"Normal": "Yes", "Severe Alert": "No/Unsure"}
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
    if vital_name == "Level of consciousness (fully awake and responsive?)":
        if value == "Yes":
            return "Normal"
        else:  # "No" or "No/Unsure"
            return "Severe Alert"
    
    vital_thresholds = thresholds[vital_name] #vital name is the key, value is the vital ranges (vital_thresholds is a dictionary of alert levels)

    for alert_level, level_range in vital_thresholds.items(): #looping through the ranges in the dictionary of alert levels
                                                              # alert_level = "Normal", "Mild Alert", ...
                                                              # level_range = (min, max) or [(min1,max1),(min2,max2)]
        if isinstance(level_range, list): #checking whether the range is either a tuple (min, max) or a list of tuples [(min1,max1),(min2,max2)]
            for min_val, max_val in level_range: #loop through each tuple in the list, tuple unpacking so you don't need to manually index
                if (min_val is None or value >= min_val) and (max_val is None or value <= max_val): # value is inside this range
                    return alert_level
        else: #if the range is a simple tuple
            min_val, max_val = level_range #defining the values in the tuple
            if (min_val is None or value >= min_val) and (max_val is None or value <= max_val):
                return alert_level #Once a match is found, the function immediately returns the corresponding alert level

    # If nothing matched
    print(f"Warning: No alert level matched {vital_name} = {value}")
    return "Normal"  # Default fallback


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

    file_exists = Path(filename).exists() #checks if CSV file exists 

    # If file exists, check the first line
    if file_exists:
        with open(filename, 'r', newline='') as f:
            first_line = f.readline().strip() #reads just the first line of the file.
        correct_header = ','.join(CSVNAMES) #turns that CSVNAMES list into a single string separated by commas
        if first_line != correct_header: #if the first line isn't correct
            # Prepend correct header without losing existing data
            with open(filename, 'r', newline='') as f:
                rows = f.readlines() #Opens the file again in read mode and reads all lines into a list rows.
            rows.insert(0, correct_header + '\n') #	Inserts the correct header as the very first line in the list of rows.
                                                  # + '\n' ensures the header ends with a newline, so the CSV formatting stays correct.
            with open(filename, 'w', newline='') as f: #Opens the file in write mode, which overwrites the current file.
                f.writelines(rows) #Writes all lines from rows back to the file, now with the correct header at the top.


    with open(filename, 'a', newline='') as f: #append the vitals csv file, adds rows without overwriting existing data
        writer = csv.DictWriter(f, fieldnames=CSVNAMES) #map dictionary keys defined in CSVNAMES to CSV column headers in fieldnames.

        if not file_exists:   # only write header if file is new
            writer.writeheader() #if it does not exist (first ever run), we must write the header before the first row of data.  
        
        writer.writerow(flat_vitals) #write a single row with the flat_vitals dictionary



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
            f"BP: {row['bp_systolic']:>3}/{row['bp_diastolic']:>3} mmHg | "
            f"HR: {row['heart_rate']:>3} bpm | "
            f"RR: {row['respiratory_rate']:>3} bpm | "
            f"Temp: {row['temperature']:>5} °C | "
            f"O2 sats: {row['oxygen_sats']:>3} % | "
            f"Awake and fully responsive?: {row['loc']} | "
        )
        print("-" * 140)
    #prints a nicely formatted line showing all values in a readbale way


#function for finding patient ID when a patient wants to view past readings in the main menu
def find_patient_id():
    while True: #loops to keep asking for a name and dob until it finds a patient ID that matches
        patient_name = input("Enter full name: ").strip().lower()
        dob = get_valid_dob()

        matches = [] #list of matching patient ID
        with open(mapping_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['patient_name'].strip().lower() == patient_name and row['dob'].strip() == dob:
                    matches.append(row['patient_id']) #add the corresponding patient id if the input name and dob matches 

        if not matches:
            print("No matching patient found. Please try again") #if there is no matching patient id in the csv file, this is printed
            continue
        elif len(matches) == 1: #if there is a patient id in the matches list
            print(f"Patient found. ID: {matches[0]}. Retrieving vitals...") #print the patient id for them to enter 
            return matches[0] #returns the string 


#function for plotting the vital trends using ASCII
def plot_ascii(patient_id): #plotting based on input of patient_id
    patient_vitals_history = load_from_csv(patient_id) #defined list of dictionaries output from the load_from_csv function
    
    if len(patient_vitals_history) < 2:
        print("Not enough data to plot trends (need at least 2 readings).") #only plot vitals if there is 2 or more entries to show a trend
        return 
    
    #list includes keys that only have numerical values.
    numerical_vitals = ["news2_score", "bp_systolic", "bp_diastolic", "heart_rate", "respiratory_rate", "temperature", "oxygen_sats"]

    #outer loop picks which vital to process, and the list comprehension goes through all readings (all dictionaries) to collect that vital’s values.
    for vitals in numerical_vitals: #loops over each vital sign in the list of vitals we have made
        values = [float(readings[vitals]) for readings in patient_vitals_history] #list comprehension loops through every dictionary in the list patient_vitals_history and collects the values for that specific vital into a new list:
                                                                                  #make sure all strings are converted to floats/int
        min_val = min(values)
        max_val = max(values)
        #The range is how spread out your values are. It’s used to normalise each value between 0 and 1 (or 0% to 100%).
        range_val = max_val - min_val if max_val != min_val else 1  #gives you total spread of values
                                                                    #avoid division by zero, defaults to 1 if min and max values are the same
                                                                    #avoids the crash and just produces bars of the same length for all readings
        plot_width = 50

        timestamps = [readings["timestamp"] for readings in patient_vitals_history] #creates a list of timestamps from all patient readings

        print(f"\n{vitals} trends:") #prints name of the vital
        for t, v in zip(timestamps, values): #zip(timestamps, values) pairs up elements from both lists positionally.
                                            #for loop so each timestamp is matched to its corresponding vital reading
            num_hashes = int((v - min_val) / range_val * plot_width) #Normalises the value relative to the min and max: (v - min_val) / range_val → a number between 0 and 1.
                                                                    #Data normalisation means different vitals with different units can be proportionatly represented in the ASCII plot
                                                                    #v - min_val shifts the smallest reading to 0
                                                                    #divides by range_val to normalise values and have them all scale between 0 and 1.
                                                                    #Multiplies by plot_width to scale it to the number of # characters to print.
                                                                    #int() converts to an integer, because we can only print whole characters.
            print(f"{t} | {v:>5} | {'#' * num_hashes}") #prints timestamp, numeric value, and bar
                                              #v:>5 means right align the value 'v' (numerical reading) allocating 5 character spaces (lines up columns neatly for all readings)
                                              # | is a seperator between the value and the bar
                                              #num_hashes is an integer representing length of the bar, so the number of times # repeats creates a horizontal bar proportional to the normalised readings
            print("\n" + "-"*60) #horizontal divider after each plot, makes charts easier to read


#function to plot matplotlib 
def plot_matplotlib(patient_id):
    patient_vitals_history = load_from_csv(patient_id) #defined list of dictionaries output from the load_from_csv function
    
    if len(patient_vitals_history) < 2:
        print("Not enough data to plot trends (need at least 2 readings).")
        return
    
    timestamps = [datetime.fromisoformat(readings["timestamp"]) for readings in patient_vitals_history] #creates a list of timestamps from all patient readings
                                                                                                        #datetime.fromisoformat converts each timestamps to datetime objects so it reads better
    numerical_vitals = ["bp_systolic", "heart_rate", 
                      "respiratory_rate", "temperature", "oxygen_sats"] #list of numeral vitals we want to plot 
    
    plt.figure(figsize=(12, 6)) #creates a new figure window (blank cavas) for plot
                                #figsize=(12, 6) sets the width to 12 inches and height to 6 inches.
    
    # Primary axis for vitals
    ax1 = plt.gca()  # gca = get current axis of that figure.
                     # When you call it right after plt.figure(), it returns the primary plotting area (the “main axis”) of that figure.
    #Plot each numeric vital as a line over time.
    for vitals in numerical_vitals: #for each vital in the list
        values = [float(readings[vitals]) for readings in patient_vitals_history] #This is a list comprehension that extracts the values of this vital from all historical readings.
                                                                                  #float() ensures the values are numbers (CSV reads everything as strings)
        ax1.plot(timestamps, values, marker='o', label=vitals.replace("_", " ").title()) #timestamps = plot on x-axis
                                                                                         #values = plot on y-axis
                                                                                         #marker = 'o' adds a dot at each data point
                                                                                         #label = legend label, formatted to remove underscore and also capitalise word
    #formatting the plot
    ax1.set_xlabel("Timestamp") # x-axis label
    ax1.set_ylabel("Vital Values") # y-axis label
    ax1.tick_params(axis='x', rotation=45) # rotate x-axis labels

    # Secondary axis for NEWS2 score
    ax2 = ax1.twinx()  #.twinx creates a secondary y-axis that shares the same x-axis as ax1 (hence twin x).
                       #necessary if you want vitals on one scale and NEWS2 scores on another scale
    news2_values = [float(row["news2_score"]) for row in patient_vitals_history] #list comprehension containing all total news2 scores
    ax2.plot(timestamps, news2_values, color='red', marker='x', linestyle='--', label="NEWS2 Score") #plot on the secondary y-axis (ax2)
                                                                                                     #line will be red
                                                                                                     #marker data point will be x
                                                                                                     #linestyle the line is dashed
                                                                                                     #label in the legend will be NEWS2 score
    ax2.set_ylabel("NEWS2 Score", color='red') #sets text label of y-axis
    ax2.tick_params(axis='y', labelcolor='red') #Makes all numbers on the right y-axis red, so you know they belong to the red NEWS2 Score line.

    # Combine legends from both axes
    lines_1, labels_1 = ax1.get_legend_handles_labels() #get all lines and their labels plotted on ax1 (your vitals).
    lines_2, labels_2 = ax2.get_legend_handles_labels() #get all lines and their labels plotted on ax2 (the NEWS2 line).
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left') #display a single combined legend on the figure, so you see both vitals and NEWS2 score together.
                                                                         #merge the lines and then merge the strings (labels)

    plt.title(f"Vital Trends for Patient {patient_id}") #title for both plots
    plt.tight_layout() #adjusts spacing so labels and titles don’t overlap. 
    
    # Format x-axis for readability
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b-%y %H:%M"))  # e.g., 27-Aug-86 13:22
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())  # auto spacing of ticks
    plt.xticks(rotation=45)

    plt.show() #opens a window instantly showing the plot


#while loop for continuous input, text-based interface
def main():
    while True:
        print("\nPatient vitals Monitoring App")
        print("=============================")
        print("1. Add new reading")
        print("2. View past readings")
        print("3. View trends")
        print("4. Exit\n")

        choice = input("Select an option (1/2/3/4): ").strip()

        if choice == "1":
            while True: #loop for multiple readings without leaving main menu 
                print("\n=== Enter Patient Vitals ===\n")
                patient_vitals = user_inputs()
                print("\nVitals recorded successfully!\n") 

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
            while True:
                patient_id = find_patient_id() #get patient id
                style = input("View trends as (1) ASCII or (2) matplotlib? ")
                if style == "1":
                    plot_ascii(patient_id) #prints plots based on patient id using the ascii function 
                elif style == "2":
                    plot_matplotlib(patient_id) #prints plots based on patient id using the matplotlib function 
                another_plot = input("View another patient's trend? (y/n): ").strip().lower()
                if another_plot != 'y':
                    break

        elif choice == "4":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()