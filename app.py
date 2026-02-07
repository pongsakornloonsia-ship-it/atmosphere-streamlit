import streamlit as st
import pandas as pd
import random

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
    padding: 28px;
    border-radius: 26px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.1);
    margin-bottom: 35px;
}

/* HEADER */
.title-box {
    text-align:center;
    padding:55px;
    background: linear-gradient(135deg,#b8f3dc,#a7c7ff);
    border-radius:32px;
    margin-bottom:45px;
}

.badge {
    display:inline-block;
    padding:10px 20px;
    background:#dcfce7;
    border-radius:25px;
    font-weight:600;
    margin:6px;
}

/* BIG NUMBER */
.big-number {
    font-size:50px;
    font-weight:800;
    color:#0f766e;
}

/* forecast row */
.forecast-box {
    background: linear-gradient(135deg,#ecfeff,#f0fdf4);
    padding:18px;
    border-radius:18px;
    text-align:center;
    box-shadow:0 6px 18px rgba(0,0,0,0.08);
}

.day-title {
    font-size:18px;
    font-weight:700;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="title-box">
<h1>🌍 เครื่องมือพยากรณ์อากาศ</h1>
<h4>แดชบอร์ดวิเคราะห์สภาพอากาศรายสัปดาห์</h4>
<span class="badge">🌡️ อุณหภูมิ</span>
<span class="badge">💧 ความชื้น</span>
<span class="badge">🌬️ ลม</span>
<span class="badge">☁️ เมฆ</span>
<span class="badge">📅 7 วัน</span>
</div>
""", unsafe_allow_html=True)

# ==================================================
# 🌡️ TEMPERATURE
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌡️ อุณหภูมิวันนี้")

temp = st.number_input("อุณหภูมิปัจจุบัน (°C)", value=29.0)
t_min = st.number_input("ต่ำสุดวันนี้ (°C)", value=25.0)
t_max = st.number_input("สูงสุดวันนี้ (°C)", value=35.0)

st.markdown(
    f"<div class='big-number'>{temp:.1f}°C</div>"
    f"ต่ำสุด {t_min:.1f}°C | สูงสุด {t_max:.1f}°C",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 💧 HUMIDITY
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("💧 ความชื้น")

m_real = st.number_input("มวลไอน้ำจริง (g)", value=14.0)
m_sat = st.number_input("มวลไอน้ำอิ่มตัว (g)", value=20.0)
volume = st.number_input("ปริมาตรอากาศ (m³)", value=1.0)

rh = (m_real / m_sat) * 100 if m_sat else 0
ah = m_real / volume if volume else 0

st.markdown(f"<div class='big-number'>{rh:.1f}%</div>", unsafe_allow_html=True)
st.caption(f"ความชื้นสมบูรณ์ ≈ {ah:.2f} g/m³")
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 🌬️ WIND
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌬️ ลม")

wind_speed = st.slider("ความเร็วลม (km/h)", 0, 100, 15)
wind_dir = st.selectbox(
    "ทิศลม",
    [
        "เหนือ","ตะวันออก","ใต้","ตะวันตก",
        "ตะวันออกเฉียงเหนือ","ตะวันออกเฉียงใต้",
        "ตะวันตกเฉียงใต้","ตะวันตกเฉียงเหนือ"
    ]
)

st.markdown(f"<div class='big-number'>{wind_speed} km/h</div>", unsafe_allow_html=True)
st.info(f"➡️ ทิศลม: {wind_dir}")
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# ☁️ CLOUD + RAIN
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("☁️ เมฆและโอกาสฝน")

cloud_type = st.selectbox(
    "ชนิดเมฆ",
    ["Cirrus","Cumulus","Stratus","Nimbus","Cumulonimbus"]
)

cloud_amount = st.slider("ปริมาณเมฆ (%)", 0, 100, 60)

rain_chance = cloud_amount * 0.4 + rh * 0.4

if cloud_type in ["Nimbus", "Cumulonimbus"]:
    rain_chance += 20
if wind_speed > 40:
    rain_chance += 10

rain_chance = min(rain_chance, 100)

if rain_chance < 30:
    condition = "☀️ ฟ้าโปร่ง"
elif rain_chance < 60:
    condition = "🌥️ ครึ้ม"
elif rain_chance < 85:
    condition = "🌧️ ฝนตก"
else:
    condition = "⛈️ พายุฝน"

st.markdown(f"<div class='big-number'>{rain_chance:.0f}%</div>", unsafe_allow_html=True)
st.warning(f"สภาพโดยรวม: {condition}")
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 📅 7 DAY FORECAST
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📅 พยากรณ์ล่วงหน้า 7 วัน")

cols = st.columns(7)

for i in range(7):
    with cols[i]:
        tmin = round(random.uniform(23, 27), 1)
        tmax = round(random.uniform(32, 38), 1)
        rain = round(random.uniform(20, 90))
        icon = "🌧️" if rain > 60 else "🌤️"

        st.markdown(
            f"""
            <div class="forecast-box">
                <div class="day-title">Day {i+1}</div>
                <h2>{icon}</h2>
                <b>{tmin}° / {tmax}°</b><br>
                🌧️ {rain}%
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)
