import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Guide", layout="wide")

st.title("📘 Dashboard Guide")

st.markdown("""
Welcome to the Sales Dashboard for Acadia Team! This guide walks you through each section of the dashboard to help you navigate and interpret the visuals effectively.
""")

# ---------------- Key Metrics ----------------
st.subheader("Key Metrics Section")

with st.expander("Total Sales"):
    st.markdown("""
    This is the total number of sales of Acadia, not considering any filtering on the data. Please select the filters to understand how sales are performing in the selected cohort.
    """)

with st.expander("Total Customers"):
    st.markdown("""
    This is the total number of unique customers of Acadia, not considering any filtering on the data. Please apply the filters to analyze customer numbers in the selected cohort.
    """)

with st.expander("Top Profile"):
    st.markdown("""
    The top profile shows the most profitable customer type based on sales. Use this insight to explore strategies for nurturing high-value customers or turning them into brand advocates.
    """)

with st.expander("Year over Year Analysis"):
    st.markdown("""
    This metric highlights changes in sales from the previous year to the current one. A helpful tool to evaluate strategic shifts or seasonal performance variations.
    """)

# ---------------- Breakdown Charts ----------------
st.subheader("Breakdown Charts")

with st.expander("Segment Sales Stacked by Department"):
    st.markdown("""
    This chart shows how revenue is distributed across different customer segments and departments. It's useful for spotting trends or gaps in performance by department or segment.
    """)

with st.expander("Revenue Heatmap"):
    st.markdown("""
    A more visual alternative to the stacked chart, this heatmap emphasizes discrepancies between segment and department combinations. Great for quickly identifying outliers.
    """)

with st.expander("Customer Funnel Dropdown"):
    st.markdown("""
    This funnel chart illustrates customer volume by segment. While traditionally used to represent lifecycle stages, here it's used to communicate segment strength in terms of customer base size.
    """)

# ---------------- Filters & Interactions ----------------
st.subheader("Filters, Buttons & Tooltips")

with st.expander("Sidebar Filters"):
    st.markdown("""
    Located on the left side of the dashboard, the sidebar allows you to filter the data by year, department, and segment. These filters help narrow down the insights to a specific cohort or business slice you want to analyze.
    """)

with st.expander("Buttons & Interactivity"):
    st.markdown("""
    The dashboard components respond instantly to your filter selections. Some charts may also include interactive features like dropdowns, dynamic resizing, and scrollable views depending on your input.
    """)

with st.expander("Tooltips"):
    st.markdown("""
    Hover over any point or bar on the charts to reveal detailed tooltips. These show precise data values, including segment names, sales amounts, or customer counts—helping you better interpret visual trends.
    """)

# ---------------- Conclusion Section ----------------
st.subheader("Actionable Insights page")

with st.expander("Actionable insights"):
    st.markdown("""
    The page summarizes insights we can observe from the dashboard data. Use this section to align the team's understanding of trends, identify key takeaways, and explore strategic opportunities.
    """)

# ---------------- Footer ----------------
st.markdown("---")
st.caption(f"Developed by Joao Almada · Data automatically updated on: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}")
