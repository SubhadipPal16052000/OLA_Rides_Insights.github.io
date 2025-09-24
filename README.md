# 🚕 OLA Ride Analytics Dashboard

An interactive web application to explore and analyse OLA ride data, built with Streamlit, PostgreSQL, and Power BI.

---

## 📌 Project Overview

This project provides:
- Real-time KPIs and interactive visualisations of OLA ride data
- SQL query runner to execute business intelligence queries
- Embedded Power BI dashboard for advanced analytics
- Easy-to-use filters for vehicle types, booking status, and more
- Cloud deployment using Streamlit Community Cloud and Supabase PostgreSQL

---

## 🛠️ Technologies Used

- Python 3.x
- Streamlit for interactive UI
- Pandas and NumPy for data manipulation
- Plotly for visualisations
- SQLAlchemy for PostgreSQL integration
- Supabase as a cloud-hosted PostgreSQL database
- Power BI for embedded dashboards

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or above
- Git installed
- Supabase account and created a PostgreSQL database

### Installation

1. Clone the repository:  git clone https://github.com/SubhadipPal16052000/ola-ride-analytics.git
cd ola-ride-analytics

2. Install dependencies:
                    streamlit>=1.28.0
                    pandas>=2.0.0
                    plotly>=5.17.0
                    sqlalchemy>=2.0.0
                    psycopg2-binary>=2.9.0
                    numpy>=1.24.0

4. Set up your Supabase database and get connection credentials.

5. Configure your database credentials as Streamlit secrets:

   Create `.streamlit/secrets.toml` with:
   [database]
  db_host = "my_supabase_host"
  db_name = "postgres"
  db_user = "my_supabase_user"
  db_password = "my_supabase_password"
  db_port = "5432"

6. Run data transfer script (optional, if data is not in Supabase):    python transfer_data.py

### Running the App

To run locally:  streamlit run OLA_app.py

---

## 🌐 Deployment

This app is deployed on Streamlit Community Cloud. Link to live demo:

[https://my-app-url.streamlit.app](https://olaridesinsightsappio-d8ucuzfr9lduufcuuzgw3w.streamlit.app/)

---

## ✅ Features we'll Get:

  ☁️ Cloud database connectivity with Supabase

  📊 Interactive KPIs (rides, revenue, ratings, success rate)

  🎨 Advanced visualisations with filtering capabilities

  🔍 SQL query interface with business intelligence queries

  📈 Large Power BI dashboard for comprehensive analytics

  📱 Mobile-responsive design for all devices

  🚀 Professional presentation ready for portfolios

---

## 📈 Performance Metrics:
  
  1. Sub-3 second loading times

  2. 99.9% uptime with cloud infrastructure

  3. Global accessibility from anywhere

  4. Multi-user support with concurrent access

## 👨‍💻 About the Developer

**Subhadip Pal**  
Data Analyst (Intern)  
Email: subhadip.pal2k@gmail.com  
Phone: +91 9749788063

---

## 📄 License

This project is licensed under the MIT License.

---

## 🔗 Acknowledgements

- Streamlit Community
- Supabase Documentation
- Power BI Embedded Analytics

---


