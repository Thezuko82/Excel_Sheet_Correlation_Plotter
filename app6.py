import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Streamlit page config
st.set_page_config(page_title="Excel Sheet Correlation Plotter", layout="wide")
st.title("📊 Multi-Sheet Excel Plot Dashboard")

# Step 1: Choose file source
file_option = st.sidebar.radio("📂 Choose Excel File Source", ["Use Built-in File", "Upload Your Own File"])

# Step 2: Load the Excel file
excel_file = None

if file_option == "Use Built-in File":
    default_file = "C:\Users\rohit\Downloads\SCILAB\Data.xlsx"  # 📝 Replace with actual file name
    if os.path.exists(default_file):
        excel_file = default_file
        st.sidebar.success(f"✅ Using built-in file: {default_file}")
    else:
        st.sidebar.error(f"❌ File '{default_file}' not found.")
        st.stop()

elif file_option == "Upload Your Own File":
    uploaded_file = st.sidebar.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"])
    if uploaded_file:
        excel_file = uploaded_file
        st.sidebar.success("✅ File uploaded successfully.")
    else:
        st.sidebar.info("⬆️ Please upload an Excel file to proceed.")
        st.stop()

# Step 3: Load sheets and process
xls = pd.ExcelFile(excel_file)
sheet_names = xls.sheet_names[:6]  # Consider only first 6 sheets
sheet_data = {name: xls.parse(name) for name in sheet_names}

# Step 4: Tabs per sheet
tab_list = st.tabs([f"📄 {name}" for name in sheet_names])

for i, (name, df) in enumerate(sheet_data.items()):
    with tab_list[i]:
        st.header(f"🧾 Analysis for Sheet: {name}")

        if df.empty:
            st.warning(f"⚠️ The sheet '{name}' is empty or unreadable.")
            continue

        st.dataframe(df, height=250)

        # Column selections
        col1 = st.selectbox(f"Select X-axis column", df.columns, key=f"x_{name}")
        col2 = st.selectbox(f"Select Y-axis column", df.columns, key=f"y_{name}")
        col3 = st.selectbox(f"Select Z-axis column (optional for 3D)", ["None"] + list(df.columns), key=f"z_{name}")

        graph_type = st.radio(f"📈 Choose plot type", ["2D Scatter", "Line", "3D Scatter"], key=f"gtype_{name}")

        # Plot logic
        try:
            if graph_type == "2D Scatter":
                fig = px.scatter(df, x=col1, y=col2, title=f"{name} - 2D Scatter Plot")
            elif graph_type == "Line":
                fig = px.line(df, x=col1, y=col2, title=f"{name} - Line Plot")
            elif graph_type == "3D Scatter":
                if col3 == "None":
                    st.warning("Please select a Z-axis column for 3D plot.")
                    continue
                fig = px.scatter_3d(df, x=col1, y=col2, z=col3, title=f"{name} - 3D Scatter Plot")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Plotting error: {e}")
