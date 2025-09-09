# -------------------------
# IMPORTS
# -------------------------
from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import Optional

from v2_api.vitals_tracker_v2 import (
    add_vitals,
    get_patient_vitals,
    get_trends,
    get_trends_json
)
import json  # <-- needed for json.dumps

# -------------------------
# FASTAPI APP INSTANCE
# -------------------------
app = FastAPI(title="Clinically-Informed Vitals Tracker API v2")

# -------------------------
# Pydantic Models
# -------------------------
class BloodPressure(BaseModel):
    systolic: int = Field(..., example=120)
    diastolic: int = Field(..., example=80)

class VitalsInput(BaseModel):
    Blood_pressure: BloodPressure = Field(..., alias="Blood pressure")
    Heart_rate: int = Field(..., alias="Heart rate", example=75)
    Respiratory_rate: int = Field(..., alias="Respiratory rate", example=18)
    Temperature: float = Field(..., example=37.0)
    Oxygen_saturations: int = Field(..., alias="Oxygen saturations", example=98)
    Level_of_consciousness: str = Field(
        ...,
        alias="Level of consciousness (fully awake and responsive?)",
        example="Yes"
    )

    class Config:
        populate_by_name = True  # allows JSON keys with spaces to map correctly

# -------------------------
# ROOT ENDPOINT
# -------------------------
@app.get("/")
def root():
    """Sanity check endpoint to verify the API is running."""
    return {"message": "Clinically-Informed Vitals Tracker API is running"}

# -------------------------
# HELPER FUNCTION FOR ALERT FORMATTING
# -------------------------
def format_alerts_horizontal(alerts: dict) -> dict:
    """
    Format nested alert dicts horizontally for JSON output.
    Keeps top-level keys vertical, inner dicts horizontal.
    """
    formatted = {}
    for vital, value in alerts.items():
        if isinstance(value, dict):
            formatted[vital] = {
                k: v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items()}
                for k, v in value.items()
            }
        else:
            formatted[vital] = value
    return formatted

# -------------------------
# 1. ADD NEW VITALS
# -------------------------
@app.post("/add_vitals/")
def add_vitals_api(patient_name: str, dob: str, vitals: VitalsInput):
    result = add_vitals(patient_name, dob, vitals.dict(by_alias=True))

    # Format alerts for compact display
    formatted_alerts = format_alerts_horizontal(result["alerts"])

    response_dict = {
        "patient_id": result["patient_id"],
        "total_news2_score": result["total_news2_score"],
        "alerts": formatted_alerts
    }

    # Pretty-print outer JSON, compact inner dicts
    return Response(
        content=json.dumps(response_dict, indent=2, separators=(",", ": ")),
        media_type="application/json"
    )

# -------------------------
# 2. VIEW PATIENT VITALS HISTORY
# -------------------------
@app.get("/patient/{patient_id}")
def get_patient_vitals_api(patient_id: str):
    """Retrieve all saved vitals for a patient as JSON list."""
    return get_patient_vitals(patient_id)

# -------------------------
# 3. PLOT PATIENT VITALS TRENDS
# -------------------------
@app.get("/trends/{patient_id}/png")
def get_trends_png(patient_id: str):
    """Return a PNG plot of vitals and NEWS2 trends."""
    return get_trends(patient_id)

# -------------------------
# 4. GET TRENDS AS JSON
# -------------------------
@app.get("/trends/{patient_id}/json")
def get_trends_json_api(patient_id: str):
    """Return patient vitals and NEWS2 history as JSON."""
    return get_trends_json(patient_id)