import pandas as pd
import streamlit as st 


st.title("Order Data Integration & Custom Analytical Q&A")

st.subheader("1.How many unique restaurants are listed in this dataset?")

df=pd.read_csv("orders.csv")
st.dataframe(df)
# Calculate the unique count from your column
unique_restaurants = df['restaurant_name'].nunique()

# Display the exact quantity
st.metric(label="Total Unique Restaurants", value=unique_restaurants)

st.divider()

st.subheader("2.What is the restaurant_name for the order placed on 2026-01-08?")


st.dataframe(df[df['order_date'] == '2026-01-08']['restaurant_name'])

st.divider()

st.subheader("""3.List all order IDs where a discount was actually used (discount_used is "Yes")""")

discount_orders = df[df['discount_used']=='yes']['order_id']

st.write("order_id with discount used")
st.dataframe(discount_orders)

#st.dataframe([{"""Category,Count
#"Discount Used (Yes)":,"12,491"
#"No Discount (No)":,"12,509"
#"Total Orders":,"25,000"""}])

st.divider()

st.subheader("4.What is the total sum of order_value for all orders placed at Bawarchi Inn?")


bawarchi_sum = df[df['restaurant_name'] == 'bawarchi inn']['order_value'].sum()

# Display the result
st.metric(label="Total Sales: Bawarchi Inn", value=f"₹{bawarchi_sum:,.2f}")


st.divider()

st.subheader("5.Which restaurant had the highest single order_value in the entire list?")


max_order = df['order_value'].idxmax()

top_restaurant = df.loc[max_order, 'restaurant_name']
max_value = df.loc[max_order, 'order_value']

# Display as a metric or a highlight
st.write("### Highest Value Order")
st.metric(label=f"Highest Order: {top_restaurant.title()}", value=f"₹{max_value:,.2f}")

st.divider()




