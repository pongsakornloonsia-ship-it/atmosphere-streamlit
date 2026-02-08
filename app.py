import streamlit as st
import random
import pandas as pd

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="เครื่องมือพยากรณ์อากาศ",
    page_icon="🌤️",
    layout="wide"
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("⚙️ แผงควบคุม")

page = st.sidebar.radio(
    "เลือกหน้า",
    ["หน้าหลัก", "ข้อมูลเชิงลึก", "แผนที่"]
)

province_data = {
    "กรุงเทพฯ": {"temp": 30, "hum": 70},
    "เชียงใหม่": {"temp": 26, "hum": 60},
    "ภูเก็ต": {"temp": 29, "hum": 75},
    "ขอนแก่น": {"temp": 28, "hum": 65},
    "สงขลา": {"temp": 29, "hum": 78},
}

city = st.sidebar.selectbox("เลือกจังหวัด", list(province_data.keys()))

dark_mode = st.sidebar.toggle("🌙 โหมดกลางคืน")

# =====================================================
# GEOLOCATION (Browser)
# =====================================================

params = st.query_params

lat_user = float(params.get("lat", 13.75))
lon_user = float(params.get("lon", 100.5))

# =====================================================
# THEME
# =====================================================

if dark_mode:
    bg = "#0f172a"
    card = "rgba(30,41,59,0.9)"
else:
    bg = "linear-gradient(135deg,#7dd3fc,#a7f3d0,#fbcfe8)"
    card = "rgba(255,255,255,0.75)"

# =====================================================
# CSS
# =====================================================

st.markdown(f"""
<style>

.stApp {{
    background:{bg};
}}

.block-container {{
    padding:2rem 3rem;
}}

.card {{
    background:{card};
    padding:32px;
    border-radius:30px;
    box-shadow:0 15px 40px rgba(0,0,0,0.25);
    margin-bottom:40px;
}}

.title-box {{
    text-align:center;
    padding:60px;
    background:{card};
    border-radius:40px;
    margin-bottom:50px;
}}

.big-number {{
    font-size:42px;
    font-weight:800;
}}

.formula {{
    background:rgba(255,255,255,0.6);
    padding:12px;
    border-radius:12px;
    margin-top:12px;
}}

.week-grid {{
    display:grid;
    grid-template-columns:repeat(7,1fr);
    gap:16px;
}}

.day-box {{
    background:rgba(255,255,255,0.6);
    border-radius:18px;
    padding:14px;
    text-align:center;
}}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown(f"""
<div class="title-box">
<h1>🌍 เครื่องมือพยากรณ์อากาศ</h1>
<h3>พื้นที่: {city}</h3>
</div>
""", unsafe_allow_html=True)

# =====================================================
# GEO BUTTON
# =====================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📍 ใช้ตำแหน่งของคุณ")

geo_html = """
<script>
function getLocation() {
navigator.geolocation.getCurrentPosition(
(pos)=>{
const params = new URLSearchParams(window.location.search);
params.set("lat",pos.coords.latitude.toFixed(6));
params.set("lon",pos.coords.longitude.toFixed(6));
window.location.search=params.toString();
},
()=>alert("ไม่สามารถดึงตำแหน่งได้")
);
}
</script>

<button onclick="getLocation()" style="
padding:14px 26px;
border-radius:18px;
border:none;
background:#22c55e;
color:white;
font-size:16px;">
📍 ใช้ตำแหน่งของฉัน
</button>
"""
st.components.v1.html(geo_html, height=80)
st.markdown(f"พิกัดที่ใช้: {lat_user}, {lon_user}")
st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# BASE WEATHER BY CITY
# =====================================================

base_temp = province_data[city]["temp"]
base_hum = province_data[city]["hum"]

# =====================================================
# MAIN PAGE
# =====================================================

if page == "หน้าหลัก":

    # ---------- TEMP ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    temp = st.number_input("🌡️ อุณหภูมิ (°C)", value=float(base_temp))
    st.markdown("<div class='formula'>สูตร: ค่าอุณหภูมิจากผู้ใช้</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-number'>{temp:.1f} °C</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- PRESSURE ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    F = st.number_input("แรง (N)", value=101325.0)
    A = st.number_input("พื้นที่ (m²)", value=1.0)
    P = F / A if A != 0 else 0
    st.markdown("<div class='formula'>P = F / A</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-number'>{P:,.0f} Pa</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- HUMIDITY ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    m_real = st.number_input("มวลไอน้ำจริง (g)", value=base_hum / 4)
    m_sat = st.number_input("มวลไอน้ำอิ่มตัว (g)", value=18.0)
    RH = (m_real / m_sat) * 100 if m_sat else 0
    st.markdown("<div class='formula'>RH = (mจริง / mอิ่มตัว) × 100</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-number'>{RH:.1f}%</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- WIND ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    wind = st.slider("🌬️ ความเร็วลม (km/h)", 0, 120, 20)
    direction = st.selectbox("ทิศทาง", ["N","NE","E","SE","S","SW","W","NW"])
    st.markdown(f"🌬️ {wind} km/h | ➡️ {direction}")
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- CLOUD ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    cloud = st.slider("☁️ ปริมาณเมฆ (%)", 0, 100, 40)
    icon = ["☀️","🌤️","⛅","☁️","🌧️","⛈️"][min(5, cloud//20)]
    st.markdown(f"<div class='big-number'>{icon}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- RAIN ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    rain_prob = min(100, int((RH + cloud) / 2))
    st.markdown("<div class='formula'>โอกาสฝน ≈ (RH + เมฆ)/2</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-number'>{rain_prob}%</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- 7 DAYS ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    temps = [temp + random.randint(-4,4) for _ in range(7)]
    df = pd.DataFrame({"Day":days,"Temp":temps}).set_index("Day")
    st.line_chart(df)
    st.markdown("<div class='week-grid'>", unsafe_allow_html=True)
    for d,t in zip(days,temps):
        st.markdown(f"<div class='day-box'>{d}<br>{t}°C</div>", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

# =====================================================
# MAP PAGE
# =====================================================

elif page == "แผนที่":
    st.subheader("🗺️ ตำแหน่งพื้นที่")
    st.map(pd.DataFrame({"lat":[lat_user],"lon":[lon_user]}))

# =====================================================
# INSIGHT PAGE
# =====================================================

elif page == "ข้อมูลเชิงลึก":
    st.subheader("📊 วิเคราะห์")
    df = pd.DataFrame({
        "Temp":[random.randint(24,35) for _ in range(7)],
        "Rain":[random.randint(0,50) for _ in range(7)],
        "Humidity":[random.randint(40,90) for _ in range(7)]
    })
    st.area_chart(df)
