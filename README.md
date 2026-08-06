<div align="center">

# 🌱 Smart Water & Crop Advisor
### *An Intelligent Full-Stack IoT Platform for Real-Time Water Quality Monitoring, Crop Recommendation & Treatment Planning*

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask)
![Arduino](https://img.shields.io/badge/Arduino-Uno-00979D?style=for-the-badge&logo=arduino)
![ESP8266](https://img.shields.io/badge/ESP8266-NodeMCU-blue?style=for-the-badge)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-success?style=for-the-badge)
![REST API](https://img.shields.io/badge/REST-API-red?style=for-the-badge)
![Chart.js](https://img.shields.io/badge/Chart.js-Visualization-ff6384?style=for-the-badge&logo=chartdotjs)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

### 📡 IoT • 🌐 Full Stack • 🤖 Machine Learning • 📊 Analytics • 🌾 Smart Agriculture

---

### ⭐ Academic Major Project

**IoT-Oriented Strategies in Agri-Aqua Systems**

Developed as a complete Full Stack IoT platform integrating **embedded hardware**, **wireless communication**, **cloud computing**, **machine learning**, and an **interactive web dashboard** to monitor irrigation water quality, evaluate suitability, recommend crops, and provide intelligent treatment plans.

</div>

---

# 📷 Project Preview

## Hardware Prototype

<p align="center">
<img src="docs/hardware-setup.png" width="900">
</p>

---

## Complete System Architecture

<p align="center">
<img src="docs/system-architecture.png" width="900">
</p>

---

# 🌟 Overview

Agriculture depends heavily on the quality of irrigation water. Traditional testing methods are manual, time-consuming, and unsuitable for continuous monitoring. Farmers often make decisions without accurate water quality information, resulting in reduced crop yield, excessive fertilizer usage, and increased cultivation costs.

**Smart Water & Crop Advisor** addresses these challenges by integrating IoT sensors, cloud computing, machine learning, and full-stack web technologies into a unified intelligent platform.

The system continuously measures critical water quality parameters such as:

- 🌡 Temperature
- 💧 pH
- 🧂 Total Dissolved Solids (TDS)
- 🌊 Turbidity

These readings are transmitted wirelessly to a Flask cloud server where machine learning algorithms classify water quality, recommend suitable crops based on seasonal conditions, generate treatment plans, maintain historical records, and visualize everything through an interactive dashboard.

The result is a scalable decision-support platform capable of assisting farmers in making data-driven agricultural decisions.

---

# 🚀 Key Highlights

<table>

<tr>
<td width="50%">

## 🌱 Smart Farming

- Live water quality monitoring
- Automatic crop recommendations
- Seasonal crop intelligence
- Groundwater management
- Historical trend analysis

</td>

<td width="50%">

## 🤖 Artificial Intelligence

- K-Nearest Neighbors Classification
- Random Forest Crop Prediction
- Treatment Recommendation Engine
- AI Farming Assistant
- Intelligent Alerts

</td>

</tr>

<tr>

<td>

## 🌐 Full Stack Development

- Flask Backend
- REST APIs
- HTML/CSS/JavaScript
- Bootstrap UI
- Chart.js Analytics

</td>

<td>

## 📡 IoT Integration

- Arduino Uno
- NodeMCU ESP8266
- Wi-Fi Communication
- HTTP JSON Transfer
- Cloud Database

</td>

</tr>

</table>

---

# ✨ Core Features

## 📊 Real-Time Sensor Monitoring

✔ Live pH Monitoring

✔ Water Temperature

✔ Turbidity Analysis

✔ TDS Measurement

✔ Automatic Refresh

✔ Status Classification

---

## 🌾 Crop Recommendation Engine

- Season-based prediction
- Multiple crop suggestions
- Recommendation confidence
- Smart ranking
- Personalized selection

---

## 💧 Water Quality Assessment

The platform automatically classifies irrigation water into:

🟢 Suitable

🟡 Caution

🔴 Unsuitable

using a trained **K-Nearest Neighbors Machine Learning model**.

---

## 🤖 Intelligent Treatment Planner

Based on detected issues, the system automatically generates:

- Treatment procedures
- Estimated duration
- Required resources
- Cost estimation
- Preventive recommendations

---

## 📈 Dashboard Analytics

The dashboard provides:

- Interactive Charts
- Live Sensor Cards
- Historical Records
- CSV Export
- PDF Reports
- Trend Analysis
- Water Quality Insights

---

## 💬 AI Farming Assistant

An integrated AI chatbot assists users by answering agriculture-related queries including:

- Water quality
- Crop selection
- Soil conditions
- Irrigation
- Farming best practices

---

# 🎯 Why This Project?

Unlike conventional IoT monitoring systems that simply collect sensor data, this platform transforms raw environmental data into **actionable agricultural intelligence**.

It combines:

- IoT Hardware
- Wireless Communication
- Machine Learning
- Cloud Computing
- Full Stack Development
- Data Analytics
- Decision Support

into a single end-to-end intelligent ecosystem.

---

# 🏗 High-Level Architecture

<p align="center">

```text
             ┌───────────────────────┐
             │   Water Sensors       │
             │ pH • TDS • Temp • NTU │
             └──────────┬────────────┘
                        │
                Arduino UNO
                        │
                 Serial UART
                        │
                 NodeMCU ESP8266
                        │
                  HTTP / JSON
                        │
                  Flask Server
                        │
      ┌─────────────────┼─────────────────┐
      │                 │                 │
   MySQL          ML Models        REST APIs
      │                 │                 │
      └──────────────┬────────────────────┘
                     │
              Web Dashboard
                     │
             Farmer / Administrator

```

</p>

---

# 🖼 Architecture Gallery

<table>

<tr>

<td>

### System Architecture

<img src="docs/system-architecture.png">

</td>

<td>

### Layered Architecture

<img src="docs/layer-architecture.png">

</td>

</tr>

<tr>

<td>

### Decision Pipeline

<img src="docs/decision-pipeline.png">

</td>

<td>

### ML Prediction Pipeline

<img src="docs/ml-flowchart.png">

</td>

</tr>

</table>

---

# 🛠 Technology Stack

| Category | Technologies |
|-----------|--------------|
| Programming | Python, C/C++ |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap |
| Backend | Flask |
| Database | MySQL |
| Machine Learning | Scikit-Learn, KNN, Random Forest |
| Libraries | NumPy, Pandas |
| IoT | Arduino UNO, NodeMCU ESP8266 |
| Communication | Wi-Fi, HTTP, JSON |
| Visualization | Chart.js |
| IDE | Arduino IDE, VS Code, Jupyter Notebook |
| Version Control | Git, GitHub |

---

# 📚 Table of Contents

- Overview
- Features
- Architecture
- Technology Stack
- Project Structure
- Hardware Components
- Software Architecture
- Machine Learning
- Dashboard
- API Documentation
- Installation
- Usage
- Future Scope
- Contributors
- License

---

# 📂 Project Structure

```text
Smart-Water-Crop-Advisor/
│
├── 📂 arduino/
│   ├── sensor_readings/
│   ├── calibration/
│   └── esp8266_wifi/
│
├── 📂 flask_app/
│   ├── app.py
│   ├── routes.py
│   ├── models.py
│   ├── config.py
│   ├── recommendation.py
│   ├── treatment_engine.py
│   ├── ai_assistant.py
│   └── utils.py
│
├── 📂 templates/
│   ├── dashboard.html
│   ├── history.html
│   ├── recommendations.html
│   ├── treatment.html
│   └── chatbot.html
│
├── 📂 static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── icons/
│
├── 📂 ml_models/
│   ├── knn_water_classifier.pkl
│   ├── random_forest_crop.pkl
│   ├── train_knn.py
│   ├── train_random_forest.py
│   └── preprocess.py
│
├── 📂 datasets/
│   ├── water_quality.csv
│   ├── crop_dataset.csv
│   └── processed_data.csv
│
├── 📂 docs/
│   ├── hardware-setup.jpg
│   ├── system-architecture.png
│   ├── layer-architecture.png
│   ├── decision-pipeline.png
│   ├── ml-flowchart.png
│   └── dashboard/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# ⚙️ Hardware Components

The hardware subsystem continuously captures real-time water quality parameters from multiple sensors and transmits them to the cloud platform through wireless communication.

| Component | Purpose |
|------------|---------|
| Arduino Uno | Primary sensor controller |
| NodeMCU ESP8266 | Wi-Fi communication module |
| pH Sensor | Measures acidity/alkalinity |
| TDS Sensor | Determines dissolved solids |
| Turbidity Sensor | Measures water clarity |
| DS18B20 | Water temperature measurement |

---

## 📸 Hardware Prototype

<p align="center">

<img src="docs/hardware-setup.jpg" width="900">

</p>

---

# 🔌 Sensor Configuration

| Sensor | Connected To | Output |
|----------|-------------|---------|
| pH Sensor | A0 | Analog |
| TDS Sensor | A1 | Analog |
| Turbidity Sensor | A2 | Analog |
| DS18B20 | D4 | Digital |

---

# 🧠 Edge Computing

Instead of directly sending noisy sensor readings to the cloud, the Arduino performs local preprocessing.

### Operations performed

✅ Sensor Calibration

✅ Noise Reduction

✅ Median Filtering

✅ Temperature Compensation

✅ Analog-to-Digital Conversion

This significantly improves prediction accuracy while reducing communication overhead.

---

# 🌐 Communication Layer

The processed sensor readings are forwarded from the Arduino Uno to the NodeMCU ESP8266 using UART Serial Communication.

The ESP8266 then packages the readings into JSON format and transmits them over Wi-Fi to the Flask server using HTTP POST requests.

```text
Sensors
    │
Arduino UNO
    │
Serial UART
    │
NodeMCU ESP8266
    │
HTTP POST (JSON)
    │
Flask REST API
```

---

# 📦 JSON Payload Example

```json
{
  "ph": 7.38,
  "tds": 512,
  "turbidity": 24,
  "temperature": 27.3
}
```

---

# ☁️ Cloud Processing Pipeline

Once the Flask server receives sensor data, it performs multiple backend operations simultaneously.

```text
Receive JSON
      │
Validate Input
      │
Store in MySQL
      │
Run Water Classification
      │
Run Crop Recommendation
      │
Generate Treatment Plan
      │
Update Dashboard
```

---

# 🧱 Software Architecture

<p align="center">

<img src="docs/layer-architecture.png" width="900">

</p>

---

# 🧩 Layered Architecture

## 🟦 Sensor Layer

Responsible for collecting real-world environmental parameters.

Collected Parameters

- pH
- Temperature
- Turbidity
- Total Dissolved Solids

---

## 🟩 Edge Processing Layer

Runs on Arduino Uno.

Responsibilities

- Sensor calibration
- Signal filtering
- Temperature compensation
- Analog processing

---

## 🟧 Communication Layer

Runs on NodeMCU ESP8266.

Responsibilities

- Parse sensor values
- Build JSON payload
- HTTP POST requests
- Wi-Fi connectivity

---

## 🟪 Cloud Layer

Runs on Flask.

Responsibilities

- REST APIs
- Authentication
- Data storage
- Model inference
- Dashboard rendering

---

## 🟨 Decision Support Layer

Responsible for intelligent prediction.

Contains

- KNN Water Classification
- Random Forest Crop Recommendation
- Treatment Recommendation Engine

---

## 🟥 Application Layer

User-facing interface providing

- Live Dashboard
- Crop Suggestions
- Analytics
- Reports
- History
- Alerts

---

# 🔄 Complete Data Flow

```text
Water Sample
      │
      ▼
Sensors
      │
      ▼
Arduino Uno
(Filter + Calibration)
      │
      ▼
NodeMCU ESP8266
(JSON + Wi-Fi)
      │
      ▼
Flask REST API
      │
      ▼
MySQL Database
      │
      ▼
Machine Learning Models
      │
      ▼
Decision Engine
      │
      ▼
Dashboard
      │
      ▼
Farmer
```

---

# 🧠 Machine Learning Pipeline

<p align="center">

<img src="docs/ml-flowchart.png" width="550">

</p>

---

# 🤖 Stage 1 — Water Suitability Classification

The first prediction stage evaluates the incoming water sample using a trained **K-Nearest Neighbors (KNN)** classifier.

### Input Features

- pH
- TDS
- Turbidity
- Temperature

### Output Classes

🟢 Suitable

🟡 Caution

🔴 Unsuitable

This stage acts as an intelligent screening process before crop recommendations are generated.

---

# 🌾 Stage 2 — Crop Recommendation

After successful water classification, a Random Forest model predicts the most suitable crops based on:

- Water Quality
- Selected Season
- Environmental Parameters
- Historical Dataset

The model returns ranked crop recommendations with confidence scores.

---

# 📊 Decision Pipeline

<p align="center">

<img src="docs/decision-pipeline.png" width="700">

</p>

---

# 📈 Prediction Workflow

```text
Receive Sensor Data
        │
Feature Engineering
        │
Water Classification (KNN)
        │
Suitable?
 ┌──────┴─────────┐
 │                │
No              Yes
 │                │
Treatment     Crop Prediction
 │                │
Alert       Random Forest
 │                │
Recommendations
 │
Dashboard
```

---

# 🗄️ Database Design

The system stores every incoming water sample for future analytics.

## Main Tables

### Water Readings

| Field | Type |
|---------|------|
| id | INT |
| timestamp | DATETIME |
| ph | FLOAT |
| tds | FLOAT |
| turbidity | FLOAT |
| temperature | FLOAT |
| status | VARCHAR |

---

### Crop Recommendations

| Field | Type |
|---------|------|
| id | INT |
| crop_name | VARCHAR |
| confidence | FLOAT |
| season | VARCHAR |
| created_at | DATETIME |

---

### Treatment History

| Field | Type |
|---------|------|
| id | INT |
| issue | VARCHAR |
| recommendation | TEXT |
| estimated_cost | FLOAT |
| duration | VARCHAR |

---

# 🔌 REST API Overview

| Method | Endpoint | Description |
|----------|----------|-------------|
| POST | /api/sensor-data | Receive live sensor values |
| GET | /dashboard | Render dashboard |
| GET | /recommendations | Crop predictions |
| GET | /history | Historical records |
| GET | /treatment | Water treatment plan |
| GET | /export/csv | Export data as CSV |
| GET | /export/pdf | Export report as PDF |

---

# 🔐 Security Considerations

- Input validation
- JSON schema validation
- SQL parameterized queries
- Error handling
- HTTP status codes
- Exception logging
- Data integrity checks

---

> **📌 Part 2 Complete:** At this point, the README fully documents the system architecture, IoT communication pipeline, backend processing, machine learning workflow, database structure, and REST APIs—giving readers a clear understanding of how the platform operates end to end.
