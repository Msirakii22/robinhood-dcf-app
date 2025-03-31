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
