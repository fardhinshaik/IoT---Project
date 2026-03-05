# Water Quality API – Testing (cURL & Postman)

Base URL: `http://localhost:5000` (run `python app.py` first).

**MySQL (history):** Set env `WATER_QUALITY_USE_MYSQL=1` and `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE` (default: `water_quality`). Then `GET /api/history` returns stored readings with Stage-2 fields. If MySQL is not enabled, `/api/history` returns an empty list.

---

## 1. Stage-2 Recommend – Three scenarios

### Suitable (KNN_Status = 2)
```bash
curl -X POST http://localhost:5000/api/stage2/recommend \
  -H "Content-Type: application/json" \
  -d "{\"pH\": 7.2, \"TDS\": 1200, \"Turbidity\": 10, \"Temperature\": 28, \"Season\": \"Kharif\", \"KNN_Status\": 2, \"Desired_Crop\": \"Paddy\"}"
```
**Expected:** HTTP 200, `ok: true`, `halt: false`, 4–5 crops in `recommendations`, `insight` (en/te).

---

### Caution (KNN_Status = 1)
```bash
curl -X POST http://localhost:5000/api/stage2/recommend \
  -H "Content-Type: application/json" \
  -d "{\"pH\": 8.2, \"TDS\": 1800, \"Turbidity\": 22, \"Temperature\": 35, \"Season\": \"Rabi\", \"KNN_Status\": 1}"
```
**Expected:** HTTP 200, ranked crops and dynamic insight (caution-oriented).

---

### Unsuitable (KNN_Status = 0)
```bash
curl -X POST http://localhost:5000/api/stage2/recommend \
  -H "Content-Type: application/json" \
  -d "{\"pH\": 4.5, \"TDS\": 3500, \"Turbidity\": 80, \"Temperature\": 42, \"Season\": \"Summer\", \"KNN_Status\": 0}"
```
**Expected:** HTTP 200, `halt: true`, empty or no crop list, message: *"Water is severely unsuitable. Immediate full treatment required."*

---

## 2. Payload validation (Module F) – expect HTTP 400

Invalid sensor value (e.g. pH out of range):
```bash
curl -X POST http://localhost:5000/api/stage2/recommend \
  -H "Content-Type: application/json" \
  -d "{\"pH\": -2, \"TDS\": 500, \"Turbidity\": 5, \"Temperature\": 25, \"Season\": \"Kharif\", \"KNN_Status\": 2}"
```
**Expected:** HTTP 400, body: `{"ok": false, "error": "Sensor error detected. Please check hardware calibration."}`

---

Missing sensor field (e.g. no `Turbidity`):
```bash
curl -X POST http://localhost:5000/api/stage2/recommend \
  -H "Content-Type: application/json" \
  -d "{\"pH\": 7, \"TDS\": 1000, \"Temperature\": 28, \"Season\": \"Kharif\", \"KNN_Status\": 2}"
```
**Expected:** HTTP 400, same error message.

---

## 3. IoT endpoint (with validation)

Valid payload (`temperature#TDS#turbidity#pH`):
```bash
curl -X POST http://localhost:5000/iot/data \
  -H "Content-Type: application/json" \
  -d "{\"data\": \"28#1200#10#7.2\"}"
```
**Expected:** HTTP 200, `"message": "IoT data received and parsed"`.

Invalid (e.g. TDS out of range):
```bash
curl -X POST http://localhost:5000/iot/data \
  -H "Content-Type: application/json" \
  -d "{\"data\": \"28#99999#10#7.2\"}"
```
**Expected:** HTTP 400, `"error": "Sensor error detected. Please check hardware calibration."`

---

## 4. Other useful calls

- **Latest IoT:** `curl http://localhost:5000/iot/latest`
- **Stage-2 from latest:** `curl "http://localhost:5000/api/stage2/recommend/latest?season=Kharif&desired_crop=Paddy"`
- **History (MySQL):** `curl "http://localhost:5000/api/history?limit=50"`

---

## 5. Postman

Import **`Water_Quality_API.postman_collection.json`** into Postman. It includes the three scenarios (Suitable, Caution, Unsuitable), validation-fail examples, IoT data, and history. Set `baseUrl` to `http://localhost:5000` if needed.
