import streamlit as st

st.set_page_config(
    page_title="Earth Atmosphere",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 ชั้นบรรยากาศของโลก")

st.write("เว็บไซต์นี้ใช้เพื่อเรียนรู้โครงสร้างชั้นบรรยากาศของโลก")

menu = st.radio(
    "เลือกชั้นบรรยากาศ:",
    [
        "Troposphere",
        "Stratosphere",
        "Mesosphere",
        "Thermosphere",
        "Exosphere"
    ],
    horizontal=True
)

def show_layer(title, height, temp, detail):
    st.subheader(title)
    st.write(f"📏 ความสูง: {height}")
    st.write(f"🌡️ อุณหภูมิ: {temp}")
    st.write(detail)

if menu == "Troposphere":
    show_layer(
        "Troposphere",
        "0–12 km",
        "ลดลงเมื่อสูงขึ้น",
        "เกิดสภาพอากาศ เมฆ และฝน"
    )

elif menu == "Stratosphere":
    show_layer(
        "Stratosphere",
        "12–50 km",
        "อุณหภูมิเพิ่ม",
        "มีชั้นโอโซน"
    )

elif menu == "Mesosphere":
    show_layer(
        "Mesosphere",
        "50–85 km",
        "หนาวจัด",
        "อุกกาบาตเผาไหม้ที่นี่"
    )

elif menu == "Thermosphere":
    show_layer(
        "Thermosphere",
        "85–600 km",
        "ร้อนมาก",
        "เกิดแสงออโรรา"
    )

elif menu == "Exosphere":
    show_layer(
        "Exosphere",
        "600+ km",
        "เบาบาง",
        "ขอบเขตสู่อวกาศ"
    )
import streamlit as st

st.set_page_config(page_title="เครื่องมือพยากรณ์อากาศ", layout="centered")

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align:center;color:#1b7f5c;'>🌦 เครื่องมือพยากรณ์อากาศ</h1>
<p style='text-align:center;'>พยากรณ์อากาศพร้อมการคำนวณ</p>
""", unsafe_allow_html=True)

# ---------- TEMPERATURE ----------
st.subheader("🌡 อุณหภูมิ")
temp = st.number_input("อุณหภูมิ (°C)", value=28)

# ---------- PRESSURE ----------
st.subheader("📉 ความดันอากาศ")
F = st.number_input("แรง (N)", value=101300)
A = st.number_input("พื้นที่ (m²)", value=1.0)

pressure = F / A if A != 0 else 0

st.success(f"ความดันอากาศ = {pressure:,.2f} N/m²")

# ---------- HUMIDITY ----------
st.subheader("💧 ความชื้นสัมพัทธ์ (RH)")
real = st.number_input("มวลไอน้ำจริง (g)", value=12.5)
sat = st.number_input("มวลไอน้ำอิ่มตัว (g)", value=17.3)

rh = (real / sat) * 100 if sat != 0 else 0
st.success(f"RH = {rh:.1f} %")

# ---------- RAIN ----------
st.subheader("🌧 ปริมาณน้ำฝน")

rain = st.slider("เลือกปริมาณฝน (mm)", 0, 50, 5)

col1, col2, col3 = st.columns(3)

if col1.button("ไม่มีฝน"):
    rain = 0
if col2.button("ฝนเบา"):
    rain = 5
if col3.button("ฝนหนัก"):
    rain = 30

st.info(f"☔ ปริมาณฝนปัจจุบัน: {rain} mm")

# ---------- CLOUD ----------
st.subheader("☁ ปริมาณเมฆ")

cloud = st.radio(
    "เลือกปริมาณเมฆ",
    ["แจ่มใส 0%", "เมฆน้อย 20%", "เมฆบาง 40%", "เมฆมาก 60%", "เมฆหนา 80%", "ปกคลุม 100%"]
)

st.write("คุณเลือก:", cloud)
st.divider()
st.caption("จัดทำเพื่อการศึกษา | Streamlit App")
