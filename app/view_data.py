import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import errorcode

@st.cache_data(max_entries=5)
def load_data():
    data = pd.read_csv("data/data.csv")
    # Select the first five columns
    return data.iloc[:, :6]

# @st.cache_data(max_entries=5)
# def load_data(query: str):
#     # Function to get data from MySQL
#     config = {
#         'host':'mysql-server-azure.mysql.database.azure.com',
#         'user':'AzureAdminNebuhan',
#         'password':'Fg3*d12786',
#         'database':'etisalat_project'
#     }

#     # Construct connection string

#     try:
#         sql_connection = mysql.connector.connect(**config)
#         print("Connection established")
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Something is wrong with the user name or password")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("Database does not exist")
#         else:
#             print(err)

#     data = pd.read_sql(
#         query,
#         sql_connection
#     )

#     return data

st.header("🛢️ Raw Data as in Database")

IPV4_IPV6_df = load_data()

st.dataframe(IPV4_IPV6_df)

