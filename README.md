# ☀️ SUPT :: SunWolf ReSunance Continuum v6.1

**SunWolf ReSunance Continuum** is a live, AI-integrated dashboard built on **Sheppard’s Universal Proxy Theory (SUPT)**.  
It continuously tracks and visualizes **solar–volcanic coupling**, focusing on **Campi Flegrei** and related global geomagnetic conditions.

---

## 🌍 Live Data Feeds
| Source | API | Description |
|--------|-----|-------------|
| **NOAA SWPC** | `/noaa-planetary-k-index.json` | Real-time geomagnetic Kp index |
| **NOAA Solar Wind** | `/solar-wind/plasma-7-day.json` | Plasma speed and density |
| **NASA DONKI** | `/DONKI/CME` | CME events and timings |
| **INGV FDSNWS** | `/fdsnws/event/1/query` | Campi Flegrei seismic activity |

---

## ⚙️ Features
- Real-time updates every **60 seconds**
- Automatic caching + API fallback safety
- SUPT Energetic Instability Index (EII) computation
- ψₛ–Depth coupling gauge (CCI metric)
- 48-hour ψₛ resonance forecast
- Live solar wind, density, and CME feed integration
- Streamlit-native UI (dark theme optimized)

---

## 🚀 Running Locally
```bash
git clone https://github.com/<your-username>/SunWolf_ReSunance_Continuum.git
cd SunWolf_ReSunance_Continuum
pip install -r requirements.txt
streamlit run app.py
