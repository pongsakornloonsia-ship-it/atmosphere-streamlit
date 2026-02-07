import streamlit as st
import plotly.graph_objects as go

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #eafff4, #e0f2ff);
}

.block-container {
    padding-top: 2rem;
}

/* HERO */
.hero {
    background: linear-gradient(135deg,#a7f3d0,#93c5fd);
    padding:60px;
    border-radius:40px;
    text-align:center;
    box-shadow:0 20px 40px rgba(0,0,0,.12);
}

/* BADGE */
.badge {
    display:inline-block;
    padding:10px 18px;
    background:#ffffffaa;
    border-radius:25px;
    margin:5px;
    font-weight:600;
}

/* CARD */
.card {
    background:rgba(255,255,255,0.8);
    backdrop-filter: blur(10px);
    padding:30px;
    border-radius:28px;
    box-shadow:0 15px 30px rgba(0,0,0,0.1);
    margin-bottom:30px;
}

/* BIG NUMBER */
.big {
    font-size:52px;
    font-weight:800;
    color:#059669;
}

.center {
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌤️ เมนู")
page = st.sidebar.radio(
    "เลือกหน้า",
    ["หน้าแรก", "อุณหภูมิ", "ความดัน", "ความชื้น", "ฝน", "เมฆ", "Dashboard รวม"]
)

# ---------------- HERO ----------------
if page == "หน้าแรก":
    st.markdown("""
    <div class="hero">
        <h1>🌍 เครื่องมือพยากรณ์อากาศ</h1>
        <h4>Weather & Atmosphere Interactive Lab</h4>
        <div>
            <span class="badge">⚡ ใช้งานง่าย</span>
            <span class="badge">📊 Interactive</span>
            <span class="badge">🎨 Modern UI</span>
            <span class="badge">🚀 Dashboard</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("👈 ใช้เมนูด้านซ้ายเพื่อเลือกเครื่องมือแต่ละแบบ")

# ---------------- TEMP ----------------
elif page == "อุณหภูมิ":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🌡️ อุณหภูมิ")

    temp = st.slider("เลือกอุณหภูมิ °C", -10, 50, 28)

    st.markdown(f"<div class='big center'>{temp} °C</div>", unsafe_allow_html=True)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=temp,
        gauge={'axis': {'range': [-10, 50]}}
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PRESSURE ----------------
elif page == "ความดัน":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📉 ความดันอากาศ")

    F = st.number_input("แรง (N)", 0.0, value=101300.0)
    A = st.number_input("พื้นที่ (m²)", 0.1, value=1.0)

    P = F / A

    st.markdown(f"<div class='big center'>{P:,.0f} N/m²</div>", unsafe_allow_html=True)

    st.progress(min(int(P / 200000 * 100), 100))

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- HUMID ----------------
elif page == "ความชื้น":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💧 ความชื้น")

    c1, c2 = st.columns(2)

    with c1:
        m1 = st.number_input("มวลไอน้ำจริง (g)", value=12.5)
        m2 = st.number_input("มวลไอน้ำอิ่มตัว (g)", value=17.3)

    rh = (m1 / m2) * 100 if m2 else 0

    with c2:
        mv = st.number_input("มวลไอน้ำ (g)", value=15.5)
        vol = st.number_input("ปริมาตร (m³)", value=1.0)

    ah = mv / vol if vol else 0

    st.markdown(f"""
        <div class='center big'>{rh:.1f}% RH</div>
        <div class='center big'>{ah:.2f} g/m³</div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- RAIN ----------------
elif page == "ฝน":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🌧️ ปริมาณฝน")

    rain = st.slider("mm", 0, 50, 5)

    st.markdown(f"<div class='big center'>{rain} mm</div>", unsafe_allow_html=True)

    bar = go.Figure(go.Bar(x=["Rain"], y=[rain]))
    st.plotly_chart(bar, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CLOUD ----------------
elif page == "เมฆ":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("☁️ ปริมาณเมฆ")

    cloud = st.select_slider(
        "เลือก",
        options=["0%", "20%", "40%", "60%", "80%", "100%"],
        value="40%"
    )

    st.success(f"☁️ ปริมาณเมฆ: {cloud}")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------
elif page == "Dashboard รวม":
    st.markdown("<h1>📊 Weather Dashboard</h1>", unsafe_allow_html=True)

    tcol, pcol, rcol = st.columns(3)

    with tcol:
        st.metric("🌡️ อุณหภูมิ", "28°C")

    with pcol:
        st.metric("📉 ความดัน", "101,300 N/m²")

    with rcol:
        st.metric("🌧️ ฝน", "5 mm")

    st.markdown("---")

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=[28,30,29,27,26,25,24], mode="lines+markers"))
    fig.update_layout(title="แนวโน้ม 7 วัน")
    st.plotly_chart(fig, use_container_width=True)
