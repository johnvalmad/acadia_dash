import streamlit as st
import pandas as pd
import altair as alt
import psycopg2
from psycopg2 import sql
import warnings

# DATABASE CONNECTION
# ============================================
@st.cache_resource
def init_connection():
    try:
        conn = psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            port=st.secrets["postgres"]["port"],
            dbname=st.secrets["postgres"]["database"],
            user=st.secrets["postgres"]["username"],
            password=st.secrets["postgres"]["password"],
            sslmode="require"  # Supabase exige SSL
        )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar ao banco: {e}")
        st.stop()

# DATA FETCHING FUNCTION 
# ============================================
def get_sales_data():
    try:
        conn = psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            port=st.secrets["postgres"]["port"],
            dbname=st.secrets["postgres"]["database"],
            user=st.secrets["postgres"]["username"],
            password=st.secrets["postgres"]["password"],
            sslmode="require"
        )

        query = """
            SELECT 
                ds.*,
                p.profile_description,
                d.department_description,
                s.segment_description
            FROM dept_sales ds
            LEFT JOIN profile p ON ds.profile_id = p.profile_id
            LEFT JOIN department d ON ds.department_id = d.department_id
            LEFT JOIN segment s ON ds.segment_id = s.segment_id
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"🔴 Data query failed: {str(e)}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

# MAIN DASHBOARD LOGIC

def main():
    st.set_page_config(
        page_title="📊 Sales Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# LOGO
# ============================================
    st.markdown(
        """
        <style>
        .logo-container {
            position: fixed;
            top: 0px; 
            left: 0px;
            z-index: 100;
            padding: 5px;
            background-color: white;
        }
        </style>
        <div class="logo-container">
        """,
        unsafe_allow_html=True
    )

    # Load and display the image using Streamlit
    st.image("logo.png", width=170)
    st.markdown("</div>", unsafe_allow_html=True)


    st.title("Sales Performance Dashboard")

    # Load data
    df = get_sales_data()

    if df.empty:
        st.warning("⚠️ No data loaded - check database connection or table content.")
        return

    # ========= SIDEBAR FILTERS =========
    with st.sidebar:
        st.header("🔍 Filters")

        # Year filter
        years = sorted(df["year"].dropna().unique())
        year_options = ["All"] + years
        selected_year = st.selectbox("Select Year", year_options, index=0)

        # Department filter
        departments = sorted(df["department_description"].dropna().unique())
        department_options = ["All"] + departments
        selected_departments = st.multiselect("Select Departments", department_options, default=["All"])

        # Segment filter
        segments = sorted(df["segment_description"].dropna().unique())
        segment_options = ["All"] + segments
        selected_segments = st.multiselect("Select Segments", segment_options, default=["All"])

    # ========= APPLY FILTERS =========
    filtered_df = df.copy()

    if selected_year != "All":
        filtered_df = filtered_df[filtered_df["year"] == selected_year]

    if "All" not in selected_departments:
        filtered_df = filtered_df[filtered_df["department_description"].isin(selected_departments)]

    if "All" not in selected_segments:
        filtered_df = filtered_df[filtered_df["segment_description"].isin(selected_segments)]

    # ========= METRIC CARDS =========
    st.subheader("How is the business perfoming?")

    st.markdown("""
    <style>
    .metric-card {
        background-color: #fffff;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 10px 10px 10px rgba(0,0,0,0.06);
        text-align: center;
        height: 100%;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-title {
        font-size: 1rem;
        color: #6c757d;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 600;
        color: #212529;
    }
    .metric-subvalue {
        font-size: 1.3rem;
        color: #198754;
        margin-top: 0.3rem;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_sales = filtered_df["sales"].sum()
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">💰 Total Sales</div>
                <div class="metric-value">${total_sales:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        total_customers = filtered_df["customers"].sum()
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🧍 Total Customers</div>
                <div class="metric-value">{total_customers:,}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        with st.container():
            top_profile = (
                filtered_df.groupby("profile_description")["sales"]
                .sum()
                .sort_values(ascending=False)
            )
            if not top_profile.empty:
                top_name = top_profile.index[0]
                top_value = top_profile.iloc[0]
                top_display = f"{top_name}<br><span class='metric-subvalue'>${top_value:,.2f}</span>"
            else:
                top_display = "No data"

            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">🏆 Top Profile</div>
                    <div class="metric-value-smaller">{top_display}</div>
                </div>
            """, unsafe_allow_html=True)

    with col4:
        sales_by_year = filtered_df.groupby("year")["sales"].sum().sort_index()
        sales_2023 = sales_by_year.get(2023, 0)
        sales_2022 = sales_by_year.get(2022, 0)

        if sales_2022 > 0:
            yoy_delta = ((sales_2023 - sales_2022) / sales_2022) * 100
            delta_display = f"{yoy_delta:.2f}%"
        else:
            delta_display = "N/A"

        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">% YoY Analysis</div>
                <div class="metric-value">${sales_2023:,.0f}</div>
                <div class="metric-subvalue">{delta_display}</div>
            </div>
        """, unsafe_allow_html=True)

    st.divider() 

    st.subheader("Understanding our numbers breakdown")

    if filtered_df.empty:
        st.info("No data available for this chart.")
    else:
        stacked_df = (
            filtered_df.groupby(["segment_description", "department_description"])
            .agg(total_sales=("sales", "sum"))
            .reset_index()
        )

        unique_departments = stacked_df["department_description"].unique().tolist()

        custom_green_palette = [
            "#00441b", "#006d2c", "#238b45", "#41ab5d",
            "#74c476", "#a1d99b", "#c7e9c0", "#e5f5e0"
        ]

        color_palette = custom_green_palette[:len(unique_departments)]

        chart = alt.Chart(stacked_df).mark_bar().encode(
            x=alt.X("segment_description:N", title="Segment", axis=alt.Axis(labelAngle=-30)),
            y=alt.Y("total_sales:Q", title="Total Sales ($)", stack="zero"),
            color=alt.Color("department_description:N",
                title="Department",
                scale=alt.Scale(
                    domain=unique_departments,
                    range=color_palette
                )
            ),
            tooltip=[
                alt.Tooltip("segment_description", title="Segment"),
                alt.Tooltip("department_description", title="Department"),
                alt.Tooltip("total_sales", title="Sales", format=",.2f")
            ]
        ).properties(
            height=500,
            width=800,
            title="Segment Sales Stacked by Department"
        )

        st.altair_chart(chart, use_container_width=True)

    # ========== COMBINED HEATMAP + FUNNEL VIEW ==========
    st.markdown("---")
    spacer_col, col1, col2 = st.columns([0.2, 1, 1])

    with col1:
        st.markdown(
            "<h3 style='text-align: center; margin-bottom: 20px;'>Revenue Heatmap</h3>",
            unsafe_allow_html=True
        )

        heatmap_df = (
            filtered_df.groupby(["department_description", "segment_description"])
            .agg(total_sales=("sales", "sum"))
            .reset_index()
        )

        heatmap_chart = alt.Chart(heatmap_df).mark_rect().encode(
            x=alt.X("segment_description:N", title="Segment"),
            y=alt.Y("department_description:N", title="Department"),
            color=alt.Color("total_sales:Q", scale=alt.Scale(scheme="greens"), title="Sales"),
            tooltip=[
                alt.Tooltip("department_description", title="Department"),
                alt.Tooltip("segment_description", title="Segment"),
                alt.Tooltip("total_sales", title="Sales", format=",.2f")
            ]
        ).properties(
            width=500,
            height=450
        )

        st.altair_chart(heatmap_chart, use_container_width=False)

    with col2:
        st.markdown(
            "<h3 style='text-align: center; margin-bottom: 20px;'>Our solid customer numbers</h3>",
            unsafe_allow_html=True
        )

        funnel_df = (
            filtered_df.groupby("segment_description")
            .agg(total_customers=("customers", "sum"))
            .reset_index()
            .sort_values(by="total_customers", ascending=False)
        )

        funnel_df["width"] = funnel_df["total_customers"] / funnel_df["total_customers"].max()
        funnel_df["x_start"] = (1 - funnel_df["width"]) / 2
        funnel_df["x_end"] = funnel_df["x_start"] + funnel_df["width"]

        col_spacer, col_funnel = st.columns([0.2, 1.8])

        with col_funnel:
            funnel = alt.Chart(funnel_df).mark_bar().encode(
                y=alt.Y("segment_description:N", 
                        sort=alt.EncodingSortField(field="total_customers", order="descending"), 
                        title="Segment"),
                x=alt.X("x_start:Q", axis=None, title=""),
                x2=alt.X2("x_end:Q"),
                color=alt.Color("segment_description:N", legend=None, scale=alt.Scale(scheme="blues")),
                tooltip=[
                    alt.Tooltip("segment_description", title="Segment"),
                    alt.Tooltip("total_customers", title="Customers", format=",")
                ]
            ).properties(
                width=500,
                height=450
            ).configure_view(
                stroke=None
            )

            st.altair_chart(funnel, use_container_width=False)

    # Footer
    st.markdown("---")
    st.caption(f"Developed by Joao Almada @ Data automatically updated in: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}")

if __name__ == "__main__":
    main()
