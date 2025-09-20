import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =========================
# Load Excel Data
# =========================
try:
    excel_file = "Cloud_Actual_Optimization.xlsx"
    df_csp = pd.read_excel(excel_file, sheet_name="CSP")
    df_services = pd.read_excel(excel_file, sheet_name="Services")
    df_app = pd.read_excel(excel_file, sheet_name="Application")
except Exception as e:
    st.warning(f"Error reading Excel: {e}")
    st.info("Using dummy data instead")
    # Dummy data
    df_csp = pd.DataFrame({
        "CSP": ["AWS", "Azure", "GCP"],
        "Spend": [100000, 75000, 50000],
        "Marketplace": [15000, 12000, 8000]
    })
    df_services = pd.DataFrame({
        "Service": ["Compute", "Database", "Storage"],
        "Spend": [50000, 40000, 35000]
    })
    df_app = pd.DataFrame({
        "Application": ["App1", "App2", "App3"],
        "Spend": [40000, 35000, 30000]
    })

# =========================
# Page Title
# =========================
st.set_page_config(page_title="Cloud Cost Dashboard", layout="wide")
st.title("Cloud Cost Dashboard")

# =========================
# CSP Section
# =========================
st.header("CSP Overview")

# Waterfall Charts side-by-side
col1, col2 = st.columns(2)

with col1:
    st.subheader("Services Spend Waterfall")
    fig_services = go.Figure(go.Waterfall(
        x=df_csp["CSP"],
        y=df_csp["Spend"],
        text=df_csp["Spend"],
        textposition="outside",
        marker=dict(color="#0052cc")  # McKinsey-style blue
    ))
    fig_services.update_layout(
        title="Services Spend by CSP",
        font=dict(family="Calibri", size=12, color="#000000")
    )
    st.plotly_chart(fig_services, use_container_width=True)

with col2:
    st.subheader("Marketplace Spend Waterfall")
    fig_market = go.Figure(go.Waterfall(
        x=df_csp["CSP"],
        y=df_csp["Marketplace"],
        text=df_csp["Marketplace"],
        textposition="outside",
        marker=dict(color="#3399ff")  # lighter blue
    ))
    fig_market.update_layout(
        title="Marketplace Spend by CSP",
        font=dict(family="Calibri", size=12, color="#000000")
    )
    st.plotly_chart(fig_market, use_container_width=True)

# =========================
# Services Section
# =========================
st.header("Services Overview")
fig_services_bar = go.Figure(go.Bar(
    x=df_services["Service"],
    y=df_services["Spend"],
    text=df_services["Spend"],
    textposition="auto",
    marker_color="#0052cc"
))
fig_services_bar.update_layout(
    title="Spend by Service",
    font=dict(family="Calibri", size=12, color="#000000")
)
st.plotly_chart(fig_services_bar, use_container_width=True)

# =========================
# Heatmap (simplified)
# =========================
st.header("Application Spend Heatmap")
fig_heat = go.Figure(data=go.Heatmap(
    z=df_app["Spend"],
    x=df_app["Application"],
    y=["Spend"],
    colorscale=[[0, '#cce0ff'], [1, '#0052cc']],  # light blue to McKinsey blue
    showscale=True
))
fig_heat.update_layout(
    title="Application Spend Heatmap",
    font=dict(family="Calibri", size=12, color="#000000")
)
st.plotly_chart(fig_heat, use_container_width=True)
