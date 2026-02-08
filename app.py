import streamlit as st
import datetime
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
# 📍 PROVINCES + COORDS
# =====================================================

province_coords = {
    "กรุงเทพมหานคร": (13.7563, 100.5018),
    "กระบี่": (8.0863, 98.9063),
    "กาญจนบุรี": (14.0228, 99.5328),
    "กาฬสินธุ์": (16.4314, 103.5059),
    "กำแพงเพชร": (16.4828, 99.5227),
    "ขอนแก่น": (16.4419, 102.8350),
    "จันทบุรี": (12.6113, 102.1039),
    "ฉะเชิงเทรา": (13.6904, 101.0779),
    "ชลบุรี": (13.3611, 100.9847),
    "ชัยนาท": (15.1864, 100.1235),
    "ชัยภูมิ": (15.8068, 102.0315),
    "ชุมพร": (10.4930, 99.1800),
    "เชียงราย": (19.9072, 99.8309),
    "เชียงใหม่": (18.7883, 98.9853),
    "ตรัง": (7.5594, 99.6114),
    "ตราด": (12.2426, 102.5175),
    "ตาก": (16.8790, 99.1256),
    "นครนายก": (14.2069, 101.2131),
    "นครปฐม": (13.8199, 100.0622),
    "นครพนม": (17.4108, 104.7784),
    "นครราชสีมา": (14.9799, 102.0977),
    "นครศรีธรรมราช": (8.4304, 99.9631),
    "นครสวรรค์": (15.7047, 100.1372),
    "นนทบุรี": (13.8621, 100.5144),
    "นราธิวาส": (6.4255, 101.8253),
    "น่าน": (18.7756, 100.7730),
    "บึงกาฬ": (18.3609, 103.6464),
    "บุรีรัมย์": (14.9930, 103.1039),
    "ปทุมธานี": (14.0208, 100.5250),
    "ประจวบคีรีขันธ์": (11.8124, 99.7973),
    "ปราจีนบุรี": (14.0500, 101.3700),
    "ปัตตานี": (6.8695, 101.2505),
    "พระนครศรีอยุธยา": (14.3532, 100.5689),
    "พะเยา": (19.1667, 99.9000),
    "พังงา": (8.4510, 98.5340),
    "พัทลุง": (7.6170, 100.0740),
    "พิจิตร": (16.4429, 100.3480),
    "พิษณุโลก": (16.8211, 100.2659),
    "เพชรบุรี": (13.1119, 99.9447),
    "เพชรบูรณ์": (16.4189, 101.1606),
    "แพร่": (18.1446, 100.1403),
    "ภูเก็ต": (7.8804, 98.3923),
    "มหาสารคาม": (16.1867, 103.3020),
    "มุกดาหาร": (16.5453, 104.7235),
    "แม่ฮ่องสอน": (19.2990, 97.9685),
    "ยะลา": (6.5410, 101.2804),
    "ยโสธร": (15.7927, 104.1453),
    "ร้อยเอ็ด": (16.0567, 103.6531),
    "ระนอง": (9.9529, 98.6085),
    "ระยอง": (12.6814, 101.2789),
    "ราชบุรี": (13.5283, 99.8134),
    "ลพบุรี": (14.7995, 100.6534),
    "ลำปาง": (18.2888, 99.4909),
    "ลำพูน": (18.5745, 99.0087),
    "เลย": (17.4860, 101.7223),
    "ศรีสะเกษ": (15.1186, 104.3220),
    "สกลนคร": (17.1546, 104.1348),
    "สงขลา": (7.1756, 100.6143),
    "สตูล": (6.6238, 100.0673),
    "สมุทรปราการ": (13.5991, 100.5998),
    "สมุทรสงคราม": (13.4098, 100.0023),
    "สมุทรสาคร": (13.5475, 100.2744),
    "สระแก้ว": (13.8240, 102.0646),
    "สระบุรี": (14.5289, 100.9100),
    "สิงห์บุรี": (14.8936, 100.3967),
    "สุโขทัย": (17.0068, 99.8265),
    "สุพรรณบุรี": (14.4745, 100.1177),
    "สุราษฎร์ธานี": (9.1382, 99.3215),
    "สุรินทร์": (14.8829, 103.4937),
    "หนองคาย": (17.8783, 102.7413),
    "หนองบัวลำภู": (17.2043, 102.4407),
    "อ่างทอง": (14.5896, 100.4555),
    "อำนาจเจริญ": (15.8650, 104.6250),
    "อุดรธานี": (17.4138, 102.7873),
    "อุตรดิตถ์": (17.6200, 100.0990),
    "อุทัยธานี": (15.3835, 100.0240),
    "อุบลราชธานี": (15.2447, 104.8473)
}

provinces = list(province_coords.keys())
province = st.selectbox("📍 เลือกจังหวัด", provinces)

lat, lon = province_coords[province]
st.success(f"จังหวัด: {province} | พิกัด: {lat}, {lon}")

# =====================================================
# 🗺️ MAP
# =====================================================

st.markdown("## 🗺️ แผนที่")
st.map([{"lat": lat, "lon": lon}])

# =====================================================
# 🌡️ TEMPERATURE
# =====================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌡️ อุณหภูมิ")

temp = st.number_input("อุณหภูมิ (°C)", value=28.0)
st.markdown(f"<div class='big-number'>{temp:.1f} °C</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# 📉 PRESSURE
# =====================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📉 ความดันอากาศ")

F = st.number_input("แรง (N)", value=101300.0)
A = st.number_input("พื้นที่ (m²)", value=1.0)

P = F / A if A != 0 else 0
st.markdown(f"<div class='big-number'>{P:,.0f} N/m²</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# 💧 HUMIDITY
# =====================================================

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

# =====================================================
# 🌧️ RAIN
# =====================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌧️ ปริมาณน้ำฝน")

rain = st.slider("เลือกปริมาณฝน (mm)", 0, 50, 5)
st.markdown(f"<div class='big-number'>{rain} mm</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# ☁️ CLOUD
# =====================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("☁️ ปริมาณเมฆบนท้องฟ้า")

cloud_percent = st.slider("ปริมาณเมฆ (%)", 0, 100, 40)
rain_prob = int(cloud_percent * 0.8)

st.markdown(f"""
<b>☁️ เมฆ:</b> {cloud_percent} %  
<b>🌧️ โอกาสฝน:</b> {rain_prob} %
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# 📐 FORMULAS
# =====================================================

st.markdown("""
<div class="card">
<h3>📐 สูตรที่ใช้</h3>

P = F / A  

RH = (mจริง / mอิ่มตัว) × 100  

AH = m / V  

Rain ≈ Cloud × 0.8
</div>
""", unsafe_allow_html=True)
st.title("โปรแกรมพยากรณ์อากาศ 7 วัน")

# 👉 ใส่ตรงนี้
# =====================================
# 🌧️ RAINFALL VISUAL (CUSTOM STYLE)
# =====================================

st.markdown("## 🌧️ ปริมาณฝนคาดการณ์")

rain = st.slider(
    "เลือกปริมาณฝน (mm)",
    min_value=0,
    max_value=100,
    value=40
)

if rain == 0:
    level = "☀️ ไม่มีฝน"
elif rain <= 10:
    level = "🌦️ ฝนเบา"
elif rain <= 30:
    level = "🌧️ ฝนปานกลาง"
elif rain <= 60:
    level = "🌧️🌧️ ฝนหนัก"
else:
    level = "⛈️ ฝนตกหนักมาก"

st.subheader(level)
st.progress(rain / 100)

st.metric("Rainfall", f"{rain} mm")

st.markdown("""
<div style="font-size:40px; text-align:center;">
☁️ 🌧️ ☁️
</div>
""", unsafe_allow_html=True)

# =====================================================
# 📅 7 DAY FORECAST
# =====================================================

st.markdown("## 📅 พยากรณ์ 7 วัน")

today = datetime.date.today()
cols = st.columns(7)

for i in range(7):
    date = today + datetime.timedelta(days=i)

    tmin = round(random.uniform(22, 27), 1)
    tmax = round(tmin + random.uniform(4, 9), 1)

    hum = random.randint(55, 95)
    pres = random.randint(100500, 101800)
    cloud = random.randint(0, 100)
    rainp = min(100, int(cloud * 0.8))

    with cols[i]:
        st.markdown(f"""
        <div class="card">
        <h4>{date.strftime('%d/%m')}</h4>
        🌡️ {tmin}–{tmax} °C<br>
        💧 {hum} %<br>
        ☁️ {cloud} %<br>
        🌧️ {rainp} %<br>
        📉 {pres} Pa
        </div>
        """, unsafe_allow_html=True)
        # =====================================================
# 📦 เตรียมข้อมูล 7 วัน สำหรับกราฟ
# =====================================================

week_data = []

today = datetime.date.today()

for i in range(7):
    date = today + datetime.timedelta(days=i)

    tmin = round(random.uniform(22, 27), 1)
    tmax = round(tmin + random.uniform(4, 9), 1)

    hum = random.randint(55, 95)
    pres = random.randint(100500, 101800)
    cloud = random.randint(0, 100)
    rainp = min(100, int(cloud * 0.8))

    week_data.append(
        (date, tmin, tmax, hum, pres, cloud, rainp)
    )
    # =====================================================
# ☁️ CLOUD TYPE VISUAL CARDS
# =====================================================

st.markdown("## ☁️ ประเภทเมฆบนท้องฟ้า")

st.markdown("""
<style>

.cloud-grid {
    display:grid;
    grid-template-columns: repeat(auto-fit,minmax(260px,1fr));
    gap:20px;
}

.cloud-card {
    border-radius:20px;
    padding:18px;
    background:white;
    box-shadow:0 10px 20px rgba(0,0,0,0.08);
}

.cloud-box {
    height:110px;
    border-radius:14px;
    margin-top:10px;
    position:relative;
}

/* ---- Individual types ---- */

.cumulus {
    background:linear-gradient(#e0f2fe,#f8fafc);
}
.stratus {
    background:linear-gradient(#d1d5db,#f3f4f6);
}
.cirrus {
    background:linear-gradient(#dbeafe,#eff6ff);
}
.cumulonimbus {
    background:linear-gradient(#6b7280,#111827);
}
.nimbostratus {
    background:linear-gradient(#9ca3af,#374151);
}

/* cloud shapes */
.cloud-shape {
    position:absolute;
    background:white;
    border-radius:50%;
    opacity:0.9;
}

</style>

<div class="cloud-grid">

<div class="cloud-card">
<h4>☁️ เมฆคิวมูลัส</h4>
Cumulus
<div class="cloud-box cumulus">
<div class="cloud-shape" style="width:60px;height:40px;top:40px;left:30px;"></div>
<div class="cloud-shape" style="width:80px;height:55px;top:30px;left:70px;"></div>
</div>
เมฆขาวปุย ลอยเดี่ยว อากาศดี
</div>

<div class="cloud-card">
<h4>🌫️ เมฆสเตรตัส</h4>
Stratus
<div class="cloud-box stratus"></div>
เมฆชั้นต่ำ ปกคลุมท้องฟ้า
</div>

<div class="cloud-card">
<h4>🌤️ เมฆซีร์รัส</h4>
Cirrus
<div class="cloud-box cirrus">
<div class="cloud-shape" style="width:100px;height:10px;top:40px;left:40px;border-radius:20px;"></div>
</div>
เมฆเส้นบาง ระดับสูง
</div>

<div class="cloud-card">
<h4>⛈️ เมฆคิวมูโลนิมบัส</h4>
Cumulonimbus
<div class="cloud-box cumulonimbus"></div>
เมฆฝนฟ้าคะนอง อันตราย
</div>

<div class="cloud-card">
<h4>🌧️ เมฆนิมโบสเตรตัส</h4>
Nimbostratus
<div class="cloud-box nimbostratus"></div>
เมฆฝนต่อเนื่อง ฟ้าครึ้ม
</div>

</div>
""", unsafe_allow_html=True)
        # =====================================================
# 📊 GRAPH SECTION (NO EXTRA LIBRARIES)
# =====================================================

st.markdown("## 📊 กราฟพยากรณ์ 7 วัน")

days = []
tmins = []
tmaxs = []
hums = []
pressures = []
rains = []

for d in week_data:
    days.append(d[0].strftime("%d/%m"))
    tmins.append(d[1])
    tmaxs.append(d[2])
    hums.append(d[3])
    pressures.append(d[4])
    rains.append(d[6])

st.subheader("🌡️ อุณหภูมิ")

st.line_chart({
    "ต่ำสุด": tmins,
    "สูงสุด": tmaxs
})

st.subheader("💧 ความชื้น")
st.line_chart(hums)

st.subheader("📉 ความดันอากาศ")
st.line_chart(pressures)

st.subheader("🌧️ โอกาสฝน")
st.line_chart(rains)
# =====================================================
# 👤 ผู้จัดทำ
# =====================================================

st.markdown("""
<div style="
    margin-top:60px;
    padding:25px;
    text-align:center;
    border-radius:22px;
    background:linear-gradient(135deg,#d1fae5,#bfdbfe);
    box-shadow:0 8px 20px rgba(0,0,0,0.08);
">
    <h3>👤 ผู้จัดทำ</h3>
    <p style="font-size:18px;font-weight:600;">
        พงศกร ลุ่นเซียะ
    </p>
    <p style="font-size:16px;">
        ม.1/7 เลขที่ 25
    </p>
    <p style="color:#555;">
        โครงงานระบบพยากรณ์อากาศด้วย Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
