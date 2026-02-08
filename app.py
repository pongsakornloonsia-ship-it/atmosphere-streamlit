import streamlit as st
import random

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="เครื่องมือพยากรณ์อากาศ",
    page_icon="🌤️",
    layout="wide"
)

# ---------------- THEME SWITCH ----------------
theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])

bg_light = "#c7d2fe"
bg_dark = "#020617"

card_light = "rgba(255,255,255,0.6)"
card_dark = "rgba(15,23,42,0.7)"

text_color = "#0f172a" if theme == "Light" else "#e5e7eb"

bg = bg_light if theme == "Light" else bg_dark
card = card_light if theme == "Light" else card_dark

# ---------------- CSS ----------------
st.markdown(f"""
<style>

.stApp {{
    background:{bg};
}}

.block-container {{
    padding-top:2rem;
}}

.card {{
    background:{card};
    backdrop-filter: blur(14px);
    padding:30px;
    border-radius:26px;
    box-shadow:0 15px 35px rgba(0,0,0,0.25);
    margin-bottom:30px;
    color:{text_color};
}}

.title-box {{
    text-align:center;
    padding:55px;
    border-radius:35px;
    background:{card};
    margin-bottom:45px;
}}

.week {{
    display:grid;
    grid-template-columns: repeat(7,1fr);
    gap:14px;
}}

.day {{
    background:{card};
    border-radius:18px;
    padding:14px;
    text-align:center;
}}

.cloud-float {{
    animation: float 6s ease-in-out infinite;
}}

@keyframes float {{
    0% {{transform:translateY(0);}}
    50% {{transform:translateY(-12px);}}
    100% {{transform:translateY(0);}}
}}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="title-box">
<h1>🌍 เครื่องมือพยากรณ์อากาศ</h1>
<h4>โปรแกรมคำนวณสภาพอากาศ และบรรยากาศ</h4>
</div>
""", unsafe_allow_html=True)

# ---------------- TEMPERATURE ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🌡️ อุณหภูมิ")

temp = st.number_input("อุณหภูมิ (°C)", value=28.0)

st.write(f"ค่าอุณหภูมิ: **{temp:.1f} °C**")
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PRESSURE ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📉 ความดันอากาศ")

F = st.number_input("แรง (N)", value=101300.0)
A = st.number_input("พื้นที่ (m²)", value=1.0)

P = F / A if A != 0 else 0

st.write(f"ความดัน = **{P:,.0f} N/m²**")
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- HUMIDITY ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("💧 ความชื้น")

m_real = st.number_input("มวลไอน้ำจริง (g)", value=12.5)
m_sat = st.number_input("มวลไอน้ำอิ่มตัว (g)", value=17.3)

rh = (m_real / m_sat) * 100 if m_sat else 0

st.write(f"RH = **{rh:.1f}%**")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CLOUD ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("☁️ เมฆ")

cloud = st.slider("ปริมาณเมฆ (%)", 0, 100, 40)

emoji="☀️"
if cloud>20: emoji="🌤"
if cloud>40: emoji="⛅"
if cloud>60: emoji="🌥"
if cloud>80: emoji="☁️"

st.markdown(f"<h1 class='cloud-float'>{emoji}</h1>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- 7 DAYS ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📅 พยากรณ์ 7 วัน")

temps = [temp + random.randint(-5,5) for _ in range(7)]

st.line_chart(temps)

days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

st.markdown("<div class='week'>", unsafe_allow_html=True)

for d,t in zip(days,temps):
    st.markdown(f"""
    <div class='day'>
        {d}<br>
        🌤<br>
        {t}°C
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)
