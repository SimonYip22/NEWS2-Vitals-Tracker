vitals  = {
    "Blood pressure": {"systolic": None, "diastolic": None},

    "Heart rate": None,

    "Temperature": None,

    "Oxygen saturations": None
}

#function for asking for patient inputs and mapping to dictionary
def user_inputs():
    print("Please enter vital signs\n")
    print("Enter blood pressure (systolic/diastolic):")

    while True: #loop until a valid input is entered
        try: #for handling potentiel ValueError
            systolic_pressure = int(input("  Systolic (mmHg): "))
            if 50 <= systolic_pressure <= 250: #is the input number within an acceptable range?
                break #if so, then the loop ends
            else:
                print("Systolic pressure outside of range. Please enter again.") #if outside of range, ask to enter again
        except ValueError:
            print("Invalid input. Please enter a number.") #if the input is not an integar, ValueError is thrown and will print this

    while True:
        try:
            diastolic_pressure = int(input("  Diastolic (mmHg): "))
            if 30 <= diastolic_pressure <= 150:
                break 
            else:
                print("Diastolic pressure outside of range. Please enter again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            heart_rate = int(input("\nEnter heart rate (BPM): "))
            if 30 <= heart_rate <= 220:
                break 
            else:
                print("Heart rate outside of range. Please enter again.")
        except ValueError:
            print("Invalid input. Please enter a number.") 

    
    while True:
        try:
            temperature = float(input("\nEnter temperature (°C): "))
            if 30 <= temperature <= 45:
                break 
            else:
                print("Temperature outside of range. Please enter again.")
        except ValueError:
            print("Invalid input. Please enter a number.")  
    
    while True:
        try:
            oxygen_sats = int(input("\nEnter oxygen saturations (%): "))
            if 50 <= oxygen_sats <= 100:
                break 
            else:
                print("Oxygen saturations outside of range. Please enter again.")
        except ValueError:
            print("Invalid input. Please enter a number.")    
    
    vitals["Blood pressure"]["systolic"] = systolic_pressure
    vitals["Blood pressure"]["diastolic"] = diastolic_pressure
    vitals["Heart rate"] = heart_rate
    vitals["Temperature"] = temperature
    vitals["Oxygen saturations"] = oxygen_sats

    return vitals