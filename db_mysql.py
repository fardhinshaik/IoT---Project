"""
Module E: Backend data storage (MySQL).
Stores raw sensor data + Stage-2 outputs: KNN_Status, Top_Crops (JSON), Dynamic_Insight.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

# Optional: only use MySQL if env is set and pymysql available
USE_MYSQL = os.environ.get("WATER_QUALITY_USE_MYSQL", "").strip().lower() in ("1", "true", "yes")
_db = None


def _get_config() -> Dict[str, str]:
    return {
        "host": os.environ.get("MYSQL_HOST", "localhost"),
        "port": os.environ.get("MYSQL_PORT", "3306"),
        "user": os.environ.get("MYSQL_USER", "root"),
        "password": os.environ.get("MYSQL_PASSWORD", ""),
        "database": os.environ.get("MYSQL_DATABASE", "water_quality"),
        "charset": "utf8mb4",
    }


def get_connection():
    if not USE_MYSQL:
        return None
    try:
        import pymysql
    except ImportError:
        return None
    cfg = _get_config()
    return pymysql.connect(
        host=cfg["host"],
        port=int(cfg["port"]),
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        charset=cfg["charset"],
        cursorclass=pymysql.cursors.DictCursor,
    )


def init_schema(conn) -> None:
    """Create or update sensor_readings table with Stage-2 columns."""
    sql = """
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME NOT NULL,
        ph DOUBLE NOT NULL,
        tds DOUBLE NOT NULL,
        turbidity DOUBLE NOT NULL,
        temperature DOUBLE NOT NULL,
        knn_status TINYINT NULL COMMENT '0=Unsuitable, 1=Caution, 2=Suitable',
        top_crops JSON NULL COMMENT 'Array of {crop_en, crop_te, score}',
        dynamic_insight TEXT NULL COMMENT 'Generated insight text (English)',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_timestamp (timestamp),
        INDEX idx_knn_status (knn_status)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()


def insert_reading(
    timestamp: datetime,
    ph: float,
    tds: float,
    turbidity: float,
    temperature: float,
    knn_status: Optional[int] = None,
    top_crops: Optional[List[Dict[str, Any]]] = None,
    dynamic_insight: Optional[str] = None,
) -> bool:
    """Insert one sensor reading with optional Stage-2 outputs. Returns True if written."""
    if not USE_MYSQL:
        return False
    try:
        conn = get_connection()
        if conn is None:
            return False
        init_schema(conn)
        top_crops_json = json.dumps(top_crops, ensure_ascii=False) if top_crops is not None else None
        insight_text = (dynamic_insight or "").strip() or None
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sensor_readings
                (timestamp, ph, tds, turbidity, temperature, knn_status, top_crops, dynamic_insight)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    timestamp,
                    ph,
                    tds,
                    turbidity,
                    temperature,
                    knn_status,
                    top_crops_json,
                    insight_text,
                ),
            )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def is_available() -> bool:
    """True if MySQL is configured and connectable."""
    if not USE_MYSQL:
        return False
    try:
        c = get_connection()
        if c is None:
            return False
        c.close()
        return True
    except Exception:
        return False


def get_recent_readings(limit: int = 100) -> List[Dict[str, Any]]:
    """Return recent sensor_readings with Stage-2 fields for frontend history/trends."""
    if not USE_MYSQL:
        return []
    try:
        conn = get_connection()
        if conn is None:
            return []
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, timestamp, ph, tds, turbidity, temperature,
                       knn_status, top_crops, dynamic_insight
                FROM sensor_readings
                ORDER BY timestamp DESC
                LIMIT %s
                """,
                (max(1, min(limit, 500)),),
            )
            rows = cur.fetchall()
        conn.close()
        out = []
        for r in rows:
            ts = r.get("timestamp")
            if hasattr(ts, "isoformat"):
                ts = ts.isoformat()
            top_crops = r.get("top_crops")
            if isinstance(top_crops, str):
                try:
                    top_crops = json.loads(top_crops) if top_crops else None
                except Exception:
                    top_crops = None
            out.append({
                "id": r.get("id"),
                "timestamp": ts,
                "pH": float(r.get("ph", 0)),
                "TDS": float(r.get("tds", 0)),
                "Turbidity": float(r.get("turbidity", 0)),
                "Temperature": float(r.get("temperature", 0)),
                "knn_status": r.get("knn_status"),
                "top_crops": top_crops,
                "dynamic_insight": r.get("dynamic_insight"),
            })
        return out
    except Exception:
        return []
