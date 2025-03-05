import streamlit as st
import pandas as pd
import os
from io import BytesIO
import matplotlib.pyplot as plt


# Set up Streamlit page configuration
st.set_page_config(page_title="Data Uploader", page_icon="favicon.ico", layout="wide")
st.title("Data Uploader")
st.write("Easily convert CSV, Excel, JSON, Parquet, and TXT files with integrated data cleaning and visualization features!")

# File uploader widget
uploaded_files = st.file_uploader("Choose a file", type=["csv", "xlsx", "json", "parquet", "txt"], accept_multiple_files=True)

if uploaded_files:
    for idx, file in enumerate(uploaded_files):  # Ensure unique keys by using index
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Read file based on type
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        elif file_ext == ".json":
            df = pd.read_json(file)
        elif file_ext == ".parquet":
            df = pd.read_parquet(file)
        elif file_ext == ".txt":
            df = pd.read_csv(file, delimiter="\t")
        else:
            st.error(f"File type not supported: {file_ext}")
            continue
        
        # Display basic file information
        st.write(f"**{file.name}** ({file.size / (1024*1024):.2f} MB, {df.shape[0]} rows, {df.shape[1]} columns)")
        num_rows = st.slider(f"Rows to preview", 5, len(df), 5, key=f"rows_{idx}")
        st.dataframe(df.head(num_rows))
        
        # Data summary
        st.subheader("Data Summary")
        st.write(df.describe())
        st.write(f"Missing Values per Column:")
        st.write(df.isnull().sum())
        
        # Data cleaning options
        if st.checkbox(f"Clean {file.name}", key=f"clean_{idx}"):
            if st.button(f"Remove Duplicates", key=f"dup_{idx}"):
                df.drop_duplicates(inplace=True)
                st.write("Duplicates removed.")
            if st.button(f"Fill Missing Values", key=f"fill_{idx}"):
                df.fillna(df.mean(), inplace=True)
                st.write("Missing values filled.")
        
        # Column selection (Ensuring unique keys)
        df = df[st.multiselect("Select columns", df.columns, default=df.columns, key=f"cols_{idx}")]
        
        # Data visualization
        if st.checkbox(f"Show Visualizations", key=f"viz_{idx}"):
            chart_type = st.selectbox("Choose chart type", ["Bar Chart", "Line Chart", "Scatter Plot"], key=f"chart_{idx}")
            numeric_cols = df.select_dtypes(include="number").columns
            selected_cols = st.multiselect("Select columns for visualization", numeric_cols, default=numeric_cols[:2], key=f"numcols_{idx}")
            
            if chart_type == "Bar Chart":
                st.bar_chart(df[selected_cols])
            elif chart_type == "Line Chart":
                st.line_chart(df[selected_cols])
            elif chart_type == "Scatter Plot" and len(selected_cols) >= 2:
                st.scatter_chart(df[selected_cols])
        
        # File conversion options
        conversion_type = st.radio("Convert to", ["CSV", "Excel", "JSON", "Parquet"], key=f"convert_{idx}")
        if st.button(f"Convert {file.name}", key=f"btn_{idx}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name, mime_type = file.name.replace(file_ext, ".csv"), "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name, mime_type = file.name.replace(file_ext, ".xlsx"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            elif conversion_type == "JSON":
                df.to_json(buffer, orient="records")
                file_name, mime_type = file.name.replace(file_ext, ".json"), "application/json"
            elif conversion_type == "Parquet":
                df.to_parquet(buffer)
                file_name, mime_type = file.name.replace(file_ext, ".parquet"), "application/octet-stream"
            
            st.download_button(f"Download {file.name}", buffer.getvalue(), file_name, mime_type)
    
    st.success("Files processed successfully!")

# Footer with author info
st.markdown('<div style="text-align: center; padding-top: 20px;"><h6>Made with ❤️ by <a href="https://github.com/aqsaaQaazi" target="_blank" style="text-decoration: none; color: inherit;">Aqsaa Qaazi</a></h6></div>', unsafe_allow_html=True)
