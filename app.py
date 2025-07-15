import streamlit as st
import pandas as pd
import os
import sys
from PIL import Image  # For logo

# Add backend agents to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.business_summary_agent import summarize_business_insights
from agents.trend_analysis_agent import analyze_trends

# ---- Page Config ----
st.set_page_config(
    page_title="Geospatial Insight Agents",
    layout="wide",
    page_icon="🌐"
)

# ---- Load Logo ----
logo_path = os.path.join("data", "logo.png")
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.sidebar.image(logo, use_container_width=True)


# ---- Custom CSS Styling ----
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .sidebar .sidebar-content {
            background-color: #e9ecef;
        }
        h1 {
            color: #003366;
        }
        .stButton>button {
            background-color: #003366;
            color: white;
            border: none;
            padding: 0.5em 1em;
            border-radius: 5px;
        }
        .footer {
            margin-top: 30px;
            font-size: 0.8rem;
            color: #6c757d;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Title ----
st.title("📍 NYC Business Map - Geospatial Insight Agents")
st.markdown("### Powered by Geospatial Solutions LLC — AI-Powered Location Intelligence")

# ---- Load Data ----
DATA_PATH = os.path.join("data", "cleaned_nyc_businesses.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=["latitude", "longitude"])
    return df

df = load_data()

# ---- Sidebar Filters ----
st.sidebar.header("🔍 Filter Businesses")
unique_tracts = df['census_tract'].dropna().unique()
selected_tract = st.sidebar.selectbox("Select Census Tract", sorted(unique_tracts))

# ---- Filter Data ----
filtered_df = df[df['census_tract'] == selected_tract]

# ---- Map View ----
st.subheader("🗺️ Business Locations")
if not filtered_df.empty:
    map_df = filtered_df.rename(columns={"latitude": "lat", "longitude": "lon"})
    st.map(map_df)
else:
    st.warning("No business locations found for the selected tract.")

# ---- Business Table ----
st.subheader("📋 Business Details")
st.dataframe(filtered_df)

# ---- Insight Agent: Summary ----
st.subheader("🤖 Run Business Insight Agent")
if st.button("📝 Generate Insight Summary"):
    business_data = filtered_df.to_dict(orient="records")
    if not business_data:
        st.warning("No data to summarize.")
    else:
        with st.spinner("Running summary agent..."):
            summary = summarize_business_insights(business_data)
        st.markdown("### 🧠 Insight Summary")
        st.success(summary)

# ---- Insight Agent: Trends ----
st.subheader("📈 Business Trend Agent")
if st.button("📊 Generate Trend Analysis"):
    business_data = filtered_df.to_dict(orient="records")
    if not business_data:
        st.warning("No data to analyze.")
    else:
        with st.spinner("Running trend agent..."):
            trend_summary = analyze_trends(business_data)
        st.markdown("### 📊 Trend Summary")
        st.info(trend_summary)

# ---- Footer ----
st.markdown("<div class='footer'>© 2025 Geospatial Solutions LLC · All rights reserved</div>", unsafe_allow_html=True)
