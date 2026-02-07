import streamlit as st
import math

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="เครื่องมือพยากรณ์อากาศ",
    page_icon="🌤️",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #e8fff5, #d9f7ef);
}

.block-container {
    padding-top: 2rem;
}

/* CARD */
.card {
    background: white;
    padding: 25px;
    border-radius: 22px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    margin-bottom: 30px;
}

/* HEADER */
.title-box {
    text-align:center;
    padding:50px;
    background: linear-gradient(135deg,#b8f3dc,#a7c7ff);
    border-radius:30px;
    margin-bottom:40px;
}

.badge {
    display:inline-block;
    padding:10px 18px;
    background:#dcfce7;
    border-radius:25px;
    font-weight:600;
    margin:6px;
}

/* BIG NUMBER */
.big-number {
    font-size:48px;
    font-weight:bold;
    color:#0f766e;
    margin-top:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="title-box">
    <h1>🌍 เครื่องมือพยากรณ์อากาศ</h1>
    <h4>โปรแกรมคำนวณสภาพอากาศและบรรยากาศ</h4>
    <div>
        <span class="badge">🌡️ อุณหภูมิ</span>
        <span class="badge">💧 ความชื้น</span>
        <span class="badge">🌬️ ลม</span>
        <span class="badge">☁️ เมฆ</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================================================
# 🌡️ TEMPERATURE
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌡️ อุณหภูมิ")

temp = st.number_input("อุณหภูมิปัจจุบัน (°C)", value=28.0)

t_min = st.number_input("🌙 อุณหภูมิต่ำสุดของวัน (°C)", value=24.0)
t_max = st.number_input("☀️ อุณหภูมิสูงสุดของวัน (°C)", value=34.0)

st.markdown(
    f"<div class='big-number'>{temp:.1f} °C</div>"
    f"ต่ำสุด {t_min:.1f}°C | สูงสุด {t_max:.1f}°C",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 💧 HUMIDITY
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("💧 ความชื้นในอากาศ")

m_real = st.number_input("มวลไอน้ำจริง (g)", value=12.0)
m_sat = st.number_input("มวลไอน้ำอิ่มตัว (g)", value=18.0)

rh = (m_real / m_sat) * 100 if m_sat != 0 else 0

volume = st.number_input("ปริมาตรอากาศ (m³)", value=1.0)
ah = m_real / volume if volume != 0 else 0

st.markdown(f"<div class='big-number'>{rh:.1f}%</div>", unsafe_allow_html=True)
st.caption(f"💧 ความชื้นสมบูรณ์ ≈ {ah:.2f} g/m³")

st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 🌬️ WIND
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌬️ ลม")

wind_speed = st.slider("ความเร็วลม (km/h)", 0, 100, 12)

wind_dir = st.selectbox(
    "ทิศทางลม",
    ["เหนือ", "ตะวันออกเฉียงเหนือ", "ตะวันออก",
     "ตะวันออกเฉียงใต้", "ใต้", "ตะวันตกเฉียงใต้",
     "ตะวันตก", "ตะวันตกเฉียงเหนือ"]
)

st.markdown(
    f"<div class='big-number'>{wind_speed} km/h</div>",
    unsafe_allow_html=True
)
st.info(f"➡️ ลมพัดจากทิศ: {wind_dir}")

st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# ☁️ CLOUD TYPE
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("☁️ ประเภทเมฆ")

cloud_type = st.selectbox(
    "ชนิดเมฆ",
    [
        "Cumulus (ก้อนขาว)",
        "Stratus (เป็นชั้น)",
        "Cirrus (ริ้วบาง)",
        "Nimbus (ฝน)",
        "Cumulonimbus (พายุฝน)"
    ]
)

cloud_amount = st.slider("ปริมาณเมฆ (%)", 0, 100, 50)

# ประเมินโอกาสฝนคร่าวๆ
rain_chance = cloud_amount * 0.6

if cloud_type == "Nimbus (ฝน)" or cloud_type == "Cumulonimbus (พายุฝน)":
    rain_chance += 25

rain_chance = min(rain_chance, 100)

st.markdown(
    f"<div class='big-number'>{cloud_amount}%</div>",
    unsafe_allow_html=True
)

st.warning(f"🌧️ โอกาสเกิดฝนประมาณ {rain_chance:.0f}%")

st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 🌧️ RAIN AMOUNT
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌧️ ปริมาณฝนโดยประมาณ")

rain = st.slider("มิลลิเมตร/วัน", 0, 100, 10)

st.markdown(
    f"<div class='big-number'>{rain} mm</div>",
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)
