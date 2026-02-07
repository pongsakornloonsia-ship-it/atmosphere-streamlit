import streamlit as st
import random

# ================= CONFIG =================
st.set_page_config(
    page_title="Atmosphere Lab",
    page_icon="🌤️",
    layout="wide"
)

# ================= CSS =================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#a1c4fd,#c2e9fb);
}

.block-container {
    padding-top: 2rem;
}

/* HERO */
.hero {
    text-align:center;
    padding:60px;
    border-radius:36px;
    background: linear-gradient(120deg,#667eea,#764ba2);
    color:white;
    box-shadow: 0 25px 60px rgba(0,0,0,0.35);
    margin-bottom:50px;
}

/* CARD */
.card {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(16px);
    padding:32px;
    border-radius:30px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.25);
    margin-bottom:35px;
}

/* TEXT */
.big {
    font-size:48px;
    font-weight:900;
    color:#1d4ed8;
}

.formula {
    background:#020617;
    color:#86efac;
    padding:15px;
    border-radius:14px;
    font-family:monospace;
    margin-top:10px;
}

.cloud {
    font-size:120px;
    text-align:center;
}

.wind {
    font-size:80px;
    text-align:center;
}

/* WEEK */
.week {
    display:grid;
    grid-template-columns: repeat(7,1fr);
    gap:16px;
}

.day {
    background:linear-gradient(135deg,#fdfbfb,#ebedee);
    border-radius:20px;
    padding:15px;
    text-align:center;
    font-weight:700;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="hero">
<h1>🌍 Atmosphere Lab</h1>
<h3>ระบบทดลองและคำนวณสภาพอากาศ</h3>
</div>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.header("⚙️ ปรับค่า")

temp = st.sidebar.slider("🌡 อุณหภูมิ (°C)", -10, 45, 30)

force = st.sidebar.number_input("แรง F (N)", value=101300.0)
area = st.sidebar.number_input("พื้นที่ A (m²)", value=1.0)

m_real = st.sidebar.number_input("มวลไอน้ำจริง (g)", value=12.0)
m_sat = st.sidebar.number_input("มวลไอน้ำอิ่มตัว (g)", value=18.0)

wind_speed = st.sidebar.slider("💨 ความเร็วลม (km/h)", 0, 120, 20)
wind_dir = st.sidebar.slider("🧭 ทิศลม (°)", 0, 360, 90)

cloud_cover = st.sidebar.slider("☁️ ปริมาณเมฆ (%)", 0, 100, 40)

rain_amount = st.sidebar.slider("🌧️ ปริมาณฝน (mm)", 0, 100, 10)

# ================= CALC =================
P = force / area if area else 0
rh = (m_real / m_sat) * 100 if m_sat else 0
ah = m_real

chance_rain = min(100, int((rh*0.6 + cloud_cover*0.4)))

t_max = temp + random.randint(3,6)
t_min = temp - random.randint(4,8)

# ================= TEMP =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🌡️ อุณหภูมิวันนี้")
st.markdown(f"<div class='big'>{temp} °C</div>", unsafe_allow_html=True)
st.write(f"สูงสุด: **{t_max}°C** | ต่ำสุด: **{t_min}°C**")

st.markdown("""
<div class="formula">
Tmax ≈ T + Δ<br>
Tmin ≈ T - Δ
</div>
""", unsafe_allow_html=True)

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
st.write(f"Absolute humidity ≈ {ah:.2f} g/m³")

st.markdown("""
<div class="formula">
RH = (mจริง / mอิ่มตัว) × 100
</div>
""", unsafe_allow_html=True)

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
speed = distance / time<br>
direction = 0–360°
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ================= CLOUD =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("☁️ เมฆ")

emoji="☀️"
ctype="ท้องฟ้าแจ่มใส"

if cloud_cover>20:
    emoji="🌤"; ctype="Cirrus"
if cloud_cover>40:
    emoji="⛅"; ctype="Altocumulus"
if cloud_cover>60:
    emoji="🌥"; ctype="Stratus"
if cloud_cover>80:
    emoji="☁️"; ctype="Nimbus"

st.markdown(f"<div class='cloud'>{emoji}</div>", unsafe_allow_html=True)
st.write(f"ประเภทเมฆ: **{ctype}**")

st.markdown("</div>", unsafe_allow_html=True)

# ================= RAIN =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🌧️ ฝน")

st.markdown(f"<div class='big'>โอกาส {chance_rain}%</div>", unsafe_allow_html=True)
st.progress(chance_rain/100)
st.write(f"ปริมาณฝน: {rain_amount} mm")

st.markdown("</div>", unsafe_allow_html=True)

# ================= 7 DAYS =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📅 พยากรณ์ 7 วัน")

days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

st.markdown("<div class='week'>", unsafe_allow_html=True)

for d in days:
    hi = temp + random.randint(2,6)
    lo = temp - random.randint(3,7)

    st.markdown(f"""
    <div class='day'>
        {d}<br>
        🌦️<br>
        {lo}° / {hi}°
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)
