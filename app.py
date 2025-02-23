import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS with valid color name
st.markdown(
    """
    <style>
    .stApp {
        background-color: yellow;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Datasweeper Sterling Integrator By Aurangzaib Mughal!")
st.write(
    "Transform your files between CSV and Excel formats with built-in data "
    "cleaning and visualization for Quarter 3 project!"
)

# File uploader section
uploaded_files = st.file_uploader(
    "Upload your files (accepts CSV or Excel)",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # File preview
        st.write(f"### Preview of {file.name}")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader(f"Data Cleaning Options for {file.name}")

        if st.checkbox(
            f"Clean data for {file.name}", key=f"clean_{file.name}"
        ):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    f"Remove duplicates from {file.name}",
                    key=f"dup_{file.name}"
                ):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed successfully!")

            with col2:
                if st.button(
                    f"Fill missing values for {file.name}",
                    key=f"fill_{file.name}"
                ):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(
                        df[numeric_cols].mean()
                    )
                    st.write("✅ Missing values filled successfully!")

        # Column selection
        st.subheader(f"Select Columns to Keep for {file.name}")
        columns = st.multiselect(
            f"Select columns for {file.name}",
            df.columns,
            default=df.columns
        )
        df = df[columns]

        # Data visualization
        st.subheader(f"Data Visualization for {file.name}")
        if st.checkbox(
            f"Show visualization for {file.name}", key=f"viz_{file.name}"
        ):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion options
        st.subheader(f"Conversion Options for {file.name}")
        conversion_type = st.radio(
            f"Convert {file.name} to:",
            ["CSV", "Excel"],
            key=f"conv_{file.name}"
        )

        if st.button(f"Convert {file.name}", key=f"convert_{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:  # "Excel"
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = (
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )

            buffer.seek(0)

            st.download_button(
                label=f"Download {file_name}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

    st.success("All files processed successfully!")
