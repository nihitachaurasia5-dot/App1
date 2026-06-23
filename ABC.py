import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Excel Forecasting Checker", layout="wide")

st.title("📊 Excel Data Forecasting Analyzer")

st.write(
    """
    Upload an Excel file. The app will:
    - Detect numerical columns
    - Create histograms
    - Calculate Mean and Median
    - Check if Mean and Median are close
    - Suggest whether the data may be suitable for forecasting
    """
)

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:

    try:
        df = pd.read_excel(uploaded_file)

        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        numeric_cols = df.select_dtypes(include=np.number).columns

        if len(numeric_cols) == 0:
            st.error("No numerical columns found.")
        else:

            results = []

            for col in numeric_cols:

                st.markdown("---")
                st.subheader(f"Column: {col}")

                data = df[col].dropna()

                mean_val = data.mean()
                median_val = data.median()

                difference_percent = (
                    abs(mean_val - median_val)
                    / max(abs(mean_val), 1)
                ) * 100

                if difference_percent <= 10:
                    forecast_message = "✅ Mean and Median are close. Data may be suitable for forecasting."
                else:
                    forecast_message = "⚠ Mean and Median differ significantly. Forecasting may require additional analysis."

                results.append({
                    "Column": col,
                    "Mean": round(mean_val, 4),
                    "Median": round(median_val, 4),
                    "Difference %": round(difference_percent, 2),
                    "Forecast Suitability": forecast_message
                })

                st.write(f"**Mean:** {mean_val:.4f}")
                st.write(f"**Median:** {median_val:.4f}")
                st.write(f"**Difference %:** {difference_percent:.2f}%")
                st.write(forecast_message)

                fig, ax = plt.subplots(figsize=(8,4))
                ax.hist(data, bins=15)
                ax.set_title(f"Histogram - {col}")
                ax.set_xlabel(col)
                ax.set_ylabel("Frequency")

                st.pyplot(fig)

            st.markdown("---")
            st.subheader("Summary")

            summary_df = pd.DataFrame(results)
            st.dataframe(summary_df)

    except Exception as e:
        st.error(f"Error reading file: {e}")
