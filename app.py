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
# 📍 GEOLOCATION (IP BASED)
# =====================================================

st.subheader("📍 ตรวจสอบตำแหน่งปัจจุบัน")

def get_location_ip():
    try:
        r = requests.get("https://ipapi.co/json/", timeout=10)
        data = r.json()
        return (
            data.get("latitude"),
            data.get("longitude"),
            data.get("city"),
            data.get("country_name"),
        )
    except:
        return None, None, None, None


if "user_lat" not in st.session_state:

    lat, lon, city, country = get_location_ip()

    st.session_state.user_lat = lat
    st.session_state.user_lon = lon
    st.session_state.city = city
    st.session_state.country = country


if st.session_state.user_lat:

    st.success(
        f"Lat: {st.session_state.user_lat:.4f} | "
        f"Lon: {st.session_state.user_lon:.4f}"
    )

    st.write("📍 พื้นที่โดยประมาณ:")
    st.code(f"{st.session_state.city}, {st.session_state.country}")

    st.map({
        "lat": [st.session_state.user_lat],
        "lon": [st.session_state.user_lon]
    })

else:
    st.warning("ไม่สามารถตรวจตำแหน่งอัตโนมัติได้")

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

st.write("สูตร: RH = (มวลจริง / มวลอิ่มตัว) × 100")

st.markdown(f"<div class='big-number'>{rh:.1f} %</div>", unsafe_allow_html=True)

m_vapor = st.number_input("มวลไอน้ำ (g)", value=15.5)
volume = st.number_input("ปริมาตรอากาศ (m³)", value=1.0)

ah = m_vapor / volume if volume != 0 else 0

st.write("สูตร: AH = มวลไอน้ำ / ปริมาตร")

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
    ["0%", "20%", "40%", "60%", "80%", "100%"]
)

st.success(f"☁️ เมฆปกคลุม: {cloud}")

st.markdown('</div>', unsafe_allow_html=True)
# =====================================================
# 📆 FORECAST 7 DAYS (FROM OPEN-METEO)
# =====================================================

st.subheader("📆 พยากรณ์อากาศ 7 วัน")

if st.session_state.get("user_lat"):

    lat = st.session_state.user_lat
    lon = st.session_state.user_lon

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

            st.write(f"📅 วันที่: {days[i]}")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("🌡️ สูงสุด", f"{tmax[i]} °C")
                st.metric("🌡️ ต่ำสุด", f"{tmin[i]} °C")

            with col2:
                st.metric("☁️ เมฆเฉลี่ย", f"{cloud_avg[i]} %")

            with col3:
                st.metric("🌧️ โอกาสฝน", f"{rain_prob[i]} %")

            with col4:
                if rain_prob[i] > 60:
                    st.progress(rain_prob[i] / 100)

            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error("โหลดพยากรณ์ 7 วันไม่สำเร็จ")
        st.code(e)

else:
    st.warning("ยังไม่ทราบตำแหน่งผู้ใช้")
