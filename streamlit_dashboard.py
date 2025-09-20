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
        
        # Try different possible sheet names
        xl_file = pd.ExcelFile(excel_file)
        sheet_names = xl_file.sheet_names
        
        # Find the correct sheet names (case-insensitive)
        csp_sheet = None
        services_sheet = None
        app_sheet = None
        
        for sheet in sheet_names:
            if sheet.lower() in ['csp', 'csps', 'cloud service provider', 'providers']:
                csp_sheet = sheet
            elif sheet.lower() in ['service', 'services']:
                services_sheet = sheet
            elif sheet.lower() in ['app', 'application', 'applications']:
                app_sheet = sheet
        
        # Load data with found sheet names
        if csp_sheet:
            df_csp = pd.read_excel(excel_file, sheet_name=csp_sheet)
        else:
            raise Exception(f"CSP sheet not found. Available sheets: {sheet_names}")
            
        if services_sheet:
            df_services = pd.read_excel(excel_file, sheet_name=services_sheet)
        else:
            raise Exception(f"Services sheet not found. Available sheets: {sheet_names}")
            
        if app_sheet:
            df_app = pd.read_excel(excel_file, sheet_name=app_sheet)
        else:
            raise Exception(f"Application sheet not found. Available sheets: {sheet_names}")
        
        return df_csp, df_services, df_app, None, sheet_names
        
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
        return df_csp, df_services, df_app, error_msg, []

# Load the data
df_csp, df_services, df_app, error_msg, sheet_names = load_data()

# =========================
# Page Title
# =========================
st.title("☁️ Cloud Cost Dashboard")

# Show warning if using dummy data
if error_msg:
    st.error(error_msg)
    if sheet_names:
        st.info(f"Available sheets in Excel file: {', '.join(sheet_names)}")
    st.info("Using dummy data for demonstration")

# =========================
# Summary Metrics at Top
# =========================
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

st.divider()

# =========================
# CSP Section
# =========================
st.header("🏢 Cloud Service Provider Overview")

# =========================
# WATERFALL CHARTS (Consolidated All CSP View)
# =========================
st.subheader("📊 Consolidated CSP Waterfall Charts")

col1, col2 = st.columns(2)

with col1:
    st.write("**All CSP Services Spend - Waterfall**")
    
    # Create waterfall data for services
    services_values = df_csp["Spend"].tolist()
    services_labels = df_csp["CSP"].tolist()
    
    # Create proper waterfall chart
    fig_services_waterfall = go.Figure()
    
    # Add waterfall trace
    fig_services_waterfall.add_trace(go.Waterfall(
        name="Services Spend",
        orientation="v",
        measure=["relative"] * len(services_labels),
        x=services_labels,
        textposition="outside",
        text=[f"${x:,.0f}" for x in services_values],
        y=services_values,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#0052cc"}},
        decreasing={"marker": {"color": "#cc0000"}},
        totals={"marker": {"color": "#00cc52"}}
    ))
    
    fig_services_waterfall.update_layout(
        title="Services Spend Waterfall (All CSPs)",
        font=dict(family="Arial", size=12),
        yaxis_title="Spend ($)",
        xaxis_title="Cloud Service Provider",
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_services_waterfall, use_container_width=True)

with col2:
    st.write("**All CSP Marketplace Spend - Waterfall**")
    
    # Create waterfall data for marketplace
    marketplace_values = df_csp["Marketplace"].tolist()
    marketplace_labels = df_csp["CSP"].tolist()
    
    fig_marketplace_waterfall = go.Figure()
    
    # Add waterfall trace
    fig_marketplace_waterfall.add_trace(go.Waterfall(
        name="Marketplace Spend",
        orientation="v",
        measure=["relative"] * len(marketplace_labels),
        x=marketplace_labels,
        textposition="outside",
        text=[f"${x:,.0f}" for x in marketplace_values],
        y=marketplace_values,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#3399ff"}},
        decreasing={"marker": {"color": "#cc0000"}},
        totals={"marker": {"color": "#00cc52"}}
    ))
    
    fig_marketplace_waterfall.update_layout(
        title="Marketplace Spend Waterfall (All CSPs)",
        font=dict(family="Arial", size=12),
        yaxis_title="Spend ($)",
        xaxis_title="Cloud Service Provider",
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_marketplace_waterfall, use_container_width=True)

st.divider()

# =========================
# Individual CSP Bar Charts
# =========================
st.subheader("📈 Individual CSP Breakdown")

# Bar Charts side-by-side
col1, col2 = st.columns(2)

with col1:
    st.write("**Services Spend by Individual CSP**")
    fig_services = go.Figure(go.Bar(
        x=df_csp["CSP"],
        y=df_csp["Spend"],
        text=[f"${x:,.0f}" for x in df_csp["Spend"]],
        textposition="auto",
        marker_color="#0052cc",
        name="Services Spend"
    ))
    fig_services.update_layout(
        title="Services Spend by CSP",
        font=dict(family="Arial", size=12),
        yaxis_title="Spend ($)",
        xaxis_title="Cloud Service Provider",
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_services, use_container_width=True)

with col2:
    st.write("**Marketplace Spend by Individual CSP**")
    fig_market = go.Figure(go.Bar(
        x=df_csp["CSP"],
        y=df_csp["Marketplace"],
        text=[f"${x:,.0f}" for x in df_csp["Marketplace"]],
        textposition="auto",
        marker_color="#3399ff",
        name="Marketplace Spend"
    ))
    fig_market.update_layout(
        title="Marketplace Spend by CSP",
        font=dict(family="Arial", size=12),
        yaxis_title="Spend ($)",
        xaxis_title="Cloud Service Provider",
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_market, use_container_width=True)

st.divider()

# =========================
# Services Section
# =========================
st.header("🔧 Services Overview")

# Create two columns for different views
col1, col2 = st.columns(2)

with col1:
    # Bar chart
    fig_services_bar = go.Figure(go.Bar(
        x=df_services["Service"],
        y=df_services["Spend"],
        text=[f"${x:,.0f}" for x in df_services["Spend"]],
        textposition="auto",
        marker_color="#0052cc"
    ))
    fig_services_bar.update_layout(
        title="Spend by Service",
        font=dict(family="Arial", size=12),
        yaxis_title="Spend ($)",
        xaxis_title="Service",
        height=400
    )
    st.plotly_chart(fig_services_bar, use_container_width=True)

with col2:
    # Pie chart
    fig_services_pie = go.Figure(go.Pie(
        labels=df_services["Service"],
        values=df_services["Spend"],
        textinfo='label+percent+value',
        texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}',
        marker=dict(colors=['#0052cc', '#3399ff', '#66b3ff'])
    ))
    fig_services_pie.update_layout(
        title="Service Spend Distribution",
        font=dict(family="Arial", size=12),
        height=400
    )
    st.plotly_chart(fig_services_pie, use_container_width=True)

st.divider()

# =========================
# Application Section
# =========================
st.header("📱 Application Overview")

col1, col2 = st.columns(2)

with col1:
    # Application bar chart
    fig_app_bar = go.Figure(go.Bar(
        x=df_app["Application"],
        y=df_app["Spend"],
        text=[f"${x:,.0f}" for x in df_app["Spend"]],
        textposition="auto",
        marker_color="#0052cc"
    ))
    fig_app_bar.update_layout(
        title="Spend by Application",
        font=dict(family="Arial", size=12),
        yaxis_title="Spend ($)",
        xaxis_title="Application",
        height=400
    )
    st.plotly_chart(fig_app_bar, use_container_width=True)

with col2:
    # Application heatmap (alternative visualization)
    heatmap_data = df_app["Spend"].values.reshape(1, -1)
    
    fig_heat = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=df_app["Application"],
        y=["Application Spend"],
        colorscale=[[0, '#cce0ff'], [1, '#0052cc']],
        showscale=True,
        text=[[f"${x:,.0f}" for x in df_app["Spend"]]],
        texttemplate="%{text}",
        textfont={"size": 12}
    ))
    fig_heat.update_layout(
        title="Application Spend Heatmap",
        font=dict(family="Arial", size=12),
        xaxis_title="Application",
        yaxis_title="",
        height=400
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# =========================
# Data Tables Section
# =========================
st.header("📊 Data Tables")

tab1, tab2, tab3 = st.tabs(["CSP Data", "Services Data", "Application Data"])

with tab1:
    st.subheader("Cloud Service Provider Spending")
    # Add percentage calculations
    df_csp_display = df_csp.copy()
    df_csp_display['Services %'] = (df_csp_display['Spend'] / df_csp_display['Spend'].sum() * 100).round(1)
    df_csp_display['Marketplace %'] = (df_csp_display['Marketplace'] / df_csp_display['Marketplace'].sum() * 100).round(1)
    st.dataframe(df_csp_display, use_container_width=True)

with tab2:
    st.subheader("Services Spending")
    df_services_display = df_services.copy()
    df_services_display['Percentage'] = (df_services_display['Spend'] / df_services_display['Spend'].sum() * 100).round(1)
    st.dataframe(df_services_display, use_container_width=True)

with tab3:
    st.subheader("Application Spending")
    df_app_display = df_app.copy()
    df_app_display['Percentage'] = (df_app_display['Spend'] / df_app_display['Spend'].sum() * 100).round(1)
    st.dataframe(df_app_display, use_container_width=True)

# =========================
# Footer
# =========================
st.divider()
st.caption("💡 Dashboard automatically detects Excel sheet names and handles missing data gracefully.")
