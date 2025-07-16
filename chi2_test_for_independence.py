import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency

st.title("Chi-Square Test of Independence")

# Upload CSV
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data Preview")
    st.write(df.head())

    # Filter only categorical columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    if len(cat_cols) < 2:
        st.warning("Need at least two categorical columns for the test.")
    else:
        # Select columns for Chi-Square Test of Independence
        col1 = st.selectbox("Select first categorical column", cat_cols)
        col2 = st.selectbox("Select second categorical column", cat_cols)

        if col1 and col2:
            st.write(f"### Contingency Table: {col1} vs {col2}")
            contingency_table = pd.crosstab(df[col1], df[col2])
            st.dataframe(contingency_table)

            # Perform Chi-Square Test of Independence
            stat, p, dof, expected = chi2_contingency(contingency_table)
            st.write(f"**Chi² Statistic** = {stat:.4f}")
            st.write(f"**Degrees of Freedom** = {dof}")
            st.write(f"**p-value** = {p:.4f}")
            # st.write("Expected  values")
            # st.dataframe(expected)

            if p < 0.05:
                st.success("Reject H₀ → Variables are associated")
            else:
                st.info("Fail to Reject H₀ → Variables are independent")
