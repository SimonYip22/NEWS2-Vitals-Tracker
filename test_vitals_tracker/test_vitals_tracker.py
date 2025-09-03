import pytest
import csv
import os
from vitals_tracker import (
    validate_input,
    check_alert,
    get_alert_message,
    flatten_vitals,
    get_or_create_patient_id,
    save_to_csv,
    load_from_csv,
    print_patient_vitals,
    plot_ascii,
    plot_matplotlib,
    mapping_file
)

TEST_MAPPING = "test_patient_mapping.csv"
TEST_CSV = "test_vitals.csv"

# Helper to reset test CSVs
def reset_csv_files():
    # Patient mapping CSV
    with open(TEST_MAPPING, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["patient_id","patient_name","dob"])
        writer.writeheader()
    # Vitals CSV
    with open(TEST_CSV, "w", newline="") as f:
        f.write("patient_id,timestamp,news2_score,bp_systolic,bp_diastolic,heart_rate,respiratory_rate,temperature,oxygen_sats,loc\n")

@pytest.fixture(autouse=True)
def run_around_tests(monkeypatch):
    # Reset files before each test
    reset_csv_files()
    # Monkeypatch mapping_file to test CSV
    monkeypatch.setattr("vitals_tracker.mapping_file", TEST_MAPPING)

def test_validate_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "50")
    val = validate_input("Enter number: ", 0, 100)
    assert val == 50

def test_check_alert_and_message():
    # Testing blood pressure (systolic)
    thresholds = {
        "Blood pressure": {
            "Normal": (111, 219),
            "Mild Alert": (101, 110),
            "Moderate Alert": (91, 100),
            "Severe Alert": [(None, 90), (220, None)]
        }
    }
    alert_messages = {
        "Normal": "Normal",
        "Mild Alert": "Mild Alert",
        "Moderate Alert": "Moderate Alert",
        "Severe Alert": "Severe Alert"
    }

    # Inject thresholds for test
    from vitals_tracker import thresholds as original_thresholds
    from vitals_tracker import alert_messages as original_alert_messages
    vitals_tracker_thresholds_backup = original_thresholds.copy()
    original_thresholds.update(thresholds)
    original_alert_messages.update(alert_messages)

    level = check_alert("Blood pressure", 120)
    assert level == "Normal"
    msg = get_alert_message(level, alert_messages)
    assert msg == "Normal"

    # Restore original thresholds
    original_thresholds.clear()
    original_thresholds.update(vitals_tracker_thresholds_backup)

def test_flatten_vitals():
    nested = {"Blood pressure": {"systolic": 120, "diastolic": 80}, "Heart rate": 75}
    flat = flatten_vitals(nested)
    assert flat["bp_systolic"] == 120
    assert flat["bp_diastolic"] == 80
    assert flat["heart_rate"] == 75

def test_get_or_create_patient_id(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "Test Patient" if "name" in prompt else "01/01/00")
    pid = get_or_create_patient_id()
    assert pid == "1"  # first patient should get ID 1

def test_save_and_load_csv(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "Test Patient" if "name" in prompt else "01/01/00")
    vitals = {
        "Blood pressure": {"systolic": 120, "diastolic": 80},
        "Heart rate": 75,
        "Respiratory rate": 16,
        "Temperature": 37.0,
        "Oxygen saturations": 98,
        "Level of consciousness (fully awake and responsive?)": "Yes"
    }
    save_to_csv(vitals, total_score=0, filename=TEST_CSV)
    records = load_from_csv("1", filename=TEST_CSV)
    assert len(records) == 1
    assert records[0]["bp_systolic"] == "120"
    assert records[0]["heart_rate"] == "75"

def test_print_patient_vitals(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: "Test Patient" if "name" in prompt else "01/01/00")
    vitals = {
        "Blood pressure": {"systolic": 120, "diastolic": 80},
        "Heart rate": 75,
        "Respiratory rate": 16,
        "Temperature": 37.0,
        "Oxygen saturations": 98,
        "Level of consciousness (fully awake and responsive?)": "Yes"
    }
    save_to_csv(vitals, total_score=0, filename=TEST_CSV)
    print_patient_vitals("1")
    captured = capsys.readouterr()
    # Use spacing-robust match
    assert "BP: 120/ 80" in captured.out

def test_ascii_and_matplotlib(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "Test Patient" if "name" in prompt else "01/01/00")
    vitals = {
        "Blood pressure": {"systolic": 120, "diastolic": 80},
        "Heart rate": 75,
        "Respiratory rate": 16,
        "Temperature": 37.0,
        "Oxygen saturations": 98,
        "Level of consciousness (fully awake and responsive?)": "Yes"
    }
    for _ in range(2):
        save_to_csv(vitals, total_score=0, filename=TEST_CSV)
    from vitals_tracker import plot_ascii, plot_matplotlib
    # just run functions to ensure no crash
    plot_ascii("1")
    plot_matplotlib("1")