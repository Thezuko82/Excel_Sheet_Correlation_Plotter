import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page setup
st.set_page_config(page_title="Excel Sheet Correlation Plotter", layout="wide")
st.title("📊 Multi-Sheet Excel Visualizer")

# Path to the Excel file already in the directory
excel_file = ""C:\Users\rohit\Downloads\SCILAB\Data-Copy.xlsx""  # 🔁 Replace this with your file name

# Check file existence
if not os.path.exists(excel_file):
    st.error(f"❌ Excel file '{excel_file}' not found in the directory.")
    st.stop()

# Load sheets
xls = pd.ExcelFile(excel_file)
sheet_names = xls.sheet_names[:6]  # Load first 6 sheets only
sheet_data = {name: xls.parse(name) for name in sheet_names}

# Create tabs for each sheet
tab_list = st.tabs([f"Sheet: {name}" for name in sheet_names])

# Plotting section for each sheet
for i, (name, df) in enumerate(sheet_data.items()):
    with tab_list[i]:
        st.header(f"📄 Sheet Analysis: {name}")

        if df.empty:
            st.warning(f"The sheet '{name}' is empty.")
            continue

        # Show sheet data
        st.dataframe(df, height=250)

        # Column selections
        col1 = st.selectbox(f"Select X-axis for {name}", df.columns, key=f"x_{name}")
        col2 = st.selectbox(f"Select Y-axis for {name}", df.columns, key=f"y_{name}")
        col3 = st.selectbox(f"Select Z-axis (optional for 3D)", ["None"] + list(df.columns), key=f"z_{name}")

        graph_type = st.radio(f"Choose graph type", ["2D Scatter", "Line", "3D Scatter"], key=f"gtype_{name}")

        # Plot based on type
        try:
            if graph_type == "2D Scatter":
                fig = px.scatter(df, x=col1, y=col2, title=f"{name} - 2D Scatter Plot")
            elif graph_type == "Line":
                fig = px.line(df, x=col1, y=col2, title=f"{name} - Line Plot")
            elif graph_type == "3D Scatter":
                if col3 == "None":
                    st.warning("Please select a Z-axis column for 3D Scatter.")
                    continue
                fig = px.scatter_3d(df, x=col1, y=col2, z=col3, title=f"{name} - 3D Scatter Plot")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"⚠️ Plotting Error: {e}")
