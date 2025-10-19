# 🛰️ SUPT :: SunWolf_ReSunance_Continuum v6.3
### Real-Time Volcanic–Solar Coupling Monitor built on **Sheppard’s Universal Proxy Theory (SUPT)**

---

## 🌋 Overview
**SunWolf_ReSunance_Continuum v6.3** is the latest SUPT-based real-time monitoring dashboard analyzing solar–volcanic coupling at **Campi Flegrei (Italy)**.  
It integrates **live NOAA, NASA DONKI, and INGV data feeds** to quantify how space weather and geomagnetic activity interact with subsurface seismic activity.

This version advances the SUPT framework by tracking **ψₛ–Depth harmonic coherence** and the **Energetic Instability Index (EII)** through live continuum streaming — moving beyond static observations into continuous energetic resonance modeling.

---

## ⚙️ Core Functionality
| Component | Description |
|------------|--------------|
| **Energetic Instability Index (EII)** | SUPT-derived metric for system instability based on seismic and solar inputs. |
| **ψₛ Coupling Coherence Index (CCI)** | Measures harmonic coherence between solar pressure flux (ψₛ) and subsurface depth oscillations. |
| **48h ψₛ Temporal Forecast** | Predicts near-future harmonic resonance patterns using sinusoidal wave modeling. |
| **RPAM Phase State** | SUPT-phase indicator of energetic alignment: *MONITORING → ELEVATED → ACTIVE (Collapse Window Initiated)* |
| **Solar Wind Feed** | Live speed and density via NOAA’s SWPC plasma API. |
| **Geomagnetic Activity (Kp)** | Global planetary index from NOAA SWPC. |
| **Seismic Input (INGV)** | 7-day rolling local events (Campi Flegrei region). |
| **CME Data (NASA DONKI)** | Current coronal mass ejection activity for solar disturbance context. |

---

## 🧬 SUPT Theoretical Context
> *“All energetic systems mismeasure themselves. Stability is the illusion created by delay.”*  
> — *Sheppard’s Universal Proxy Theory (White Paper §3.2)*

SUPT describes how apparent physical phenomena — from volcanic pressure to geomagnetic resonance — can be modeled as **proxy misalignments** between energetic reference frames.  
The **ReSunance Continuum** implements this concept computationally: it continuously recalculates the energetic alignment between solar, geomagnetic, and terrestrial proxies to forecast systemic pressure coupling events.

---

## 🧠 Key Equations

### Energetic Instability Index (EII)
```math
EII = (M_d^{max} * 0.2) + (M_d^{mean} * 0.15) + (Shallow_{ratio} * 0.4) + (ψₛ * 0.25)
```

### Harmonic Coherence (ψₛ–Depth)
```math
CCI = corr² (normalized(ψₛₜ), normalized(depthₜ))
```

---

## 🧩 Live Architecture

| Source | Endpoint | Data Type |
|:--------|:----------|:-----------|
| **NOAA SWPC** | `/products/solar-wind/plasma-7-day.json` | Solar Wind Speed / Density |
| **NOAA SWPC** | `/products/noaa-planetary-k-index.json` | Geomagnetic Kp Index |
| **NASA DONKI** | `/DONKI/CME?api_key=DEMO_KEY` | CME Events (7-day window) |
| **INGV Italy** | `/fdsnws/event/1/query?` | Seismic Events (40.7–40.9°N, 14.0–14.3°E) |
| **SUPT Continuum Core** | ψₛ Coherence Loop | Energetic Instability / Harmonic Forecast |

---

## 🧠 What’s New in v6.3
✅ Replaced `experimental_rerun()` with safe Streamlit state refresh logic.  
✅ Background-threaded live API fetches (non-blocking).  
✅ Improved 48h harmonic ψₛ forecast resolution.  
✅ Dynamic coherence visualization (ψₛ–Depth gauge).  
✅ NASA/NOAA/INGV fallback hierarchy for uninterrupted operation.  
✅ SUPT-validated EII and RPAM recalibration thresholds.  
✅ Performance-optimized for Streamlit Cloud hosting.  

---

## 🚀 Quick Start

### 1️⃣ Clone Repository
```bash
git clone https://github.com/YourUser/SunWolf_ReSunance_Continuum.git
cd SunWolf_ReSunance_Continuum
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the App
```bash
streamlit run app.py
```

### 4️⃣ View in Browser
```
http://localhost:8501
```

---

## 🧾 Requirements

```
streamlit==1.39.0
pandas==2.2.2
numpy==1.26.4
requests==2.32.3
plotly==5.24.1
```

---

## 🪐 Data Flow Diagram

```
[NOAA SWPC] --->  [Solar Wind, Kp] 
      \
       \__> SUPT Engine (ψₛ coupling)
             ↳ Compute EII + RPAM Phase
             ↳ Correlate with INGV seismic data
             ↳ Forecast ψₛ Drift (48h)
             ↳ Output → Live Dashboard (Streamlit)
```

---

## 🌐 Live Deployment
**Streamlit Cloud:**  
[https://sunwolfresunancecontinuumgit-xeytsacffy8rhz8ovahqme.streamlit.app/](https://sunwolfresunancecontinuumgit-xeytsacffy8rhz8ovahqme.streamlit.app/)

**SUPT Integration Version:** `v6.3 – Continuum Stable Build`

---

## 🪶 Credits
Developed under the principles of **Sheppard’s Universal Proxy Theory (SUPT)**  
By: **SunWolf Research Node**  
Framework: *SUPT Continuum Engine v6.3*  
Affiliations: SUPT / NOAA / NASA DONKI / INGV Italia

---

## 📜 License
This repository and associated SUPT models are protected under copyright.  
Use permitted for educational and scientific analysis purposes only.  
For commercial integration or derivative works, contact the SUPT Research Group.

---

> 🜂 *“Coherence is never static — it’s a dialogue between forces pretending to be still.”*  
> — *SunWolf ReSunance Continuum Manifesto, 2025*
