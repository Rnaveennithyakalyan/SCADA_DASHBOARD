from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from models.anomaly_detector import run_detection
from utils.telegram_alert import send_telegram_alert, send_csv_document

# Load environment variables 
load_dotenv()
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

st.set_page_config(page_title="Solar Anomaly Dashboard", layout="wide")
st.title("🔆 Solar Anomaly Detection Dashboard")
st.markdown("Upload your solar dataset or run detection using simulated data.")

# Sidebar
with st.sidebar:
    mode = st.radio("Select Mode", ["Upload CSV", "Simulate from Example"])
    contamination = st.slider("Contamination Rate (for IF model)", 0.01, 0.10, 0.02, step=0.01)
    alert_toggle = st.checkbox("📲 Send Telegram alerts with anomaly log", value=True)

    if mode == "Upload CSV":
        uploaded_file = st.file_uploader("Upload merged solar data", type=["csv"])
    else:
        uploaded_file = None

#  Load Data 
if mode == "Simulate from Example":
    df = pd.read_csv("data/Merged_Solar_Data.csv")
    st.success("Using simulated solar data ✅")
elif uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully ✅")
    except Exception as e:
        st.error(f"Error loading file: {e}")
        df = None
else:
    df = None

# Run Detection 
if df is not None:
    if st.button("🚀 Run Anomaly Detection"):
        with st.spinner("Running models and generating results..."):
            results = run_detection(df, contamination=contamination)
            df_out = results["df"]

            st.subheader("✅ Detection Results")
            st.dataframe(df_out[["DATE_TIME", "IF_anomaly", "RF_anomaly"]].head(10))

            st.metric("Random Forest Accuracy", f"{results['accuracy']:.4f}")
            st.write("Classification Report:")
            st.json(results["report"])

            # Plot 
            st.markdown("---")
            st.subheader("📈 AC Power vs Irradiation (Colored by IF Anomalies)")
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(df_out["IRRADIATION"], df_out["AC_POWER"],
                       c=df_out["IF_anomaly"].map({"Normal": "blue", "Anomaly": "red"}),
                       alpha=0.5)
            ax.set_xlabel("Irradiation")
            ax.set_ylabel("AC Power")
            ax.set_title("Anomaly Detection: Isolation Forest")
            st.pyplot(fig)

            #  Download 
            st.markdown("---")
            st.subheader("📁 Download Detected Anomalies")
            anomalies = df_out[
                (df_out["IF_anomaly"] == "Anomaly") |
                (df_out["RF_anomaly"] == "Anomaly")
            ]
            csv_filename = "anomalies_detected.csv"
            anomalies.to_csv(csv_filename, index=False)
            csv_encoded = anomalies.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Anomaly Log (CSV)",
                data=csv_encoded,
                file_name=csv_filename,
                mime="text/csv"
            )

            #  Telegram Alerts
            if alert_toggle and not anomalies.empty:
                summary = f"⚠️ {len(anomalies)} anomalies detected!\nContamination: {contamination:.2f}"
                send_telegram_alert(summary, bot_token, chat_id)
                send_csv_document(csv_filename, bot_token, chat_id)
                st.success("Telegram summary + CSV report sent ✅")

        st.success("Anomaly detection completed! 🎯")

else:
    st.info("Upload a dataset or choose simulation mode to get started.")
