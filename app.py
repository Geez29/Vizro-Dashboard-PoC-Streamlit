import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =========================
# Page Configuration (must be first Streamlit command)
# =========================
st.set_page_config(page_title="Cloud Cost Dashboard", layout="wide")

# =========================
# Load Excel Data
# =========================
@st.cache_data
def load_data():
    try:
        excel_file = "Cloud_Actual_Optimization.xlsx"
        df_csp = pd.read_excel(excel_file, sheet_name="CSP")
        df_services = pd.read_excel(excel_file, sheet_name="Services")
        df_app = pd.read_excel(excel_file, sheet_name="Application")
        return df_csp, df_services, df_app, None
    except Exception as e:
        error_msg = f"Error reading Excel: {e}"
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
        return df_csp, df_services, df_app, error_msg

# Load the data
df_csp, df_services, df_app, error_msg = load_data()

# =========================
# Page Title
# =========================
st.title("Cloud Cost Dashboard")

# Show warning if using dummy data
if error_msg:
    st.warning(error_msg)
    st.info("Using dummy data instead")

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
        text=[f"${x:,.0f}" for x in df_csp["Spend"]],
        textposition="outside",
        marker=dict(color="#0052cc")  # McKinsey-style blue
    ))
    fig_services.update_layout(
        title="Services Spend by CSP",
        font=dict(family="Calibri", size=12, color="#000000"),
        yaxis_title="Spend ($)",
        showlegend=False
    )
    st.plotly_chart(fig_services, use_container_width=True)

with col2:
    st.subheader("Marketplace Spend Waterfall")
    fig_market = go.Figure(go.Waterfall(
        x=df_csp["CSP"],
        y=df_csp["Marketplace"],
        text=[f"${x:,.0f}" for x in df_csp["Marketplace"]],
        textposition="outside",
        marker=dict(color="#3399ff")  # lighter blue
    ))
    fig_market.update_layout(
        title="Marketplace Spend by CSP",
        font=dict(family="Calibri", size=12, color="#000000"),
        yaxis_title="Spend ($)",
        showlegend=False
    )
    st.plotly_chart(fig_market, use_container_width=True)

# =========================
# Services Section
# =========================
st.header("Services Overview")

fig_services_bar = go.Figure(go.Bar(
    x=df_services["Service"],
    y=df_services["Spend"],
    text=[f"${x:,.0f}" for x in df_services["Spend"]],
    textposition="auto",
    marker_color="#0052cc"
))
fig_services_bar.update_layout(
    title="Spend by Service",
    font=dict(family="Calibri", size=12, color="#000000"),
    yaxis_title="Spend ($)",
    xaxis_title="Service"
)
st.plotly_chart(fig_services_bar, use_container_width=True)

# =========================
# Application Spend Heatmap
# =========================
st.header("Application Spend Heatmap")

# Create a proper heatmap with reshaped data
heatmap_data = df_app["Spend"].values.reshape(1, -1)

fig_heat = go.Figure(data=go.Heatmap(
    z=heatmap_data,
    x=df_app["Application"],
    y=["Spend"],
    colorscale=[[0, '#cce0ff'], [1, '#0052cc']],  # light blue to McKinsey blue
    showscale=True,
    text=[[f"${x:,.0f}" for x in df_app["Spend"]]],
    texttemplate="%{text}",
    textfont={"size": 12}
))
fig_heat.update_layout(
    title="Application Spend Heatmap",
    font=dict(family="Calibri", size=12, color="#000000"),
    xaxis_title="Application",
    yaxis_title=""
)
st.plotly_chart(fig_heat, use_container_width=True)

# =========================
# Summary Metrics
# =========================
st.header("Summary Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_csp_spend = df_csp["Spend"].sum()
    st.metric("Total CSP Spend", f"${total_csp_spend:,.0f}")

with col2:
    total_marketplace = df_csp["Marketplace"].sum()
    st.metric("Total Marketplace", f"${total_marketplace:,.0f}")

with col3:
    total_services = df_services["Spend"].sum()
    st.metric("Total Services", f"${total_services:,.0f}")

with col4:
    total_apps = df_app["Spend"].sum()
    st.metric("Total Applications", f"${total_apps:,.0f}")
