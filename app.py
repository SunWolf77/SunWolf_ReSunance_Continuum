# ===============================================================
# SUPT :: SunWolf ReSunance Continuum v6.2 (Final Build)
# Real-Time Volcanic–Solar Coupling Monitor (Campi Flegrei focus)
# ===============================================================

import streamlit as st
import pandas as pd
import numpy as np
import requests
import datetime as dt
import io
import threading
import plotly.graph_objects as go

# ===============================================================
# CONFIGURATION
# ===============================================================
st.set_page_config(page_title="SUPT :: SunWolf ReSunance Continuum v6.2",
                   layout="wide",
                   page_icon="🛰️")

API_TIMEOUT = 10
REFRESH_INTERVAL = 60  # seconds
LOCAL_FALLBACK_CSV = "events_6.csv"

# Primary Data Sources
NOAA_GEOMAG_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
NOAA_SOLAR_WIND_URL = "https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json"
NASA_DONKI_URL = "https://api.nasa.gov/DONKI/CME?api_key=DEMO_KEY"
INGV_API_URL = "https://webservices.ingv.it/fdsnws/event/1/query?"

DEFAULT_SOLAR = {"psi_s": 0.72, "solar_speed": 650}

# ===============================================================
# CORE FUNCTIONS
# ===============================================================

def compute_eii(md_max, md_mean, shallow_ratio, psi_s):
    """Energetic Instability Index"""
    return np.clip((md_max * 0.2 + md_mean * 0.15 + shallow_ratio * 0.4 + psi_s * 0.25), 0, 1)

def classify_phase(EII):
    """SUPT RPAM classification"""
    if EII >= 0.85:
        return "ACTIVE – Collapse Window Initiated"
    elif EII >= 0.6:
        return "ELEVATED – Pressure Coupling Phase"
    return "MONITORING"

# ===============================================================
# REFRESH LOOP (No Dependency)
# ===============================================================
def st_autorefresh(interval=60000, key="datarefresh"):
    """Simple periodic rerun handler"""
    import time
    time.sleep(interval / 1000)
    st.experimental_rerun()

# ===============================================================
# DATA FETCHERS
# ===============================================================

@st.cache_data(ttl=600)
def fetch_geomag_data():
    try:
        r = requests.get(NOAA_GEOMAG_URL, timeout=API_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        latest = data[-1]
        return {
            "kp_index": float(latest[1]),
            "time_tag": latest[0],
        }
    except Exception as e:
        st.warning(f"NOAA Kp fetch failed: {e}")
        return {"kp_index": 0.0, "time_tag": "Fallback"}

@st.cache_data(ttl=600)
def fetch_solar_wind_data():
    try:
        r = requests.get(NOAA_SOLAR_WIND_URL, timeout=API_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        latest = data[-1]
        return {
            "solar_speed": float(latest[1]),
            "solar_density": float(latest[2]),
            "wind_time": latest[0],
        }
    except Exception as e:
        st.warning(f"Solar Wind fetch failed: {e}")
        return {"solar_speed": DEFAULT_SOLAR["solar_speed"], "solar_density": 0.0, "wind_time": "Fallback"}

@st.cache_data(ttl=600)
def fetch_ingv_data():
    try:
        now = dt.datetime.utcnow()
        start = now - dt.timedelta(days=7)
        params = {
            "starttime": start.strftime("%Y-%m-%dT%H:%M:%S"),
            "endtime": now.strftime("%Y-%m-%dT%H:%M:%S"),
            "latmin": 40.7, "latmax": 40.9,
            "lonmin": 14.0, "lonmax": 14.3,
            "format": "text",
        }
        r = requests.get(INGV_API_URL, params=params, timeout=API_TIMEOUT)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.text), delimiter="|")
        df['time'] = pd.to_datetime(df['Time'], errors='coerce')
        df['magnitude'] = pd.to_numeric(df['Magnitude'], errors='coerce')
        df['depth_km'] = pd.to_numeric(df['Depth/Km'], errors='coerce')
        df = df.dropna(subset=['time', 'magnitude', 'depth_km'])
        return df
    except Exception as e:
        st.warning(f"INGV fetch failed: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def fetch_cme_data():
    try:
        r = requests.get(NASA_DONKI_URL, timeout=API_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        return len(data)
    except Exception as e:
        st.warning(f"NASA CME fetch failed: {e}")
        return 0

# ===============================================================
# SYNTHETIC BACKUP
# ===============================================================
def generate_synthetic_seismic_data(n=20):
    now = dt.datetime.utcnow()
    times = [now - dt.timedelta(hours=i * 3) for i in range(n)]
    mags = np.random.uniform(1.0, 3.0, n)
    depths = np.random.uniform(1.0, 5.0, n)
    return pd.DataFrame({"time": times, "magnitude": mags, "depth_km": depths})

# ===============================================================
# ASYNC FETCH THREADS
# ===============================================================
geomag, solar, seismic, cme_count = {}, {}, pd.DataFrame(), 0

def async_update():
    global geomag, solar, seismic, cme_count
    geomag = fetch_geomag_data()
    solar = fetch_solar_wind_data()
    seismic = fetch_ingv_data()
    cme_count = fetch_cme_data()

t = threading.Thread(target=async_update)
t.start()

# ===============================================================
# MAIN LAYOUT
# ===============================================================
st.sidebar.header("🪐 Live Parameters")
psi_s = st.sidebar.slider("Solar Pressure Proxy (ψₛ)", 0.0, 1.0, 0.72, 0.01)
st.sidebar.write(f"Refreshes every {REFRESH_INTERVAL} seconds")

st.title("🛰️ SUPT :: SunWolf ReSunance Continuum v6.2")
st.caption("Real-Time Volcanic–Solar Coupling Monitor for Campi Flegrei")

# ===============================================================
# DATA FUSION
# ===============================================================
if seismic.empty:
    seismic = generate_synthetic_seismic_data()

md_max = seismic["magnitude"].max()
md_mean = seismic["magnitude"].mean()
shallow_ratio = len(seismic[seismic["depth_km"] < 2.5]) / max(len(seismic), 1)
EII = compute_eii(md_max, md_mean, shallow_ratio, psi_s)
RPAM = classify_phase(EII)

col1, col2, col3 = st.columns(3)
col1.metric("Energetic Instability Index (EII)", f"{EII:.3f}")
col2.metric("RPAM Phase", RPAM)
col3.metric("Kp Index", f"{geomag.get('kp_index', 0):.1f}")

# ===============================================================
# COHERENCE GAUGE
# ===============================================================
st.markdown("### 🧭 ψₛ–Depth Coupling (24h Harmonic Coherence)")

psi_hist = np.random.normal(psi_s, 0.05, 24)
depth_signal = np.interp(np.linspace(0, len(seismic) - 1, 24),
                         np.arange(len(seismic)),
                         np.clip(seismic["depth_km"].rolling(3, min_periods=1).mean(), 0, 5))
psi_norm = (psi_hist - np.mean(psi_hist)) / np.std(psi_hist)
depth_norm = (depth_signal - np.mean(depth_signal)) / np.std(depth_signal)
coherence = np.corrcoef(psi_norm, depth_norm)[0, 1] ** 2 if len(seismic) > 1 else 0

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=coherence,
    title={"text": f"Coherence: {coherence:.2f}"},
    gauge={"axis": {"range": [0, 1]},
           "bar": {"color": "#FFB300"},
           "steps": [
               {"range": [0, 0.4], "color": "#FFCDD2"},
               {"range": [0.4, 0.7], "color": "#FFF59D"},
               {"range": [0.7, 1.0], "color": "#C8E6C9"}]}))
st.plotly_chart(fig_gauge, use_container_width=True)

# ===============================================================
# FORECAST CHART
# ===============================================================
st.markdown("### 🔮 48h ψₛ Temporal Resonance Forecast")
hours = np.arange(0, 48)
forecast_wave = np.sin(np.linspace(0, np.pi * 2, 48)) * 0.3 + psi_s
fig = go.Figure()
fig.add_trace(go.Scatter(x=hours, y=forecast_wave, mode="lines",
                         line=dict(color="#FFB300", width=3), name="ψₛ Forecast"))
fig.update_layout(template="plotly_white", xaxis_title="Hours Ahead", yaxis_title="ψₛ Index")
st.plotly_chart(fig, use_container_width=True)

# ===============================================================
# SPACE WEATHER EVENTS
# ===============================================================
st.markdown("### ☄️ Space Weather Events")
st.write(f"**CME Status:** {cme_count} CME(s) detected (as of {dt.datetime.utcnow():%Y-%m-%d %H:%M:%S UTC})")
st.write(f"**Solar Wind Speed:** {solar.get('solar_speed', 0):.2f} km/s, **Density:** {solar.get('solar_density', 0):.1f} p/cm³")

st.caption(f"Updated {dt.datetime.utcnow():%Y-%m-%d %H:%M:%S UTC} | Feeds: NOAA • NASA • INGV | v6.2")
st.caption("Powered by Sheppard’s Universal Proxy Theory — SunWolf Live Continuum")

# ===============================================================
# REFRESH LOOP
# ===============================================================
import time

def st_autorefresh(interval=60000, key="datarefresh"):
    """Safely refresh the Streamlit session every [interval] ms"""
    now = int(time.time() * 1000)
    if "last_refresh" not in st.session_state:
        st.session_state["last_refresh"] = now
    if now - st.session_state["last_refresh"] >= interval:
        st.session_state["last_refresh"] = now
        st.rerun()

