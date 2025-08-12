import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(layout="wide")

    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title("DataViz App ")
    st.markdown("Visualise your data in simple manner to get an understanding on the key data elements present in your data in no time. Just upload your data file in CSV, XLS, XLSX (Limit 200MB per file) ")

    st.sidebar.header("Upload")
    uploaded_file = st.sidebar.file_uploader("Upload your XLS or CSV file", type=["csv", "xls", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return

        st.header("Data Summary")
        st.write(df.head())

        st.header("Data Visualisation")
        st.write(df.info())

        st.sidebar.header("Chart Configuration")
        chart_type = st.sidebar.selectbox("Select Chart Type", ["Bar", "Line", "Scatter", "Pie"])

        columns = df.columns.tolist()

        if chart_type == "Pie":
            names_col = st.sidebar.selectbox("Select Column for Labels", columns)
            values_col = st.sidebar.selectbox("Select Column for Values", columns)
            fig = px.pie(df, names=names_col, values=values_col, title=f"{chart_type} Chart")
        else:
            x_axis = st.sidebar.selectbox("Select X-axis", columns)
            y_axis = st.sidebar.selectbox("Select Y-axis", columns)
            fig = getattr(px, chart_type.lower())(df, x=x_axis, y=y_axis, title=f"{chart_type} Chart")

        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
