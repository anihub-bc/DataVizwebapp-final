import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="Data Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Apply custom CSS
local_css("style.css")

# --- Sidebar --- #
st.sidebar.header("Dashboard Controls")

# File uploader
uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV or Excel file", 
    type=['csv', 'xls', 'xlsx']
)

# --- Main Page --- #
st.title("📊 Data Analytics Dashboard")
st.write("Upload your data and start exploring!")

if uploaded_file is not None:
    try:
        # Read the file into a pandas DataFrame
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully!")

        # --- Data Preview --- #
        st.header("Data Preview")
        st.dataframe(df.head())



        # --- Charting --- #
        st.header("Data Visualization")

        # Get column names
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

        # Sidebar controls for charting
        st.sidebar.subheader("Chart Settings")
        chart_type = st.sidebar.selectbox("Select Chart Type", ["Bar Chart", "Scatter Plot", "Histogram", "Pie Chart"])

        if chart_type == "Bar Chart":
            st.sidebar.write("Select columns for the Bar Chart:")
            x_axis = st.sidebar.selectbox("X-Axis", categorical_columns)
            y_axis = st.sidebar.selectbox("Y-Axis", categorical_columns)
            if x_axis and y_axis:
                fig = px.bar(df, x=x_axis, y=y_axis, title=f'{y_axis} by {x_axis}', template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Scatter Plot":
            st.sidebar.write("Select columns for the Scatter Plot:")
            x_axis = st.sidebar.selectbox("X-Axis",  categorical_columns)
            y_axis = st.sidebar.selectbox("Y-Axis",  categorical_columns, index=1 if len(categorical_columns) > 1 else 0)
            if x_axis and y_axis:
                fig = px.scatter(df, x=x_axis, y=y_axis, title=f'{y_axis} vs {x_axis}', template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Histogram":
            st.sidebar.write("Select a column for the Histogram:")
            hist_col = st.sidebar.selectbox("Column", categorical_columns)
            if hist_col:
                fig = px.histogram(df, x=hist_col, title=f'Histogram of {hist_col}', template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Pie Chart":
            st.sidebar.write("Select columns for the Pie Chart:")
            names_col = st.sidebar.selectbox("Labels", categorical_columns)
            values_col = st.sidebar.selectbox("Values", categorical_columns)
            if names_col and values_col:
                fig = px.pie(df, names=names_col, values=values_col, title=f'Distribution of {values_col} by {names_col}', template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Awaiting for a file to be uploaded.") 
