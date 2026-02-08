import streamlit as st
import requests
import math
import streamlit.components.v1 as components

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
    background: linear-gradient(135deg,#c7f9ff,#e0ffe9);
}

.block-container {
    padding-top: 2rem;
}

/* CARD */
.card {
    background: rgba(255,255,255,0.95);
    padding: 25px;
    border-radius: 22px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    margin-bottom: 30px;
}

/* HEADER */
.title-box {
    text-align:center;
    padding:50px;
    background: linear-gradient(135deg,#9ee7ff,#baffc9);
    border-radius:30px;
    margin-bottom:40px;
}

/* BADGE */
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
    color:#047857;
    margin-top:10px;
}

.formula-box {
    background:#f0fdf4;
    padding:10px;
    border-radius:12px;
    font-family:monospace;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="title-box">
    <h1>🌍 เครื่องมือพยากรณ์อากาศ</h1>
    <h4>ระบบคำนวณบรรยากาศ + ตรวจพิกัดอัตโนมัติ</h4>
    <div>
        <span class="badge">📍 Location</span>
        <span class="badge">📊 Formula</span>
        <span class="badge">7 Days</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# 📍 GEOLOCATION
# =====================================================

st.subheader("📍 ตรวจสอบตำแหน่งปัจจุบัน")

geo_js = """
<script>
navigator.geolocation.getCurrentPosition(
    (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;

        window.parent.postMessage(
            { type: "streamlit:setComponentValue",
              value: {lat: lat, lon: lon} },
            "*"
        );
    }
);
</script>
"""

coords = components.html(geo_js, height=0)

if "user_lat" not in st.session_state:
    st.session_state.user_lat = None
    st.session_state.user_lon = None

if coords:
    st.session_state.user_lat = coords["lat"]
    st.session_state.user_lon = coords["lon"]

if st.session_state.user_lat:
    st.success(
        f"Lat: {st.session_state.user_lat:.4f} | "
        f"Lon: {st.session_state.user_lon:.4f}"
    )
else:
    st.info("กำลังขอพิกัดจากอุปกรณ์...")

# =====================================================
# 🌍 REVERSE GEOCODE
# =====================================================

def reverse_geocode(lat, lon):

    url = (
        "https://nominatim.openstreetmap.org/reverse"
        f"?format=json&lat={lat}&lon={lon}"
    )

    headers = {"User-Agent": "streamlit-weather"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data.get("display_name", "ไม่ทราบพื้นที่")
    except:
        pass

    return "ไม่สามารถระบุพื้นที่"


if st.session_state.user_lat:

    place_name = reverse_geocode(
        st.session_state.user_lat,
        st.session_state.user_lon
    )

    st.write("📌 พื้นที่โดยประมาณ:")
    st.code(place_name)

# =====================================================
# 🗺 MAP
# =====================================================

if st.session_state.user_lat:
    st.map({
        "lat": [st.session_state.user_lat],
        "lon": [st.session_state.user_lon]
    })

# =====================================================
# 🌡 TEMPERATURE
# =====================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌡️ อุณหภูมิ")

temp = st.number_input("อุณหภูมิ (°C)", value=28.0)

tmax = temp + 4
tmin = temp - 5

st.markdown(f"<div class='big-number'>{temp:.1f} °C</div>", unsafe_allow_html=True)

st.write("คาดการณ์วันนี้")
st.write(f"สูงสุด: {tmax:.1f} °C | ต่ำสุด: {tmin:.1f} °C")

st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# 📉 PRESSURE
# =====================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📉 ความดันอากาศ")

F = st.number_input("แรง (N)", value=101300.0)
A = st.number_input("พื้นที่ (m²)", value=1.0)

P = F / A if A else 0

st.markdown("<div class='formula-box'>P = F / A</div>", unsafe_allow_html=True)
st.markdown(f"<div class='big-number'>{P:,.0f} Pa</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# 💧 HUMIDITY
# =====================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("💧 ความชื้น")

m_real = st.number_input("มวลไอน้ำจริง (g)", value=12.5)
m_sat = st.number_input("มวลไอน้ำอิ่มตัว (g)", value=17.3)

rh = (m_real / m_sat) * 100 if m_sat else 0

st.markdown("<div class='formula-box'>RH = (mจริง / mอิ่มตัว) × 100</div>", unsafe_allow_html=True)
st.markdown(f"<div class='big-number'>{rh:.1f} %</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# 🌬 WIND
# =====================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌬 ลม")

wind_speed = st.slider("ความเร็วลม (km/h)", 0, 120, 12)
wind_dir = st.selectbox("ทิศทางลม", ["เหนือ","ตะวันออก","ใต้","ตะวันตก","ตะวันออกเฉียงเหนือ",
                                     "ตะวันออกเฉียงใต้","ตะวันตกเฉียงใต้","ตะวันตกเฉียงเหนือ"])

st.markdown(f"<div class='big-number'>{wind_speed} km/h</div>", unsafe_allow_html=True)
st.success(f"➡ ทิศทาง: {wind_dir}")

st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# ☁ CLOUD + RAIN
# =====================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("☁ เมฆและโอกาสฝน")

cloud_cover = st.slider("ปริมาณเมฆ (%)", 0, 100, 40)

rain_prob = min(100, cloud_cover + rh/2)

st.markdown(f"<div class='big-number'>{cloud_cover}%</div>", unsafe_allow_html=True)

st.write(f"🌧 โอกาสฝน: {rain_prob:.0f}%")

st.progress(int(rain_prob))

st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# 📆 7 DAY FORECAST
# =====================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📆 พยากรณ์ 7 วัน")

base = temp

for i in range(1,8):

    t_hi = base + math.sin(i)*3 + 3
    t_lo = base - 5 + math.cos(i)*2

    st.write(
        f"Day {i}: 🌡 {t_lo:.1f}°C - {t_hi:.1f}°C | "
        f"☁ {cloud_cover}% | 🌧 {rain_prob:.0f}%"
    )

st.markdown('</div>', unsafe_allow_html=True)
