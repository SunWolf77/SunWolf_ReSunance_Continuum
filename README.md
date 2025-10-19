<p align="center">
  <img src="https://github.com/<your-username>/SunWolf_ReSunance_Continuum/assets/logo-sunwolf.png" alt="SunWolf Logo" width="140"/>
</p>

<h1 align="center">🛰️ SUPT :: SunWolf ReSunance Continuum v6.1</h1>
<h3 align="center">Real-Time Solar–Volcanic Coupling Monitor (Campi Flegrei Focus)</h3>

<p align="center">
  <a href="https://supt-dashboard-anx3dpczdl7ksbqittqx4t.streamlit.app/">
    <img src="https://img.shields.io/badge/Live-Dashboard%20Online-brightgreen?style=for-the-badge&logo=streamlit">
  </a>
  <a href="https://api.nasa.gov/">
    <img src="https://img.shields.io/badge/API-NASA%20DONKI-blue?style=for-the-badge&logo=nasa">
  </a>
  <a href="https://services.swpc.noaa.gov/">
    <img src="https://img.shields.io/badge/API-NOAA%20SWPC-orange?style=for-the-badge&logo=noaa">
  </a>
  <a href="https://webservices.ingv.it/">
    <img src="https://img.shields.io/badge/API-INGV%20Italy-red?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjZmZmIiB2aWV3Qm94PSIwIDAgNTEyIDUxMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNNDk2IDE1NmMtMTItNDYtNDItOTAtODctMTI3LTEwNi05MC0yNjAtMTAyLTM4OC0zLTIxIDktNDUgMjgtNjMgNzAtODkgMTI1LTIwMCAyMjQtMTk5IDEyMiA4NSA0MyAxNjYgMTIyIDIwOSAxOTcgMTEgMTkgMTYgMjEgMjkgMzggNTAgNzMgMTI0IDExMyAyMDIgMTE1IDE0NCAyIDIzMS02MiAyNTMtMjA3bDIzLTIyIDQzIDY0YzQzLTU0IDY3LTEyNCA3My0yMDV6Ii8+PC9zdmc+" alt="INGV Icon">
  </a>
</p>

---

<p align="center">
  <img src="https://github.com/<your-username>/SunWolf_ReSunance_Continuum/assets/dashboard-preview.png" alt="Dashboard Preview" width="80%">
</p>

---

### 🌞 Overview

**SunWolf ReSunance Continuum** is a real-time monitoring system built on **Sheppard’s Universal Proxy Theory (SUPT)**.  
It models and visualizes **energetic coherence** between solar–geomagnetic inputs and volcanic subsurface dynamics.

The current focus is **Campi Flegrei (Italy)**, integrating:
- 🌋 INGV seismic API (real-time quakes)
- ☀️ NOAA solar wind & geomagnetic Kp indices
- 🛰️ NASA DONKI CME and flare data
- 🧮 SUPT metrics for Energetic Instability Index (EII) and ψₛ Coupling Coherence (CCI)

---

### ⚙️ Core Architecture
| Module | Function | Live Feed |
|:--------|:----------|:-----------|
| **app.py** | Streamlit dashboard logic | NOAA / NASA / INGV |
| **compute_eii()** | SUPT Energetic Instability Index | Dynamic recalculation |
| **fetch_ingv_seismic()** | Campi Flegrei FDSNWS data | 7-day rolling window |
| **ψₛ Coupling Gauge** | Real-time ψₛ–depth coherence | SUPT signal processor |
| **Forecast Wave** | 48-hour ψₛ harmonic resonance | Modeled trendline |

---

### 🧠 SUPT Logic Core

The **Energetic Instability Index (EII)** follows:
