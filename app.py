import streamlit as st
import requests

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
    font-size:48px;
    font-weight:bold;
    color:#16a34a;
    margin-top:10px;
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

# =====================================================
# 📍 SELECT PROVINCE
# =====================================================

st.subheader("📍 เลือกจังหวัด")

TH_PROVINCES = {
    "กรุงเทพมหานคร": (13.7563, 100.5018),
    "เชียงใหม่": (18.7883, 98.9853),
    "ขอนแก่น": (16.4419, 102.8350),
    "นครราชสีมา": (14.9799, 102.0977),
    "ชลบุรี": (13.3611, 100.9847),
    "ภูเก็ต": (7.8804, 98.3923),
    "สงขลา": (7.1898, 100.5950),
    "สุราษฎร์ธานี": (9.1382, 99.3215),
    "อุบลราชธานี": (15.2448, 104.8473),
    "พิษณุโลก": (16.8298, 100.2615),
}

province = st.selectbox("เลือกจังหวัด", list(TH_PROVINCES.keys()))
lat, lon = TH_PROVINCES[province]

st.session_state.user_lat = lat
st.session_state.user_lon = lon

st.success(f"{province} | {lat}, {lon}")

st.map({"lat": [lat], "lon": [lon]})

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

rh = (m_real / m_sat) * 100 if m_sat else 0
st.write("สูตร: RH = (มวลจริง / มวลอิ่มตัว) × 100")
st.markdown(f"<div class='big-number'>{rh:.1f} %</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- CLOUD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("☁️ ปริมาณเมฆ")

cloud = st.selectbox("เมฆปกคลุม", ["0%", "20%", "40%", "60%", "80%", "100%"])
st.success(f"☁️ {cloud}")
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# 📆 FORECAST 7 DAYS
# =====================================================

st.subheader("📆 พยากรณ์อากาศ 7 วัน")

url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={lat}&longitude={lon}"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,cloud_cover_mean"
    "&timezone=auto"
)

try:
    r = requests.get(url, timeout=10)
    data = r.json()

    days = data["daily"]["time"]
    tmax = data["daily"]["temperature_2m_max"]
    tmin = data["daily"]["temperature_2m_min"]
    rain_prob = data["daily"]["precipitation_probability_max"]
    cloud_avg = data["daily"]["cloud_cover_mean"]

    for i in range(7):
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.write(f"📅 {days[i]}")
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("สูงสุด", f"{tmax[i]} °C")
            st.metric("ต่ำสุด", f"{tmin[i]} °C")

        with c2:
            st.metric("เมฆ", f"{cloud_avg[i]} %")

        with c3:
            st.metric("ฝน", f"{rain_prob[i]} %")

        with c4:
            st.progress(rain_prob[i] / 100)

        st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error("โหลดข้อมูล 7 วันไม่ได้")
    st.code(e)
