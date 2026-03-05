# Hardware → Flask interface

## Flow

1. **Arduino** (`water_quality_arduino_code/`) reads pH, TDS, turbidity, temperature and prints to **Serial** every second:
   - Format: `temperature#TDS#turbidity#pH` (e.g. `28.5#1200#10#7.2`)
   - This order matches the Flask backend (`/iot/data`).

2. **ESP8266** (`water_quality_mcu_code/`) connects to WiFi, reads that string from **Serial** (Arduino TX → ESP8266 RX if wired together), and POSTs to your Flask server:
   - URL: set `server` in the .ino to your PC (e.g. `http://192.168.1.10:5000/iot/data`).
   - Body: `{"data": "28.5#1200#10#7.2"}`.

3. **Flask** (`app.py`) receives `POST /iot/data`, parses the string, validates ranges, runs Stage-1/Stage-2, and (optionally) stores in MySQL.

## What you need to run it

| Step | Action |
|------|--------|
| 1 | Flash **Arduino** sketch to the sensor board; open Serial Monitor to see the `temp#tds#turbidity#pH` line. |
| 2 | Set **ESP8266** `ssid`/`pass` and **`server`** to the IP and port where Flask runs (e.g. `http://YOUR_PC_IP:5000/iot/data`). |
| 3 | Connect Arduino Serial output to ESP8266 Serial input (or use one board that does both sensors + WiFi if you merge the sketches). |
| 4 | Start Flask: `python app.py` (listens on `0.0.0.0:5000`). Ensure your PC IP is the one used in `server`. |

## Data format (must match)

- **Arduino sends:** `temperature#TDS#turbidity#pH` (e.g. `28.5#1200#10#7.2`).
- **Backend expects:** same order. If the order is wrong, readings will be misinterpreted and validation may fail (e.g. TDS out of range).

## Validation (backend)

If any value is missing or out of range (e.g. pH &lt; 0 or &gt; 14, TDS &gt; 50000), the API returns **400** with:  
`"Sensor error detected. Please check hardware calibration."`
