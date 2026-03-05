from __future__ import annotations

import csv
import os
import warnings
from datetime import datetime
from typing import Any, Dict, Optional

import joblib
from flask import Flask, jsonify, render_template, request

from stage2.logic import SensorInput, Stage2Engine
from stage2.validation import ERROR_MSG, validate_sensor_payload

try:
    from db_mysql import get_recent_readings, insert_reading, is_available as mysql_available
except ImportError:
    insert_reading = None
    get_recent_readings = lambda limit=100: []
    mysql_available = lambda: False


warnings.filterwarnings("ignore")

app = Flask(__name__)
def hydro_model(hydro_value):    
    global result
    
    if model is None:
        result = "Model not available"
        return result

    for i in range(len(hydro_value)):
        hydro_value[i]=float(hydro_value[i])
    print('latest values',hydro_value)
    prediction = model.predict([hydro_value])  # include Season if used  
    print(prediction)
      
    f = open("output.txt","w")
    f.write(prediction[0])
    f.close()
    result=prediction[0]
    return prediction[0]
def hydro_quality(hydro_value):    
    global result1
    if DTC_MODEL is None:
        result1 = "Unknown"
        return result1

    for i in range(len(hydro_value)):
        hydro_value[i]=float(hydro_value[i])
    print('latest values',hydro_value)
    
    new_pred = DTC_MODEL.predict([hydro_value])

    if new_pred==[0.]:
        result1 = 'Abnormal'
        print(result1)
    else:
        result1 = 'Normal'
        print(result1)
    f = open("output1.txt","w")
    f.write(result1)
    f.close()
    print('\n')
    
    
    return result1
result=''
result1=''

# Stage-1 KNN (0=Unsuitable, 1=Caution, 2=Suitable)
KNN_MODEL = None
try:
    KNN_MODEL = joblib.load("knn.sav")
except Exception:
    KNN_MODEL = None

# Legacy water-quality classifier
DTC_MODEL = None
try:
    DTC_MODEL = joblib.load("dtc.sav")
except Exception:
    DTC_MODEL = None
# --------------------------------------------------
# GLOBAL SETTINGS (NOT FROM IOT)
# --------------------------------------------------
DEFAULT_CROP = "Rice"
DEFAULT_SEASON = "Kharif"

latest_iot_data = {}
last_updated = None

CSV_FILE = "data_log.csv"

# --------------------------------------------------
# CREATE CSV FILE IF NOT EXISTS
# --------------------------------------------------
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Timestamp",
            "pH",
            "TDS",
            "Turbidity",
            "Temperature"
        ])

# --------------------------------------------------
# CROP THRESHOLDS (EC REMOVED)
# --------------------------------------------------
CROP_THRESHOLDS = {
    "Rice": {
        "Kharif": {"pH": (5.5, 7.5), "TDS": 2000},
        "Rabi":   {"pH": (5.5, 7.2), "TDS": 1800},
        "Summer": {"pH": (5.8, 7.0), "TDS": 1500},
    },
    "Wheat": {
        "Rabi": {"pH": (6.0, 7.5), "TDS": 1700}
    }
}

# Legacy crop model (kept for backward compatibility; Stage-2 uses its own artifacts)
model = None
scaler = None
target_encoder = None
try:
    model = joblib.load("best_model.pkl")
    scaler = joblib.load("scaler.pkl")
    target_encoder = joblib.load("target_encoder.pkl")
    print("Legacy model and preprocessors loaded successfully!")
except Exception:
    model = None
    scaler = None
    target_encoder = None

# --------------------------------------------------
# STAGE-2 ENGINE (Season-aware RF ranking + insights)
# --------------------------------------------------
STAGE2_ENGINE: Optional[Stage2Engine] = None
try:
    STAGE2_ENGINE = Stage2Engine()
except Exception as e:
    # API will report a friendly error if artifacts aren't trained yet.
    STAGE2_ENGINE = None

# --------------------------------------------------
# DECISION LOGIC
# --------------------------------------------------
def evaluate_water_quality(data):
    crop = DEFAULT_CROP
    season = DEFAULT_SEASON

    limits = CROP_THRESHOLDS[crop][season]
    issues = []

    if not (limits["pH"][0] <= data["pH"] <= limits["pH"][1]):
        issues.append("pH out of range")

    if data["TDS"] > limits["TDS"]:
        issues.append("High TDS")

    if not issues:
        return "Suitable", f"Water is suitable for {crop} ({season})"
    elif len(issues) == 1:
        return "Caution", issues[0]
    else:
        return "Unsuitable", "Water is not suitable for irrigation"

# --------------------------------------------------
# ROUTES
# --------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


def _compute_knn_status(ph: float, tds: float, turbidity: float, temperature: float) -> Optional[int]:
    if KNN_MODEL is None:
        return None
    try:
        pred = KNN_MODEL.predict([[ph, tds, turbidity, temperature]])[0]
        return int(pred)
    except Exception:
        return None

# --------------------------------------------------
# IOT DEVICE SENDS DATA HERE (with validation & MySQL Stage-2 logging)
# --------------------------------------------------
@app.route("/iot/data", methods=["POST"])
def receive_iot_data():
    global latest_iot_data, last_updated, result

    payload = request.get_json()
    if not payload or "data" not in payload:
        return jsonify({"error": "Invalid payload"}), 400

    try:
        temp, tds, turbidity, ph = payload["data"].split("#")
        temp_f = float(temp)
        tds_f = float(tds)
        turb_f = float(turbidity)
        ph_f = float(ph)
    except Exception:
        return jsonify({"error": "Data parsing failed"}), 400

    # Module F: validation before ML
    sensor_dict = {"pH": ph_f, "TDS": tds_f, "Turbidity": turb_f, "Temperature": temp_f}
    ok, err = validate_sensor_payload(sensor_dict)
    if not ok:
        return jsonify({"error": err}), 400

    latest_iot_data = {
        "temperature": temp_f,
        "TDS": tds_f,
        "turbidity": turb_f,
        "pH": ph_f,
    }
    knn_status = _compute_knn_status(ph_f, tds_f, turb_f, temp_f)
    if knn_status is not None:
        latest_iot_data["knn_status"] = knn_status

    # Legacy outputs
    result1 = hydro_quality([temp_f, turb_f, tds_f, ph_f])
    result = hydro_model([ph_f, tds_f, turb_f, temp_f])

    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ts_dt = datetime.now()

    # Stage-2 outputs for history (Module E)
    top_crops_for_db = None
    insight_en_for_db = None
    if STAGE2_ENGINE is not None:
        sensor = SensorInput(
            ph=ph_f, tds=tds_f, turbidity=turb_f, temperature=temp_f,
            season=DEFAULT_SEASON, knn_status=knn_status if knn_status is not None else 2,
            desired_crop=None,
        )
        stage2_resp = STAGE2_ENGINE.build_response(sensor)
        if not stage2_resp.get("halt"):
            top_crops_for_db = stage2_resp.get("recommendations") or []
            insight_en_for_db = (stage2_resp.get("insight") or {}).get("en")

    # MySQL: store raw sensors + KNN_Status + Top_Crops + Dynamic_Insight
    if insert_reading is not None:
        insert_reading(
            timestamp=ts_dt,
            ph=ph_f,
            tds=tds_f,
            turbidity=turb_f,
            temperature=temp_f,
            knn_status=knn_status,
            top_crops=top_crops_for_db,
            dynamic_insight=insight_en_for_db,
        )

    # CSV fallback (unchanged columns for backward compatibility)
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            last_updated,
            latest_iot_data["pH"],
            latest_iot_data["TDS"],
            latest_iot_data["turbidity"],
            latest_iot_data["temperature"],
        ])

    return jsonify({"message": "IoT data received and parsed"})


# --------------------------------------------------
# DASHBOARD FETCHES LIVE DATA
# --------------------------------------------------
@app.route("/iot/latest", methods=["GET"])
def get_latest_iot_data():
    if not latest_iot_data:
        return jsonify({"status": "No data yet"})

    status, recommendation = evaluate_water_quality(latest_iot_data)

    return jsonify({
        "sensor_data": latest_iot_data,
        "crop": DEFAULT_CROP,
        "season": DEFAULT_SEASON,
        "status": status,
        "recommendation": recommendation,
        "ml_prediction": "Suggested Crop: "+result+"    Water Quality: "+result1,   
        "last_updated": last_updated
    })


# --------------------------------------------------
# STAGE-2 API: Crop ranking + insights + treatment
# --------------------------------------------------
@app.route("/api/stage2/recommend", methods=["POST"])
def stage2_recommend():
    if STAGE2_ENGINE is None:
        return (
            jsonify(
                {
                    "ok": False,
                    "error": "Stage-2 model artifacts not found. Run: python stage2/train_stage2_model.py",
                }
            ),
            500,
        )

    payload: Dict[str, Any] = request.get_json(force=True) or {}

    # Module F: validate sensor payload before ML
    ok, err = validate_sensor_payload(payload)
    if not ok:
        return jsonify({"ok": False, "error": err}), 400

    try:
        ph = float(payload["pH"])
        tds = float(payload["TDS"])
        turb = float(payload["Turbidity"])
        temp = float(payload["Temperature"])
        season = str(payload.get("Season", "Kharif"))
        knn_status = int(payload.get("KNN_Status", 2))
        desired_crop = payload.get("Desired_Crop")
        desired_crop = str(desired_crop).strip() if desired_crop else None
    except Exception:
        return jsonify({"ok": False, "error": "Invalid input payload"}), 400

    sensor = SensorInput(
        ph=ph,
        tds=tds,
        turbidity=turb,
        temperature=temp,
        season=season,
        knn_status=knn_status,
        desired_crop=desired_crop,
    )
    return jsonify(STAGE2_ENGINE.build_response(sensor))


@app.route("/api/stage2/recommend/latest", methods=["GET"])
def stage2_recommend_latest():
    if STAGE2_ENGINE is None:
        return (
            jsonify(
                {
                    "ok": False,
                    "error": "Stage-2 model artifacts not found. Run: python stage2/train_stage2_model.py",
                }
            ),
            500,
        )
    if not latest_iot_data:
        return jsonify({"ok": False, "error": "No IoT data yet"}), 400

    season = request.args.get("season", DEFAULT_SEASON)
    desired_crop = request.args.get("desired_crop")
    desired_crop = desired_crop.strip() if desired_crop else None

    knn_status = latest_iot_data.get("knn_status")
    if knn_status is None:
        # Fall back to "Suitable" if the Stage-1 KNN isn't available.
        knn_status = 2

    sensor = SensorInput(
        ph=float(latest_iot_data["pH"]),
        tds=float(latest_iot_data["TDS"]),
        turbidity=float(latest_iot_data["turbidity"]),
        temperature=float(latest_iot_data["temperature"]),
        season=season,
        knn_status=int(knn_status),
        desired_crop=desired_crop,
    )
    return jsonify(STAGE2_ENGINE.build_response(sensor))


# --------------------------------------------------
# HISTORY (Module E: frontend trend from MySQL)
# --------------------------------------------------
@app.route("/api/history", methods=["GET"])
def api_history():
    limit = request.args.get("limit", 100, type=int)
    readings = get_recent_readings(limit=limit) if get_recent_readings else []
    return jsonify({"ok": True, "readings": readings})


# --------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
