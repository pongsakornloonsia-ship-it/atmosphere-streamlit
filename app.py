import streamlit as st
import pandas as pd
import random

# ================= CONFIG =================
st.set_page_config(
    page_title="เครื่องมือพยากรณ์อากาศ",
    page_icon="🌤️",
    layout="wide"
)

# ================= CSS =================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#d9f7ef,#ecfeff);
}

.block-container { padding-top:2rem; }

.card {
    background:white;
    padding:34px;
    border-radius:36px;
    box-shadow:0 18px 40px rgba(0,0,0,0.14);
    margin-bottom:38px;
}

.title-box {
    text-align:center;
    padding:65px;
    background:linear-gradient(135deg,#99f6e4,#93c5fd);
    border-radius:42px;
    margin-bottom:55px;
}

.badge {
    display:inline-block;
    padding:12px 22px;
    background:#dcfce7;
    border-radius:30px;
    font-weight:700;
    margin:6px;
}

.big-number {
    font-size:52px;
    font-weight:900;
    color:#0f766e;
}

.formula-box {
    background:#f0fdfa;
    padding:18px;
    border-radius:22px;
    border-left:7px solid #14b8a6;
    margin-top:14px;
}

/* -------- CLOUD VISUAL -------- */

.cloud-area {
    display:flex;
    justify-content:center;
    gap:25px;
    margin-top:25px;
}

.cloud {
    width:150px;
    height:85px;
    background:#e5e7eb;
    border-radius:55px;
    position:relative;
    box-shadow:0 12px 22px rgba(0,0,0,0.18);
}

.cloud::before,
.cloud::after {
    content:"";
    position:absolute;
    background:#e5e7eb;
    width:75px;
    height:75px;
    border-radius:50%;
    top:-38px;
}

.cloud::before { left:20px; }
.cloud::after { right:28px; }

.cloud.dark,
.cloud.dark::before,
.cloud.dark::after {
    background:#9ca3af;
}

.cloud.tall { height:105px; }

/* rain animation */
.rain {
    font-size:30px;
    animation: fall 1.4s infinite;
}

@keyframes fall {
    0% {opacity:0; transform:translateY(0);}
    100% {opacity:1; transform:translateY(26px);}
}

/* forecast */
.forecast-box {
    background:linear-gradient(135deg,#ecfeff,#f0fdf4);
    padding:20px;
    border-radius:22px;
    text-align:center;
    box-shadow:0 8px 20px rgba(0,0,0,0.1);
}

.day-title {
    font-weight:900;
    font-size:18px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="title-box">
<h1>🌍 เครื่องมือพยากรณ์อากาศ</h1>
<h4>แดชบอร์ดคำนวณสภาพอากาศเชิงการศึกษา</h4>
<span class="badge">🌡️ อุณหภูมิ</span>
<span class="badge">📉 ความดัน</span>
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

temp = st.slider("อุณหภูมิปัจจุบัน (°C)", -10.0, 50.0, 30.0)
t_min = st.slider("ต่ำสุดวันนี้ (°C)", -10.0, 40.0, 24.0)
t_max = st.slider("สูงสุดวันนี้ (°C)", 0.0, 50.0, 35.0)

st.markdown(f"<div class='big-number'>{temp:.1f}°C</div>", unsafe_allow_html=True)
st.caption(f"ต่ำสุด {t_min:.1f}°C | สูงสุด {t_max:.1f}°C")

st.markdown("""
<div class="formula-box">
<b>ข้อมูล:</b> รับค่าจากผู้ใช้โดยตรง
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 📉 PRESSURE
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📉 ความดันอากาศ")

F = st.slider("แรง (N)", 0.0, 200000.0, 101300.0)
A = st.slider("พื้นที่ (m²)", 0.1, 20.0, 1.0)

P = F / A if A else 0

st.markdown(f"<div class='big-number'>{P:,.0f} Pa</div>", unsafe_allow_html=True)

st.markdown("""
<div class="formula-box">
<b>สูตร:</b> P = F ÷ A
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 💧 HUMIDITY
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("💧 ความชื้น")

m_real = st.slider("มวลไอน้ำจริง (g)", 0.0, 40.0, 15.0)
m_sat = st.slider("มวลไอน้ำอิ่มตัว (g)", 1.0, 50.0, 22.0)
volume = st.slider("ปริมาตรอากาศ (m³)", 0.5, 5.0, 1.0)

rh = (m_real / m_sat) * 100
ah = m_real / volume

st.markdown(f"<div class='big-number'>{rh:.1f}%</div>", unsafe_allow_html=True)
st.write(f"ความชื้นสมบูรณ์ = {ah:.2f} g/m³")

st.markdown("""
<div class="formula-box">
<b>สูตร:</b><br>
RH = (มวลไอน้ำจริง ÷ มวลไอน้ำอิ่มตัว) × 100<br>
AH = มวลไอน้ำ ÷ ปริมาตรอากาศ
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 🌬️ WIND
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌬️ ลม")

wind_speed = st.slider("ความเร็วลม (km/h)", 0, 120, 15)
wind_dir = st.selectbox(
    "ทิศลม",
    ["เหนือ","ตะวันออก","ใต้","ตะวันตก",
     "ตะวันออกเฉียงเหนือ","ตะวันออกเฉียงใต้",
     "ตะวันตกเฉียงใต้","ตะวันตกเฉียงเหนือ"]
)

st.markdown(f"<div class='big-number'>{wind_speed} km/h</div>", unsafe_allow_html=True)

st.markdown("""
<div class="formula-box">
<b>ข้อมูล:</b> รับค่าจากผู้ใช้
</div>
""", unsafe_allow_html=True)
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

cloud_class = "cloud"
if cloud_type in ["Nimbus","Cumulonimbus"]:
    cloud_class += " dark"
if cloud_type == "Cumulonimbus":
    cloud_class += " tall"

drops = "💧💧💧" if cloud_amount > 60 else ""

st.markdown(
    f"""
    <div class="cloud-area">
        <div class="{cloud_class}"></div>
        <div class="rain">{drops}</div>
    </div>
    """,
    unsafe_allow_html=True
)

rain_chance = cloud_amount*0.4 + rh*0.4
if cloud_type in ["Nimbus","Cumulonimbus"]:
    rain_chance += 20

rain_chance = min(rain_chance,100)

st.markdown(f"<div class='big-number'>{rain_chance:.0f}%</div>", unsafe_allow_html=True)

st.markdown("""
<div class="formula-box">
<b>สูตรโอกาสฝน:</b><br>
(ปริมาณเมฆ × 0.4) + (RH × 0.4)<br>
+20 ถ้าเป็น Nimbus หรือ Cumulonimbus
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 📅 7 DAY FORECAST
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📅 พยากรณ์ล่วงหน้า 7 วัน")

cols = st.columns(7)

for i in range(7):
    with cols[i]:
        tmin = round(random.uniform(23,27),1)
        tmax = round(random.uniform(32,38),1)
        rain = round(random.uniform(20,90))
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
