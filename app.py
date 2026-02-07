import streamlit as st
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Earth Atmosphere Explorer",
    page_icon="🌍",
    layout="wide"
)

# ---------------- CSS STYLE ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom,#0b132b,#1c2541);
}
.big-title {
    font-size:60px;
    font-weight:800;
    text-align:center;
    background: linear-gradient(to right,#5bc0be,#f1faee);
    -webkit-background-clip:text;
    color:transparent;
}
.subtitle {
    text-align:center;
    font-size:22px;
    color:#ddd;
}
.card {
    background: rgba(255,255,255,0.12);
    padding:25px;
    border-radius:20px;
    box-shadow:0 0 20px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="big-title">🌍 Earth Atmosphere Explorer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">สำรวจชั้นบรรยากาศโลกแบบอินเทอร์แอคทีฟ</div>', unsafe_allow_html=True)
st.divider()

# ---------------- DATA ----------------
layers = {
    "Troposphere": {
        "height": "0–12 km",
        "temp": "15°C → -56°C",
        "desc": "ชั้นที่มนุษย์อาศัยอยู่ เกิดสภาพอากาศ เมฆ ฝน",
    },
    "Stratosphere": {
        "height": "12–50 km",
        "temp": "-56°C → 0°C",
        "desc": "มีโอโซน ดูดซับรังสี UV",
    },
    "Mesosphere": {
        "height": "50–85 km",
        "temp": "0°C → -90°C",
        "desc": "อุกกาบาตไหม้ในชั้นนี้",
    },
    "Thermosphere": {
        "height": "85–600 km",
        "temp": "สูงกว่า 1000°C",
        "desc": "เกิดแสงออโรรา",
    },
    "Exosphere": {
        "height": "600+ km",
        "temp": "เบาบางมาก",
        "desc": "ขอบเขตสู่อวกาศ",
    }
}

# ---------------- SIDEBAR ----------------
st.sidebar.title("🚀 Control Panel")
selected = st.sidebar.selectbox("เลือกชั้นบรรยากาศ", list(layers.keys()))

st.sidebar.markdown("---")
st.sidebar.write("📘 เว็บนี้สร้างด้วย Python + Streamlit")

# ---------------- MAIN CONTENT ----------------
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(f"📍 {selected}")
    st.write(f"**ความสูง:** {layers[selected]['height']}")
    st.write(f"**อุณหภูมิ:** {layers[selected]['temp']}")
    st.write(layers[selected]['desc'])
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- 3D GRAPH ----------------
with col2:

    heights = [0,12,50,85,600,800]
    names = list(layers.keys()) + ["Space"]

    fig = go.Figure()

    for i in range(len(heights)-1):
        fig.add_trace(go.Scatter3d(
            x=[0,0],
            y=[0,0],
            z=[heights[i],heights[i+1]],
            mode='lines',
            line=dict(width=20),
            name=names[i]
        ))

    fig.update_layout(
        height=500,
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(title="Altitude (km)")
        ),
        margin=dict(l=0,r=0,t=0,b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    "<center>🌎 Atmosphere Project | Made with Streamlit</center>",
    unsafe_allow_html=True
)
