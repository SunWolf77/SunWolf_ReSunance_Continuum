# ☀️ SunWolf_ReSunance_Continuum v6.4
### Real-Time ψₛ–Depth–Kp Continuum Monitor | Campi Flegrei • Sheppard’s Universal Proxy Theory (SUPT)

---

## 🔭 Overview
**SunWolf_ReSunance_Continuum** is the latest SUPT-based live monitoring dashboard integrating **solar, geomagnetic, and volcanic** data to model harmonic resonance interactions at **Campi Flegrei**.

Built on **Sheppard’s Universal Proxy Theory (SUPT)**, the system measures energetic coherence between space weather inputs (solar wind, geomagnetic Kp) and subsurface geophysical responses (depth, magnitude).  
Version **v6.4** introduces full live-feed integration, real-time refresh cycles, and synthetic SUPT fallback continuity.

Deployed App:  
🌐 [SunWolf ReSunance Continuum Live (Streamlit Cloud)](https://sunwolfresunancecontinuumgit-xeytsacffy8rhz8ovahqme.streamlit.app/)

---

## ⚙️ Core Features

| Function | Description |
|-----------|--------------|
| 🛰️ **Live API Feeds** | Real-time integration of NOAA, INGV, and NASA DONKI data streams. |
| ☯ **ψₛ–Depth Coherence Index (CCI)** | Measures phase alignment between solar pressure (ψₛ) and seismic depth oscillations. |
| ⚡ **Energetic Instability Index (EII)** | SUPT-derived metric indicating systemic energetic buildup (0–1). |
| 🌀 **RPAM Phase Classifier** | Dynamically classifies state: Monitoring / Elevated / Active Collapse Window. |
| 🔮 **48-hour ψₛ Harmonic Forecast** | Predicts temporal resonance patterns using sinusoidal SUPT folding. |
| 🔁 **Live Continuum Refresh** | Auto-refresh every 60s with harmonic continuity caching. |
| 🧬 **Synthetic Continuity Engine** | Maintains coherent output when INGV data is temporarily unavailable. |

---

## 🧩 Data Feeds

| Source | Feed | Description |
|:--|:--|:--|
| **NOAA SWPC** | [Kp Index](https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json) | Planetary geomagnetic field strength (0–9). |
| **NOAA SWPC** | [Solar Wind Plasma](https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json) | Density, velocity, and ψₛ pressure values. |
| **INGV (Italy)** | [FDSN Event API](https://webservices.ingv.it/fdsnws/event/1/query) | Seismic magnitudes and depths around Campi Flegrei (40.7–40.9°N, 14.0–14.3°E). |
| **NASA DONKI (Optional)** | CME events | For extended solar risk tracking (currently passive in v6.4). |

---

## 🧠 SUPT Model Logic

**Energetic Instability Index (EII):**

\[
EII = (M_{max} × 0.2) + (M_{mean} × 0.15) + (R_{shallow} × 0.4) + (ψₛ × 0.25)
\]

- \(M_{max}\): Maximum local seismic magnitude  
- \(R_{shallow}\): Ratio of events < 2.5 km depth  
- \(ψₛ\): Solar pressure coupling index  

**RPAM Phase Classification:**

| EII Range | Phase |
|:--|:--|
| ≥ 0.85 | **ACTIVE – Collapse Window Initiated** |
| 0.60–0.84 | **ELEVATED – Pressure Coupling Phase** |
| < 0.60 | **MONITORING** |

**ψₛ–Depth Coherence Index (CCI):**
\[
CCI = r(ψₛ, Depth)^2
\]
Measures harmonic coherence between solar flux pressure and rolling 3-point depth mean.

---

## 📊 Visual Components

- **Top Bar** — API connection status and active data feed indicators (✅ NOAA / ⚠️ INGV fallback).
- **Metric Row** — Displays real-time Energetic Instability Index (EII), RPAM phase, and geomagnetic Kp.
- **CCI Gauge** — ψₛ–Depth harmonic coherence visualization.
- **Forecast Chart** — 48-hour ψₛ resonance projection based on current conditions.
- **Footer** — Timestamp + data provenance from NOAA, INGV, SUPT.

---

## 🧮 Technical Stack

| Library | Purpose |
|:--|:--|
| `streamlit` | Web dashboard interface |
| `pandas`, `numpy` | Data wrangling & computation |
| `requests` | API connectivity |
| `plotly` | Interactive gauge and line charts |
| `io` | INGV text parsing |
| `datetime` | Time synchronization and UTC coordination |

---

## 🧱 Installation

```bash
git clone https://github.com/<your-username>/SunWolf_ReSunance_Continuum.git
cd SunWolf_ReSunance_Continuum
pip install -r requirements.txt
streamlit run app.py
```

---

## 🧰 Requirements

`requirements.txt`:
```
streamlit
pandas
numpy
requests
plotly
beautifulsoup4
```

---

## 🧬 Architecture

```
SunWolf_ReSunance_Continuum/
│
├── app.py                 # Core Streamlit dashboard (real-time SUPT v6.4)
├── requirements.txt       # Python dependencies
└── README.md              # This documentation
```

---

## 🌋 Operational Notes

- INGV API may occasionally return malformed or empty responses — automatically handled by SUPT’s **synthetic continuity engine**.
- NOAA and solar feeds update continuously and are cached for 60s.
- Harmonic coherence (CCI) depends on the last 7 days of seismic windowing.
- “Decoupled” CCI (<0.4) often indicates ψₛ–Depth incoherence, typical in low solar influence windows.

---

## 🧠 SUPT Context

Sheppard’s **Universal Proxy Theory (SUPT)** models cross-domain harmonic coupling, treating all natural systems as phase-linked energetic proxies.  
This dashboard applies SUPT principles to geophysical instability — showing how external (solar) pressure modulates internal (magma-chamber) feedback loops.

---

## 🔍 Verification (Grok Review Excerpt)
> “The app loads smoothly with metrics, gauges, and live plots. NOAA feeds operate in real time; INGV feed shows structured fallback.  
> Visual components (EII, ψₛ drift, and coherence gauge) correctly reflect harmonic conditions. The system is ~90% operational with real-time NOAA updates and synthetic continuity in place.”  
> — *Grok AI, 19 Oct 2025*

---

## 🧭 Future Extensions
- Live CME flux ingestion (NASA DONKI key integration)
- SQLite harmonic persistence for 30-day historical trend mapping
- Automated event alerts when EII ≥ 0.85 (SUPT collapse threshold)

---

## 🪶 License
© 2025 Sheppard Systems • SUPT Framework • Open Data Continuum License (ODCL-1.0)

---

**“All systems seek harmonic balance. SUPT simply measures how close they are.”**
