import streamlit as st
import plotly.graph_objects as go

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Earth Atmosphere Explorer",
    page_icon="🌍",
    layout="wide"
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
    color: white;
}

.title {
    text-align: center;
    font-size: 56px;
    font-weight: bold;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 22px;
    color: #ddd;
}

.card {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 0 20px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------
st.markdown("<div class='title'>🌍 Earth's Atmosphere</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Explore the Layers of the Sky</div>", unsafe_allow_html=True)

st.write("")
st.write("")

# ----------------------------
# Data
# ----------------------------
layers = [
    "Troposphere",
    "Stratosphere",
    "Mesosphere",
    "Thermosphere",
    "Exosphere"
]

altitude = [12, 50, 85, 600, 10000]

descriptions = {
    "Troposphere": "Where weather happens and humans live.",
    "Stratosphere": "Contains the ozone layer that protects Earth.",
    "Mesosphere": "Cold layer where meteors burn up.",
    "Thermosphere": "Very hot and contains auroras.",
    "Exosphere": "Outer edge of Earth's atmosphere."
}

# ----------------------------
# Layout
# ----------------------------
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📚 Atmospheric Layers")

    selected = st.radio(
        "Select a layer:",
        layers
    )

    st.write("### 📝 Description")
    st.info(descriptions[selected])
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# Plotly Graph
# ----------------------------
with col2:
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=altitude,
        y=layers,
        orientation="h"
    ))

    fig.update_layout(
        title="Altitude of Atmospheric Layers (km)",
        xaxis_title="Altitude (km)",
        yaxis_title="Layer",
        height=500,
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Footer
# ----------------------------
st.markdown("""
<div style="text-align:center; margin-top:40px; color:#ccc;">
    🌌 Created with Streamlit & Python <br>
    Atmosphere Visualization Project
</div>
""", unsafe_allow_html=True)
