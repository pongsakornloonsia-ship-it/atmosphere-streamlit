import streamlit as st
import random

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="เครื่องมือพยากรณ์อากาศ",
    page_icon="🌤️",
    layout="wide"
)

# =====================================================
# GLOBAL CSS
# =====================================================

st.markdown("""
<style>

/* ---------- BACKGROUND ---------- */

.stApp {
    background: linear-gradient(135deg,#7dd3fc,#a7f3d0,#fbcfe8);
}

/* ---------- CONTAINER ---------- */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ---------- HEADER ---------- */

.title-box {
    text-align:center;
    padding:70px;
    background: rgba(255,255,255,0.65);
    border-radius:40px;
    margin-bottom:50px;
    box-shadow:0 20px 50px rgba(0,0,0,0.25);
}

.badge {
    display:inline-block;
    padding:10px 22px;
    background:#2563eb;
    color:white;
    border-radius:30px;
    margin:6px;
    font-weight:600;
}

/* ---------- CARD ---------- */

.card {
    background: rgba(255,255,255,0.7);
    padding:34px;
    border-radius:30px;
    box-shadow:0 15px 40px rgba(0,0,0,0.25);
    margin-bottom:40px;
}

/* ---------- NUMBER ---------- */

.big-number {
    font-size:46px;
    font-weight:800;
    color:#0f172a;
}

/* ---------- FORMULA ---------- */

.formula {
    background:#f8fafc;
    padding:14px;
    border-radius:12px;
    margin-top:12px;
    border-left:6px solid #0ea5e9;
}

/* ---------- WEEK ---------- */

.week-grid {
    display:grid;
    grid-template-columns: repeat(7,1fr);
    gap:18px;
}

.day-box {
    background: rgba(255,255,255,0.75);
    border-radius:22px;
    padding:16px;
    text-align:center;
    font-weight:600;
}

/* ---------- CLOUD ICON ---------- */

.cloud-icon {
    font-size:40px;
}

.wind-box {
    background:#e0f2fe;
    padding:12px;
    border-radius:16px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="title-box">
    <h1>🌍 เครื่องมือพยากรณ์อากาศ</h1>
    <h3>ระบบจำลองการคำนวณสภาพอากาศ</h3>
    <div>
        <span class="badge">สูตรคำนวณ</span>
        <span class="badge">7 วัน</span>
        <span class="badge">Interactive</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# TEMPERATURE
# =====================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🌡️ อุณหภูมิ")

temp = st.number_input("อุณหภูมิอากาศ (°C)", value=28.0)

st.markdown("""
<div class="formula">
<b>สูตร:</b> ใช้ค่าที่ผู้ใช้กำหนดโดยตรง (°C)
</div>
""", unsafe_allow_html=True)

st.markdown(f"<div class='big-number'>{temp:.1f} °C</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# PRESSURE
# =====================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📉 ความดันอากาศ")

F = st.number_input("แรง (N)", value=101325.0)
A = st.number_input("พื้นที่ (m²)", value=1.0)

pressure = F / A if A != 0 else 0

st.markdown("""
<div class="formula">
<b>สูตร:</b> P = F / A
</div>
""", unsafe_allow_html=True)

st.markdown(f"<div class='big-number'>{pressure:,.0f} Pa</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# HUMIDITY
# =====================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("💧 ความชื้นในอากาศ")

m_real = st.number_input("มวลไอน้ำจริง (g)", value=12.5)
m_sat = st.number_input("มวลไอน้ำอิ่มตัว (g)", value=18.0)

RH = (m_real / m_sat) * 100 if m_sat != 0 else 0

st.markdown("""
<div class="formula">
<b>ความชื้นสัมพัทธ์:</b> RH = (mจริง / mอิ่มตัว) × 100
</div>
""", unsafe_allow_html=True)

st.markdown(f"<div class='big-number'>{RH:.1f} %</div>", unsafe_allow_html=True)

m_vapor = st.number_input("มวลไอน้ำรวม (g)", value=15.0)
volume = st.number_input("ปริมาตรอากาศ (m³)", value=1.0)

AH = m_vapor / volume if volume != 0 else 0

st.markdown("""
<div class="formula">
<b>ความชื้นสมบูรณ์:</b> AH = m / V
</div>
""", unsafe_allow_html=True)

st.markdown(f"<div class='big-number'>{AH:.2f} g/m³</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# WIND
# =====================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🌬️ ลม")

wind_speed = st.slider("ความเร็วลม (km/h)", 0, 120, 15)

direction = st.selectbox(
    "ทิศทางลม",
    ["เหนือ","ตะวันออกเฉียงเหนือ","ตะวันออก",
     "ตะวันออกเฉียงใต้","ใต้",
     "ตะวันตกเฉียงใต้","ตะวันตก","ตะวันตกเฉียงเหนือ"]
)

st.markdown("""
<div class="formula">
<b>แนวคิด:</b> ความเร็วลมวัดเป็น km/h และทิศทาง 8 ทิศ
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="wind-box">
🌬️ {wind_speed} km/h<br>
➡️ {direction}
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# CLOUD TYPE
# =====================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("☁️ ประเภทเมฆ")

cloud_type = st.selectbox(
    "เลือกชนิดเมฆ",
    ["Cumulus","Stratus","Cirrus","Nimbus","Cumulonimbus"]
)

icons = {
    "Cumulus":"☁️",
    "Stratus":"🌫️",
    "Cirrus":"🌥️",
    "Nimbus":"🌧️",
    "Cumulonimbus":"⛈️"
}

st.markdown("""
<div class="formula">
<b>ตัวอย่าง:</b> Nimbus และ Cumulonimbus มักก่อให้เกิดฝน
</div>
""", unsafe_allow_html=True)

st.markdown(
    f"<div class='cloud-icon'>{icons[cloud_type]}</div>",
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# RAIN PROBABILITY
# =====================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🌧️ โอกาสเกิดฝน")

rain_mm = st.slider("ปริมาณฝน (mm)", 0, 100, 10)

rain_prob = min(100, int((RH + rain_mm) / 2))

st.markdown("""
<div class="formula">
<b>แนวคิด:</b> โอกาสฝน ≈ (RH + ปริมาณฝน) / 2
</div>
""", unsafe_allow_html=True)

st.markdown(f"<div class='big-number'>{rain_prob} %</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# DAILY MAX / MIN
# =====================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📊 อุณหภูมิสูงสุด / ต่ำสุด")

t_max = temp + random.randint(2,6)
t_min = temp - random.randint(2,6)

st.markdown("""
<div class="formula">
<b>แนวคิด:</b> Tmax = T + (2–6), Tmin = T − (2–6)
</div>
""", unsafe_allow_html=True)

st.markdown(
    f"<div class='big-number'>สูงสุด {t_max} °C | ต่ำสุด {t_min} °C</div>",
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# 7 DAYS FORECAST
# =====================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📅 พยากรณ์ล่วงหน้า 7 วัน")

st.markdown("""
<div class="formula">
<b>แนวคิด:</b> อุณหภูมิแต่ละวัน = T ± 4°C
</div>
""", unsafe_allow_html=True)

days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
temps = [temp + random.randint(-4,4) for _ in range(7)]

st.line_chart(temps)

st.markdown("<div class='week-grid'>", unsafe_allow_html=True)

for d,t in zip(days,temps):
    st.markdown(f"""
    <div class="day-box">
        {d}<br>
        🌤️<br>
        {t} °C
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<hr>
<center>
📘 Atmospheric Simulator — Streamlit Project
</center>
""", unsafe_allow_html=True)
