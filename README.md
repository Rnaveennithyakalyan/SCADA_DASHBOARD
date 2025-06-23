# Solar SCADA Anomaly Dashboard

##  Overview

**Solar SCADA Anomaly Dashboard** is a modular, Streamlit-based AI system for detecting and reporting anomalies in solar power datasets. It uses Isolation Forest and Random Forest for detection and delivers real-time Telegram alerts with downloadable anomaly reports.

---

##  Features

- Upload or simulate solar CSV data
- Hybrid ML anomaly detection (Isolation Forest + Random Forest)
- Interactive results table and scatter plot
- Downloadable CSV report of flagged anomalies
- Real-time Telegram notifications with CSV attachment
- Secure `.env` token handling

---

##  Quickstart

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/scada-anomaly-dashboard.git
cd scada-anomaly-dashboard
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate         # macOS/Linux
.venv\Scripts\activate            # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Telegram Alerts

Create a `.env` file at the project root with your credentials:

```
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

---

##  Run the Dashboard

```bash
streamlit run app.py
```

Then open your browser and go to:  
[http://localhost:8501](http://localhost:8501)

---

##  How to Use the Dashboard

1. **Choose Input Mode**  
   - Upload your own dataset (CSV with solar parameters)  
   - Or simulate using the built-in sample from `data/Merged_Solar_Data.csv`

2. **Set Contamination Rate**  
   - Use the sidebar slider to estimate anomaly frequency (e.g. 2%)

3. **Enable Telegram Alerts (optional)**  
   - Tick the checkbox to send real-time alerts via Telegram

4. **Click “ Run Anomaly Detection”**  
   - Triggers ML detection + visualization pipeline

5. **Explore Results**  
   - Table of IF and RF anomalies  
   - Accuracy and classification metrics  
   - Scatter plot: Irradiation vs AC Power  
   - Download the CSV report  
   - Receive Telegram alert (if enabled)

---

## Project Structure

```
scada-anomaly-dashboard/
├── app.py                      # Streamlit UI entry point
├── .env                        # Telegram credentials (excluded from Git)
├── requirements.txt            # Python dependencies
├── data/
│   └── Merged_Solar_Data.csv   # Sample solar dataset
├── models/
│   └── anomaly_detector.py     # ML detection logic
├── utils/
│   └── telegram_alert.py       # Telegram messaging functions
└── anomalies_detected.csv      # Output report (generated dynamically)
```

---

##  Detection Pipeline

- `Isolation Forest`: Unsupervised anomaly detection
- `Random Forest`: Supervised classifier trained on Isolation Forest labels
- Output includes anomaly tags, accuracy score, and classification report
- Streamlit displays data, graphs, and download buttons

---

##  Telegram Integration

If alerting is enabled, the system:

- Sends a summary message to your chat via `send_telegram_alert`
- Sends the anomaly report as CSV via `send_csv_document`

Only triggers if anomalies are found.

---

##  Future Enhancements

- Confidence scoring for each anomaly
- Email and WhatsApp alert support
- Dashboard login and multi-user access
- Persistent alert history and session logging

---

##  License

MIT License © 2025

---

##  Contact

- GitHub: [@Rnaveennithyakalyan](https://github.com/Rnaveennithyakalyan)
- Email: [naveennithyakalyan@gmail.com](mailto:naveennithyakalyan@gmail.com)
```

