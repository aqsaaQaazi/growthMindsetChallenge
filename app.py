import streamlit as st #installed package
import pandas as pd #installed package
import os
from io import BytesIO


# app setup
st.set_page_config(
    page_title="Data Uploader",
    page_icon=":crown:",
    layout="wide"
)

st.title("Data Uploader")
st.write("Easily convert CSV and Excel files with integrated data cleaning and visualization features!")

# file uploader
uploaded_files = st.file_uploader("Choose a file (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)


# conditions
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:st.error("file type not supported: {file_ext}")
        
        # display information about the file 
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024} KB")
        st.write(f"**File Type:** {file_ext}")
        st.write(f"**Number of rows:** {df.shape[0]}")
        st.write(f"**Number of columns:** {df.shape[1]}")

        # display the first few rows of the dataframe
        st.write("**preview head of the dataframe:**")
        st.dataframe(df.head())
        
        # data cleaning options
        st.write("**Data Cleaning Options:**")
        if st.checkbox(f"clean {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write(f"**Duplicates removed from {file.name}**")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write(f"**Missing values filled for {file.name}**")
                    
        # specific columns to keep or convert
        st.subheader("Select columns to convert")
        columns = st.multiselect(f"Select columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # visualisations
        st.subheader("Data Visualisations")
        if st.checkbox(f"show {file.name} visualisations"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

        # convert CSV to excel
        st.subheader("Cnversion options")
        conversion_type = st.radio(f"Select conversion type for {file.name}", ["CSV to Excel", "Excel to CSV"], key = file.name)
        if st.button(f"Convert {file.name} to {conversion_type}"):
           buffer = BytesIO()
           if conversion_type == "Excel to CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, '.csv')
                mime_type = "text/csv"
           elif conversion_type == "CSV to Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, '.xlsx')
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

           buffer.seek(0)


        #    download 
           st.download_button(label=f"Download {conversion_type} {file.name}", data=buffer, file_name=file_name, mime=mime_type)
                    
st.success("**your files have been procesed successfully **")
