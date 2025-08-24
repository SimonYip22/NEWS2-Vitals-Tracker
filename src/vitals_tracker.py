vitals  = {
    "Blood pressure": {"systolic": None, "diastolic": None},

    "Heart rate": None,

    "Temperature": None,

    "Oxygen saturations": None
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
    print("Please enter patient vital signs\n")
    
    #Blood pressure requires two values
    print("Enter blood pressure (systolic/diastolic):")
    systolic_pressure = validate_input("  Systolic (mmHg): ", 50, 250)
    diastolic_pressure = validate_input("  Diastolic (mmHg): ", 30, 150)

    #Other vitals
    heart_rate = validate_input("\nEnter heart rate (BPM): ", 30, 220)
    temperature = validate_input("\nEnter temperature (°C): ", 30, 45, float)
    oxygen_sats = validate_input("\nEnter oxygen saturations (%): ", 50, 100)
 
    #Map inputs to dictionary
    vitals["Blood pressure"]["systolic"] = systolic_pressure
    vitals["Blood pressure"]["diastolic"] = diastolic_pressure
    vitals["Heart rate"] = heart_rate
    vitals["Temperature"] = temperature
    vitals["Oxygen saturations"] = oxygen_sats

#Allows recording multiple sets of vitals in one session
while True:
    current_vitals = user_inputs()
    print("Here are the vital signs you have entered: ", current_vitals) #shows input vitals in dictionary
    repeat = input("Record another set of values? (y/n): ").lower()
    if repeat != 'y': #loop breaks if user declines recording another set of vitals
        print("Goodbye!")
        break