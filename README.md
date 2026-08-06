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
<img src="docs/hardware-setup.jpg" width="900">
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

## ⭐ Part 1 Complete
