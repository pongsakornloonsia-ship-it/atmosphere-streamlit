import streamlit as st
import random
import pandas as pd

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="เครื่องมือพยากรณ์อากาศ",
    page_icon="🌤️",
    layout="wide"
)

# =====================================================
# SIDEBAR CONTROL
# =====================================================

st.sidebar.header("⚙️ แผงควบคุม")

page = st.sidebar.radio(
    "เลือกหน้า",
    ["หน้าหลัก", "ข้อมูลเชิงลึก", "แผนที่"]
)

city = st.sidebar.selectbox(
    "เลือกจังหวัด",
    ["กรุงเทพฯ", "เชียงใหม่", "ภูเก็ต", "ขอนแก่น", "สงขลา"]
)

lat = st.sidebar.number_input("Latitude", value=13.75)
lon = st.sidebar.number_input("Longitude", value=100.5)

dark_mode = st.sidebar.toggle("🌙 โหมดกลางคืน")

# =====================================================
# THEME MODE
# =====================================================

if dark_mode:
    bg = "#0f172a"
    card = "rgba(30,41,59,0.9)"
    text = "white"
else:
    bg = "linear-gradient(135deg,#7dd3fc,#a7f3d0,#fbcfe8)"
    card = "rgba(255,255,255,0.75)"
    text = "#0f172a"

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
    padding:34px;
    border-radius:30px;
    box-shadow:0 15px 40px rgba(0,0,0,0.25);
    margin-bottom:40px;
    color:{text};
}}

.title-box {{
    text-align:center;
    padding:70px;
    background:{card};
    border-radius:40px;
    margin-bottom:50px;
}}

.badge {{
    display:inline-block;
    padding:10px 22px;
    background:#2563eb;
    color:white;
    border-radius:30px;
    margin:6px;
    font-weight:600;
}}

.big-number {{
    font-size:44px;
    font-weight:800;
}}

.formula {{
    background:rgba(255,255,255,0.5);
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
    border-radius:20px;
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
<div>
<span class="badge">สูตรคำนวณ</span>
<span class="badge">7 วัน</span>
<span class="badge">Interactive</span>
</div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# PAGE SWITCH
# =====================================================

if page == "หน้าหลัก":

    # ---------------- TEMPERATURE ----------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🌡️ อุณหภูมิ")

    temp = st.number_input("อุณหภูมิ (°C)", value=28.0)

    st.markdown("<div class='formula'>สูตร: ค่าอุณหภูมิจากผู้ใช้</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-number'>{temp:.1f} °C</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- PRESSURE ----------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📉 ความดันอากาศ")

    F = st.number_input("แรง (N)", value=101325.0)
    A = st.number_input("พื้นที่ (m²)", value=1.0)

    P = F / A if A != 0 else 0

    st.markdown("<div class='formula'>สูตร: P = F / A</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-number'>{P:,.0f} Pa</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- HUMIDITY ----------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💧 ความชื้น")

    m_real = st.number_input("มวลไอน้ำจริง (g)", value=12.5)
    m_sat = st.number_input("มวลไอน้ำอิ่มตัว (g)", value=18.0)

    RH = (m_real / m_sat) * 100 if m_sat != 0 else 0

    st.markdown("<div class='formula'>RH = (mจริง / mอิ่มตัว) × 100</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-number'>{RH:.1f}%</div>", unsafe_allow_html=True)

    m_vapor = st.number_input("มวลไอน้ำรวม (g)", value=15.0)
    volume = st.number_input("ปริมาตร (m³)", value=1.0)

    AH = m_vapor / volume if volume != 0 else 0

    st.markdown("<div class='formula'>AH = m / V</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-number'>{AH:.2f} g/m³</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- RAIN ----------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🌧️ ฝน")

    rain = st.slider("ปริมาณฝน (mm)", 0, 100, 10)

    rain_prob = min(100, int((RH + rain) / 2))

    st.markdown("<div class='formula'>โอกาสฝน ≈ (RH + mm)/2</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-number'>{rain_prob}%</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- 7 DAYS ----------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📅 พยากรณ์ 7 วัน")

    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    temps = [temp + random.randint(-4,4) for _ in range(7)]

    df = pd.DataFrame({"Day":days,"Temp":temps})

    st.line_chart(df.set_index("Day"))

    st.markdown("<div class='week-grid'>", unsafe_allow_html=True)

    for d,t in zip(days,temps):
        st.markdown(f"""
        <div class='day-box'>
        {d}<br>{t}°C
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

# =====================================================
# INSIGHT PAGE
# =====================================================

elif page == "ข้อมูลเชิงลึก":

    st.subheader("📊 วิเคราะห์ข้อมูล")

    data = pd.DataFrame({
        "Temperature": temps if "temps" in locals() else [25]*7,
        "Rain": [random.randint(0,40) for _ in range(7)],
        "Humidity":[random.randint(40,90) for _ in range(7)]
    })

    st.area_chart(data)

# =====================================================
# MAP PAGE
# =====================================================

elif page == "แผนที่":

    st.subheader("🗺️ ตำแหน่งพื้นที่")

    map_df = pd.DataFrame({
        "lat":[lat],
        "lon":[lon]
    })

    st.map(map_df)
