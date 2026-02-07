import streamlit as st
import math
import random

# ================= CONFIG =================
st.set_page_config(
    page_title="Atmosphere Simulator",
    page_icon="🌤️",
    layout="wide"
)

# ================= CSS =================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#89f7fe,#fbc2eb);
}

.block-container {
    padding-top: 2rem;
}

/* ===== HEADER ===== */
.hero {
    text-align:center;
    padding:60px;
    border-radius:35px;
    background: linear-gradient(120deg,#66a6ff,#89f7fe);
    box-shadow: 0 20px 50px rgba(0,0,0,0.25);
    margin-bottom:50px;
}

.hero h1 {font-size:52px;}

.tag {
    display:inline-block;
    padding:10px 22px;
    background:white;
    border-radius:30px;
    font-weight:700;
    margin:6px;
}

/* ===== CARD ===== */
.card {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(14px);
    padding:30px;
    border-radius:28px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.18);
    margin-bottom:35px;
    transition:0.3s;
}

.card:hover {
    transform: scale(1.02);
}

.big {
    font-size:46px;
    font-weight:900;
    color:#2563eb;
}

.formula {
    background:#020617;
    color:#a7f3d0;
    padding:16px;
    border-radius:14px;
    font-family: monospace;
    margin-top:10px;
}

.wind {
    font-size:80px;
    text-align:center;
}

.cloud {
    font-size:120px;
    text-align:center;
}

/* ===== WEEK ===== */
.week {
    display:grid;
    grid-template-columns: repeat(7,1fr);
    gap:18px;
}

.day {
    background:linear-gradient(135deg,#fff1eb,#ace0f9);
    border-radius:22px;
    padding:18px;
    text-align:center;
    font-weight:700;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="hero">
    <h1>🌍 ระบบพยากรณ์อากาศ</h1>
    <h3>Atmosphere Simulator</h3>
    <div>
        <span class="tag">7-Day Forecast</span>
        <span class="tag">Interactive</span>
        <span class="tag">Science Based</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= INPUT SIDEBAR =================
st.sidebar.header("⚙️ ควบคุมค่า")

temp = st.sidebar.slider("🌡 อุณหภูมิ (°C)", -10, 45, 30)
pressure_force = st.sidebar.number_input("แรง (N)", value=101300.0)
area = st.sidebar.number_input("พื้นที่ (m²)", value=1.0)

m_real = st.sidebar.number_input("มวลไอน้ำจริง (g)", value=12.0)
m_sat = st.sidebar.number_input("มวลไอน้ำอิ่มตัว (g)", value=18.0)

wind_speed = st.sidebar.slider("💨 ความเร็วลม (km/h)", 0, 120, 20)
wind_dir = st.sidebar.slider("🧭 ทิศลม (°)", 0, 360, 90)

cloud_cover = st.sidebar.slider("☁️ Cloud %", 0, 100, 40)

# ================= CALCULATIONS =================
P = pressure_force / area if area else 0
rh = (m_real / m_sat) * 100 if m_sat else 0
ah = m_real
chance_rain = min(100, int((rh + cloud_cover) / 2))

t_max = temp + random.randint(3,6)
t_min = temp - random.randint(4,8)

# ================= TEMP =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🌡️ อุณหภูมิวันนี้")
st.markdown(f"<div class='big'>{temp} °C</div>", unsafe_allow_html=True)
st.write(f"สูงสุด: **{t_max}°C** | ต่ำสุด: **{t_min}°C**")
st.markdown("</div>", unsafe_allow_html=True)

# ================= PRESSURE =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📉 ความดันอากาศ")
st.markdown(f"<div class='big'>{P:,.0f} Pa</div>", unsafe_allow_html=True)
st.markdown("""
<div class="formula">
P = F / A
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ================= HUMIDITY =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("💧 ความชื้น")

st.markdown(f"<div class='big'>{rh:.1f}%</div>", unsafe_allow_html=True)
st.markdown("""
<div class="formula">
RH = (mจริง / mอิ่มตัว) × 100
</div>
""", unsafe_allow_html=True)

st.write(f"Absolute humidity ≈ {ah:.2f} g/m³")

st.markdown("</div>", unsafe_allow_html=True)

# ================= WIND =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("💨 ลม")

arrow="➡️"
if wind_dir>45 and wind_dir<=135: arrow="⬇️"
elif wind_dir>135 and wind_dir<=225: arrow="⬅️"
elif wind_dir>225 and wind_dir<=315: arrow="⬆️"

st.markdown(f"<div class='wind'>{arrow}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='big'>{wind_speed} km/h</div>", unsafe_allow_html=True)

st.markdown("""
<div class="formula">
Speed = distance / time<br>
Direction = 0–360°
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ================= CLOUD =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("☁️ เมฆบนท้องฟ้า")

emoji="☀️"
if cloud_cover>20: emoji="🌤"
if cloud_cover>40: emoji="⛅"
if cloud_cover>60: emoji="🌥"
if cloud_cover>80: emoji="☁️"

st.markdown(f"<div class='cloud'>{emoji}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='big'>{cloud_cover}%</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ================= RAIN =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🌧️ โอกาสเกิดฝน")
st.markdown(f"<div class='big'>{chance_rain}%</div>", unsafe_allow_html=True)
st.progress(chance_rain/100)
st.markdown("</div>", unsafe_allow_html=True)

# ================= 7 DAYS =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📅 พยากรณ์ 7 วัน")

days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

st.markdown("<div class='week'>", unsafe_allow_html=True)

for d in days:
    hi=temp+random.randint(2,6)
    lo=temp-random.randint(3,7)

    st.markdown(f"""
    <div class='day'>
        {d}<br>
        🌤<br>
        {lo}° / {hi}°
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)
