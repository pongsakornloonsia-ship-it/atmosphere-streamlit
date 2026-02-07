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

st.divider()
st.caption("จัดทำเพื่อการศึกษา | Streamlit App")
