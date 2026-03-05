"""
Module F: Payload validation & failsafes.
Validates sensor payloads before data hits ML models.
Returns HTTP 400 with a fixed message on invalid/corrupted data.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

# Hard physical limits for irrigation water sensors
SENSOR_LIMITS = {
    "pH": (0.0, 14.0),
    "TDS": (0.0, 50_000.0),       # ppm
    "Turbidity": (0.0, 1000.0),   # NTU
    "Temperature": (-5.0, 60.0),  # °C (allow some margin)
}

SENSOR_KEYS = ("pH", "TDS", "Turbidity", "Temperature")

ERROR_MSG = "Sensor error detected. Please check hardware calibration."


def _in_range(value: float, key: str) -> bool:
    lo, hi = SENSOR_LIMITS[key]
    return lo <= value <= hi


def validate_sensor_payload(payload: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Check presence and validity of the four sensor values.
    Returns (True, None) if valid, else (False, error_message).
    Use ERROR_MSG for API response when False.
    """
    if not payload:
        return False, ERROR_MSG

    for key in SENSOR_KEYS:
        if key not in payload:
            return False, ERROR_MSG
        raw = payload[key]
        try:
            val = float(raw)
        except (TypeError, ValueError):
            return False, ERROR_MSG
        if not _in_range(val, key):
            return False, ERROR_MSG

    return True, None


def parse_validated_sensors(payload: Dict[str, Any]) -> Dict[str, float]:
    """After validate_sensor_payload returned True, extract floats."""
    return {
        "pH": float(payload["pH"]),
        "TDS": float(payload["TDS"]),
        "Turbidity": float(payload["Turbidity"]),
        "Temperature": float(payload["Temperature"]),
    }
