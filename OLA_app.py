import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text


# --- DATABASE CONNECTION ---

@st.cache_resource
def init_connection():
    db_credentials = st.secrets["database"]
    db_url = (
        f"postgresql+psycopg2://{db_credentials['db_user']}:{db_credentials['db_password']}"
        f"@{db_credentials['db_host']}:{db_credentials['db_port']}/{db_credentials['db_name']}"
    )
    return create_engine(db_url)

engine = init_connection()

# --- POWER BI EMBED ---

POWER_BI_EMBED_URL = "https://app.powerbi.com/view?r=eyJrIjoiOWE3YWNjN2EtYmQwNC00ODhhLWIzNTMtY2E4ZDY3NWVkMDNlIiwidCI6IjlhOTkzMjZhLTliZjQtNGYwNS04MmFmLWVkNWMwOTZhMjQ1OSJ9"
# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="OLA Ride Analytics",
    page_icon="🚕",
    layout="wide"
)

# --- HEADER ---
st.title("🚕 OLA Ride Insights Analytics Dashboard")
st.write("An interactive dashboard to explore OLA ride data, from raw SQL queries to embedded Power BI visuals.   **MADE BY SUBHADIP_PAL**")


# --- SIDEBAR FOR FILTERS & NAVIGATION ---

st.sidebar.header("Filters & Navigation")

# Create tabs for different sections
app_mode = st.sidebar.radio(
    "Choose a section",
    ["Interactive Dashboard", "SQL Query Runner"]
)

# --- SQL QUERY RUNNER SECTION ---

if app_mode == "SQL Query Runner":
    st.header("SQL Query Runner")
    st.write("Select a predefined query to explore the data.")

    # Dictionary of predefined SQL queries
    sql_queries = {
        "Retrieve all successful bookings": 'select * from successful_bookings;',
        "Find the average ride distance for each vehicle type": 'select * from average_ride_distance_each_vehicle;',
        "Get the total number of cancelled rides by customers": 'select * from cancelled_rides_by_customers;',
        "List the top 5 customers by booked rides": 'select * from booked_the_highest_rides;',
        "Get the number of rides cancelled by drivers due to personal and car-related issues": 'select * from cancelled_by_drivers_due_to_p_c_issues;',
        "Find the maximum and minimum driver ratings for Prime Sedan bookings": 'select * from prime_sedan_min_max_rating;',
        "Show the total number of rides for each vehicle type": 'select * from average_ride_distance_each_vehicle;',
        "Retrieve all rides where payment was made using UPI": 'select * from upi_payment;',
        "Find the average customer rating per vehicle type": 'select * from per_vehicle_avg_customer_rating;',
        "Calculate the total booking value of rides completed successfully": 'select * from total_booking_successfully_complete;',
        "List all incomplete rides along with the reason": 'select * from incomplete_rides_with_reason;',
        "Number of rides per day": 'select * from number_of_rides_booking_per_hour_in_day;'
    }

    selected_query_name = st.selectbox("Select a query", options=list(sql_queries.keys()))

    query_text = st.text_area("SQL Query", value=sql_queries[selected_query_name], height=200)

    if st.button("Run Query"):
        with st.spinner("Executing query..."):
            try:
                with engine.connect() as connection:
                    df = pd.read_sql(text(query_text), connection)
                st.success("Query executed successfully!")
                st.dataframe(df)
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- DASHBOARD SECTION ---

elif app_mode == "Interactive Dashboard":
    st.header("Interactive Analytics")

    # Fetching the full dataset for filtering
    @st.cache_data
    def load_data():
        with engine.connect() as connection:
            df = pd.read_sql('SELECT * FROM "cleaned_OLAride_data"', connection)
        return df

    data = load_data()

    # --- INTERACTIVE FILTERS IN SIDEBAR ---
    st.sidebar.subheader("Dashboard Filters")
    # Vehicle Type Filter
    vehicle_types = st.sidebar.multiselect(
        "Select Vehicle Type(s)",
        options=data["Vehicle_Type"].unique(),
        default=data["Vehicle_Type"].unique()
    )

    # Booking Status Filter
    booking_statuses = st.sidebar.multiselect(
        "Select Booking Status(es)",
        options=data["Booking_Status"].unique(),
        default=data["Booking_Status"].unique()
    )

    # --- CONTACT INFORMATION IN SIDEBAR ---
    st.sidebar.markdown("---")
    st.sidebar.header("About")
    st.sidebar.markdown("""
    **Name:** SUBHADIP PAL
    **Profession:** DATA ANALYST(INTERN)
    **Email:** subhadip.pal2k@gmail.com
    **Contact:** +91 9749788063""")

    # Apply filters
    filtered_data = data[
        data["Vehicle_Type"].isin(vehicle_types) &
        data["Booking_Status"].isin(booking_statuses)
    ]

    st.write(f"Displaying data for selected filters. Total Records: {len(filtered_data)}")
    st.dataframe(filtered_data.head())


    st.header("OLA Rides Insights Power BI Dashboard")
    st.write("A complete Power BI dashboard is embedded below for a comprehensive analytics experience.")

    # Check if the placeholder URL has been replaced
    placeholder_url = "https://app.powerbi.com/view?r=eyJrIjoiMY_REPORT_ID_HEREiLCJ0IjoiYOUR_TENANT_ID_HERE"
    
    if POWER_BI_EMBED_URL != placeholder_url:
        # This will now be TRUE and your dashboard will display
        st.components.v1.iframe(POWER_BI_EMBED_URL, height=800, width =836)
    else:
        st.warning("Please replace the placeholder URL in the script with your Power BI embed URL to see the dashboard.")
        st.info("To get the URL, open your report in Power BI Service, go to File > Embed report > Publish to web (public), and copy the link from the embed code.")
    