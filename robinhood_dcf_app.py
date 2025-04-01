# robinhood_dcf_app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Load Excel data
df = pd.read_excel("RobinHood 81 Possible Stock Price Outcome.xlsx", sheet_name="Sheet1")


# Rename for clarity
df.rename(columns={
    'Rev Growth Switch': 'Revenue_Switch',
    'EBIT Margin Switch': 'EBIT_Switch',
    'Cost of Capital Switch': 'WACC_Switch',
    'TGR Switch': 'TGR_Switch',
    'Price Target': 'Price_Target'
}, inplace=True)

# Streamlit UI
st.title("📊 Robinhood DCF Heatmap App")
st.markdown("Use the dropdowns below to explore price target heatmaps based on WACC and TGR assumptions.")

# Select boxes for assumptions
wacc_option = st.selectbox("Select Cost of Capital (WACC) Scenario", sorted(df['WACC_Switch'].unique()))
tgr_option = st.selectbox("Select Terminal Growth Rate (TGR) Scenario", sorted(df['TGR_Switch'].unique()))

# Filter for selection
subset = df[(df['WACC_Switch'] == wacc_option) & (df['TGR_Switch'] == tgr_option)]
heatmap_data = subset.pivot(index='Revenue_Switch', columns='EBIT_Switch', values='Price_Target')

# Define color scale: red (low) → yellow (mid) → green (high)
colors = ["red", "yellow", "green"]
cmap = LinearSegmentedColormap.from_list("ryg_colormap", colors)

# Plot heatmap
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".2f",
    cmap=cmap,
    cbar_kws={"label": "Implied Share Price"},
    ax=ax
)
ax.set_title(f"Price Target Heatmap | WACC: {wacc_option}, TGR: {tgr_option}")
ax.set_xlabel("EBIT Margin Switch")
ax.set_ylabel("Revenue Growth Switch")

# Display in Streamlit
st.pyplot(fig)

# Show Assumption Tables
with st.expander("📋 View Scenario Assumptions"):
    st.markdown("### 📈 Total Revenue Growth Rate")
    st.dataframe(pd.DataFrame({
        "2025": ["28.04%", "55.17%", "19.83%"],
        "2026": ["26.96%", "51.66%", "18.37%"],
        "2027": ["24.11%", "46.30%", "17.33%"],
        "2028": ["19.63%", "38.86%", "14.77%"],
        "2029": ["16.66%", "20.62%", "8.61%"],
    }, index=["Base Case", "Best Case", "Worst Case"]))

    st.markdown("### 🧮 EBIT Margin")
    st.dataframe(pd.DataFrame({
        "2025": ["13.01%", "26.70%", "12.62%"],
        "2026": ["26.70%", "40.18%", "12.65%"],
        "2027": ["26.90%", "40.28%", "12.77%"],
        "2028": ["27.05%", "40.28%", "12.86%"],
        "2029": ["27.09%", "40.28%", "13.01%"],
    }, index=["Base Case", "Best Case", "Worst Case"]))

    st.markdown("### 🏦 Cost of Capital (WACC)")
    st.dataframe(pd.DataFrame({
        "2025": ["10.0%", "8.0%", "11.0%"],
        "2026": ["10.0%", "8.0%", "11.0%"],
        "2027": ["10.0%", "8.0%", "11.0%"],
        "2028": ["10.0%", "8.0%", "11.0%"],
        "2029": ["10.0%", "8.0%", "11.0%"],
    }, index=["Base Case", "Best Case", "Worst Case"]))

    st.markdown("### 🌱 Terminal Growth Rate (TGR)")
    st.dataframe(pd.DataFrame({
        "2025": ["2.0%", "3.0%", "1.0%"],
        "2026": ["2.0%", "3.0%", "1.0%"],
        "2027": ["2.0%", "3.0%", "1.0%"],
        "2028": ["2.0%", "3.0%", "1.0%"],
        "2029": ["2.0%", "3.0%", "1.0%"],
    }, index=["Base Case", "Best Case", "Worst Case"]))
