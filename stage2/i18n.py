from __future__ import annotations

from dataclasses import dataclass


SEASONS = ("Kharif", "Rabi", "Summer")


CROP_TE = {
    "Banana": "అరటి",
    "Bengal Gram": "సెనగలు",
    "Castor": "ఆముదం",
    "Chillies": "మిర్చి",
    "Cotton": "పత్తి",
    "Groundnut": "వేరుశనగ",
    "Jowar": "జొన్న",
    "Maize": "మొక్కజొన్న",
    "Mango": "మామిడి",
    "Onion": "ఉల్లిపాయ",
    "Paddy": "వరి",
    "Pomegranate": "దానిమ్మ",
    "Red Gram": "కంది",
    "Sunflower": "పొద్దుతిరుగుడు",
    "Sweet Orange": "కమలపండు",
    "Tomato": "టమాట",
}


SEASON_TE = {"Kharif": "ఖరీఫ్", "Rabi": "రబీ", "Summer": "వేసవి"}


UI_TE = {
    "app_title": "స్మార్ట్ నీటి నాణ్యత & పంట సూచన",
    "live_readings": "లైవ్ రీడింగ్స్",
    "season": "సీజన్",
    "desired_crop_optional": "కావలసిన పంట (ఐచ్ఛికం)",
    "get_recommendations": "సిఫార్సులు పొందండి",
    "top_crops": "సిఫార్సు చేసిన పంటలు",
    "insight": "ఇన్‌సైట్",
    "treatment": "చర్య సూచనలు",
    "water_severely_unsuitable": "నీరు చాలా అనుకూలం కాదు. వెంటనే పూర్తి ట్రీట్మెంట్ అవసరం.",
    "no_data": "ఇంకా డేటా రాలేదు",
    "knn_status": "నీటి స్థితి",
    "suitable": "అనుకూలం",
    "caution": "జాగ్రత్త",
    "unsuitable": "అననుకూలం",
}


@dataclass(frozen=True)
class BilingualText:
    en: str
    te: str

