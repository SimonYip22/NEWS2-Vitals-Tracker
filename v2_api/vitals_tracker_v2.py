# -------------------------
# IMPORTS
# -------------------------
import csv
from pathlib import Path
from datetime import datetime
import matplotlib          # Import matplotlib first
matplotlib.use("Agg")  # Non-GUI backend for PNG output
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from fastapi import HTTPException
import io
from fastapi.responses import StreamingResponse

# -------------------------
# PATHS
# -------------------------
ROOT_DIR = Path(__file__).parent.parent  # parent of v2_api/
MAPPING_FILE = ROOT_DIR / "patient_mapping.csv"
VITALS_FILE = ROOT_DIR / "vitals.csv"

# Ensure patient mapping exists
if not MAPPING_FILE.exists():
    with open(MAPPING_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['patient_id', 'patient_name', 'dob'])
        writer.writeheader()

# -------------------------
# GLOBALS
# -------------------------
CSVNAMES = [
    "patient_id", "timestamp", "news2_score",
    "bp_systolic", "bp_diastolic", "heart_rate",
    "respiratory_rate", "temperature", "oxygen_sats", "loc"
]

REQUIRED_KEYS = [
    "Blood pressure", "Heart rate", "Respiratory rate",
    "Temperature", "Oxygen saturations",
    "Level of consciousness (fully awake and responsive?)"
]

vitals_template = {
    "Blood pressure": {"systolic": None, "diastolic": None},
    "Heart rate": None,
    "Respiratory rate": None,
    "Temperature": None,
    "Oxygen saturations": None,
    "Level of consciousness (fully awake and responsive?)": None,
}

thresholds = {
    "bp_systolic": {"Normal": (111, 219), "Mild Alert": (101, 110), "Moderate Alert": (91, 100),
                    "Severe Alert": [(None, 90), (220, None)]},
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

alert_scores = {"Normal": 0, "Mild Alert": 1, "Moderate Alert": 2, "Severe Alert": 3}

# -------------------------
# UTILITY FUNCTIONS
# -------------------------
def validate_dob(dob_input: str) -> str:
    """Validate DOB and normalize format."""
    try:
        dob = datetime.strptime(dob_input, "%d/%m/%y").date()
        return dob.strftime("%d/%m/%y")
    except ValueError:
        raise ValueError("Invalid format. Use dd/mm/yy (e.g., 26/11/00).")
    
def get_or_create_patient_id(patient_name: str, dob: str) -> str:
    """Return existing patient ID or create new one."""
    dob = validate_dob(dob)
    patient_name = patient_name.strip().lower()
    
    # Ensure mapping file exists
    if not MAPPING_FILE.exists():
        with open(MAPPING_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['patient_id', 'patient_name', 'dob'])
            writer.writeheader()

    # Check if headers are missing
    with open(MAPPING_FILE, 'r', newline='') as f:
        first_line = f.readline()
    expected_header = "patient_id,patient_name,dob"
    if first_line.strip() != expected_header:
        # Read the rest of the data
        with open(MAPPING_FILE, 'r', newline='') as f:
            lines = f.readlines()
        # Prepend header and overwrite file
        with open(MAPPING_FILE, 'w', newline='') as f:
            f.write(expected_header + "\n")
            f.writelines(lines)

    # Load current mapping
    patient_map = {}
    with open(MAPPING_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            patient_map[row['patient_id']] = (row['patient_name'], row['dob'])

    # Look for existing patient
    for pid, (name, existing_dob) in patient_map.items():
        if name == patient_name and existing_dob == dob:
            return pid

    # Assign new ID
    new_id = str(max([int(pid) for pid in patient_map.keys()], default=0) + 1)

    # Append patient
    with open(MAPPING_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['patient_id', 'patient_name', 'dob'])
        writer.writerow({'patient_id': new_id, 'patient_name': patient_name, 'dob': dob})

    return new_id

def check_alert(vital_name, value):
    """Determine alert level for a single vital."""
    if vital_name=="Level of consciousness (fully awake and responsive?)":
        return "Normal" if value=="Yes" else "Severe Alert"
    vital_thresholds = thresholds[vital_name]
    for alert_level, level_range in vital_thresholds.items():
        if isinstance(level_range,list):
            for min_val,max_val in level_range:
                if (min_val is None or value>=min_val) and (max_val is None or value<=max_val):
                    return alert_level
        else:
            min_val,max_val = level_range
            if (min_val is None or value>=min_val) and (max_val is None or value<=max_val):
                return alert_level
    return "Normal"

def get_alert_message_level(level):
    """Return alert message for a level."""
    return alert_messages.get(level, f"⚠️ Unknown level: {level}")

def flatten_vitals(patient_vitals):
    """Flatten nested vitals dict for CSV storage."""
    flat_vitals = {}
    if "Blood pressure" in patient_vitals:
        flat_vitals["bp_systolic"] = patient_vitals["Blood pressure"]["systolic"]
        flat_vitals["bp_diastolic"] = patient_vitals["Blood pressure"]["diastolic"]
    flat_vitals["heart_rate"] = patient_vitals.get("Heart rate")
    flat_vitals["respiratory_rate"] = patient_vitals.get("Respiratory rate")
    flat_vitals["temperature"] = patient_vitals.get("Temperature")
    flat_vitals["oxygen_sats"] = patient_vitals.get("Oxygen saturations")
    flat_vitals["loc"] = patient_vitals.get("Level of consciousness (fully awake and responsive?)")
    return flat_vitals

def compute_news2_score(vitals: dict) -> int:
    """Compute NEWS2 total score."""
    total_score=0
    for vital,value in vitals.items():
        if isinstance(value,dict):
            for bp_type,bp_val in value.items():
                level=check_alert(bp_type,bp_val)
                if bp_type=="systolic":
                    total_score+=alert_scores[level]
        else:
            level=check_alert(vital,value)
            total_score+=alert_scores[level]
    return total_score

def save_to_csv(flat_vitals: dict):
    file_exists = VITALS_FILE.exists()
    if not file_exists:
        with open(VITALS_FILE,'w',newline='') as f:
            writer = csv.DictWriter(f,fieldnames=CSVNAMES)
            writer.writeheader()
    with open(VITALS_FILE,'a',newline='') as f:
        writer = csv.DictWriter(f,fieldnames=CSVNAMES)
        writer.writerow(flat_vitals)

def load_from_csv(patient_id):
    # Ensure file exists and has headers
    if not VITALS_FILE.exists():
        return []

    with open(VITALS_FILE, 'r+', newline='') as f:
        first_line = f.readline()
        expected_header = ",".join(CSVNAMES)
        if first_line.strip() != expected_header:
            # Read rest of lines
            f.seek(0)
            lines = f.readlines()
            # Write header + lines back
            f.seek(0)
            f.write(expected_header + "\n")
            f.writelines(lines)
            f.truncate()

    with open(VITALS_FILE,'r',newline='') as f:
        reader = csv.DictReader(f)
        return [row for row in reader if row['patient_id']==patient_id]
    
# -------------------------
# MAIN FUNCTIONS
# -------------------------

def compute_news2_score(vitals: dict) -> int:
    """Compute NEWS2 total score."""
    total_score = 0
    for vital, value in vitals.items():
        if isinstance(value, dict):  # Blood pressure
            for bp_type, bp_val in value.items():
                key = f"bp_{bp_type}"  # maps "systolic" -> "bp_systolic"
                level = check_alert(key, bp_val)
                if bp_type == "systolic":  # only systolic contributes to NEWS2
                    total_score += alert_scores[level]
        else:
            level = check_alert(vital, value)
            total_score += alert_scores[level]
    return total_score


def add_vitals(patient_name: str, dob: str, vitals: dict) -> dict:
    """Add vitals, compute NEWS2, save CSV, return patient_id, alerts, and messages"""
    # Validate
    for key in REQUIRED_KEYS:
        if key not in vitals:
            raise HTTPException(status_code=400, detail=f"Missing vital: {key}")
    if not isinstance(vitals["Blood pressure"], dict) or "systolic" not in vitals["Blood pressure"] or "diastolic" not in vitals["Blood pressure"]:
        raise HTTPException(status_code=400, detail="Blood pressure must include systolic and diastolic.")
    
    # Patient ID
    patient_id = get_or_create_patient_id(patient_name, dob)

    # NEWS2
    total_score = compute_news2_score(vitals)

    # Flatten vitals for CSV
    flat_vitals = flatten_vitals(vitals)
    flat_vitals.update({
        "patient_id": patient_id,
        "timestamp": datetime.now().isoformat(),
        "news2_score": total_score
    })
    save_to_csv(flat_vitals)

    # Build alerts with messages including actual values
    alerts = {}
    for vital, value in vitals.items():
        if isinstance(value, dict):  # Blood pressure
            bp_alert = {}
            for bp_type, bp_val in value.items():
                key = f"bp_{bp_type}"  # maps to thresholds
                level = check_alert(key, bp_val)
                bp_alert[bp_type] = {
                    "value": bp_val,
                    "level": level,
                    "score": alert_scores.get(level, None),  # use None if level not scored
                    "message": get_alert_message_level(level)
                }
            alerts[vital] = bp_alert
        else:
            level = check_alert(vital, value)
            alerts[vital] = {
                "value": value,
                "level": level,
                "score": alert_scores.get(level, None),
                "message": get_alert_message_level(level)
            }

    return {"patient_id": patient_id, "total_news2_score": total_score, "alerts": alerts}

def get_patient_vitals(patient_id:str):
    """Return all vitals for a patient."""
    return load_from_csv(patient_id)

def get_trends(patient_id: str) -> StreamingResponse:
    """Generate PNG plot of vitals trends."""
    patient_vitals_history = load_from_csv(patient_id)
    if len(patient_vitals_history)<2:
        raise HTTPException(status_code=400, detail="Not enough data to plot trends.")

    timestamps = [datetime.fromisoformat(r["timestamp"]) for r in patient_vitals_history]
    numerical_vitals = ["bp_systolic","heart_rate","respiratory_rate","temperature","oxygen_sats"]

    plt.figure(figsize=(12,6))
    ax1 = plt.gca()
    for vital in numerical_vitals:
        values = [float(r[vital]) for r in patient_vitals_history]
        ax1.plot(timestamps, values, marker='o', label=vital.replace("_"," ").title())
    ax1.set_xlabel("Timestamp")
    ax1.set_ylabel("Vital Values")
    ax1.tick_params(axis='x', rotation=45)

    ax2 = ax1.twinx()
    news2_values = [float(r["news2_score"]) for r in patient_vitals_history]
    ax2.plot(timestamps, news2_values, color='red', marker='x', linestyle='--', label="NEWS2 Score")
    ax2.set_ylabel("NEWS2 Score", color='red')

    # Legend
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1+lines_2, labels_1+labels_2, loc='upper left')

    plt.title(f"Vital Trends for Patient {patient_id}")
    plt.tight_layout()
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b-%y %H:%M"))

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return StreamingResponse(buf, media_type="image/png")

def get_trends_json(patient_id: str):
    """Return vitals as JSON."""
    return load_from_csv(patient_id)