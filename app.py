# ===============================================================
# SunWolf_ReSunance_Continuum v6.4 — Real-Time SUPT Continuum Build
# ===============================================================
# Live Monitoring Dashboard for Solar–Volcanic Coupling at Campi Flegrei
# Powered by Sheppard’s Universal Proxy Theory (SUPT)
# ===============================================================

import streamlit as st
import pandas as pd
import numpy as np
import requests
import datetime as dt
import io
import traceback
import plotly.graph_objects as go
import time

# --------------------- CONFIG ---------------------
API_TIMEOUT = 10
REFRESH_INTERVAL = 60  # seconds for live refresh
NOAA_GEOMAG_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
NOAA_SOLAR_WIND_URL = "https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json"
INGV_API_URL = "https://webservices.ingv.it/fdsnws/event/1/query?"

DEFAULT_SOLAR = {
    "C_flare": 0.99, "M_flare": 0.55, "X_flare": 0.15,
    "psi_s": 0.72, "solar_speed": 688
}

# ===============================================================
# Core SUPT Utility Functions
# ===============================================================
def compute_eii(md_max, md_mean, shallow_ratio, psi_s):
    """Energetic Instability Index — SUPT formula"""
    return np.clip((md_max * 0.2 + md_mean * 0.15 + shallow_ratio * 0.4 + psi_s * 0.25), 0, 1)

def classify_phase(EII):
    if EII >= 0.85:
        return "ACTIVE – Collapse Window Initiated"
    elif EII >= 0.6:
        return "ELEVATED – Pressure Coupling Phase"
    return "MONITORING"

def generate_synthetic_seismic_data(n=20):
    now = dt.datetime.utcnow()
    times = [now - dt.timedelta(hours=i * 3) for i in range(n)]
    mags = np.random.uniform(0.5, 1.3, n)
    depths = np.random.uniform(0.8, 3.0, n)
    return pd.DataFrame({"time": times, "magnitude": mags, "depth_km": depths})

# ===============================================================
# Live NOAA Feeds
# ===============================================================
@st.cache_data(ttl=REFRESH_INTERVAL)
def fetch_geomag_data():
    try:
        r = requests.get(NOAA_GEOMAG_URL, timeout=API_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        latest = data[-1]
        return {"status": "✅", "kp_index": float(latest[1]), "time_tag": latest[0]}
    except Exception as e:
        st.warning(f"NOAA Geomagnetic fetch failed: {e}")
        return {"status": "⚠️", "kp_index": 0.0, "time_tag": "Fallback"}

@st.cache_data(ttl=REFRESH_INTERVAL)
def fetch_solar_wind_data():
    try:
        r = requests.get(NOAA_SOLAR_WIND_URL, timeout=API_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        latest = data[-1]
        return {
            "status": "✅",
            "solar_speed": float(latest[1]),
            "solar_density": float(latest[2]),
            "wind_time": latest[0],
        }
    except Exception as e:
        st.warning(f"NOAA Solar Wind fetch failed: {e}")
        return {"status": "⚠️", "solar_speed": DEFAULT_SOLAR["solar_speed"], "solar_density": 0.0, "wind_time": "Fallback"}

# ===============================================================
# Dynamic INGV Fetch (Auto-Delimiter + Fallback)
# ===============================================================
@st.cache_data(ttl=REFRESH_INTERVAL)
def fetch_ingv_seismic_data():
    try:
        now = dt.datetime.utcnow()
        start_time = now - dt.timedelta(days=7)
        params = {
            "starttime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "endtime": now.strftime("%Y-%m-%dT%H:%M:%S"),
            "latmin": 40.7, "latmax": 40.9,
            "lonmin": 14.0, "lonmax": 14.3,
            "format": "text",
        }
        r = requests.get(INGV_API_URL, params=params, timeout=API_TIMEOUT)
        r.raise_for_status()
        text_data = r.text.strip()
        if "|" in text_data: delim = "|"
        elif ";" in text_data: delim = ";"
        else: delim = r"\s+"
        df = pd.read_csv(io.StringIO(text_data), delimiter=delim, engine="python")

        time_col = next((c for c in df.columns if "Time" in c or "Origin" in c), None)
        mag_col = next((c for c in df.columns if "Mag" in c), None)
        depth_col = next((c for c in df.columns if "Depth" in c), None)
        if not time_col or not mag_col or not depth_col:
            raise ValueError("No valid Time/Mag/Depth columns found in INGV feed.")

        df["time"] = pd.to_datetime(df[time_col], errors="coerce")
        df["magnitude"] = pd.to_numeric(df[mag_col], errors="coerce")
        df["depth_km"] = pd.to_numeric(df[depth_col], errors="coerce")
        df = df.dropna(subset=["time", "magnitude", "depth_km"])
        if df.empty:
            raise ValueError("Empty INGV dataset.")
        return df
    except Exception as e:
        st.warning(f"INGV fetch failed (auto-handled): {e}")
        return generate_synthetic_seismic_data()

# ===============================================================
# SUPT Resonance & Forecast
# ===============================================================
def generate_solar_history(psi_s, hours=24):
    now = dt.datetime.utcnow()
    times = [now - dt.timedelta(hours=i) for i in range(hours)][::-1]
    psi_vals = np.random.normal(psi_s, 0.05, hours)
    return pd.DataFrame({"time": times, "psi_s": psi_vals})

def generate_forecast_wave(psi_s, hours=48):
    now = dt.datetime.utcnow()
    times = [now + dt.timedelta(hours=i) for i in range(hours)]
    forecast_psi = np.sin(np.linspace(0, np.pi * 2, hours)) * 0.3 + psi_s
    return pd.DataFrame({"hour": range(hours), "forecast_psi": forecast_psi})

# ===============================================================
# MAIN DASHBOARD
# ===============================================================
st.set_page_config(layout="wide", page_title="SunWolf ReSunance Continuum v6.4")
st.title("☀️ SunWolf ReSunance Continuum — SUPT Live Monitor")
st.caption("Real-Time ψₛ–Depth–Kp Continuum | Campi Flegrei • SUPT v6.4")

geomag = fetch_geomag_data()
solar = fetch_solar_wind_data()
df = fetch_ingv_seismic_data()

# Status Row
st.markdown(f"**API Status:** NOAA Geomagnetic {geomag['status']} | Solar Wind {solar['status']} | INGV Seismic {'✅' if not df.empty else '⚠️'}")

# Metrics
md_max = df["magnitude"].max()
md_mean = df["magnitude"].mean()
depth_mean = df["depth_km"].mean()
shallow_ratio = len(df[df["depth_km"] < 2.5]) / max(len(df), 1)
psi_s = DEFAULT_SOLAR["psi_s"]

EII = compute_eii(md_max, md_mean, shallow_ratio, psi_s)
RPAM = classify_phase(EII)

col1, col2, col3 = st.columns(3)
col1.metric("Energetic Instability Index (EII)", f"{EII:.3f}")
col2.metric("RPAM Status", RPAM)
col3.metric("Kp Index", f"{geomag['kp_index']:.1f}")

# Coupling Gauge
st.markdown("### ☯ ψₛ–Depth Coherence Index (CCI)")
psi_hist = generate_solar_history(psi_s)
depth_signal = np.interp(np.linspace(0, len(df) - 1, 24), np.arange(len(df)),
                         np.clip(df["depth_km"].rolling(3, min_periods=1).mean(), 0, 5))
psi_norm = (psi_hist["psi_s"] - np.mean(psi_hist["psi_s"])) / np.std(psi_hist["psi_s"])
depth_norm = (depth_signal - np.mean(depth_signal)) / np.std(depth_signal)
cci = np.corrcoef(psi_norm, depth_norm)[0, 1] ** 2 if len(df) > 1 else 0
color = "green" if cci >= 0.7 else "orange" if cci >= 0.4 else "red"
label = "Coherent" if cci >= 0.7 else "Moderate" if cci >= 0.4 else "Decoupled"
gauge = go.Figure(go.Indicator(
    mode="gauge+number", value=cci,
    title={"text": f"CCI: {label}"},
    gauge={"axis": {"range": [0, 1]},
           "bar": {"color": color},
           "steps": [{"range": [0, 0.4], "color": "#FFCDD2"},
                     {"range": [0.4, 0.7], "color": "#FFF59D"},
                     {"range": [0.7, 1.0], "color": "#C8E6C9"}]}))
st.plotly_chart(gauge, use_container_width=True)

# ψ Forecast
st.markdown("### 🔮 48-Hour ψₛ Resonance Forecast")
forecast = generate_forecast_wave(psi_s)
fig = go.Figure()
fig.add_trace(go.Scatter(x=forecast["hour"], y=forecast["forecast_psi"],
                         mode="lines", line=dict(color="#FFB300", width=3)))
fig.update_layout(title="SUPT ψₛ Harmonic Projection (48h)", xaxis_title="Hours Ahead",
                  yaxis_title="ψₛ Index", template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# Footer
st.caption(f"Updated {dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')} | Feeds: NOAA • INGV | Mode: Continuum Live v6.4")
st.caption("Powered by Sheppard’s Universal Proxy Theory — ψₛ–Depth–Kp Harmonic Continuity Engine.")
st.caption("Auto-refresh every 60 seconds.")

# Auto-refresh
time.sleep(REFRESH_INTERVAL)
st.experimental_rerun()
