
import mysql.connector
import pandas as pd
import streamlit as st
from tabulate import tabulate
# Establish connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root12345",
    database="project"
)
mycursor=conn.cursor()
# Function to run queries for your 10 business questions
def run_query(query):
    return pd.read_sql(query, conn)



# Displaying in Streamlit as a structured table
st.title("📊Business Q&A")

# qustion number : 1

st.subheader("""1. Which Bangalore locations have the highest average restaurant ratings?
**Business Value:** Identifies premium-performing areas suitable for brand positioning and new partner onboarding.""")

#SQL QUERY

mycursor.execute("""select location,avg(rate) from uber_eats_res_data
where rate is not null
group by location
order by avg(rate) desc limit 10""")
out=mycursor.fetchall()
df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])
st.dataframe(df.head(10), hide_index=True)

#ANSWER

st.markdown(""" ***Based on my analysis, 
1.Lavelle Road (4.19), 
2.Koramangala 5th Block (4.15), 
3.Sankey Road (4.10) 
 have the highest average restaurant ratings in Bangalore.
 these areas very suitable for brand positioning and new partner onboarding.***""")


#Qustion number 2:

st.subheader(""" 2. Which locations are over-saturated with restaurants?
**Business Value:** Helps avoid overcrowded markets and guides smarter expansion decisions.""")

#SQL QUERY

mycursor.execute("""select location,count(*)total from uber_eats_res_data
group by location
order by count(name) desc limit 5""")
out=mycursor.fetchall()
df = pd.DataFrame(out,columns=[i[0]for i in mycursor.description])
st.dataframe(df, hide_index=True)

#ANSWER:

st.markdown(""" ***koramangala 5th bolck , this area has a 1782no of resturant
btm has a 1454no of resturant
indranagar has a 1345 no of resturants
hsr has a 1161 no of resturants
jayanagar has a 1037 no of resturants.***""")


# Qustion number 3: 

st.subheader("""3.Does online ordering improve restaurant ratings?
**Business Value:** Evaluates the ROI of Uber Eats online ordering feature for partners.
             """)

#SQL QUERY

mycursor.execute("""select online_order,avg(rate), count(*) from uber_eats_res_data
group by online_order """)
out=mycursor.fetchall()
df=pd.DataFrame(out,columns=[i[0]for i in mycursor.description])
st.dataframe(df,hide_index=True)

#ANSWER:

st.markdown("""***online order does not improving restaurant rating.
#it shows the online orders alone does not significantly improve restaurant rating
#Therefore, Uber Eats may need to focus on improving delivery experience, order accuracy, and service quality to increase partner ROI.***""")


#Qustion number 4:

st.subheader("""4. Does table booking correlate with higher customer ratings?
**Business Value:** Measures the effectiveness of table booking as a premium feature.""")

#SQL QUERY

mycursor.execute("""select book_table, avg(rate),count(*)as total from uber_eats_res_data
group by book_table""")
out=mycursor.fetchall()
df = pd.DataFrame(out,columns=[i[0]for i in mycursor.description])
st.dataframe(df,hide_index=True)

#ANSWER:

st.markdown("""***COMBINE OF ONLINE ORDER AND TABLE BOOKING OPTIONS SIGNIFICANTLY IMPROVING THE RATING OF THE RESTAURENT
“This indicates a strong positive correlation between table booking and ratings.
Customers likely prefer convenience and reduced waiting time.***""")


#Qustion number 5:

st.subheader("""5.What price range delivers the best customer satisfaction?
**Business Value:** Helps define the optimal pricing segment for partner success.""")

#SQL QUERY

mycursor.execute("""select `approx_cost(for two people)`,avg(rate),count(
*)name from uber_eats_res_data
group by `approx_cost(for two people)`
order by avg(rate) desc""")
out=mycursor.fetchall()
df = pd.DataFrame(out,columns=[i[0]for i in mycursor.description])
st.dataframe(df,hide_index=True)

#ANSWER:

st.markdown("""***Mid to high price range restaurants (₹800–₹2000) deliver the best customer satisfaction, 
as they maintain consistently high ratings with a significant number of restaurants. While very high-priced restaurants show slightly higher ratings, 
the sample size is small, making mid-range the most reliable segment.***""")



#Qustion number 6:
 
st.subheader("""6.How do low, mid, and premium-priced restaurants perform in terms of ratings?
**Business Value:** Supports pricing-based market segmentation strategies.""")

#SQL QUERY

mycursor.execute("""
select 
price_catagory,
avg(rate) as avg_rating,
count(*) as total
from(
select
     rate,
     case
        when `approx_cost(for two people)`<=500 then 'low'
        when `approx_cost(for two people)` between 501 and 1500 then 'mid'
        else 'premium'
        end as price_catagory from uber_eats_res_data
)t
group by price_catagory
order by avg_rating desc

""")

out=mycursor.fetchall()
df=pd.DataFrame(out,columns=[i[0]for i in mycursor.description])
st.dataframe(df,hide_index=True)

#ANSWER:

st.markdown("""***Premium-priced restaurants have the highest average ratings (4.23), 
  followed by mid-range restaurants (3.96) and low-priced restaurants (3.79). 
  This indicates that customer satisfaction tends to increase with price, 
  likely due to better quality, service, and overall experience.***

      “Premium restaurants provide superior experience, while mid-range offers a balance between affordability and quality.”

***“However, this reflects correlation, not causation. Higher ratings may also be influenced by factors like cuisine, service quality, and location.”***""")

#Qustion number 7:

st.subheader("""7.Which cuisines are most common in Bangalore? 
**Business Value:** Reveals market demand and cuisine saturation levels.""")


#SQL Query

query=("select cuisines, count(*) from uber_eats_res_data group by cuisines")
df = pd.read_sql(query,conn)

df['cuisines']=df['cuisines'].str.split(',')
df=df.explode('cuisines')

df['cuisines'] = df['cuisines'].str.strip()           
df['cuisines'] = df['cuisines'].str.replace('_','')  
df['cuisines'] = df['cuisines'].str.lower()  

df['cuisines']=df['cuisines'].str.strip()
result=df['cuisines'].value_counts().reset_index()
result.columns=['cuisines','total']
st.dataframe(result.head(10))

# ANSWER:

st.markdown("""***North Indian and Chinese cuisines are the most common in Bangalore.
This indicates high customer demand but also high market saturation.***""")

#Qustion number 8:

st.subheader("""8.Which cuisines receive the highest average ratings?
**Business Value:** Identifies high-quality cuisine categories suitable for promotion.""")

#SQL Query

query=("select cuisines,rate from uber_eats_res_data")

df=pd.read_sql(query,conn)
df=df.dropna(subset=['cuisines','rate'])

df['cuisines']=df['cuisines'].str.split(',')

df=df.explode('cuisines')

df['cuisines']=df['cuisines'].str.strip()
df['cuisines']=df['cuisines'].str.replace('_','')
df['cuisines']=df['cuisines'].str.lower()

result=df.groupby('cuisines')['rate'].mean().reset_index()
counts=df['cuisines'].value_counts()
valid=counts[counts>50].index
filtered_df=df[df['cuisines'].isin(valid)]

result=filtered_df.groupby('cuisines')['rate'].mean().reset_index()
result=result.sort_values(by='rate',ascending=False)
st.dataframe(result.head(10))

# ANSWER:

st.markdown("""***After filtering cuisines with sufficient data, 
I found that Malaysian, Modern Indian, and Mediterranean cuisines have the highest average ratings.
This indicates that these cuisines deliver better customer satisfaction and belong to the premium segment.
These categories can be targeted for promotions or high-end restaurant investments.***""")

#Qustion number 9:

st.subheader("""9.Which cuisines perform well despite having fewer restaurants?
**Business Value:** Highlights niche opportunities for differentiation.""")

#SQL QUERY

query = ("select cuisines,rate from uber_eats_res_data")
df=pd.read_sql(query,conn)

df=df.dropna(subset=['cuisines','rate'])

df['cuisines']=df['cuisines'].str.split(',')

df=df.explode('cuisines')

df['cuisines']=df['cuisines'].str.strip()
df['cuisines']=df['cuisines'].str.replace('_','')
df['cuisines']=df['cuisines'].str.lower()

res1=df.groupby('cuisines').agg(total_restaurents=('cuisines','count'),
avg_rating=('rate','mean')).reset_index()

niche=res1[(res1['total_restaurents']<20)&(res1['avg_rating']>4.2)]

niche=niche.sort_values(by='avg_rating',ascending=False)
st.dataframe(niche)

#ANSWER:

st.markdown("""***These cuisines represent niche opportunities where demand quality is high but supply is limited. 
Expanding these categories can help platforms differentiate and attract premium customers.”
Cuisines like Cantonese, African, and Belgian perform exceptionally well despite low availability,
indicating strong niche demand and expansion opportunities.***""")


#Qustion number 10:

st.subheader("""10.What is the relationship between restaurant cost and rating?
**Business Value:** Determines whether higher pricing translates to better customer perception.""")

#SQL QUERY

mycursor.execute(""" select 
case
when `approx_cost(for two people)` <= 500 then 'low'
when `approx_cost(for two people)` between 501 and 1500 then 'mid'
else 'premium' 
end as price_category,
count(*) as total_restaurents,
avg(rate) as avg_rating
from uber_eats_res_data 
group by price_category
order by avg_rating desc; 
""")
out=mycursor.fetchall()
df=pd.DataFrame(out,columns=[i[0]for i in mycursor.description])
st.dataframe(df,hide_index=True)

#ANSWER:
st.markdown("""***There is a mild positive relationship between cost and rating, 
but high pricing does not guarantee significantly better customer satisfaction.***""")












