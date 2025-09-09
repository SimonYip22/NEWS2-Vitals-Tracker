# -------------------------
# IMPORTS
# -------------------------
from fastapi import FastAPI, Body
from fastapi.responses import Response
from v2_api.vitals_tracker_v2 import (
    add_vitals,
    get_patient_vitals,
    get_trends,
    get_trends_json
)
import json

# -------------------------
# FASTAPI APP INSTANCE
# -------------------------
app = FastAPI(title="Clinically-Informed Vitals Tracker API v2")

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
            # For nested dicts (like Blood pressure), compact inner dicts
            formatted[vital] = {
                k: {kk: vv for kk, vv in vv.items()} if isinstance(vv, dict) else vv
                for k, vv in value.items()
            }
        else:
            formatted[vital] = value
    return formatted

# -------------------------
# 1. ADD NEW VITALS
# -------------------------
@app.post("/add_vitals/")
def add_vitals_api(
    patient_name: str,
    dob: str,
    vitals: dict = Body(..., description="Patient vitals as JSON")
):
    result = add_vitals(patient_name, dob, vitals)

    # Format alerts for horizontal display
    formatted_alerts = format_alerts_horizontal(result["alerts"])

    response_dict = {
        "patient_id": result["patient_id"],
        "total_news2_score": result["total_news2_score"],
        "alerts": formatted_alerts
    }

    # Return JSON with indentation but compact inner objects
    return Response(
        content=json.dumps(response_dict, indent=2, separators=(",", ": ")),
        media_type="application/json"
    )

# -------------------------
# 2. VIEW PATIENT VITALS HISTORY
# -------------------------
@app.get("/patient/{patient_id}")
def get_patient_vitals_api(patient_id: str):
    """
    Retrieve all saved vitals for a patient.
    Returns JSON list of historical vitals.
    """
    return get_patient_vitals(patient_id)

# -------------------------
# 3. PLOT PATIENT VITALS TRENDS
# -------------------------
@app.get("/trends/{patient_id}/png")
def get_trends_png(patient_id: str):
    """
    Returns a Matplotlib plot of vitals and NEWS2 trends as PNG image.
    """
    return get_trends(patient_id)

# -------------------------
# 4. GET TRENDS AS JSON
# -------------------------
@app.get("/trends/{patient_id}/json")
def get_trends_json_api(patient_id: str):
    """
    Return patient vitals and NEWS2 history as JSON (structured data).
    """
    return get_trends_json(patient_id)