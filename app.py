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
.card {
    background: white;
    padding: 25px;
    border-radius: 22px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    margin-bottom: 30px;
}
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
.big-number {
    font-size:46px;
    font-weight:bold;
    color:#0f766e;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="title-box">
<h1>🌍 เครื่องมือพยากรณ์อากาศ</h1>
<h4>ระบบวิเคราะห์สภาพอากาศประจำวัน</h4>
<span class="badge">🌡️ อุณหภูมิ</span>
<span class="badge">💧 ความชื้น</span>
<span class="badge">🌬️ ลม</span>
<span class="badge">☁️ เมฆ</span>
<span class="badge">📊 พยากรณ์</span>
</div>
""", unsafe_allow_html=True)

# ==================================================
# 🌡️ TEMPERATURE
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌡️ อุณหภูมิ")

temp = st.number_input("อุณหภูมิปัจจุบัน (°C)", value=29.0)
t_min = st.number_input("ต่ำสุดของวัน (°C)", value=25.0)
t_max = st.number_input("สูงสุดของวัน (°C)", value=35.0)

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

rh = (m_real / m_sat) * 100
ah = m_real / volume

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
    ["เหนือ","ตะวันออก","ใต้","ตะวันตก",
     "ตะวันออกเฉียงเหนือ","ตะวันออกเฉียงใต้",
     "ตะวันตกเฉียงใต้","ตะวันตกเฉียงเหนือ"]
)

st.markdown(f"<div class='big-number'>{wind_speed} km/h</div>", unsafe_allow_html=True)
st.info(f"➡️ ทิศทางลม: {wind_dir}")
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# ☁️ CLOUD + RAIN CHANCE
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
# 📊 HOURLY GRAPH
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 อุณหภูมิรายชั่วโมง")

hours = list(range(0, 24))
temps = [
    random.uniform(t_min, t_max)
    for _ in hours
]

df_hour = pd.DataFrame({
    "Hour": hours,
    "Temperature": temps
})

st.line_chart(df_hour.set_index("Hour"))
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 📅 3-DAY FORECAST
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📅 พยากรณ์ล่วงหน้า 3 วัน")

days = []
for i in range(1, 4):
    days.append({
        "วัน": f"Day {i}",
        "ต่ำสุด (°C)": round(random.uniform(23, 26), 1),
        "สูงสุด (°C)": round(random.uniform(32, 37), 1),
        "ฝน (%)": round(random.uniform(20, 90), 0)
    })

df_days = pd.DataFrame(days)
st.table(df_days)
st.markdown("</div>", unsafe_allow_html=True)
