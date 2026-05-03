import sqlite3
import pandas as pd
import streamlit as st


# Load Data
df = pd.read_csv("c_data.csv")


# Create in-memory SQL database
conn = sqlite3.connect(':memory:', check_same_thread=False)
df.to_sql('restaurants', conn, index=False, if_exists='replace')


st.title("Uber Eats Bangalore Restaurant Intelligence & Decision Support Systems")
st.text(""" Uber Eats operates a large-scale restaurant marketplace where business success depends on factors such as location strategy, pricing, cuisine mix, customer ratings, and platform features like online ordering and table booking.""")


# 1. Get unique values for filters using SQL
locations = pd.read_sql("SELECT DISTINCT location FROM restaurants", conn)['location'].tolist()
selected_loc = st.sidebar.selectbox("Select Location", options=["All"] + locations, )

# 2. Build the Strict SQL Query
query = "SELECT * FROM restaurants"
if selected_loc != "All":
    query = f"SELECT * FROM restaurants WHERE location = '{selected_loc}'"

# 3. Display Results
filtered_df = pd.read_sql(query, conn)
st.dataframe(filtered_df)

# 2. Restaurant Type Filter (Multiselect)
rest_type = st.sidebar.multiselect(
    "Select Restaurant Type",
    options=df['rest_type'].unique(),
    default=df['rest_type'].unique()
)

#sql query

if rest_type:
    if len(rest_type) == 1:
        selected_types = f"('{rest_type[0]}')"
    else:
        selected_types = tuple(rest_type)

    query = f"""
    SELECT *
    FROM restaurants
    WHERE rest_type IN {selected_types}
    """
filtered_df=pd.read_sql(query,conn)
st.dataframe(filtered_df)




# 3. Rating Filter (Slider)
min_rating, max_rating = st.sidebar.slider(
    "Select Rating Range",
    min_value=0.0,
    max_value=5.0,
    value=(0.0, 5.0), # Default range
    step=0.1
)


query = f"""
SELECT *
FROM restaurants
WHERE rate BETWEEN {min_rating} AND {max_rating}
"""
filtered_df=pd.read_sql(query,conn)
st.dataframe(filtered_df)








# 4. Online Order Toggle (Radio)
online_order = st.sidebar.radio(
    "Online Order Available?",
    options=['All', 'yes', 'no']
)

query = "SELECT * FROM restaurants WHERE 1=1"

if online_order != "All":
    query += f" AND online_order = '{online_order}'"
df=pd.read_sql(query,conn)   
st.dataframe(df)