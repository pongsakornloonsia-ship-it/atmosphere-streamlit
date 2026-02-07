import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================= CONFIG =================
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# ================= THEME TOGGLE =================
mode = st.sidebar.toggle("🌙 Dark mode")

if mode:
    bg = "#0f172a"
    card = "#1e293b"
    text = "#e5e7eb"
else:
    bg = "#ecfeff"
    card = "white"
    text = "#022c22"

# ================= CSS =================
st.markdown(f"""
<style>
body {{
    background:{bg};
}}

.block-container {{
    padding-top:2rem;
}}

.card {{
    background:{card};
    padding:26px;
    border-radius:22px;
    box-shadow:0 12px 30px rgba(0,0,0,.15);
    margin-bottom:25px;
}}

h1,h2,h3 {{
    color:{text};
}}

.big {{
    font-size:46px;
    font-weight:700;
}}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("🌍 Weather Forecast Dashboard")
st.caption("เครื่องมือจำลองการคำนวณและแสดงข้อมูลสภาพอากาศ")

# ================= SIDEBAR INPUT =================
st.sidebar.header("⚙️ Controls")

temp = st.sidebar.slider("🌡️ Temperature °C", -10, 45, 28)
rain = st.sidebar.slider("🌧️ Rain (mm)", 0, 50, 5)

cloud = st.sidebar.select_slider(
    "☁️ Cloud cover %",
    options=[0, 20, 40, 60, 80, 100],
    value=40
)

F = st.sidebar.number_input("📉 Force (N)", value=101300.0)
A = st.sidebar.number_input("📐 Area (m²)", value=1.0)

m_real = st.sidebar.number_input("💧 Vapor mass (g)", value=12.5)
m_sat = st.sidebar.number_input("💧 Saturated vapor (g)", value=17.3)

# ================= CALC =================
pressure = F / A if A else 0
rh = (m_real / m_sat) * 100 if m_sat else 0

# ================= OVERVIEW =================
st.subheader("📊 Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Temperature", f"{temp} °C")
c2.metric("Pressure", f"{pressure:,.0f} Pa")
c3.metric("Humidity", f"{rh:.1f}%")
c4.metric("Rain", f"{rain} mm")

# ================= FORECAST DATA =================
days = pd.date_range("today", periods=7)

df = pd.DataFrame({
    "Day": days.strftime("%a"),
    "Temperature": temp + np.random.randint(-3, 4, 7),
    "Rain": np.random.randint(0, rain + 5, 7),
    "Cloud": np.random.choice([0, 20, 40, 60, 80, 100], 7)
})

# ================= CHART =================
st.subheader("📈 7-Day Trend")

fig, ax = plt.subplots()
ax.plot(df["Day"], df["Temperature"])
ax.set_ylabel("°C")
ax.set_title("Temperature Forecast")
st.pyplot(fig)

# ================= MAP =================
st.subheader("🗺️ Map")

map_df = pd.DataFrame({
    "lat": [13.75],
    "lon": [100.5]
})

st.map(map_df)

# ================= DETAIL =================
st.subheader("📑 Details")

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='card'>🌡️ Temperature<br><span class='big'>"
                f"{temp}°C</span></div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>☁️ Cloud Cover<br><span class='big'>"
                f"{cloud}%</span></div>", unsafe_allow_html=True)
