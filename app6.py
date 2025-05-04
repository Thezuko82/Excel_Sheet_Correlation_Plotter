import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io

# Page config
st.set_page_config(page_title="GitHub Excel Visualizer", layout="wide")
st.title("📊 Excel File Plotter from GitHub URL")

# 📌 GitHub raw URL to the Excel file (change this to your actual GitHub file)
GITHUB_EXCEL_URL = "Data.xlsx"

st.sidebar.markdown("🔗 **Using Excel file from GitHub repository**")
st.sidebar.code(GITHUB_EXCEL_URL)

# Step 1: Download Excel from GitHub
try:
    response = requests.get(GITHUB_EXCEL_URL)
    response.raise_for_status()
    excel_data = io.BytesIO(response.content)
    xls = pd.ExcelFile(excel_data)
except Exception as e:
    st.error(f"❌ Failed to load Excel file from GitHub: {e}")
    st.stop()

# Step 2: Load up to 6 sheets
sheet_names = xls.sheet_names[:6]
sheet_data = {name: xls.parse(name) for name in sheet_names}

# Step 3: Tabs per sheet
tab_list = st.tabs([f"📄 {name}" for name in sheet_names])

# Step 4: Interactive Visualization
for i, (sheet_name, df) in enumerate(sheet_data.items()):
    with tab_list[i]:
        st.header(f"📑 Sheet: {sheet_name}")
        
        if df.empty:
            st.warning("⚠️ Sheet is empty.")
            continue

        st.dataframe(df, height=250)

        # Column selections
        x_col = st.selectbox("Select X-axis", df.columns, key=f"x_{sheet_name}")
        y_col = st.selectbox("Select Y-axis", df.columns, key=f"y_{sheet_name}")
        z_col = st.selectbox("Select Z-axis (for 3D)", ["None"] + list(df.columns), key=f"z_{sheet_name}")

        graph_type = st.radio("Choose graph type", ["2D Scatter", "Line", "3D Scatter"], key=f"type_{sheet_name}")

        # Plotting logic
        try:
            if graph_type == "2D Scatter":
                fig = px.scatter(df, x=x_col, y=y_col, title=f"{sheet_name} - 2D Scatter")
            elif graph_type == "Line":
                fig = px.line(df, x=x_col, y=y_col, title=f"{sheet_name} - Line Plot")
            elif graph_type == "3D Scatter":
                if z_col == "None":
                    st.warning("Please select a Z-axis column for 3D plot.")
                    continue
                fig = px.scatter_3d(df, x=x_col, y=y_col, z=z_col, title=f"{sheet_name} - 3D Scatter")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Plotting error: {e}")
