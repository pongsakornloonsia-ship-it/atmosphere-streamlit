import streamlit as st
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

.stApp {
    background: linear-gradient(135deg,#93c5fd,#a5f3fc,#fbcfe8);
}

.block-container {
    padding-top: 2rem;
}

/* HEADER */
.title-box {
    text-align:center;
    padding:60px;
    background: rgba(255,255,255,0.55);
    border-radius:40px;
    margin-bottom:45px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.25);
}

/* BADGE */
.badge {
    display:inline-block;
    padding:10px 20px;
    background:#22c55e;
    border-radius:30px;
    font-weight:700;
    margin:6px;
    color:white;
}

/* CARD */
.card {
    background: rgba(255,255,255,0.6);
    padding:32px;
    border-radius:28px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.25);
    margin-bottom:35px;
}

/* TEXT */
.big-number {
    font-size:48px;
    font-weight:800;
    color:#111827;
}

/* WEEK */
.week {
    display:grid;
    grid-template-columns: repeat(7,1fr);
    gap:16px;
}

.day {
    background: rgba(255,255,255,0.7);
    border-radius:20px;
    padding:16px;
    text-align:center;
    font-weight:700;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="title-box">
    <h1>🌍 เครื่องมือพยากรณ์อากาศ</h1>
    <h4>โปรแกรมคำนวณสภาพอากาศ และบรรยากาศ</h4>
    <div>
        <span class="badge">⚡ ใช้งานง่าย</span>
        <span class="badge">📊 Interactive</span>
        <span class="badge">🎨 ดีไซน์สวย</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- TEMPERATURE ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌡️ อุณหภูมิ")

temp = st.number_input("อุณหภูมิ (°C)", value=28.0)
st.markdown(f"<div class='big-number'>{temp:.1f} °C</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PRESSURE ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📉 ความดันอากาศ")

F = st.number_input("แรง (N)", value=101300.0)
A = st.number_input("พื้นที่ (m²)", value=1.0)

P = F / A if A != 0 else 0
st.markdown(f"<div class='big-number'>{P:,.0f} N/m²</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- HUMIDITY ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("💧 ความชื้น")

m_real = st.number_input("มวลไอน้ำจริง (g)", value=12.5)
m_sat = st.number_input("มวลไอน้ำอิ่มตัว (g)", value=17.3)

rh = (m_real / m_sat) * 100 if m_sat != 0 else 0
st.markdown(f"<div class='big-number'>{rh:.1f} %</div>", unsafe_allow_html=True)

m_vapor = st.number_input("มวลไอน้ำ (g)", value=15.5)
volume = st.number_input("ปริมาตรอากาศ (m³)", value=1.0)

ah = m_vapor / volume if volume != 0 else 0
st.markdown(f"<div class='big-number'>{ah:.2f} g/m³</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RAIN ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌧️ ปริมาณน้ำฝน")

rain = st.slider("เลือกปริมาณฝน (mm)", 0, 50, 5)
st.markdown(f"<div class='big-number'>{rain} mm</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- CLOUD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("☁️ ปริมาณเมฆบนท้องฟ้า")

cloud = st.selectbox(
    "เลือกปริมาณเมฆ",
    ["0% - แจ่มใส", "20% - เมฆน้อย", "40% - เมฆบางส่วน",
     "60% - เมฆมาก", "80% - เมฆหนา", "100% - ปกคลุมทั้งหมด"]
)

st.success(f"☁️ สภาพท้องฟ้า: {cloud}")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- 7 DAYS ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📅 พยากรณ์อากาศ 7 วัน")

days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

temps = [temp + random.randint(-4,4) for _ in range(7)]

st.line_chart(temps)

st.markdown("<div class='week'>", unsafe_allow_html=True)

for d,t in zip(days,temps):
    st.markdown(f"""
    <div class='day'>
        {d}<br>
        🌤<br>
        {t} °C
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)
