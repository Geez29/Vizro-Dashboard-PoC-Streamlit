import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# -----------------------------
# Load Excel or fallback to dummy data
# -----------------------------
EXCEL_FILE = "Cloud_Actual_Optimization.xlsx"

try:
    df_csp = pd.read_excel(EXCEL_FILE, sheet_name="CSP")
    df_services = pd.read_excel(EXCEL_FILE, sheet_name="Services")
    df_marketplace = pd.read_excel(EXCEL_FILE, sheet_name="Marketplace")
except FileNotFoundError:
    st.warning(f"{EXCEL_FILE} not found. Using dummy data.")

    df_csp = pd.DataFrame({
        "CSP": ["AWS", "Azure", "GCP"],
        "Spend": [120000, 95000, 78000]
    })

    df_services = pd.DataFrame({
        "CSP": ["AWS", "AWS", "Azure", "Azure", "GCP", "GCP"],
        "Service": ["Compute", "Storage", "Compute", "Database", "Compute", "Storage"],
        "Spend": [50000, 70000, 45000, 50000, 40000, 38000]
    })

    df_marketplace = pd.DataFrame({
        "CSP": ["AWS", "Azure", "GCP"],
        "MarketplaceSpend": [15000, 12000, 10000]
    })

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Cloud Cost Dashboard", layout="wide")
st.title("Cloud Cost Dashboard")

# -----------------------------
# CSP Selection
# -----------------------------
csp_list = df_csp["CSP"].unique()
selected_csp = st.selectbox("Select CSP", csp_list)

df_services_csp = df_services[df_services["CSP"] == selected_csp]
df_marketplace_csp = df_marketplace[df_marketplace["CSP"] == selected_csp]

# -----------------------------
# Waterfall Charts
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"{selected_csp} Services Spend Waterfall")
    fig_services = go.Figure(go.Waterfall(
        name="Services",
        orientation="v",
        measure=["relative"]*len(df_services_csp),
        x=df_services_csp["Service"],
        y=df_services_csp["Spend"],
        decreasing={"marker":{"color":"#1f77b4"}},
        increasing={"marker":{"color":"#1f77b4"}},
        totals={"marker":{"color":"#0b3d91"}}
    ))
    fig_services.update_layout(showlegend=False, font=dict(family="Calibri"))
    st.plotly_chart(fig_services, use_container_width=True)

with col2:
    st.subheader(f"{selected_csp} Marketplace Spend Waterfall")
    fig_market = go.Figure(go.Waterfall(
        name="Marketplace",
        orientation="v",
        measure=["relative"]*len(df_marketplace_csp),
        x=df_marketplace_csp["CSP"],
        y=df_marketplace_csp["MarketplaceSpend"],
        decreasing={"marker":{"color":"#1f77b4"}},
        increasing={"marker":{"color":"#1f77b4"}},
        totals={"marker":{"color":"#0b3d91"}}
    ))
    fig_market.update_layout(showlegend=False, font=dict(family="Calibri"))
    st.plotly_chart(fig_market, use_container_width=True)

# -----------------------------
# Heatmap
# -----------------------------
st.subheader(f"{selected_csp} Services Spend Heatmap")
heatmap_data = df_services_csp.pivot_table(index="Service", values="Spend", aggfunc=np.sum)
fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale="Blues",
    text=heatmap_data.values,
    texttemplate="%{text:$,.0f}"
))
fig_heatmap.update_layout(font=dict(family="Calibri"))
st.plotly_chart(fig_heatmap, use_container_width=True)

# -----------------------------
# CSP Summary Table
# -----------------------------
st.subheader("CSP Spend Summary")
st.dataframe(df_csp)
