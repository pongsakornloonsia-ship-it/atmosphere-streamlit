import streamlit as st

# ================= CONFIG =================
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# ================= SIDEBAR =================
st.sidebar.title("📌 เมนู")
menu = st.sidebar.radio(
    "เลือกหมวด",
    ["ภาพรวม", "อุณหภูมิ", "ความดัน", "ความชื้น", "ฝน", "เมฆ"]
)

# ================= CSS =================
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
    transition: 0.35s ease;
}

.card:hover {
    transform: scale(1.02);
    box-shadow: 0 25px 45px rgba(0,0,0,0.15);
}

/* HEADER */
.title-box {
    text-align:center;
    padding:55px;
    background: linear-gradient(135deg,#b8f3dc,#a7c7ff);
    border-radius:35px;
    margin-bottom:40px;
}

.badge {
    display:inline-block;
    padding:10px 20px;
    background:#dcfce7;
    border-radius:25px;
    font-weight:600;
    margin:6px;
}

/* BIG NUMBER */
.big-number {
    font-size:52px;
    font-weight:bold;
    margin-top:10px;
}

.small-note {
    color:#555;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="title-box">
    <h1>🌍 Weather Forecast Dashboard</h1>
    <h4>เครื่องมือจำลองการคำนวณสภาพอากาศระดับแข่งขัน</h4>
    <div>
        <span class="badge">⚡ Interactive</span>
        <span class="badge">📊 Dashboard</span>
        <span class="badge">🏆 แข่งขัน</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= INPUTS =================
temp = st.sidebar.slider("🌡️ อุณหภูมิ (°C)", -10, 50, 28)
F = st.sidebar.number_input("📉 แรง (N)", value=101300.0)
A = st.sidebar.number_input("📐 พื้นที่ (m²)", value=1.0)

m_real = st.sidebar.number_input("💧 มวลไอน้ำจริง (g)", value=12.5)
m_sat = st.sidebar.number_input("💧 มวลไอน้ำอิ่มตัว (g)", value=17.3)

m_vapor = st.sidebar.number_input("💦 มวลไอน้ำรวม (g)", value=15.5)
volume = st.sidebar.number_input("🌫️ ปริมาตรอากาศ (m³)", value=1.0)

rain = st.sidebar.slider("🌧️ ฝน (mm)", 0, 50, 5)

cloud_val = st.sidebar.select_slider(
    "☁️ เมฆ (%)",
    options=[0, 20, 40, 60, 80, 100],
    value=40
)

# ================= CALC =================
P = F / A if A != 0 else 0
rh = (m_real / m_sat) * 100 if m_sat != 0 else 0
ah = m_vapor / volume if volume != 0 else 0

# ================= COLOR =================
def temp_color(t):
    if t >= 35:
        return "#dc2626"
    elif t >= 25:
        return "#f97316"
    else:
        return "#2563eb"

# ================= OVERVIEW =================
if menu == "ภาพรวม":

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🌡️ อุณหภูมิ", f"{temp} °C")
    col2.metric("📉 ความดัน", f"{P:,.0f} Pa")
    col3.metric("💧 RH", f"{rh:.1f} %")
    col4.metric("🌧️ ฝน", f"{rain} mm")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("☁️ ปริมาณเมฆ")
    st.progress(cloud_val)
    st.write(f"ปกคลุม {cloud_val}%")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= TEMPERATURE =================
if menu == "อุณหภูมิ":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🌡️ อุณหภูมิ")
    st.markdown(
        f"<div class='big-number' style='color:{temp_color(temp)}'>{temp} °C</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ================= PRESSURE =================
if menu == "ความดัน":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📉 ความดันอากาศ")
    st.markdown(
        f"<div class='big-number'>{P:,.0f} Pa</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ================= HUMIDITY =================
if menu == "ความชื้น":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💧 ความชื้น")

    st.write("Relative Humidity")
    st.progress(min(int(rh), 100))
    st.markdown(f"<div class='big-number'>{rh:.1f}%</div>", unsafe_allow_html=True)

    st.write("Absolute Humidity")
    st.markdown(f"<div class='big-number'>{ah:.2f} g/m³</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= RAIN =================
if menu == "ฝน":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🌧️ ปริมาณน้ำฝน")
    st.progress(rain * 2)
    st.markdown(f"<div class='big-number'>{rain} mm</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= CLOUD =================
if menu == "เมฆ":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("☁️ เมฆบนท้องฟ้า")
    st.progress(cloud_val)
    st.markdown(f"<div class='big-number'>{cloud_val}%</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
