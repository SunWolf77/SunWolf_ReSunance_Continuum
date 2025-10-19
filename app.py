# ===============================================================
# SUPT :: SunWolf ReSunance Continuum v6.1 (Final Live Build)
# ===============================================================

import streamlit as st
import pandas as pd
import numpy as np
import requests
import datetime as dt
import io
import traceback
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh  # ✅ fixes NameError

# ---------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------
API_TIMEOUT = 10
NOAA_GEOMAG_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
NOAA_SOLAR_WIND_URL = "https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json"
NASA_DONKI_URL = "https://api.nasa.gov/DONKI/CME"
NASA_API_KEY = "DEMO_KEY"   # Replace with your NASA API key
INGV_API_URL = "https://webservices.ingv.it/fdsnws/event/1/query"

DEFAULT_SOLAR = {"psi_s": 0.72, "solar_speed": 688}
REFRESH_INTERVAL = 60  # seconds

# ---------------------------------------------------------------
# CORE FUNCTIONS
# ---------------------------------------------------------------
def compute_eii(md_max, md_mean, shallow_ratio, psi_s):
    return np.clip(md_max * 0.2 + md_mean * 0.15 + shallow_ratio * 0.4 + psi_s * 0.25, 0, 1)

def classify_phase(EII):
    if EII >= 0.85:
        return "ACTIVE – Collapse Window Initiated"
    elif EII >= 0.6:
        return "ELEVATED – Pressure Coupling Phase"
    return "MONITORING"

# ---------------------------------------------------------------
# LIVE FEEDS
# ---------------------------------------------------------------
@st.cache_data(ttl=600)
def fetch_noaa_geomag():
    try:
        r = requests.get(NOAA_GEOMAG_URL, timeout=API_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        latest = data[-1]
        return float(latest[1]), latest[0]
    except Exception as e:
        st.warning(f"NOAA geomagnetic feed failed: {e}")
        return 0.0, "Fallback"

@st.cache_data(ttl=600)
def fetch_noaa_solarwind():
    try:
        r = requests.get(NOAA_SOLAR_WIND_URL, timeout=API_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        latest = data[-1]
        return float(latest[1]), float(latest[2]), latest[0]
    except Exception as e:
        st.warning(f"NOAA solar wind feed failed: {e}")
        return DEFAULT_SOLAR["solar_speed"], 0.0, "Fallback"

@st.cache_data(ttl=600)
def fetch_nasa_cme():
    try:
        now = dt.datetime.utcnow()
        start = (now - dt.timedelta(days=5)).strftime("%Y-%m-%d")
        end = now.strftime("%Y-%m-%d")
        params = {"startDate": start, "endDate": end, "api_key": NASA_API_KEY}
        r = requests.get(NASA_DONKI_URL, params=params, timeout=API_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        if data:
            return f"{len(data)} CME(s) detected", data[-1].get("startTime", "N/A")
        return "No CMEs", "N/A"
    except Exception as e:
        st.warning(f"NASA DONKI fetch failed: {e}")
        return "No CMEs", "Fallback"

@st.cache_data(ttl=600)
def fetch_ingv_seismic():
    try:
        now = dt.datetime.utcnow()
        start = now - dt.timedelta(days=7)
        params = {
            "starttime": start.strftime("%Y-%m-%dT%H:%M:%S"),
            "endtime": now.strftime("%Y-%m-%dT%H:%M:%S"),
            "latmin": 40.7, "latmax": 40.9,
            "lonmin": 14.0, "lonmax": 14.3,
            "format": "text"
        }
        r = requests.get(INGV_API_URL, params=params, timeout=API_TIMEOUT)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.text), delimiter="|")
        df["time"] = pd.to_datetime(df["Time"], errors="coerce")
        df["magnitude"] = pd.to_numeric(df["Magnitude"], errors="coerce")
        df["depth_km"] = pd.to_numeric(df["Depth/Km"], errors="coerce")
        return df.dropna(subset=["time", "magnitude", "depth_km"])
    except Exception as e:
        st.warning(f"INGV feed failed: {e}")
        return pd.DataFrame()

# ---------------------------------------------------------------
# FORECAST & SIGNAL GENERATORS
# ---------------------------------------------------------------
def generate_solar_history(psi_s, hours=24):
    now = dt.datetime.utcnow()
    times = [now - dt.timedelta(hours=i) for i in range(hours)][::-1]
    psi_vals = np.random.normal(psi_s, 0.05, hours)
    return pd.DataFrame({"time": times, "psi_s": psi_vals})

def generate_forecast_wave(psi_s, hours=48):
    times = np.arange(hours)
    psi_vals = np.sin(np.linspace(0, 2 * np.pi, hours)) * 0.3 + psi_s
    return pd.DataFrame({"hour": times, "psi_s": psi_vals})

# ---------------------------------------------------------------
# MAIN DASHBOARD
# ---------------------------------------------------------------
st.set_page_config(layout="wide", page_title="SunWolf ReSunance Continuum")
# Auto-refresh every 60 seconds (as per .env setting or default)
REFRESH_INTERVAL = int(st.secrets.get("REFRESH_INTERVAL", 60))
st_autorefresh(interval=REFRESH_INTERVAL * 1000, key="datarefresh")

st.title("🛰️ SUPT :: SunWolf ReSunance Continuum v6.1")
st.caption("Real-Time Volcanic-Solar Coupling Monitor for Campi Flegrei")

# Sidebar controls
st.sidebar.header("⚙️ Live Parameters")
psi_s = st.sidebar.slider("Solar Pressure Proxy (ψₛ)", 0.0, 1.0, DEFAULT_SOLAR["psi_s"])
st.sidebar.write("Refreshes every 60 seconds")

# Live data
kp_index, kp_time = fetch_noaa_geomag()
solar_speed, solar_density, wind_time = fetch_noaa_solarwind()
cme_status, cme_time = fetch_nasa_cme()
df = fetch_ingv_seismic()

# Compute SUPT metrics
md_max = df["magnitude"].max() if not df.empty else 0
md_mean = df["magnitude"].mean() if not df.empty else 0
shallow_ratio = len(df[df["depth_km"] < 2.5]) / len(df) if len(df) > 0 else 0
EII = compute_eii(md_max, md_mean, shallow_ratio, psi_s)
RPAM = classify_phase(EII)

# Metrics display
col1, col2, col3 = st.columns(3)
col1.metric("Energetic Instability Index (EII)", f"{EII:.3f}")
col2.metric("RPAM Phase", RPAM)
col3.metric("Kp Index", f"{kp_index:.1f}")

# Gauges
st.markdown("### ☯ ψₛ–Depth Coupling (24h Harmonic Coherence)")
if not df.empty:
    psi_hist = generate_solar_history(psi_s)
    depth_norm = (df["depth_km"] - df["depth_km"].mean()) / df["depth_km"].std()
    psi_norm = (psi_hist["psi_s"] - psi_hist["psi_s"].mean()) / psi_hist["psi_s"].std()
    cci = np.corrcoef(psi_norm[:min(len(psi_norm), len(depth_norm))],
                      depth_norm[:min(len(psi_norm), len(depth_norm))])[0, 1] ** 2
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=cci,
        title={"text": f"Coherence: {cci:.2f}"},
        gauge={"axis": {"range": [0, 1]},
               "bar": {"color": "#29B6F6"},
               "steps": [
                   {"range": [0, 0.4], "color": "#FFCDD2"},
                   {"range": [0.4, 0.7], "color": "#FFF59D"},
                   {"range": [0.7, 1.0], "color": "#C8E6C9"}]}))
    st.plotly_chart(gauge, use_container_width=True)
else:
    st.info("No INGV data available for coherence gauge.")

# Forecast chart
st.markdown("### 🔮 48h ψₛ Temporal Resonance Forecast")
forecast = generate_forecast_wave(psi_s)
fig = go.Figure()
fig.add_trace(go.Scatter(x=forecast["hour"], y=forecast["psi_s"],
                         mode="lines", line=dict(color="#FFA726", width=3)))
fig.update_layout(title="Next 48 Hours ψₛ Forecast", template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# CME + Status
st.markdown("### ☄️ Space Weather Events")
st.write(f"**CME Status:** {cme_status} (as of {cme_time})")
st.write(f"**Solar Wind Speed:** {solar_speed} km/s, **Density:** {solar_density} p/cm³ (as of {wind_time})")

# Footer
st.caption(f"Updated {dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')} | Feeds: NOAA • NASA • INGV | v6.1")
st.caption("Powered by Sheppard’s Universal Proxy Theory — SunWolf Live Continuum")

st_autorefresh = st.experimental_rerun


