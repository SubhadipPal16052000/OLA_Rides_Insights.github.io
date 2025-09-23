import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus # Required for password encoding

# --- DATABASE CONNECTION (FIXED) ---
# This function now correctly handles special characters in the password.
@st.cache_resource
def init_connection():
    db_credentials = st.secrets["database"]
    
    # URL-encode the password to handle special characters like '@'
    encoded_password = quote_plus(db_credentials['db_password'])
    
    db_url = (
        f"postgresql+psycopg2://{db_credentials['db_user']}:{encoded_password}" # Use the encoded password
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
st.write("An interactive dashboard to explore OLA ride data, from raw SQL queries to embedded Power BI visuals.  **MADE BY SUBHADIP_PAL**")


# --- SIDEBAR FOR FILTERS & NAVIGATION ---
st.sidebar.header("Filters & Navigation")

app_mode = st.sidebar.radio(
    "Choose a section",
    ["Interactive Dashboard", "SQL Query Runner"]
)

# --- SQL QUERY RUNNER SECTION (FIXED) ---
if app_mode == "SQL Query Runner":
    st.header("SQL Query Runner")
    st.write("Select a predefined query to explore the data.")

    # Dictionary of predefined SQL queries (Now using the correct, full queries)
    sql_queries = {
        "Retrieve all successful bookings": 
            'SELECT * FROM "cleaned_OLAride_data" WHERE "Booking_Status" = \'Success\';',
        "Find the average ride distance for each vehicle type": 
            'SELECT "Vehicle_Type", AVG("Ride_Distance") AS average_distance FROM "cleaned_OLAride_data" GROUP BY "Vehicle_Type";',
        "Get the total number of cancelled rides by customers": 
            'SELECT SUM("Is_Canceled_by_Customer") AS total_customer_cancellations FROM "cleaned_OLAride_data";',
        "List the top 5 customers by booked rides": 
            'SELECT "Customer_ID", COUNT(*) AS number_of_rides FROM "cleaned_OLAride_data" GROUP BY "Customer_ID" ORDER BY number_of_rides DESC LIMIT 5;',
        "Get rides cancelled by drivers due to personal/car issues": 
            'SELECT COUNT(*) AS cancellation_count FROM "cleaned_OLAride_data" WHERE "Driver_Cancellation_Reason" = \'Personal & Car related issue\';',
        "Find min/max driver ratings for Prime Sedan": 
            'SELECT MAX("Driver_Ratings") AS max_rating, MIN("Driver_Ratings") AS min_rating FROM "cleaned_OLAride_data" WHERE "Vehicle_Type" = \'Prime Sedan\';',
        "Retrieve all rides paid with UPI": 
            'SELECT * FROM "cleaned_OLAride_data" WHERE "Payment_Method" = \'UPI\';',
        "Find average customer rating per vehicle type": 
            'SELECT "Vehicle_Type", AVG("Customer_Rating") AS average_customer_rating FROM "cleaned_OLAride_data" GROUP BY "Vehicle_Type";',
        "Calculate total value of completed rides": 
            'SELECT SUM("Booking_Value") AS total_completed_value FROM "cleaned_OLAride_data" WHERE "Booking_Status" = \'COMPLETED\';',
        "List all incomplete rides with reason": 
            'SELECT "Booking_ID", "Incomplete_Rides_Reason" FROM "cleaned_OLAride_data" WHERE "IsIncomplete" = 1;'
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

    @st.cache_data
    def load_data():
        with engine.connect() as connection:
            df = pd.read_sql('SELECT * FROM "cleaned_OLAride_data"', connection)
        return df

    data = load_data()

    st.sidebar.subheader("Dashboard Filters")
    vehicle_types = st.sidebar.multiselect(
        "Select Vehicle Type(s)",
        options=data["Vehicle_Type"].unique(),
        default=data["Vehicle_Type"].unique()
    )
    booking_statuses = st.sidebar.multiselect(
        "Select Booking Status(es)",
        options=data["Booking_Status"].unique(),
        default=data["Booking_Status"].unique()
    )

    st.sidebar.markdown("---")
    st.sidebar.header("About")
    st.sidebar.markdown("""
    **Name:** SUBHADIP PAL
    **Profession:** DATA ANALYST(INTERN)
    **Email:** [subhadip.pal2k@gmail.com](mailto:subhadip.pal2k@gmail.com)
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

    placeholder_url = "https://app.powerbi.com/view?r=eyJrIjoiMY_REPORT_ID_HEREiLCJ0IjoiYOUR_TENANT_ID_HERE"
    
    if POWER_BI_EMBED_URL != placeholder_url:
        st.components.v1.iframe(POWER_BI_EMBED_URL, height=800, width=836)
    else:
        st.warning("Please replace the placeholder URL in the script with your Power BI embed URL to see the dashboard.")
        st.info("To get the URL, open your report in Power BI Service, go to File > Embed report > Publish to web (public), and copy the link from the embed code.")
