from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import joblib
import json
from pathlib import Path

import numpy as np

from .i18n import BilingualText, CROP_TE, SEASONS


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = ROOT / "stage2" / "artifacts"

SEASON_TO_INT = {"Kharif": 0, "Rabi": 1, "Summer": 2}


@dataclass(frozen=True)
class SensorInput:
    ph: float
    tds: float
    turbidity: float
    temperature: float
    season: str
    knn_status: int
    desired_crop: Optional[str] = None


def _clamp_season(season: str) -> str:
    season = (season or "").strip()
    if season in SEASONS:
        return season
    return "Kharif"


def _severity_flags(ph: float, tds: float, turbidity: float, temperature: float) -> List[str]:
    flags: List[str] = []

    if tds >= 1500:
        flags.append("tds_high")
    elif tds >= 900:
        flags.append("tds_mid")

    if turbidity >= 25:
        flags.append("turbidity_high")
    elif turbidity >= 10:
        flags.append("turbidity_mid")

    if ph <= 5.5:
        flags.append("ph_low")
    elif ph >= 8.5:
        flags.append("ph_high")

    if temperature >= 38:
        flags.append("temp_high")
    elif temperature <= 15:
        flags.append("temp_low")

    return flags


def build_dynamic_insight(sensor: SensorInput, top_crops_en: List[str]) -> BilingualText:
    ph, tds, turb, temp = sensor.ph, sensor.tds, sensor.turbidity, sensor.temperature
    flags = _severity_flags(ph, tds, turb, temp)

    if not flags:
        en = (
            f"Your water readings look balanced for {sensor.season}. "
            f"We ranked crops that match these conditions for this season."
        )
        te = (
            f"మీ నీటి రీడింగ్స్ {sensor.season} సీజన్‌కు బాగానే ఉన్నాయి. "
            f"ఈ పరిస్థితులకు సరిపడే పంటలను మేము ర్యాంక్ చేసి చూపిస్తున్నాం."
        )
        return BilingualText(en=en, te=te)

    # Pick up to 2 strongest signals in a stable order.
    priority = ["tds_high", "ph_high", "ph_low", "turbidity_high", "temp_high", "temp_low", "tds_mid", "turbidity_mid"]
    chosen = [f for f in priority if f in flags][:2]

    parts_en: List[str] = []
    parts_te: List[str] = []

    for f in chosen:
        if f == "tds_high":
            parts_en.append(f"elevated salinity (TDS: {tds:.0f} ppm)")
            parts_te.append(f"ఉప్పుతనం ఎక్కువగా ఉంది (TDS: {tds:.0f} ppm)")
        elif f == "tds_mid":
            parts_en.append(f"moderate salinity (TDS: {tds:.0f} ppm)")
            parts_te.append(f"ఉప్పుతనం కొంచెం ఎక్కువగా ఉంది (TDS: {tds:.0f} ppm)")
        elif f == "ph_high":
            parts_en.append(f"alkaline pH (pH: {ph:.2f})")
            parts_te.append(f"pH క్షారంగా ఉంది (pH: {ph:.2f})")
        elif f == "ph_low":
            parts_en.append(f"acidic pH (pH: {ph:.2f})")
            parts_te.append(f"pH ఆమ్లంగా ఉంది (pH: {ph:.2f})")
        elif f == "turbidity_high":
            parts_en.append(f"high turbidity (NTU: {turb:.0f})")
            parts_te.append(f"మసకదనం ఎక్కువగా ఉంది (NTU: {turb:.0f})")
        elif f == "turbidity_mid":
            parts_en.append(f"some turbidity (NTU: {turb:.0f})")
            parts_te.append(f"మసకదనం కొంచెం ఉంది (NTU: {turb:.0f})")
        elif f == "temp_high":
            parts_en.append(f"high temperature (°C: {temp:.0f})")
            parts_te.append(f"ఉష్ణోగ్రత ఎక్కువగా ఉంది (°C: {temp:.0f})")
        elif f == "temp_low":
            parts_en.append(f"low temperature (°C: {temp:.0f})")
            parts_te.append(f"ఉష్ణోగ్రత తక్కువగా ఉంది (°C: {temp:.0f})")

    en = (
        f"Based on your water: {', '.join(parts_en)}. "
        f"We recommend these season-suitable crops accordingly."
    )
    te = (
        f"మీ నీటి ఆధారంగా: {', '.join(parts_te)}. "
        f"దానికి అనుగుణంగా ఈ సీజన్‌కు సరిపడే పంటలను మేము సూచిస్తున్నాం."
    )
    return BilingualText(en=en, te=te)


# Approximate irrigation-friendly bands for quick remediation advice.
CROP_IDEALS: Dict[str, Dict[str, Any]] = {
    "Paddy": {"ph": (5.5, 7.5), "tds_max": 2000, "turb_max": 50, "temp": (20, 35)},
    "Banana": {"ph": (6.0, 7.5), "tds_max": 1200, "turb_max": 20, "temp": (18, 35)},
    "Mango": {"ph": (5.5, 7.5), "tds_max": 1400, "turb_max": 20, "temp": (18, 38)},
    "Pomegranate": {"ph": (6.5, 8.0), "tds_max": 2000, "turb_max": 25, "temp": (18, 40)},
    "Cotton": {"ph": (5.8, 8.0), "tds_max": 2500, "turb_max": 25, "temp": (20, 40)},
    "Groundnut": {"ph": (6.0, 7.5), "tds_max": 1500, "turb_max": 20, "temp": (20, 35)},
    "Chillies": {"ph": (6.0, 7.5), "tds_max": 1400, "turb_max": 20, "temp": (18, 35)},
    "Tomato": {"ph": (6.0, 7.5), "tds_max": 1200, "turb_max": 20, "temp": (18, 32)},
    "Onion": {"ph": (6.0, 7.8), "tds_max": 1400, "turb_max": 20, "temp": (15, 30)},
    "Maize": {"ph": (5.8, 7.8), "tds_max": 1500, "turb_max": 20, "temp": (18, 35)},
    "Jowar": {"ph": (6.0, 8.2), "tds_max": 2000, "turb_max": 25, "temp": (18, 40)},
    "Sunflower": {"ph": (6.0, 8.0), "tds_max": 2000, "turb_max": 25, "temp": (18, 38)},
    "Castor": {"ph": (6.0, 8.5), "tds_max": 2500, "turb_max": 30, "temp": (20, 40)},
    "Red Gram": {"ph": (6.0, 8.0), "tds_max": 1800, "turb_max": 25, "temp": (18, 38)},
    "Bengal Gram": {"ph": (6.0, 7.8), "tds_max": 1600, "turb_max": 20, "temp": (12, 30)},
    "Sweet Orange": {"ph": (6.0, 7.8), "tds_max": 1200, "turb_max": 20, "temp": (18, 35)},
}


def _remediation_for(sensor: SensorInput, crop: str) -> BilingualText:
    ideals = CROP_IDEALS.get(crop)
    if not ideals:
        en = "No specific threshold profile available for this crop."
        te = "ఈ పంటకు ప్రత్యేక థ్రెషోల్డ్ సమాచారం అందుబాటులో లేదు."
        return BilingualText(en=en, te=te)

    ph_lo, ph_hi = ideals["ph"]
    tds_max = ideals["tds_max"]
    turb_max = ideals["turb_max"]
    t_lo, t_hi = ideals["temp"]

    actions_en: List[str] = []
    actions_te: List[str] = []

    if sensor.ph > ph_hi:
        actions_en.append(
            f"pH is high (ideal {ph_lo:.1f}–{ph_hi:.1f}). Consider agricultural gypsum (if sodicity), "
            f"acidifying fertilizers (ammonium sulfate), and blending with lower-pH water."
        )
        actions_te.append(
            f"pH ఎక్కువగా ఉంది (ఆదర్శం {ph_lo:.1f}–{ph_hi:.1f}). "
            f"వ్యవసాయ జిప్సమ్ (సోడిసిటీ ఉంటే), ఆమ్లీకరణ ఎరువులు (అమోనియం సల్ఫేట్), "
            f"మరియు తక్కువ pH నీటితో కలపడం పరిగణించండి."
        )
    elif sensor.ph < ph_lo:
        actions_en.append(
            f"pH is low (ideal {ph_lo:.1f}–{ph_hi:.1f}). Apply agricultural lime/dolomite gradually and re-test."
        )
        actions_te.append(
            f"pH తక్కువగా ఉంది (ఆదర్శం {ph_lo:.1f}–{ph_hi:.1f}). "
            f"వ్యవసాయ సున్నం/డోలొమైట్‌ని దశలవారీగా వేసి, మళ్లీ పరీక్షించండి."
        )

    if sensor.tds > tds_max:
        actions_en.append(
            f"TDS is high (ideal ≤ {tds_max:.0f} ppm). Blend with freshwater, prefer drip irrigation, "
            f"and do periodic leaching if soil allows."
        )
        actions_te.append(
            f"TDS ఎక్కువగా ఉంది (ఆదర్శం ≤ {tds_max:.0f} ppm). తాగునీటితో కలపడం, "
            f"డ్రిప్ ఇరిగేషన్‌కు ప్రాధాన్యం ఇవ్వడం, నేల అనుమతిస్తే లీచింగ్ చేయడం మంచిది."
        )

    if sensor.turbidity > turb_max:
        actions_en.append(
            f"Turbidity is high (ideal ≤ {turb_max:.0f} NTU). Use settling tank/sedimentation, screen filters, "
            f"and (if needed) alum coagulation before irrigation lines."
        )
        actions_te.append(
            f"మసకదనం ఎక్కువగా ఉంది (ఆదర్శం ≤ {turb_max:.0f} NTU). సెటిలింగ్ ట్యాంక్/సెడిమెంటేషన్, "
            f"స్క్రీన్ ఫిల్టర్లు, అవసరమైతే ఆలమ్‌తో కోగ్యులేషన్ ఉపయోగించండి."
        )

    if sensor.temperature < t_lo or sensor.temperature > t_hi:
        actions_en.append(
            f"Temperature is outside the preferred band ({t_lo:.0f}–{t_hi:.0f} °C). "
            f"Try irrigating early morning/evening and avoid hot mid-day watering."
        )
        actions_te.append(
            f"ఉష్ణోగ్రత ఇష్టమైన పరిధికి బయట ఉంది ({t_lo:.0f}–{t_hi:.0f} °C). "
            f"ఉదయం/సాయంత్రం నీరు పెట్టడం, మధ్యాహ్నం వేడి సమయంలో తప్పుకోవడం మంచిది."
        )

    if not actions_en:
        en = f"Your readings are within the ideal band for {crop}. No treatment required."
        te = f"{crop} పంటకు మీ రీడింగ్స్ సరైన పరిధిలో ఉన్నాయి. ట్రీట్మెంట్ అవసరం లేదు."
        return BilingualText(en=en, te=te)

    en = "For your desired crop, here are practical actions:\n- " + "\n- ".join(actions_en)
    te = "మీ కోరుకున్న పంట కోసం చేయాల్సినవి:\n- " + "\n- ".join(actions_te)
    return BilingualText(en=en, te=te)


class Stage2Engine:
    def __init__(self) -> None:
        self.model = joblib.load(ARTIFACTS_DIR / "stage2_random_forest.pkl")
        self.scaler = joblib.load(ARTIFACTS_DIR / "stage2_scaler.pkl")
        self.label_encoder = joblib.load(ARTIFACTS_DIR / "stage2_label_encoder.pkl")
        self.season_to_crops = json.loads(
            (ARTIFACTS_DIR / "stage2_season_to_crops.json").read_text(encoding="utf-8")
        )

        # sklearn stores class order; align to encoder classes.
        self.class_names = list(self.label_encoder.classes_)

    def rank_crops(self, sensor: SensorInput, top_k: int = 5) -> List[Dict[str, Any]]:
        season = _clamp_season(sensor.season)

        if sensor.knn_status == 0:
            return []

        X_num = np.array([[sensor.ph, sensor.tds, sensor.turbidity, sensor.temperature]], dtype=float)
        X_num_scaled = self.scaler.transform(X_num)
        X_season = np.array([[SEASON_TO_INT.get(season, 0)]], dtype=float)
        X = np.hstack([X_num_scaled, X_season])

        proba = self.model.predict_proba(X)[0]
        scores = {self.class_names[i]: float(proba[i]) for i in range(len(self.class_names))}

        allowed = set(self.season_to_crops.get(season, []))
        ranked = sorted(
            ((crop, score) for crop, score in scores.items() if crop in allowed),
            key=lambda t: t[1],
            reverse=True,
        )

        # Hard constraint: return 4–5 crops once Stage-1 passes.
        # Dataset has enough crops per season; if not, fall back to global ranking to reach 4.
        if len(ranked) < 4:
            fallback = sorted(scores.items(), key=lambda t: t[1], reverse=True)
            seen = {c for c, _ in ranked}
            for c, s in fallback:
                if c not in seen:
                    ranked.append((c, s))
                    seen.add(c)
                if len(ranked) >= 4:
                    break

        ranked = ranked[: max(4, min(top_k, 5))]

        return [
            {
                "crop_en": crop,
                "crop_te": CROP_TE.get(crop, crop),
                "score": round(score, 6),
            }
            for crop, score in ranked
        ]

    def build_response(self, sensor: SensorInput) -> Dict[str, Any]:
        season = _clamp_season(sensor.season)

        if sensor.knn_status == 0:
            return {
                "ok": True,
                "halt": True,
                "knn_status": 0,
                "season": season,
                "recommendations": [],
                "insight": {
                    "en": "Water is severely unsuitable. Immediate full treatment required.",
                    "te": "నీరు చాలా అనుకూలం కాదు. వెంటనే పూర్తి ట్రీట్మెంట్ అవసరం.",
                },
                "desired_crop": None,
            }

        recs = self.rank_crops(sensor, top_k=5)
        top_en = [r["crop_en"] for r in recs]
        insight = build_dynamic_insight(sensor, top_en)

        desired = None
        if sensor.desired_crop:
            crop = sensor.desired_crop.strip()
            desired = {
                "crop_en": crop,
                "crop_te": CROP_TE.get(crop, crop),
                "advice": _remediation_for(sensor, crop).__dict__,
            }

        return {
            "ok": True,
            "halt": False,
            "knn_status": int(sensor.knn_status),
            "season": season,
            "sensor": {
                "pH": sensor.ph,
                "TDS": sensor.tds,
                "Turbidity": sensor.turbidity,
                "Temperature": sensor.temperature,
            },
            "recommendations": recs,
            "insight": insight.__dict__,
            "desired_crop": desired,
        }

