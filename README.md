   # 💳 Smart Credit Card Fraud Detection System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/) 
[![Flask](https://img.shields.io/badge/Flask-%20v2.0-lightgrey)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-In_Progress-orange)]()

A full-stack machine learning-powered web application for real-time fraud detection. Built with modular and scalable design principles, the system combines intelligent detection with robust backend architecture, REST APIs, blockchain logging, and planned cloud deployment.

---

## 📚 Table of Contents

- [🎯 Features](#-features)
- [🧠 Architecture](#-architecture)
- [🛠 Tech Stack](#-tech-stack)
- [📦 Project Structure](#-project-structure)
- [⚙️ Setup & Installation](#️-setup--installation)
- [🧪 ML Model Details](#-ml-model-details)
- [📡 API Usage](#-api-usage)
- [⛓ Blockchain Logger](#-blockchain-logger)
- [🚀 Future Enhancements](#-future-enhancements)
- [📸 Screenshots](#-screenshots)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👨‍💻 Author](#-author)

---

## 🎯 Features

- ✅ ML-based real-time fraud detection
- 🔐 Secure user authentication with hashed passwords
- 🌐 RESTful API integration for external communication
- ⛓ Blockchain-style logging for immutable transaction history
- 📊 Admin dashboard for fraud analytics
- 🔔 Planned: SMS alert system (via Twilio)
- ☁️ Planned: Cloud deployment (AWS/Render)

---

## 🧠 Architecture

```mermaid
flowchart TD
    User[User Input] -->|Web Form / API| Flask[Flask Backend]
    Flask --> Auth[Authentication & Validation]
    Auth --> Predict[ML Model Prediction]
    Predict -->|Flagged/Legit| Blockchain[Blockchain Logger]
    Predict --> Dashboard[Admin Dashboard]
    Blockchain --> SQLite[SQLite DB]
