import streamlit as st
import pandas as pd

st.title("📊 Conclusion & Insights")

with st.expander("🗓 Overview of Year-over-Year Trends"):
    st.markdown("""
    - **Total Sales in 2023**: $4,395,106
    - **Total Sales in 2022**: $7,464,402  
    - 📉 **YoY Sales Decline**: **-41.12%**
    
    Action: This substantial drop suggests a need to reevaluate retention and conversion strategies, particularly around previously high-performing clusters (segment and department) cause our number of total customers did not change from 2022 to 2023
    """)

with st.expander("👥 Customer Behavior by Segment"):
    st.markdown("""
    We analyzed 5 customer profiles:
    - **Core Customers**
    - **Elite Customers**
    - **Infrequent Customers**
    - **New Customers**
    - **Power Shoppers**

    Notably:
    - **Core Customers** had the most significant decrease in sales year-over-year, which may warrant further investigation or re-engagement strategies.
    - **New Customers** was the small decrease, hinting that acquisition efforts are working the best on that vertical.
    - A deeper look shows **Elite Customers** are spending less but are still high-value.

    Action: Consider reinforcing loyalty to New and Elite Customer, as well as reactivation programs for Core Customers.
    """)

with st.expander("📌 Segment & Department Opportunities"):
    st.markdown("""
    - Some departments are still showing resilience or even slight growth in specific customer segments.
    - The heatmap highlights **low-performing departments** and **opportunities for bundled promotions** or campaigns targeting specific profiles.
    - Knick Knacks is showing a consistent and steep decline across all segments, which indicates a broader issue:
    - Review pricing or promotions for **Knick Knacks** cause they are showing a consistent decline across all segments
    - For **Women's Jeans and Misc**: Focus on Core and Power Shoppers, who traditionally drive strong volume but show signs of attrition.

    Action: We should use the heat map to understand more insights as above and **redirect sales efforts** and rebalance inventory.
    """)

with st.expander("🚀 Strategic Recommendations"):
    st.markdown("""
    - **Retarget Power Shoppers** through exclusive deals or loyalty programs.
    - **Boost Core and New Customer engagement** via onboarding campaigns.
    - Create **personalized promotions** tied to underperforming departments.
    - Evaluate **marketing spend efficiency**, especially on retention strategies.

    Action: Keep track of YoY performance in the coming months to validate strategy shifts.
    """)

st.info("✅ These insights target the dashboard audience and represent actionable suggestions for the business apply on the short-term, aiming testing and harversting better results on mid to long-term.")

# Footer
st.markdown("---")
st.caption(f" Developed by Joao Almada @ Data automatically updated in: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}")