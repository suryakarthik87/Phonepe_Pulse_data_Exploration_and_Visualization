#---------------------------------------------IMPORTING PACKAGES---------------------------------------------
import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import json
import requests
from PIL import Image
from babel.numbers import format_currency
import folium
import plotly.graph_objects as go
import os


#------------------------------------------------SQL CONNECTION-----------------------------------------------

mydb = psycopg2.connect(host = "localhost",
                        port = "5432",
                        user = "postgres",
                        password = "karthik",
                        database = "phonepe_pulse")

cursor = mydb.cursor()

#-----------------------------------------------DATAFRAME CREATION-------------------------------------------
#aggregated_insurance_dataframe

cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
agg_ins_table = cursor.fetchall()

Agg_ins_df = pd.DataFrame(agg_ins_table, columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))


#aggregated_transaction_dataframe

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
agg_trans_table = cursor.fetchall()

Agg_trans_df = pd.DataFrame(agg_trans_table, columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))


#aggregated_user_dataframe

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
agg_user_table = cursor.fetchall()

Agg_user_df = pd.DataFrame(agg_user_table, columns=("States","Years","Quarter","Brands","Transaction_count","Percentage"))


#map_insurance_dataframe

cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
map_ins_table = cursor.fetchall()

map_ins_df = pd.DataFrame(map_ins_table, columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))


#map_transaction_dataframe

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
map_trans_table = cursor.fetchall()

map_trans_df = pd.DataFrame(map_trans_table, columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))


#map_user_dataframe

cursor.execute("SELECT * FROM map_user")
mydb.commit()
map_user_table = cursor.fetchall()

map_user_df = pd.DataFrame(map_user_table, columns=("States","Years","Quarter","Districts","RegisteredUsers","AppOpens"))


#top_insurance_dataframe

cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
top_ins_table = cursor.fetchall()

top_ins_df = pd.DataFrame(top_ins_table, columns=("States","Years","Quarter","Pincode","Transaction_count","Transaction_amount"))


#top_transaction_dataframe

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
top_trans_table = cursor.fetchall()

top_trans_df = pd.DataFrame(top_trans_table, columns=("States","Years","Quarter","Pincode","Transaction_count","Transaction_amount"))


#top_user_dataframe

cursor.execute("SELECT * FROM top_user")
mydb.commit()
top_user_table = cursor.fetchall()

top_user_df = pd.DataFrame(top_user_table, columns=("States","Years","Quarter","Pincode","RegisteredUsers"))


#--------------------------------------------------FORMATING VALUES--------------------------------------------------------

def format_amount(amount):
    def format_indian_number(number):
        num_str = str(int(number))[::-1]  
        formatted_str = ""
        for i in range(len(num_str)):
            if i != 0 and (i == 3 or (i > 3 and (i - 1) % 2 == 0)):
                formatted_str += ','
            formatted_str += num_str[i]
        return formatted_str[::-1]

    if amount >= 1e7:
        amount_in_crore = amount / 1e7
        formatted_amount = format_currency(amount_in_crore, 'INR', locale='en_IN')
        return f"{formatted_amount} Cr"
    elif amount >= 1e5:
        amount_in_lakhs = amount / 1e5
        formatted_amount = format_currency(amount_in_lakhs, 'INR', locale='en_IN')
        return f"{formatted_amount} L"
    elif amount >= 1e3:
        amount_in_thousand = amount / 1e3
        formatted_amount = format_currency(amount_in_thousand, 'INR', locale='en_IN')
        return f"{formatted_amount} K"
    else:
        formatted_amount = format_currency(amount, 'INR', locale='en_IN')
        return format_indian_number(amount)

    
def format_number(number):
    num_str = str(int(number))[::-1]  
    formatted_str = ""
    for i in range(len(num_str)):
        if i != 0 and (i == 3 or (i > 3 and (i - 1) % 2 == 0)):
            formatted_str += ','
        formatted_str += num_str[i]
    return formatted_str[::-1]

#-----------------------------------------------------------GEO VIEW OF INDIAN STATES-----------------------------------------------------


url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
response = requests.get(url)
india_states_geojson = json.loads(response.content)


  
def make_choropleth(input_df):
    fig = px.choropleth(
    input_df,
    geojson=india_states_geojson,
    featureidkey='properties.ST_NM',
    locations='States',
    projection="mercator",
    hover_data=['Years','Transaction_amount'],
    color='Transaction_count',
    color_discrete_sequence=px.colors.sequential.Viridis,
    range_color=(input_df['Transaction_count'].min(), input_df['Transaction_count'].max())
    )

    fig.update_geos(fitbounds="locations", visible=False)
    
    fig.update_layout(
        width=1200,  
        height=1500, 
        margin={"r":0,"t":0,"l":0,"b":0},
        geo=dict(bgcolor='rgba(0,0,0,0)')

    )

    return fig

def ins_choropleth(input_df):
    fig = px.choropleth(
    input_df,
    geojson=india_states_geojson,
    featureidkey='properties.ST_NM',
    locations='States',
    projection="mercator",
    hover_data=['Years','Transaction_amount'],
    color='Transaction_count',
    color_discrete_sequence=px.colors.sequential.Viridis,
    range_color=(input_df['Transaction_count'].min(), input_df['Transaction_count'].max())
    )

    fig.update_geos(fitbounds="locations", visible=False)
        
    fig.update_layout(
        width=1200,  
        height=1500, 
        margin={"r":0,"t":0,"l":0,"b":0},
        geo=dict(bgcolor='rgba(0,0,0,0)')

    )
    return fig


def user_choropleth(input_df):
    fig = px.choropleth(
    input_df,
    geojson=india_states_geojson,
    featureidkey='properties.ST_NM',
    locations='States',
    projection="mercator",
    hover_data=['AppOpens','RegisteredUsers'],
    color='RegisteredUsers',
    color_discrete_sequence=px.colors.sequential.Viridis,
    range_color=(input_df['RegisteredUsers'].min(), input_df['RegisteredUsers'].max())
    )

    fig.update_geos(fitbounds="locations", visible=False)
    
    fig.update_layout(
        width=1200,  
        height=1500, 
        margin={"r":0,"t":0,"l":0,"b":0},
        geo=dict(bgcolor='rgba(0,0,0,0)')

    )
    return fig

#--------------------------------------------------------STREAMLIT USER INTERFACE----------------------------------------------------
st.set_page_config(page_title="PhonePe Pulse Dashboard",layout='wide')
st.markdown("<h1 style='text-align: center; font-size: 40px'> PHONEPE DATA VISUALIZATION AND EXPLORATION", unsafe_allow_html=True)   

#--------------------------------------------------------OPTION MENU----------------------------------------------------------------
with st.sidebar:

    select = option_menu(menu_title="DASHBOARD",
                         options=["ABOUT","DATA EXPLORATION","STATE-WISE-EXPLORE","DATA INSIGHTS"])

#---------------------------------------------------------OPTION: HOME-----------------------------------------------------------
if select == "ABOUT":
    
    col1,col2= st.columns(2)

    with col1:
        st.subheader("About Phonepe:")
        st.write("""PhonePe is a digital payments and financial services company that offers a mobile
                    payment platform and app. The app is based on India's Unified Payments Interface (UPI)
                    and allows users to make a variety of transactions.""")
        st.write("""PhonePe was founded in December 2015 by Sameer Nigam, Rahul Chari, and Burzin Engineer,
                     and the app went live in August 2016. The company's goal is to make digital payments
                     so easy, safe, and universally accepted that people no longer need to carry cash or cards.""")
        st.write("""PhonePe also offers digital payment solutions for businesses, such as accepting
                    payments at stores, processing online payments, and integrating the PhonePe Payment Gateway.""")
        
        st.subheader("About Phonepe Pulse:")
        st.write(""" PhonePe Pulse is a first-of-its-kind initiative by PhonePe that provides anonymized and
                     aggregated data on digital payment trends in India. This data is based on transactions
                     done through PhonePe. Researchers and analysts can use this data to understand how digital
                     payments are evolving in India.""")
                 
        st.write(""" PhonePe Pulse also refers to the website that showcases these data insights through informative
                     articles and visualizations.""")      
               
        
    with col2:
        st.video("D:\projects\phonepe\PhonePe Ad.mp4")

    col3,col4= st.columns(2)
    
    with col3:
                
        st.video("D:\projects\phonepe\PhonePe Pulse.mp4")

        st.subheader("BUSINESS SOLUTIONS:")
        st.write("""PhonePe can help you reach a wide user-base with targeted campaigns designed to meet your
                     business needs. Let relevant consumers sample your products and services in the
                     form of ‘reward coupons’ distributed on PhonePe, or advertise within the PhonePe app.""")
        st.image(Image.open(r"D:\projects\phonepe\business.png"),width=600)


    with col4:
        st.subheader("FEATURES:")
        st.write("Financial Transactions:")
        st.write("* Payments: Send and receive money using UPI (Unified Payments Interface) with your phone contacts.")
        st.write("* Bill Payments: Make payments for utilities, mobile recharges, DTH (Direct-to-Home) connections.")
        st.write("* In-Store Payments: Pay at stores using PhonePe QR codes. (This might require the store to support PhonePe)")
        st.write("* Wallet: Use PhonePe wallet for transactions (requires adding funds beforehand).")
        st.write("* Multiple Bank Accounts: Link and manage multiple bank accounts within the app.")
        st.write("Investments:")
        st.write("""* Stock Broking: Invest in stocks and mutual funds through PhonePe's subsidiary PhonePe Wealth Broking.
                    This includes features like intraday trading and pre-curated investment baskets""")
        st.write("* Gold: Buy digital gold directly through PhonePe.")
        st.write("Additional Features:")
        st.write("* Multiple Languages: The app is available in 11 Indian languages for wider accessibility.")
        st.write("* Security: PhonePe uses UPI for secure transactions and claims to be a safe and reliable platform.")
        st.write("* Cashbacks and Offers: Get discounts and cashback on transactions (subject to ongoing promotions).")
        st.write("* PhonePe Switch: This feature allows users to access various other apps like food ordering, travel booking, etc., without downloading them individually.")

        st.image(Image.open(r"D:\projects\phonepe\payment.png"),width=500)

#---------------------------------------------------------------OPTION: DATA EXPLORATION-------------------------------------------------------------
if select == "DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Transaction Data", "Insurance Data","User Data"])

#---------------------------------------------------------------TAB: TRANSACTION DATA--------------------------------------------------------------   
    
    with tab1:
      
            
        st.markdown("<h1 style='text-align: center; font-size: 30px'> All India Transaction Data", unsafe_allow_html=True)    

        col1, col2, col3,col4,col5,col6 = st.columns((0.7,0.8,1.5,0.9,0.9,0.9),gap="large")
        
        with col1:
            years = st.selectbox("#### Select Year:", options=Agg_trans_df["Years"].unique())
        with col2:
            quarters = st.selectbox("#### Select Quarter:", options=Agg_trans_df["Quarter"].unique())
        with col3:
            trans_type = st.selectbox("#### Select Transaction Type (Map View):", options=Agg_trans_df["Transaction_type"].unique())



        trans_selected_year = Agg_trans_df[(Agg_trans_df['Years'] == years) & 
                                        (Agg_trans_df['Quarter'] == quarters)]
        trans_selected_year_dist = map_trans_df[(map_trans_df['Years'] == years) & 
                                        (map_trans_df['Quarter'] == quarters)]        
        trans_selected_year_pin = top_trans_df[(top_trans_df['Years'] == years) & 
                                        (top_trans_df['Quarter'] == quarters)]
        
        if trans_selected_year.empty:
            st.error("#### No data available for the selected year and quarter.")
            
        else:
            trans_selected_year_grouped = trans_selected_year.groupby('States').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
            trans_selected_year_grouped['Serial'] = range(1, len(trans_selected_year_grouped) + 1)
            trans_selected_year_grouped = trans_selected_year_grouped.head(10)

            total_transactions = trans_selected_year['Transaction_count'].sum()
            total_payment_value = trans_selected_year['Transaction_amount'].sum()

            avg_transaction_value = total_payment_value / total_transactions
            total_transactions = format_number(total_transactions)
            col_map, col_data = st.columns((5, 1.65), gap='large')
            
            with col_map:          
            
                trans_selected_year_geo = Agg_trans_df[(Agg_trans_df['Years'] == years) & 
                                                (Agg_trans_df['Quarter'] == quarters) & (Agg_trans_df['Transaction_type'] == trans_type)]
                
                trans_selected_year_geo.loc[:, 'Transaction_amount'] = trans_selected_year_geo['Transaction_amount'].apply(format_amount)
                
                choropleth_map = make_choropleth(trans_selected_year_geo)
                st.plotly_chart(choropleth_map,use_container_width=True)

            with col_data:
                st.markdown("<h1 style=' font-size: 40px; color:#05C2DD'>Transactions</h1>", unsafe_allow_html=True)
                st.write(f'#### All PhonePe transactions (UPI + Cards + Wallets) (Q{quarters}) {years}')
                st.metric(label="", value=total_transactions,)
                st.write(f'#### Total Payment Value (Q{quarters}) {years}')
                st.metric(label='', value=format_amount(total_payment_value),)
                st.write(f'#### Average Payment Value (Q{quarters}) {years}')
                st.metric(label='', value=f"₹{avg_transaction_value:,.0f}")   
                trans_selected_year_grp = trans_selected_year.groupby('Transaction_type').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
                trans_selected_year_grp['Serial'] = range(1, len(trans_selected_year_grp) + 1)

                df = pd.DataFrame(trans_selected_year_grp[['Serial', 'Transaction_type', 'Transaction_amount']])
                df['Transaction_amount']=df['Transaction_amount'].apply(format_amount)
                st.markdown("***")
                st.markdown("<h1 style=' font-size: 30px; color:#05C2DD'>Categories</h1>", unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                
                for index, row in df.iterrows():
                    with col1:
                        st.markdown(f"<p style='font-size:17px;text-align: left'>{row['Transaction_type']}</p>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<p style='font-size:18px;text-align: right;font-weight:bold'>{row['Transaction_amount']}</p>", unsafe_allow_html=True)
                st.markdown("***")

                states_button_clicked = False
                districts_button_clicked = False
                postal_codes_button_clicked = False
                c11, c12, c13 = st.columns((1,1,1.5),gap="small")
                with c11:
                    if st.button("# States"):
                        states_button_clicked = True

                with c12:
                    if st.button("# Districts"):
                        districts_button_clicked = True

                with c13:
                    if st.button("# Postal Codes"):
                        postal_codes_button_clicked = True                  
                
                if states_button_clicked:
                    st.markdown("<h1 style='font-size: 30px; color:#05C2DD'> Top 10 States", unsafe_allow_html=True)
                    trans_selected_year_grouped['Transaction_amount'] = trans_selected_year_grouped['Transaction_amount'].apply(format_amount)
                    df=pd.DataFrame(trans_selected_year_grouped[['Serial', 'States', 'Transaction_amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['States', 'Transaction Amount']
                    st.table(df)
                    

                if districts_button_clicked:
                    st.markdown("<h1 style='font-size: 30px; color:#05C2DD'> Top 10 Districts", unsafe_allow_html=True)
                    trans_selected_year_grouped_dist = trans_selected_year_dist.groupby('Districts').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
                    trans_selected_year_grouped_dist['Serial'] = range(1, len(trans_selected_year_grouped_dist) + 1)
                    trans_selected_year_grouped_dist = trans_selected_year_grouped_dist.head(10)
                    trans_selected_year_grouped_dist['Transaction_amount'] = trans_selected_year_grouped_dist['Transaction_amount'].apply(format_amount)
                    df=pd.DataFrame(trans_selected_year_grouped_dist[['Serial', 'Districts', 'Transaction_amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['Districts', 'Transaction Amount']
                    st.table(df)
                    
                if postal_codes_button_clicked:
                    st.markdown("<h1 style='font-size: 30px; color:#05C2DD'>Top 10 Postal Codes", unsafe_allow_html=True)
                    trans_selected_year_grouped_pin = trans_selected_year_pin.groupby('Pincode').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
                    trans_selected_year_grouped_pin['Serial'] = range(1, len(trans_selected_year_grouped_pin) + 1)
                    trans_selected_year_grouped_pin = trans_selected_year_grouped_pin.head(10)
                    trans_selected_year_grouped_pin['Pincode'] = trans_selected_year_grouped_pin['Pincode']
                    trans_selected_year_grouped_pin['Transaction_amount'] = trans_selected_year_grouped_pin['Transaction_amount'].apply(format_amount)
                    df=pd.DataFrame(trans_selected_year_grouped_pin[['Serial', 'Pincode', 'Transaction_amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['Postal Codes', 'Transaction Amount']
                    st.table(df) 


#-----------------------------------------------------------------TAB2: INSURANCE DATA----------------------------------------------------------                   

    with tab2:  
        st.markdown("<h1 style='text-align: center; font-size: 30px'> All India Insurance Data", unsafe_allow_html=True)

        col1, col2, co3,col4,col5,col6 = st.columns((0.7,0.8,1.5,1,1,1),gap="large")
        with col1:
            years = st.selectbox("#### Select Year:", options=Agg_ins_df["Years"].unique())
        with col2:
            quarters = st.selectbox("#### Select Quarter:", options=Agg_ins_df["Quarter"].unique())


        ins_selected_year = Agg_ins_df[(Agg_ins_df['Years'] == years) & 
                                        (Agg_ins_df['Quarter'] == quarters)]
        ins_selected_year_dist = map_ins_df[(map_ins_df['Years'] == years) & 
                                        (map_ins_df['Quarter'] == quarters)]        
        ins_selected_year_pin = top_ins_df[(top_ins_df['Years'] == years) & 
                                        (top_ins_df['Quarter'] == quarters)]
        
        if ins_selected_year.empty:
            st.error("#### No data available for the selected year and quarter.")
            
        else:
            ins_selected_year_grouped = ins_selected_year.groupby('States').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
            ins_selected_year_grouped['Serial'] = range(1, len(ins_selected_year_grouped) + 1)
            ins_selected_year_grouped = ins_selected_year_grouped.head(10)

            total_transactions = ins_selected_year['Transaction_count'].sum()
            total_payment_value = ins_selected_year['Transaction_amount'].sum()
            avg_transaction_value = total_payment_value / total_transactions
            total_transactions = format_number(total_transactions)
            col_map, col_data = st.columns((5, 1.65), gap='large') 
            
            with col_map:
                                         
                choropleth_map = ins_choropleth(ins_selected_year)
                st.plotly_chart(choropleth_map,use_container_width=True)

            with col_data:
                st.markdown("<h1 style=' font-size: 40px; color:#05C2DD'>Insurance</h1>", unsafe_allow_html=True)
                st.write(f'#### All India Insurance Policies Purchased (Nos.) ****(Q{quarters}) {years}****')
                st.metric(label='', value=total_transactions)
                st.write(f'#### Total Premium Value (Q{quarters}) {years}')
                st.metric(label='', value=format_amount(total_payment_value))
                st.write(f'#### Average Premium Value (Q{quarters}) {years}')
                st.metric(label='', value=f"₹{avg_transaction_value:,.0f}")
                st.markdown('***')
                states_button_clicked = False
                districts_button_clicked = False
                postal_codes_button_clicked = False
                c11, c12, c13 = st.columns((1,1,1.5),gap="small")
                with c11:
                    if st.button("# States "):
                        states_button_clicked = True

                with c12:
                    if st.button("# Districts "):
                        districts_button_clicked = True

                with c13:
                    if st.button("# Postal Codes "):
                        postal_codes_button_clicked = True                
                
                if states_button_clicked:
                    st.markdown("<h1 style='font-size: 30px; color:#05C2DD'> Top 10 States", unsafe_allow_html=True)
                    ins_selected_year_grouped['Transaction_amount'] = ins_selected_year_grouped['Transaction_amount'].apply(format_amount)
                    df=pd.DataFrame(ins_selected_year_grouped[['Serial', 'States', 'Transaction_amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['State', 'Premium Amount']
                    st.table(df)
 
                if districts_button_clicked:
                    st.markdown("<h1 style='font-size: 30px; color:#05C2DD'> Top 10 Districts", unsafe_allow_html=True)
                    ins_selected_year_grouped_dist = ins_selected_year_dist.groupby('Districts').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
                    ins_selected_year_grouped_dist['Serial'] = range(1, len(ins_selected_year_grouped_dist) + 1)
                    ins_selected_year_grouped_dist = ins_selected_year_grouped_dist.head(10)
                    ins_selected_year_grouped_dist['Transaction_amount'] = ins_selected_year_grouped_dist['Transaction_amount'].apply(format_amount)
                    df=pd.DataFrame(ins_selected_year_grouped_dist[['Serial', 'Districts', 'Transaction_amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['Districts', 'Premium Amount']
                    st.table(df)
                    
                if postal_codes_button_clicked:
                    st.markdown("<h1 style='font-size: 30px; color:#05C2DD'>Top 10 Postal Codes", unsafe_allow_html=True)
                    ins_selected_year_grouped_pin = ins_selected_year_pin.groupby('Pincode').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
                    ins_selected_year_grouped_pin['Serial'] = range(1, len(ins_selected_year_grouped_pin) + 1)
                    ins_selected_year_grouped_pin = ins_selected_year_grouped_pin.head(10)
                    ins_selected_year_grouped_pin['Pincode'] = ins_selected_year_grouped_pin['Pincode']
                    ins_selected_year_grouped_pin['Transaction_amount'] = ins_selected_year_grouped_pin['Transaction_amount'].apply(format_amount)
                    df=pd.DataFrame(ins_selected_year_grouped_pin[['Serial', 'Pincode', 'Transaction_amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['Postal Codes', 'Premium Amount']
                    st.table(df)

#-----------------------------------------------------------------TAB3: USER DATA------------------------------------------------------------                    


    with tab3:
        st.markdown("<h1 style='text-align: center; font-size: 40px'> All India User Data", unsafe_allow_html=True)

        col1, col2, co3,col4,col5,col6 = st.columns((0.7,0.8,1.5,1,1,1),gap="large")
        with col1:
            years = st.selectbox("#### Select Year: ", options=map_user_df["Years"].unique())
        with col2:
            quarters = st.selectbox("#### Select Quarter: ", options=map_user_df["Quarter"].unique())

        user_selected_year = Agg_user_df[(Agg_user_df['Years'] == years) & 
                                        (Agg_user_df['Quarter'] == quarters)]
        user_selected_year_dist = map_user_df[(map_user_df['Years'] == years) & 
                                        (map_user_df['Quarter'] == quarters)]        
        user_selected_year_pin = top_user_df[(top_user_df['Years'] == years) & 
                                        (top_user_df['Quarter'] == quarters)]
        
        if user_selected_year_dist.empty:
            st.error("#### No data available for the selected year and quarter.")
            
        else:
            user_selected_year_grouped = user_selected_year_dist.groupby('States').sum().reset_index().sort_values(by="RegisteredUsers", ascending=False)
            user_selected_year_group = user_selected_year.groupby('States').sum().reset_index().sort_values(by="Transaction_count", ascending=False)
            user_selected_year_grouped['Serial'] = range(1, len(user_selected_year_grouped) + 1)
            user_selected_year_grouped1 = user_selected_year_grouped.head(10)

            total_user = user_selected_year_group['Transaction_count'].sum()
            total_app_opens = user_selected_year_grouped['AppOpens'].sum()
            total_user = format_number(total_user)
            total_app_opens = format_number(total_app_opens)

            col_map, col_data = st.columns((5, 1.65), gap='large') 
            
            with col_map:
                choropleth_map = user_choropleth(user_selected_year_grouped)
                st.plotly_chart(choropleth_map,use_container_width=True)

            with col_data:
                st.markdown("<h1 style=' font-size: 40px; color:#05C2DD'>Users</h1>", unsafe_allow_html=True)
                st.write(f'#### Registered PhonePe users (Q{quarters}) {years}')
                st.metric(label='',value=total_user)
                st.write(f'#### PhonePe app opens in (Q{quarters}) {years}')
                st.metric(label='',value=total_app_opens)
                
                st.markdown('***')
                
                states_button_clicked = False
                districts_button_clicked = False
                postal_codes_button_clicked = False
                c11, c12, c13 = st.columns((1,1,1.5),gap="small")
                with c11:
                    if st.button("# States  "):
                        states_button_clicked = True

                with c12:
                    if st.button("# Districts  "):
                        districts_button_clicked = True

                with c13:
                    if st.button("# Postal Codes  "):
                        postal_codes_button_clicked = True
                
                if states_button_clicked:
                    st.markdown("<h1 style='font-size: 30px; color:#05C2DD'> Top 10 States", unsafe_allow_html=True)
                    user_selected_year_grouped1['RegisteredUsers']=user_selected_year_grouped1['RegisteredUsers'].apply(format_number)
                    df=pd.DataFrame(user_selected_year_grouped1[['Serial', 'States', 'RegisteredUsers']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['States', 'Registered User']
                    st.table(df)
 
                if districts_button_clicked:
                    st.markdown("<h1 style='font-size: 30px; color:#05C2DD'> Top 10 Districts", unsafe_allow_html=True)
                    user_selected_year_grouped_dist = user_selected_year_dist.groupby('Districts').sum().reset_index().sort_values(by="RegisteredUsers", ascending=False)
                    user_selected_year_grouped_dist['Serial'] = range(1, len(user_selected_year_grouped_dist) + 1)
                    user_selected_year_grouped_dist = user_selected_year_grouped_dist.head(10)
                    user_selected_year_grouped_dist['RegisteredUsers']=user_selected_year_grouped_dist['RegisteredUsers'].apply(format_number)
                    df=pd.DataFrame(user_selected_year_grouped_dist[['Serial', 'Districts', 'RegisteredUsers']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['Districts', 'Registered User']
                    st.table(df)
                    
                if postal_codes_button_clicked:
                    st.markdown("<h1 style='font-size: 30px; color:#05C2DD'>Top 10 Postal Codes", unsafe_allow_html=True)
                    user_selected_year_grouped_pin = user_selected_year_pin.groupby('Pincode').sum().reset_index().sort_values(by="RegisteredUsers", ascending=False)
                    user_selected_year_grouped_pin['Serial'] = range(1, len(user_selected_year_grouped_pin) + 1)
                    user_selected_year_grouped_pin = user_selected_year_grouped_pin.head(10)
                    user_selected_year_grouped_pin['RegisteredUsers']=user_selected_year_grouped_pin['RegisteredUsers'].apply(format_number)
                    user_selected_year_grouped_pin['Pincode'] = user_selected_year_grouped_pin['Pincode']
                    df=pd.DataFrame(user_selected_year_grouped_pin[['Serial', 'Pincode', 'RegisteredUsers']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['Postal Codes', 'Registered User']
                    st.table(df)      
                
                st.markdown("<h1 style='font-size: 30px; color:#05C2DD'>Top 10 Brand Wise ", unsafe_allow_html=True)                     
                
                user_selected_year = user_selected_year.groupby('Brands').sum().reset_index().sort_values(by="Transaction_count", ascending=False)
                user_selected_year['Serial'] = range(1, len(user_selected_year) + 1)
                user_selected_year = user_selected_year.head(10)
                user_selected_year['Transaction_count']= user_selected_year['Transaction_count'].apply(format_number)
                df=pd.DataFrame(user_selected_year[['Serial', 'Brands', 'Transaction_count']])
                df.set_index('Serial', inplace=True)
                df.columns = ['Mobile Brands', 'User Count']
                st.table(df)


#----------------------------------------------------------------OPTION: STATE WISE EXPLORE---------------------------------------------------                

if select == "STATE-WISE-EXPLORE":
    
    tab1, tab2, tab3 = st.tabs(["Transaction Data", "Insurance Data","User Data"])

    
#---------------------------------------------------------------TAB1: TRANSACTION DATA-------------------------------------------------    
    
    with tab1:
      
            
        st.markdown("<h1 style='text-align: center; font-size: 30px'> All India Transaction Data", unsafe_allow_html=True)    

        col1, col2, col3,col4,col5,col6 = st.columns((0.7,0.8,1.5,0.9,0.9,0.9),gap="large")

        with col1:
            years = st.selectbox("#### Select Year:", options=Agg_trans_df["Years"].unique())
        with col2:
            quarters = st.selectbox("#### Select Quarter:", options=Agg_trans_df["Quarter"].unique())
        with col3:
            states = st.selectbox("#### Select State:", options=Agg_trans_df["States"].unique())            
        st.markdown(f"<h1 style='font-size: 30px'> {states} Transaction Data", unsafe_allow_html=True)


        trans_selected_year = Agg_trans_df[(Agg_trans_df['Years'] == years) & 
                                        (Agg_trans_df['Quarter'] == quarters) & (Agg_trans_df['States'] == states)] 
        trans_selected_year_dist = map_trans_df[(map_trans_df['Years'] == years) & 
                                        (map_trans_df['Quarter'] == quarters) & (map_trans_df['States'] == states)]        
        trans_selected_year_pin = top_trans_df[(top_trans_df['Years'] == years) & 
                                        (top_trans_df['Quarter'] == quarters) & (top_trans_df['States'] == states)] 
        
        if trans_selected_year.empty:
            st.error("#### No data available for the selected year and quarter.")
            
        else:
            trans_selected_year_grouped = trans_selected_year.groupby('States').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
            trans_selected_year_grouped['Serial'] = range(1, len(trans_selected_year_grouped) + 1)
            trans_selected_year_grouped = trans_selected_year_grouped.head(10)

            total_transactions = trans_selected_year['Transaction_count'].sum()
            total_payment_value = trans_selected_year['Transaction_amount'].sum()
            avg_transaction_value = total_payment_value / total_transactions
            total_transactions = format_number(total_transactions)
            col_map, col_data = st.columns((5, 1.65), gap='large')
           
            with col_map:
                
                trans_selected_year_dist.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
              
                fig_bar_1 = px.bar(trans_selected_year_dist, y= "Transaction_amount", x= "Districts", 
                                hover_data=['Years','Transaction_amount','Transaction_count'],
                                color='Transaction_amount',
                                color_discrete_sequence=px.colors.sequential.Viridis,width=800, height=800,                          
                                range_color=(trans_selected_year_dist['Transaction_amount'].min(), trans_selected_year_dist['Transaction_amount'].max()))
                st.plotly_chart(fig_bar_1,use_container_width=True)              

                
        with col_data:
            st.markdown("<h1 style=' font-size: 40px; color:#05C2DD'>Transactions</h1>", unsafe_allow_html=True)
            st.write(f'#### Total Transactions (Q {quarters}) {years})')
            st.metric(label='', value=total_transactions)
            st.write(f'#### Total Payment Value (Q {quarters}) {years})')
            st.metric(label='', value=format_amount(total_payment_value))
            st.write(f'#### Average Payment Value (Q {quarters}) {years})')
            st.metric(label='', value=f"₹{avg_transaction_value:,.0f}")
            st.markdown('***')
            
            trans_selected_year_grp = trans_selected_year.groupby('Transaction_type').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
            trans_selected_year_grp['Serial'] = range(1, len(trans_selected_year_grp) + 1)

            df = pd.DataFrame(trans_selected_year_grp[['Serial', 'Transaction_type', 'Transaction_amount']])
            df['Transaction_amount']=df['Transaction_amount'].apply(format_amount)
            
            st.markdown("<h1 style='font-size: 30px; color:#05C2DD'>Categories</h1>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            
            for index, row in df.iterrows():
                with col1:
                    st.markdown(f"<p style='font-size:18px;text-align: left'>{row['Transaction_type']}</p>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<p style='font-size:18px;text-align: right;font-weight:bold'>{row['Transaction_amount']}</p>", unsafe_allow_html=True)

            st.markdown("***")
            districts_button_clicked = False
            postal_codes_button_clicked = False
            c11,c13 = st.columns(2)
            with c11:
                if st.button("# Districts"):
                    districts_button_clicked = True

            with c13:
                if st.button("# Postal Codes"):
                    postal_codes_button_clicked = True                
        
            if districts_button_clicked:
                st.markdown("<h1 style='font-size: 30px; color:#05C2DD'> Top 10 Districts", unsafe_allow_html=True)
                trans_selected_year_grouped_dist = trans_selected_year_dist.groupby('Districts').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
                trans_selected_year_grouped_dist['Serial'] = range(1, len(trans_selected_year_grouped_dist) + 1)
                trans_selected_year_grouped_dist = trans_selected_year_grouped_dist.head(10)  
                trans_selected_year_grouped_dist['Transaction_amount'] = trans_selected_year_grouped_dist['Transaction_amount'].apply(format_amount)               
                df=pd.DataFrame(trans_selected_year_grouped_dist[['Serial', 'Districts', 'Transaction_amount']])
                df.set_index('Serial', inplace=True)
                df.columns = ['Districts', 'Transaction_amount']
                st.table(df)  

            if postal_codes_button_clicked:
                st.markdown("<h1 style='font-size: 30px; color:#05C2DD'>Top 10 Postal Codes", unsafe_allow_html=True)
                trans_selected_year_grouped_pin = trans_selected_year_pin.groupby('Pincode').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
                trans_selected_year_grouped_pin['Serial'] = range(1, len(trans_selected_year_grouped_pin) + 1)
                trans_selected_year_grouped_pin['Pincode'] = trans_selected_year_grouped_pin['Pincode']
                trans_selected_year_grouped_pin['Transaction_amount'] = trans_selected_year_grouped_pin['Transaction_amount'].apply(format_amount)
                df=pd.DataFrame(trans_selected_year_grouped_pin[['Serial', 'Pincode', 'Transaction_amount']])
                df.set_index('Serial', inplace=True)
                df.columns = ['Postal Codes', 'Transaction_amount']
                st.table(df)


#-------------------------------------------------------------------TAB2: INSURANCE DATA--------------------------------------------------------                    


    with tab2:

        st.markdown("<h1 style='text-align: center; font-size: 30px'> All India Insurance Data", unsafe_allow_html=True)  
        
        col1, col2, co3,col4,col5,col6 = st.columns((0.7,0.8,1,1,1,1),gap="large")
        with col1:
            years = st.selectbox("#### Select Year: ", options=Agg_ins_df["Years"].unique())
        with col2:
            quarters = st.selectbox("#### Select Quarter: ", options=Agg_ins_df["Quarter"].unique())
        with co3:
            states = st.selectbox("#### Select State: ", options=Agg_ins_df["States"].unique())
        st.markdown(f"<h1 style='font-size: 30px'> {states} Insurance Data", unsafe_allow_html=True)
            

        ins_selected_year = Agg_ins_df[(Agg_ins_df['Years'] == years) & 
                                        (Agg_ins_df['Quarter'] == quarters) & (Agg_ins_df['States'] == states)] 
        ins_selected_year_dist = map_ins_df[(map_ins_df['Years'] == years) & 
                                        (map_ins_df['Quarter'] == quarters) & (map_ins_df['States'] == states)]        
        ins_selected_year_pin = top_ins_df[(top_ins_df['Years'] == years) & 
                                        (top_ins_df['Quarter'] == quarters) & (top_ins_df['States'] == states)]
        

        if ins_selected_year.empty:
            st.error("No data available for the selected year and quarter.")
            
        else:
            ins_selected_year_grouped = ins_selected_year.groupby('States').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
            ins_selected_year_grouped['Serial'] = range(1, len(ins_selected_year_grouped) + 1)
            ins_selected_year_grouped = ins_selected_year_grouped.head(10)

            total_transactions = ins_selected_year['Transaction_count'].sum()
            total_payment_value = ins_selected_year['Transaction_amount'].sum()
            avg_transaction_value = total_payment_value / total_transactions
            total_transactions = format_number(total_transactions)
            
            col_map, col_data = st.columns((5, 1.65), gap='large')
             
            with col_map:
 
                # ins_selected_year_dist.loc[:, 'Transaction_amount'] = ins_selected_year_dist['Transaction_amount'].apply(format_amount)
                # ins_selected_year_dist_map=ins_selected_year_dist
                ins_selected_year_dist=ins_selected_year_dist.rename(columns={'Transaction_amount': 'Premium Amount', 'Transaction_count': 'Policy Count'})
                

                ins_selected_year_dist.groupby("Districts")[["Premium Amount","Policy Count"]].sum()
              
                fig_bar_1 = px.bar(ins_selected_year_dist, y= "Premium Amount", x= "Districts", 
                                hover_data=['Years','Premium Amount','Policy Count'],
                                color='Premium Amount',
                                color_discrete_sequence=px.colors.sequential.Viridis,width=800, height=800)                          
                               
                st.plotly_chart(fig_bar_1,use_container_width=True)              


            with col_data:
                st.markdown("<h1 style=' font-size: 40px; color:#05C2DD'>Insurance</h1>", unsafe_allow_html=True)
                st.write(f"#### Insurance Policies No's (Q{quarters}) {years})")
                st.metric(label='', value=total_transactions)
                st.write(f'#### Total Premium Value (Q{quarters}) {years})')
                st.metric(label='', value=format_amount(total_payment_value))
                st.write(f'#### Average Premium Value (Q{quarters}) {years})')
                st.metric(label='', value=f"₹{avg_transaction_value:,.0f}")                
                
                st.markdown('***')   
                districts_button_clicked = False
                postal_codes_button_clicked = False
                c11, c13 = st.columns(2)
                with c11:
                    if st.button("# Districts "):
                        districts_button_clicked = True

                with c13:
                    if st.button("# Postal Codes "):
                        postal_codes_button_clicked = True 
                           
                if districts_button_clicked:
                    st.markdown("<h1 style='font-size: 30px; color:#05C2DD'>Top 10 Districts</h1>", unsafe_allow_html=True)
                    ins_selected_year_grouped_dist = ins_selected_year_dist.groupby('Districts').sum().reset_index().sort_values(by="Premium Amount", ascending=False)
                    ins_selected_year_grouped_dist['Serial'] = range(1, len(ins_selected_year_grouped_dist) + 1)
                    ins_selected_year_grouped_dist = ins_selected_year_grouped_dist.head(10)
                    ins_selected_year_grouped_dist['Premium Amount'] = ins_selected_year_grouped_dist['Premium Amount'].apply(format_amount) 
                    df=pd.DataFrame(ins_selected_year_grouped_dist[['Serial', 'Districts', 'Premium Amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['User District', 'Premium Amount']
                    st.table(df)                     
       
                if postal_codes_button_clicked:
                    st.markdown("<h1 style='font-size: 30px; color:#05C2DD'>Top 10 Postal Codes</h1>", unsafe_allow_html=True)
                    ins_selected_year_grouped_pin = ins_selected_year_pin.groupby('Pincode').sum().reset_index().sort_values(by="Transaction_amount", ascending=False)
                    ins_selected_year_grouped_pin['Serial'] = range(1, len(ins_selected_year_grouped_pin) + 1)
                    ins_selected_year_grouped_pin['Pincode'] = ins_selected_year_grouped_pin['Pincode']
                    ins_selected_year_grouped_pin['Transaction_amount'] = ins_selected_year_grouped_pin['Transaction_amount'].apply(format_amount)                    
                    df=pd.DataFrame(ins_selected_year_grouped_pin[['Serial', 'Pincode', 'Transaction_amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['User Postal Codes', 'Premium Amount']
                    st.table(df)


#--------------------------------------------------------------------TAB3: USER DATA---------------------------------------------------------                    


    with tab3:

        st.markdown("<h1 style='text-align: center; font-size: 30px'> All India User Data", unsafe_allow_html=True) 
        col1, col2, co3,col4,col5,col6 = st.columns((0.7,0.8,1,1,1,1),gap="large")
        with col1:
            years = st.selectbox("#### Select Year", options=map_user_df["Years"].unique())
        with col2:
            quarters = st.selectbox("#### Select Quarter", options=map_user_df["Quarter"].unique())
        with co3:
            states = st.selectbox("#### Select State", options=map_user_df["States"].unique())    

        user_selected_year = Agg_user_df[(Agg_user_df['Years'] == years) & 
                                        (Agg_user_df['Quarter'] == quarters) & (Agg_user_df['States'] == states) ]
        user_selected_year_dist = map_user_df[(map_user_df['Years'] == years) & 
                                        (map_user_df['Quarter'] == quarters) & (map_user_df['States'] == states) ]     
        user_selected_year_pin = top_user_df[(top_user_df['Years'] == years) &
                                        (top_user_df['Quarter'] == quarters) & (top_user_df['States'] == states) ]
        st.markdown(f"<h1 style='font-size: 30px'> {states} Registered Users Data", unsafe_allow_html=True)
        if user_selected_year.empty:
            st.error("#### No data available for the selected year and quarter.")
                
        else:
            user_selected_year_grouped = user_selected_year_dist.groupby('States').sum().reset_index().sort_values(by="RegisteredUsers", ascending=False)
            user_selected_year_group = user_selected_year.groupby('States').sum().reset_index().sort_values(by="Transaction_count", ascending=False)
            user_selected_year_grouped['Serial'] = range(1, len(user_selected_year_grouped) + 1)

            total_user = user_selected_year_group['Transaction_count'].sum()
            total_app_opens = user_selected_year_grouped['AppOpens'].sum()
            total_app_opens = format_number(total_app_opens)
            total_user = format_number(total_user)
                
            col_map, col_data = st.columns((5, 1.65), gap='large')
            
            with col_map:
                user_selected_year_dist_map = user_selected_year_dist
                user_selected_year_dist["RegisteredUsers"] = user_selected_year_dist["RegisteredUsers"].apply(format_number)
                user_selected_year_dist["AppOpens"] = user_selected_year_dist["AppOpens"].apply(format_number)
                user_selected_year_dist= user_selected_year_dist.rename(columns={'RegisteredUsers': 'Total User', 'AppOpens': 'App Open Count'})

                user_selected_year_dist.groupby("Districts")[["Total User","App Open Count"]].sum()
              
                fig_bar_1 = px.bar(user_selected_year_dist, y= "Total User", x= "Districts", 
                                hover_data=['Years','Total User','App Open Count'],
                                color='Total User',
                                color_discrete_sequence=px.colors.sequential.Viridis,width=800, height=800)                          
                               
                st.plotly_chart(fig_bar_1,use_container_width=True)      

            with col_data:
                st.markdown("<h1 style=' font-size: 40px; color:#05C2DD'>Users</h1>", unsafe_allow_html=True)
                st.markdown(f'#### Total Registered Users (Q{quarters}) {years}')
                st.metric(label="",value=total_user)
                st.markdown(f'#### App Opens in (Q{quarters}) {years}')
                st.metric(label="",value=total_app_opens)                
                
                st.markdown('***')   
                districts_button_clicked = False
                postal_codes_button_clicked = False
                c11, c13 = st.columns(2)
                with c11:
                    if st.button("# Districts  "):
                        districts_button_clicked = True

                with c13:
                    if st.button("# Postal Codes  "):
                        postal_codes_button_clicked = True 

                if districts_button_clicked:
                    st.markdown("<h1 style='font-size: 30px; color:#05C2DD'> Top 10 Districts", unsafe_allow_html=True)
                    user_selected_year_grouped_dist = user_selected_year_dist.groupby('Districts').sum().reset_index().sort_values(by="Total User", ascending=False)
                    user_selected_year_grouped_dist['Serial'] = range(1, len(user_selected_year_grouped_dist) + 1)
                    user_selected_year_grouped_dist = user_selected_year_grouped_dist.head(10)
                    df=pd.DataFrame(user_selected_year_grouped_dist[['Serial', 'Districts', 'Total User']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['Districts', 'Registered User']
                    st.table(df)
                if postal_codes_button_clicked:
                    st.markdown("<h1 style='font-size: 30px; color:#05C2DD'>Top 10 Postal Codes", unsafe_allow_html=True)
                    user_selected_year_grouped_pin = user_selected_year_pin.groupby('Pincode').sum().reset_index().sort_values(by="RegisteredUsers", ascending=False)
                    user_selected_year_grouped_pin['Serial'] = range(1, len(user_selected_year_grouped_pin) + 1)
                    user_selected_year_grouped_pin['Pincode'] = user_selected_year_grouped_pin['Pincode']
                    user_selected_year_grouped_pin['RegisteredUsers'] = user_selected_year_grouped_pin['RegisteredUsers'].apply(format_number)                    
                    df=pd.DataFrame(user_selected_year_grouped_pin[['Serial', 'Pincode', 'RegisteredUsers']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['Postal Codes', 'Registered User']
                    st.table(df)      
                        
                st.markdown("<h1 style='font-size: 30px; color:#05C2DD'>Top 10 Brand Wise ", unsafe_allow_html=True)                     
                
                user_selected_year = user_selected_year.groupby('Brands').sum().reset_index().sort_values(by="Transaction_count", ascending=False)
                user_selected_year['Serial'] = range(1, len(user_selected_year) + 1)
                user_selected_year = user_selected_year.head(10)
                user_selected_year['Transaction_count']= user_selected_year['Transaction_count'].apply(format_number)
                df=pd.DataFrame(user_selected_year[['Serial', 'Brands', 'Transaction_count']])
                df.set_index('Serial', inplace=True)
                df.columns = ['Mobile Brands', 'User Count']
                st.table(df)



#-----------------------------------------------------------------OPTION: DATA INSIGHTS-----------------------------------------------------------------                

if select == "DATA INSIGHTS":


    selected = st.radio("INSIGHTS",("All India Insights", "State-wise-Insights"))
    
    if selected == "All India Insights":
       
        insight_options = [
            '1. Yearly Growth of Transaction Amount in India',
            '2. Yearly Growth of Transaction Count in India',
            '3. Yearly Growth of Insurance Premium amount in India',
            '4. Yearly Growth of Insurance Premium Count in India',
            '5. Yearly Growth of Registered User in India',
            '6. Yearly Growth of App Open in India',
            '7. Transaction Amount by State',
            '8. Transaction Count by State',
            '9. Transaction Count by Brand',
            '10. Insurance Premium Amount by State',
            '11. Insurance Premium Count by State',
            '12. Registered User by State',
            '13. App Opens by State',
            '14. State Wise - Brand & Count',
            '15. Transaction Types Analysis by Years and Quarters',
            '16. Average Transaction Amount by Quarter',
            '17. Percentage of Transactions by Type']

        selected_insight = st.selectbox('Select an Insight', insight_options)
#------------------------------------------------------------------RADIO BUTTON: ALL INDIA INSIGHTS-------------------------------------------------         

#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-1----------------------------------------------------------------- 
        if selected_insight == '1. Yearly Growth of Transaction Amount in India':
            st.markdown('#### Yearly Growth of Transaction Amount in India')
            query1 = '''SELECT Years, 
                                SUM(Transaction_amount) AS Transaction_amount 
                        FROM aggregated_transaction 
                        GROUP BY Years
                        ORDER BY Years  '''
            cursor.execute(query1)
            mydb.commit()
            table1 = cursor.fetchall()
            aggregated_data_yearly = pd.DataFrame(table1, columns=["Years","Transaction_amount"])
            aggregated_data_yearly['Transaction_amount']=aggregated_data_yearly['Transaction_amount'].apply(format_amount)
            fig = px.line(aggregated_data_yearly, x='Years', y='Transaction_amount', 
                    labels={'Years': 'Years', 'Transaction_amount': 'Transaction Amount'}, 
                    title='Yearly Growth of Transaction Amount in India',markers=True)
           
            st.plotly_chart(fig, use_container_width=True) 
            
                            
            on1 = st.toggle("Advanced Insights", key="states_toggle1")

            if on1:
                st.markdown("#### Quarterly Distribution of Transaction Amounts by Year in India")
                map1 , table1 = st.columns((5,2),gap= 'large')
                query2 = '''SELECT  Years, Quarter, 
                                    SUM(Transaction_amount) AS Transaction_amount , 
                                    SUM(Transaction_count) AS Transaction_count 
                            FROM aggregated_transaction GROUP BY Years,Quarter'''
                cursor.execute(query2)
                mydb.commit()
                table2 = cursor.fetchall()
                aggregated_data1 = pd.DataFrame(table2, columns=["Years","Quarter","Transaction_amount","Transaction_count"])                   
                aggregated_data1['Transaction_amount']=aggregated_data1['Transaction_amount'].apply(format_amount)
                aggregated_data1['Transaction_count']=aggregated_data1['Transaction_count'].apply(format_number)
                aggregated_data1['Years'] = aggregated_data1['Years'].astype(str)
                with map1:   
                    fig = px.box(aggregated_data1, x='Years', y='Transaction_amount', color='Quarter',
                                title='Box Plot of Quarterly Transaction Amount by Year in India',
                                points='all',  
                                hover_data=['Transaction_count'])

                    st.plotly_chart(fig, use_container_width=True)
                with table1:  
                    df_aggregated_data1=aggregated_data1
                    df_aggregated_data1.drop(columns=["Transaction_count"], inplace=True)
                    df_aggregated_data1.rename(columns={"Transaction_amount": "Transaction Amount"}, inplace=True)                    
                    st.markdown('#### Quarterly Transaction Distribution')
                    st.dataframe(df_aggregated_data1, use_container_width=True, hide_index=True)   

                query3 = '''SELECT  Years, Quarter, 
                        SUM(Transaction_amount) AS Transaction_amount 
                        FROM aggregated_transaction 
                        WHERE Years != 2024
                        GROUP BY Years,Quarter'''
                cursor.execute(query3)
                mydb.commit()
                table3 = cursor.fetchall()
                aggregated_data_state = pd.DataFrame(table3, columns=["Years","Quarter","Transaction_amount"]) 
                st.markdown('#### Quarterly Transaction Amount Distribution by Transaction Amount for Each Year')
                years = aggregated_data_state['Years'].unique()
                num_columns = 3
                columns = st.columns(num_columns)
                for i, year in enumerate(years):
                    df_year_quarter = aggregated_data_state[aggregated_data_state['Years'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_amount'], hole=.3)])
                        fig.update_layout(
                            title=f'Transaction Amount Distribution for {year} - All Quarters',
                            height=550,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### Aggregated Transaction Amount for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    aggregated_total = aggregated_data_state.groupby(['Quarter'])['Transaction_amount'].sum().reset_index()
                    fig_total = go.Figure(data=[go.Pie(labels=aggregated_total['Quarter'], values=aggregated_total['Transaction_amount'], hole=.3)])
                    fig_total.update_layout(
                        title='Aggregated Transaction Amount for All Quarters Combined',
                        height=550,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)    
            
#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-2-----------------------------------------------------------------           

        if selected_insight == "2. Yearly Growth of Transaction Count in India":
            st.markdown('#### Yearly Growth of Transaction Count in India')
            query4 = '''SELECT  Years, 
                    SUM(Transaction_count) AS Transaction_count
                    FROM aggregated_transaction 
                    WHERE Years != 2024
                    GROUP BY Years
                    ORDER BY Years'''
            cursor.execute(query4)
            mydb.commit()
            table4 = cursor.fetchall()
            aggregated_data_yearly_count = pd.DataFrame(table4, columns=["Years","Transaction_count"]) 
            aggregated_data_yearly_count['Transaction_count']=aggregated_data_yearly_count['Transaction_count'].apply(format_number)
            fig = px.line(aggregated_data_yearly_count, x='Years', y='Transaction_count', 
                            labels={'Years': 'Years', 'Transaction_count': 'Transaction Count'}, 
                            title='Yearly Growth of Transaction Count in India', markers=True)
            
            st.plotly_chart(fig, use_container_width=True)   
            
            on = st.toggle("Advanced Insights")

            if on:
                map2 , table2 = st.columns((5,2),gap= 'large') 
                query5 = '''SELECT  Years, Quarter, 
                    SUM(Transaction_amount) AS Transaction_amount , 
                    SUM(Transaction_count) AS Transaction_count
                    FROM aggregated_transaction 
                    GROUP BY Years,Quarter'''
                cursor.execute(query5)
                mydb.commit()
                table5 = cursor.fetchall()
                aggregated_data1 = pd.DataFrame(table5, columns=["Years","Quarter","Transaction_amount","Transaction_count"])  
                aggregated_data1['Transaction_amount']=aggregated_data1['Transaction_amount'].apply(format_amount)
                aggregated_data1['Transaction_count']=aggregated_data1['Transaction_count'].apply(format_number)
                aggregated_data1['Years'] = aggregated_data1['Years'].astype(str)
                with map2:   
                    st.markdown('#### Box Plot of Quarterly Transaction Count by Year in India')
                    fig = px.box(aggregated_data1, x='Years', y='Transaction_count', color='Quarter',
                                title='Box Plot of Quarterly Transaction Count by Year in India',
                                points='all',  
                                hover_data=['Transaction_amount'])
                    st.plotly_chart(fig, use_container_width=True)
                    
                with table2: 
                    df_aggregated_data1=aggregated_data1
                    df_aggregated_data1.drop(columns=["Transaction_amount"], inplace=True)
                    df_aggregated_data1.rename(columns={"Transaction_count": "Transaction Count"}, inplace=True)
                    st.markdown('#### Quarterly Transaction Count Distribution')
                    st.dataframe(df_aggregated_data1, use_container_width=True, hide_index=True)   
                
                query6 = '''SELECT  Years, Quarter, 
                        SUM(Transaction_count) AS Transaction_count
                        FROM aggregated_transaction 
                        WHERE Years != 2024
                        GROUP BY Years,Quarter'''
                cursor.execute(query6)
                mydb.commit()
                table6 = cursor.fetchall()
                aggregated_data_state = pd.DataFrame(table6, columns=["Years","Quarter","Transaction_count"])                     
                st.markdown('#### Quarterly Transaction Count Distribution by Transaction Count for Each Year')
                years = aggregated_data_state['Years'].unique()
                num_columns = 3
                columns = st.columns(num_columns)
                for i, year in enumerate(years):
                    df_year_quarter = aggregated_data_state[aggregated_data_state['Years'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_count'], hole=.3)])
                        fig.update_layout(
                            title=f'Transaction Count Distribution for {year} - All Quarters',
                            height=550,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### Aggregated Transaction Count for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    aggregated_total = aggregated_data_state.groupby(['Quarter'])['Transaction_count'].sum().reset_index()
                    fig_total = go.Figure(data=[go.Pie(labels=aggregated_total['Quarter'], values=aggregated_total['Transaction_count'], hole=.3)])
                    fig_total.update_layout(
                        title='Aggregated Transaction Count for All Quarters Combined',
                        height=550,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)    

#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-3----------------------------------------------------------------- 

        if selected_insight == '3. Yearly Growth of Insurance Premium amount in India':
            st.markdown('#### Yearly Growth of Insurance Premium Amount in India')
            query7 = '''SELECT  Years, 
                    SUM(Transaction_amount) AS Transaction_amount
                    FROM aggregated_insurance 
                    WHERE Years != 2024
                    GROUP BY Years
                    ORDER BY Years'''
            cursor.execute(query7)
            mydb.commit()
            table7= cursor.fetchall()
            agg_ins_yearly = pd.DataFrame(table7, columns=["Years","Transaction_amount"])            
            agg_ins_yearly['Transaction_amount']=agg_ins_yearly['Transaction_amount'].apply(format_amount)
            fig = px.line(agg_ins_yearly, x='Years', y='Transaction_amount', 
                    labels={'Years': 'Years', 'Transaction_amount': 'Insurance Premium Amount'}, 
                    title='Yearly Growth of Transaction Amount in India', markers=True)
            fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True) 
            
                            
            on = st.toggle("Advanced Insights")

            if on:
                st.markdown("#### Quarterly Distribution of Insurance Premium Amount by Year in India")
                map1 , table1 = st.columns((5,2),gap= 'large')   
                query8 = '''SELECT  Years, Quarter, 
                    SUM(Transaction_amount) AS Transaction_amount , 
                    SUM(Transaction_count) AS Transaction_count
                    FROM aggregated_insurance 
                    GROUP BY Years,Quarter'''
                cursor.execute(query8)
                mydb.commit()
                table8 = cursor.fetchall()
                agg_ins_data1 = pd.DataFrame(table8, columns=["Years","Quarter","Transaction_amount","Transaction_count"]) 
                agg_ins_data1['Transaction_amount']=agg_ins_data1['Transaction_amount'].apply(format_amount)
                agg_ins_data1['Transaction_count']=agg_ins_data1['Transaction_count'].apply(format_number)
                agg_ins_data1['Years'] = agg_ins_data1['Years'].astype(str)
                with map1:   
                    fig = px.box(agg_ins_data1, x='Years', y='Transaction_amount', color='Quarter',
                                title='Box Plot of Quarterly Insurance Premium Amount by Year in India',
                                points='all', 
                                hover_data=['Transaction_count'])

                    st.plotly_chart(fig, use_container_width=True)
                with table1:  
                    df_agg_ins_data1=agg_ins_data1
                    df_agg_ins_data1.drop(columns=["Transaction_count"], inplace=True)
                    df_agg_ins_data1.rename(columns={"Transaction_amount": "Transaction Amount"}, inplace=True)
                    st.markdown('#### Quarterly Insurance Premium Amount Distribution')
                    st.dataframe(df_agg_ins_data1, use_container_width=True, hide_index=True)
                    
                query9 = '''SELECT  Years, Quarter, 
                        SUM(Transaction_amount) AS Transaction_amount
                        FROM aggregated_insurance
                        WHERE Years != 2024
                        GROUP BY Years,Quarter'''
                cursor.execute(query9)
                mydb.commit()
                table9 = cursor.fetchall()
                agg_ins_state = pd.DataFrame(table9, columns=["Years","Quarter","Transaction_amount"])   
                st.markdown('#### Quarterly Transaction Amount Distribution by Insurance Premium Amount for Each Year')
                years = agg_ins_state['Years'].unique()
                num_columns = 3
                columns = st.columns(num_columns)
                for i, year in enumerate(years):
                    df_year_quarter = agg_ins_state[agg_ins_state['Years'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_amount'], hole=.3)])
                        fig.update_layout(
                            title=f'Premium Amount Distribution for {year} - All Quarters',
                            height=550,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### Insurance Premium Amount for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    agg_ins_total = agg_ins_state.groupby(['Quarter'])['Transaction_amount'].sum().reset_index()
                    
                    fig_total = go.Figure(data=[go.Pie(labels=agg_ins_total['Quarter'], values=agg_ins_total['Transaction_amount'], hole=.3)])
                    fig_total.update_layout(
                        title='Insurance Premium Amount for All Quarters Combined',
                        height=550,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)    

#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-4----------------------------------------------------------------- 

        if selected_insight == "4. Yearly Growth of Insurance Premium Count in India":
            st.markdown('#### Yearly Growth of Insurance Premium Count in India')
            query10 = '''SELECT  Years, 
                    SUM(Transaction_count) AS Transaction_count
                    FROM aggregated_insurance 
                    WHERE Years != 2024
                    GROUP BY Years
                    ORDER BY Years'''
            cursor.execute(query10)
            mydb.commit()
            table10= cursor.fetchall()
            agg_ins_data_yearly_count = pd.DataFrame(table10, columns=["Years","Transaction_count"])             
            agg_ins_data_yearly_count['Transaction_count']=agg_ins_data_yearly_count['Transaction_count'].apply(format_number)
            fig = px.line(agg_ins_data_yearly_count, x='Years', y='Transaction_count', 
                            labels={'Years': 'Years', 'Transaction_count': 'Insurance Premium Count'}, 
                            title='Yearly Growth of Insurance Premium Count in India',markers=True)
            fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True)   
            
            on = st.toggle("Advanced Insights")

            if on:
                map2 , table2 = st.columns((5,2),gap= 'large')   
                query11 = '''SELECT  Years, Quarter, 
                    SUM(Transaction_amount) AS Transaction_amount , 
                    SUM(Transaction_count) AS Transaction_count
                    FROM aggregated_insurance 
                    GROUP BY Years,Quarter'''
                cursor.execute(query11)
                mydb.commit()
                table11 = cursor.fetchall()
                aggregated_data1 = pd.DataFrame(table11, columns=["Years","Quarter","Transaction_amount","Transaction_count"])                 
                aggregated_data1['Transaction_amount']=aggregated_data1['Transaction_amount'].apply(format_amount)
                aggregated_data1['Transaction_count']=aggregated_data1['Transaction_count'].apply(format_number)
                aggregated_data1['Years'] = aggregated_data1['Years'].astype(str)
                with map2:   
                    st.markdown('#### Box Plot of Quarterly Insurance Premium Count by Year in India')
                    fig = px.box(aggregated_data1, x='Years', y='Transaction_count', color='Quarter',
                                title='Box Plot of Quarterly Insurance Premium Count by Year in India',
                                points='all', 
                                hover_data=['Transaction_amount'])
                    st.plotly_chart(fig, use_container_width=True)
                with table2:  
                    df_aggregated_data1=aggregated_data1
                    df_aggregated_data1.drop(columns=["Transaction_amount"], inplace=True)
                    df_aggregated_data1.rename(columns={"Transaction_count": "Transaction Count"}, inplace=True)
                    st.markdown('#### Quarterly Insurance Premium Count Distribution')
                    st.dataframe(df_aggregated_data1, use_container_width=True, hide_index=True)
                    
                query12 = '''SELECT  Years, Quarter, 
                        SUM(transaction_count) AS transaction_count
                        FROM aggregated_insurance
                        WHERE Years != 2024
                        GROUP BY Years,Quarter'''
                cursor.execute(query12)
                mydb.commit()
                table12 = cursor.fetchall()
                aggregated_data_state = pd.DataFrame(table12, columns=["Years","Quarter","Transaction_count"])               
                st.markdown('#### Quarterly Distribution by Insurance Premium Count for Each Year')
                years = aggregated_data_state['Years'].unique()
                num_columns = 3
                columns = st.columns(num_columns)
                for i, year in enumerate(years):
                    df_year_quarter = aggregated_data_state[aggregated_data_state['Years'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_count'], hole=.3)])
                        fig.update_layout(
                            title=f'Premium Count Distribution for {year} - All Quarters',
                            height=550,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### Insurance Premium Count for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    aggregated_total = aggregated_data_state.groupby(['Quarter'])['Transaction_count'].sum().reset_index()

                    fig_total = go.Figure(data=[go.Pie(labels=aggregated_total['Quarter'], values=aggregated_total['Transaction_count'], hole=.3)])
                    fig_total.update_layout(
                        title='Insurance Premium Count for All Quarters Combined',
                        height=550,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)    

#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-5----------------------------------------------------------------- 


        if selected_insight == "5. Yearly Growth of Registered User in India":
        
            st.markdown('#### Yearly Growth of Registered User in India')
            query13 = '''SELECT  Years, 
                    SUM(RegisteredUsers) AS RegisteredUsers
                    FROM map_user
                    WHERE Years != 2024
                    GROUP BY Years
                    ORDER BY years'''
            cursor.execute(query13)
            mydb.commit()
            table13= cursor.fetchall()
            map_user_yearly = pd.DataFrame(table13, columns=["Years","RegisteredUsers"])  
            map_user_yearly['Registered_Users']=map_user_yearly['RegisteredUsers'].apply(format_number)
            fig = px.line(map_user_yearly, x='Years', y='RegisteredUsers',
                            labels={'Years': 'Years', 'RegisteredUsers': 'Registered User'}, title='Yearly Growth of Registered User in India', markers=True)
            fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023,2024])
            st.plotly_chart(fig, use_container_width=True)
            
            on = st.toggle("Advanced Insights")

            if on:            
                st.markdown('#### Area chart Quarter-wise Growth of Registered User in India ')
                query14 = '''SELECT  Years, Quarter, 
                    SUM(RegisteredUsers) AS RegisteredUsers
                    FROM map_user
                    WHERE Years !=2024
                    GROUP BY Years,Quarter'''
                cursor.execute(query14)
                mydb.commit()
                table14 = cursor.fetchall()
                map_data1 = pd.DataFrame(table14, columns=["Years","Quarter","RegisteredUsers"])  
                map2 , table2 = st.columns((5,2),gap= 'large')   
                with map2:                               
                    map_data = map_user_df[map_user_df['Years'] != 2024].groupby(['Years', 'Quarter'])['RegisteredUsers'].sum().reset_index()
                    fig = px.area(
                        map_data,
                        x='Quarter',
                        y='RegisteredUsers',
                        color='Years',
                        title="Quarter-wise Growth of Registered User in India",
                        labels={'Quarter': 'Quarter', 'RegisteredUsers': 'Registered User'},
                        hover_data={'RegisteredUsers': ':.2f'}
                    )
                    fig.update_layout(margin=dict(t=50, b=50, l=50, r=50))
                    fig.update_xaxes(tickmode='array', tickvals=[1,2,3,4])
                    st.plotly_chart(fig, use_container_width=True)
                with table2:
                    df_map_data=map_data
                    df_map_data['Years'] = df_map_data['Years'].apply(lambda x: '{:.0f}'.format(x))
                    df_map_data["RegisteredUsers"]=df_map_data["RegisteredUsers"].apply(format_number)
                    df_map_data.rename(columns={"RegisteredUsers": "Registered Users"}, inplace=True)
                    st.markdown('#### Quarterly Registered User in India')
                    st.dataframe(df_map_data, use_container_width=True, hide_index=True)
                
                
                st.markdown('#### Quarterly Distribution by Registered User for Each Year')
                years = map_data1['Years'].unique()
                num_columns = 3
                columns = st.columns(num_columns)
                for i, year in enumerate(years):
                    df_year_quarter = map_data1[map_data1['Years'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['RegisteredUsers'], hole=.3)])
                        fig.update_layout(
                            title=f'Registered User Distribution for {year} - All Quarters',
                            height=550,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### Registered User for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    map_user_total = map_data1.groupby(['Quarter'])['RegisteredUsers'].sum().reset_index()
                    fig_total = go.Figure(data=[go.Pie(labels=map_user_total['Quarter'], values=map_user_total['RegisteredUsers'], hole=.3)])
                    fig_total.update_layout(
                        title='Registered User for All Quarters Combined',
                        height=550,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)  
#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-6----------------------------------------------------------------- 


        if selected_insight == "6. Yearly Growth of App Open in India":
            st.markdown('#### Yearly Growth of App Opens in India')
            query15 = '''SELECT  Years, 
                    SUM(AppOpens) AS AppOpens
                    FROM map_user
                    WHERE years != 2024
                    GROUP BY years
                    ORDER BY Years'''
            cursor.execute(query15)
            mydb.commit()
            table15= cursor.fetchall()
            map_user_years_appopens = pd.DataFrame(table15, columns=["Years","AppOpens"])             
            map_user_years_appopens['AppOpens']=map_user_years_appopens['AppOpens'].apply(format_number)
            fig = px.line(map_user_years_appopens, x='Years', y='AppOpens', 
                            labels={'Years': 'Years', 'AppOpens': 'App Opens'},title='Yearly Growth of App Opens in India', markers=True)
            fig.update_xaxes(tickmode='array', tickvals=[2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True) 
            
            on = st.toggle("Advanced Insights")
            if on:            
                st.markdown('#### Area chart Quarter-wise Growth of App Opens in India ')
                
                map2 , table2 = st.columns((5,2),gap= 'large')   
                with map2:          
                    map_data = map_user_df[~map_user_df['Years'].isin([2024, 2018])].groupby(['Years', 'Quarter'])['AppOpens'].sum().reset_index()
                    fig = px.area(
                        map_data,
                        x='Quarter',
                        y='AppOpens',
                        color='Years',
                        title="Quarter-wise Growth of App Opens in India",
                        labels={'Quarter': 'Quarter', 'AppOpens': 'App Opens'},
                        hover_data={'AppOpens': ':.2f'}
                    )
                    fig.update_layout(margin=dict(t=50, b=50, l=50, r=50))
                    fig.update_xaxes(tickmode='array', tickvals=[1,2,3,4])
                    st.plotly_chart(fig, use_container_width=True)
                with table2:
                    df_map_data=map_data
                    df_map_data['Years'] = df_map_data['Years'].apply(lambda x: '{:.0f}'.format(x))
                    df_map_data["AppOpens"]=df_map_data["AppOpens"].apply(format_number)
                    df_map_data.rename(columns={"AppOpens": "App Opens"}, inplace=True)
                    st.markdown('#### Quarterly App Opens in India')
                    st.dataframe(df_map_data, use_container_width=True, hide_index=True)
                
                query15 = '''SELECT  Years, Quarter, 
                    SUM(AppOpens) AS AppOpens
                    FROM map_user
                    WHERE Years NOT IN (2024, 2018)
                    GROUP BY Years,quarter'''
                cursor.execute(query15)
                mydb.commit()
                table15 = cursor.fetchall()
                map_data1 = pd.DataFrame(table15, columns=["Years","Quarter","AppOpens"]) 
                st.markdown('#### Quarterly Distribution by App Opens for Each Year')
                years = map_data1['Years'].unique()
                num_columns = 3
                columns = st.columns(num_columns)
                for i, year in enumerate(years):
                    df_year_quarter = map_data1[map_data1['Years'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['AppOpens'], hole=.3)])
                        fig.update_layout(
                            title=f'App Opens Distribution for {year} - All Quarters',
                            height=550,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown('### App Opens for All Four Quarters Combined Across All Years')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    map_user_total = map_data1.groupby(['Quarter'])['AppOpens'].sum().reset_index()
                    fig_total = go.Figure(data=[go.Pie(labels=map_user_total['Quarter'], values=map_user_total['AppOpens'], hole=.3)])
                    fig_total.update_layout(
                        title='App Opens for All Quarters Combined',
                        height=550,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)                            
#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-7----------------------------------------------------------------- 

        if selected_insight == "7. Transaction Amount by State":
            st.markdown('#### Total Transaction Amount by State in India')
            query16 = '''SELECT States , 
                                SUM(Transaction_amount) AS Transaction_amount 
                        FROM aggregated_transaction 
                        GROUP BY States'''
            cursor.execute(query16)
            mydb.commit()
            table16 = cursor.fetchall()
            aggregated_data_state = pd.DataFrame(table16, columns=["States","Transaction_amount"]) 
            fig = px.bar(aggregated_data_state, x='States', y='Transaction_amount', height=700,
                        title='Transaction Amount by State in India',
                        labels={'Transaction_amount': 'Transaction Amount', 'States': 'States'},
                        color='States', color_discrete_sequence=px.colors.qualitative.Pastel1)
            fig.update_layout(legend_title="State List")
            st.plotly_chart(fig, use_container_width=True)
#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-8----------------------------------------------------------------- 

        if selected_insight == "8. Transaction Count by State":    
            st.markdown('#### Total Transaction Count by State in India')
            query17 = '''SELECT States , 
                                SUM(Transaction_count) AS Transaction_count 
                        FROM aggregated_transaction 
                        GROUP BY States'''
            cursor.execute(query17)
            mydb.commit()
            table17 = cursor.fetchall()
            aggregated_data_state = pd.DataFrame(table17, columns=["States","Transaction_count"])             
            fig = px.bar(aggregated_data_state, x='States', y='Transaction_count', 
                        title='Total Transaction Count by State in India',
                        labels={'Transaction_count': 'Transaction Count', 'States': 'States'},
                        color='States', color_discrete_sequence=px.colors.qualitative.Pastel1,height=700)
            fig.update_layout(legend_title="State List")
            st.plotly_chart(fig, use_container_width=True)     
#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-9----------------------------------------------------------------- 
        if selected_insight == "9. Transaction Count by Brand":
            st.markdown('#### Transaction Count by Brand')
            query21 = '''SELECT Brands, 
                                SUM(Transaction_count) AS Transaction_count 
                        FROM aggregated_user 
                        GROUP BY Brands'''
            cursor.execute(query21)
            mydb.commit()
            table21 = cursor.fetchall()
            agg_user_data = pd.DataFrame(table21, columns=["Brands","Transaction_count"])              
            fig = px.bar(agg_user_data, x='Brands', y='Transaction_count',
                        title='Total Registered User Count by Mobile Brand in India',
                        labels={'Transaction_count': 'Registered Users'}, 
                        color='Brands', color_discrete_sequence=px.colors.qualitative.Pastel1,height=700)

            fig.update_layout(barmode='stack', xaxis_title="Brands", yaxis_title="Registered Users")

            fig.update_traces(hovertemplate='Brands: %{x}<br>Registered Users: %{y}<extra></extra>')

            st.plotly_chart(fig, use_container_width=True)

#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-10-----------------------------------------------------------------   

        if selected_insight == "10. Insurance Premium Amount by State":
            st.markdown('#### Total Insurance Premium Amount by State in India')
            query18 = '''SELECT States , 
                                SUM(Transaction_amount) AS Transaction_amount 
                        FROM aggregated_insurance 
                        GROUP BY States'''
            cursor.execute(query18)
            mydb.commit()
            table18 = cursor.fetchall()
            aggregated_data_state = pd.DataFrame(table18, columns=["States","Transaction_amount"])   
            fig = px.bar(aggregated_data_state, x='States', y='Transaction_amount', height=700,
                        title='Insurance Premium Amount by State in India',
                        labels={'Transaction_amount': 'Insurance Premium Amount', 'States': 'States'},
                        color='States', color_discrete_sequence=px.colors.qualitative.Pastel1)
            fig.update_layout(legend_title="State List")
            st.plotly_chart(fig, use_container_width=True) 
        
#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-11----------------------------------------------------------------- 
        if selected_insight == "11. Insurance Premium Count by State":    
            st.markdown('#### Total Insurance Premium Count by State in India')
            query19 = '''SELECT States , 
                                SUM(Transaction_count) AS Transaction_count 
                        FROM aggregated_insurance
                        GROUP BY States'''
            cursor.execute(query19)
            mydb.commit()
            table19 = cursor.fetchall()
            aggregated_data_state = pd.DataFrame(table19, columns=["States","Transaction_count"])   
            fig = px.bar(aggregated_data_state, x='States', y='Transaction_count', 
                        title='Total Insurance Premium Count by State in India',
                        labels={'Transaction_count': 'Insurance Premium Count', 'States': 'States'},
                        color='States', color_discrete_sequence=px.colors.qualitative.Pastel1,height=700)
            fig.update_layout(legend_title="State List")
            st.plotly_chart(fig, use_container_width=True)                            
#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-12----------------------------------------------------------------- 
        if selected_insight == "12. Registered User by State":
            st.markdown('#### Total Registered User Count by State in India')
            query20 = '''SELECT States , 
                                SUM(RegisteredUsers) AS RegisteredUsers 
                        FROM map_user
                        GROUP BY States'''
            cursor.execute(query20)
            mydb.commit()
            table20 = cursor.fetchall()
            map_data_state = pd.DataFrame(table20, columns=["States","RegisteredUsers"])            
            fig = px.bar(map_data_state, x='States', y='RegisteredUsers',
                        title='Total Registered User by State in India',
                        labels={'RegisteredUsers': 'Registered User', 'States': 'States'},
                        color='States', color_discrete_sequence=px.colors.qualitative.Pastel1,height=700)
            fig.update_layout(legend_title="State List")
            st.plotly_chart(fig, use_container_width=True) 
#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-13-----------------------------------------------------------------      
        if selected_insight == "13. App Opens by State":
            st.markdown('#### Total App Opens Count by State in India')
            query20 = '''SELECT States , 
                                SUM(AppOpens) AS AppOpens 
                        FROM map_user
                        GROUP BY States'''
            cursor.execute(query20)
            mydb.commit()
            table20 = cursor.fetchall()
            map_data_state = pd.DataFrame(table20, columns=["States","AppOpens"])                 
            fig = px.bar(map_data_state, x='States', y='AppOpens',
                        title='Total App Opens by State in India',
                        labels={'AppOpens': 'App Opens', 'States': 'States'},
                        color='States', color_discrete_sequence=px.colors.qualitative.Pastel1,height=700)
            fig.update_layout(legend_title="State List")
            st.plotly_chart(fig, use_container_width=True) 
#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-14-----------------------------------------------------------------               
                
        
        if selected_insight == "14. State Wise - Brand & Count":
            query22 = '''SELECT States,
                                Brands, 
                                SUM(Transaction_count) AS Transaction_count 
                        FROM aggregated_user 
                        GROUP BY States,Brands'''
            cursor.execute(query22)
            mydb.commit()
            table22 = cursor.fetchall()
            agg_user_data = pd.DataFrame(table22, columns=["States","Brands","Transaction_count"]) 
            fig = px.bar(agg_user_data, x='Brands', y='Transaction_count', color='States',
                        title='Total Registered User Count by Mobile Brand in India',
                        labels={'Transaction_count': 'Registered Users', 'States': 'States'},
                        color_discrete_sequence=px.colors.qualitative.Pastel2_r, height=1000)

            fig.update_layout(barmode='stack', legend_title="States", xaxis_title="States", yaxis_title="Registered Users")

            fig.update_traces(showlegend=True, selector=dict(type='bar'))

            st.plotly_chart(fig, use_container_width=True)  
#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-15----------------------------------------------------------------- 
        
        if selected_insight == "15. Transaction Types Analysis by Years and Quarters":
            query23 = '''SELECT Years, 
                                Transaction_type, 
                                SUM(Transaction_amount) AS Transaction_amount 
                        FROM aggregated_transaction 
                        GROUP BY Years,Transaction_type'''
            cursor.execute(query23)
            mydb.commit()
            table23 = cursor.fetchall()
            aggregated_data_state = pd.DataFrame(table23, columns=["Years","Transaction_type","Transaction_amount"])                         
            st.markdown('#### Transaction Distribution by Year & Transaction Type')
            fig = go.Figure()
            aggregated_data_state['Years'] = aggregated_data_state['Years'].astype(str)
            years = aggregated_data_state['Years'].unique()
            for year in years:
                df_year = aggregated_data_state[aggregated_data_state['Years'] == year]
                fig.add_trace(go.Bar(
                    x=df_year['Transaction_type'],
                    y=df_year['Transaction_amount'],
                    name=year
                ))
            fig.update_layout(barmode='group',
                            title='Transaction Distribution by Year & Transaction Type',
                            xaxis_title='Transaction Type',
                            yaxis_title='Transaction Amount',
                            width=900, height=550)

            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('#### Transaction Distribution by Quarter & Transaction Type')
            query24 = '''SELECT Quarter, 
                                Transaction_type, 
                                SUM(Transaction_amount) AS Transaction_amount 
                        FROM aggregated_transaction 
                        GROUP BY Quarter,Transaction_type'''
            cursor.execute(query24)
            mydb.commit()
            table24 = cursor.fetchall()
            aggregated_data_state = pd.DataFrame(table24, columns=["Quarter","Transaction_type","Transaction_amount"])  
            fig = go.Figure()
            aggregated_data_state['Quarter'] = aggregated_data_state['Quarter'].astype(str)
            quarters = aggregated_data_state['Quarter'].unique()
            for quarter in quarters:
                df_quarter = aggregated_data_state[aggregated_data_state['Quarter'] == quarter]
                fig.add_trace(go.Bar(
                    x=df_quarter['Transaction_type'],
                    y=df_quarter['Transaction_amount'],
                    name=quarter
                ))
            fig.update_layout(barmode='group',
                            title='Transaction Distribution by Quarter & Transaction Type',
                            xaxis_title='Transaction Type',
                            yaxis_title='Transaction Amount',
                            width=900, height=550)

            st.plotly_chart(fig, use_container_width=True)
#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-16----------------------------------------------------------------- 

        if selected_insight=="16. Average Transaction Amount by Quarter":
            st.markdown('### Average Transaction Amount by Quarter')
            query26 = '''SELECT Quarter, 
                                AVG(Transaction_amount) AS Transaction_amount 
                        FROM aggregated_transaction 
                        GROUP BY Quarter'''
            cursor.execute(query26)
            mydb.commit()
            table26 = cursor.fetchall()
            avg_trans_amount_data = pd.DataFrame(table26, columns=["Quarter","Transaction_amount"])
            c1, c2 = st.columns((5,2),gap="large")
            with c1:
                avg_trans_amount_data['Transaction_amount']=avg_trans_amount_data['Transaction_amount'].apply(format_amount)
                fig16 = px.bar(avg_trans_amount_data, x='Quarter', y='Transaction_amount', title='Average Transaction Amount by Quarter')
                fig16.update_xaxes(tickmode='array', tickvals=[1,2,3,4])
                st.plotly_chart(fig16)
            with c2:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                avg_trans_amount_data.rename(columns={"Transaction_amount": "Transaction Amount"}, inplace=True)
                st.dataframe(avg_trans_amount_data, use_container_width=True, hide_index=True)

#------------------------------------------------------ALL INDIA INSIGHTS: INSIGHT-17----------------------------------------------------------------- 
        if selected_insight == '17. Percentage of Transactions by Type':
            st.markdown('### Percentage of Transactions by Type')
            query27 = '''WITH total_amount AS (
                            SELECT SUM(Transaction_amount) AS total_transaction_amount
                            FROM aggregated_transaction
                        )
                        SELECT 
                            Transaction_type,
                            SUM(Transaction_amount) AS Transaction_amount,
                            (SUM(Transaction_amount) / total_amount.total_transaction_amount) * 100 AS percentage
                        FROM 
                            aggregated_transaction, total_amount
                        GROUP BY 
                            Transaction_type, total_amount.total_transaction_amount;'''
            cursor.execute(query27)
            mydb.commit()
            table27 = cursor.fetchall()
            transaction_type_percentage = pd.DataFrame(table27, columns=["Transaction_type","Transaction_amount","Percentage"])
            c1, c2 = st.columns((5,2),gap="large")
            with c1:
                fig20 = px.pie(transaction_type_percentage, names='Transaction_type', values='Percentage', title='Percentage of Transactions by Type')
                st.plotly_chart(fig20)
            with c2:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                transaction_type_percentage["Percentage"] = transaction_type_percentage["Percentage"]#.apply(lambda x: "{:.2%}".format(x))
                transaction_type_percentage.rename(columns={"Transaction_amount": "Transaction Amount"}, inplace=True)
                st.dataframe(transaction_type_percentage, use_container_width=True, hide_index=True)

#------------------------------------------------------OPTION: STATE WISE INSIGHTS----------------------------------------------------------------- 
    if selected =="State-wise-Insights":

        col1,c1,c2,c3,c4,c5 = st.columns((1,0.8,1,1,1,1),gap="large")
        with col1:
            states = st.selectbox("#### Select State:", options=map_user_df["States"].unique())            

        map_user = map_user_df[map_user_df['States'] == states] 

        insight_options = [
            f'1. Yearly Growth of Transaction Amount in {states}',
            f'2. Yearly Growth of Transaction Count in {states}',
            f'3. Yearly Growth of Insurance Premium amount in {states}',
            f'4. Yearly Growth of Insurance Premium Count in {states}',
            f'5. Yearly Growth of Registered User in {states}',
            f'6. Yearly Growth of App Open in {states}',
            f'7. {states} - Transaction Amount by District',
            f'8. {states} - Transaction Count by District',
            f'9. {states} - Insurance Premium Amount by District',
            f'10. {states} - Insurance Premium Count by District',
            f'11. {states} - Registered User by District',
            f'12. {states} - App Opens by District',
            f'13. {states} - Average Transaction Amount by Quarter by District']

        selected_insight = st.selectbox("Select an Insights:", insight_options)


#------------------------------------------------------STATE INSIGHTS: INSIGHT-1-----------------------------------------------------------------     
        if selected_insight == f'1. Yearly Growth of Transaction Amount in {states}':
            st.markdown(f'#### Yearly Growth of Transaction Amount in {states}')
            query1 = '''SELECT Years, 
                        SUM(Transaction_amount) AS Transaction_amount 
                        FROM map_transaction
                         WHERE years != 2024 and STATES = %s
                        GROUP BY Years
                        ORDER BY Years'''
            cursor.execute(query1,(states,))
            mydb.commit()
            table1 = cursor.fetchall()
            aggregated_data_yearly = pd.DataFrame(table1, columns=["Years","Transaction_amount"])          
            aggregated_data_yearly['Transaction_amount']=aggregated_data_yearly['Transaction_amount'].apply(format_amount)
            fig = px.line(aggregated_data_yearly, x='Years', y='Transaction_amount', 
                   labels={'YearS': 'Years', 'Transaction_amount': 'Transaction Amount'}, 
                    title=f'Yearly Growth of Transaction Amount in {states}',markers=True)
            fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True) 
            
                            
            on2 = st.toggle("Advanced Insights", key="states_toggle2")

            if on2:
                st.markdown(f"#### Quarterly Distribution of Transaction Amounts by Year in {states}")
                map1 , table1 = st.columns((5,2),gap= 'large')   
                query2 = '''SELECT  Years, Quarter, 
                            SUM(Transaction_amount) AS Transaction_amount
                                    
                            FROM map_transaction 
                            WHERE STATES = %s
                            GROUP BY Years,Quarter'''
                cursor.execute(query2,(states,))
                mydb.commit()
                table2 = cursor.fetchall()
                aggregated_data1 = pd.DataFrame(table2, columns=["Years","Quarter","Transaction_amount"])                                   
                aggregated_data1['Transaction_amount']=aggregated_data1['Transaction_amount'].apply(format_amount)
                
                aggregated_data1['Years'] = aggregated_data1['Years'].astype(str)
                with map1:   
                    fig = px.box(aggregated_data1, x='Years', y='Transaction_amount', color='Quarter',
                                title=f'Box Plot of Quarterly Transaction Amount by Year in {states}',
                                points='all')
                               

                    st.plotly_chart(fig, use_container_width=True)
                with table1:  
                    df_aggregated_data1=aggregated_data1
                   
                    df_aggregated_data1.rename(columns={"Transaction_amount": "Transaction Amount"}, inplace=True)                    
                    st.markdown('#### Quarterly Transaction Distribution')
                    st.dataframe(df_aggregated_data1, use_container_width=True, hide_index=True)    


                query3 = '''SELECT  Years, Quarter, 
                        SUM(Transaction_amount) AS Transaction_amount 
                        FROM map_transaction 
                        WHERE years != 2024 and states = %s
                        GROUP BY Years,Quarter'''
                cursor.execute(query3,(states,))
                mydb.commit()
                table3 = cursor.fetchall()
                aggregated_data_state = pd.DataFrame(table3, columns=["Years","Quarter","Transaction_amount"])                 
                st.markdown(f'#### Quarterly Transaction Amount Distribution by Transaction Amount for Each Year - {states}')
                years = aggregated_data_state['Years'].unique()
                num_columns = 3
                columns = st.columns(num_columns)
                for i, year in enumerate(years):
                    df_year_quarter = aggregated_data_state[aggregated_data_state['Years'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_amount'], hole=.3)])
                        fig.update_layout(
                            title=f'Transaction Amount Distribution for {year} - All Quarters',
                            height=550,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown(f'### Aggregated Transaction Amount for All Four Quarters Combined Across All Years - {states}')            
                co1,co2,co3 = st.columns(3)
                with co2:
            
                    aggregated_total = aggregated_data_state.groupby(['Quarter'])['Transaction_amount'].sum().reset_index()
            
                    
                    fig_total = go.Figure(data=[go.Pie(labels=aggregated_total['Quarter'], values=aggregated_total['Transaction_amount'], hole=.3)])
                    fig_total.update_layout(
                        title='Aggregated Transaction Amount for All Quarters Combined',
                        height=550,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)    

#------------------------------------------------------STATE INSIGHTS: INSIGHT-2----------------------------------------------------------------- 
        if selected_insight == f'2. Yearly Growth of Transaction Count in {states}':
            st.markdown(f'#### Yearly Growth of Transaction Count in {states}')
            query4 = '''SELECT  years,
                    SUM(transaction_count) AS transaction_count
                    FROM map_transaction
                    WHERE years != 2024 and states = %s
                    GROUP BY Years
                    ORDER BY Years'''
            cursor.execute(query4,(states,))
            mydb.commit()
            table4 = cursor.fetchall()
            aggregated_data_yearly_count = pd.DataFrame(table4, columns=["Years","Transaction_count"])             
            aggregated_data_yearly_count['Transaction_count']=aggregated_data_yearly_count['Transaction_count'].apply(format_number)
            fig = px.line(aggregated_data_yearly_count, x='Years', y='Transaction_count', 
                            labels={'Years': 'Years', 'Transaction_count': 'Transaction Count'}, 
                            title=f'Yearly Growth of Transaction Count in {states}', markers=True)
            #fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True)   
            
            on3 = st.toggle("Advanced Insights", key="states_toggle3")

            if on3:
                map2 , table2 = st.columns((5,2),gap= 'large')   
                query5 = '''SELECT  years, quarter,                     
                    SUM(transaction_count) AS transaction_count
                    FROM map_transaction
                    WHERE states = %s
                    GROUP BY years,quarter'''
                cursor.execute(query5,(states,))
                mydb.commit()
                table5 = cursor.fetchall()
                aggregated_data1 = pd.DataFrame(table5, columns=["Years","Quarter","Transaction_count"])                 
                
                aggregated_data1['Transaction_count']=aggregated_data1['Transaction_count'].apply(format_number)
                aggregated_data1['Years'] = aggregated_data1['Years'].astype(str)
                with map2:   
                    st.markdown(f'#### Box Plot of Quarterly Transaction Count by Year in {states}')
                    fig = px.box(aggregated_data1, x='Years', y='Transaction_count', color='Quarter',
                                title=f'Box Plot of Quarterly Transaction Count by Year in {states}',
                                points='all') 
                             

                    st.plotly_chart(fig, use_container_width=True)
                with table2:  
                    df_aggregated_data1=aggregated_data1
                   
                    df_aggregated_data1.rename(columns={"Transaction_count": "Transaction Count"}, inplace=True)
                    st.markdown('#### Quarterly Transaction Count Distribution')
                    st.dataframe(df_aggregated_data1, use_container_width=True, hide_index=True)   
                    

                query6 = '''SELECT  years, quarter, 
                        SUM(transaction_count) AS transaction_count
                        FROM map_transaction
                        WHERE years != 2024 and states = %s
                        GROUP BY years,quarter'''
                cursor.execute(query6,(states,))
                mydb.commit()
                table6 = cursor.fetchall()
                aggregated_data_state = pd.DataFrame(table6, columns=["Years","Quarter","Transaction_count"]) 
                st.markdown(f'#### Quarterly Transaction Count Distribution by Transaction Count for Each Year - {states}')
                years = aggregated_data_state['Years'].unique()

           
                num_columns = 3
                columns = st.columns(num_columns)
                for i, year in enumerate(years):
                    df_year_quarter = aggregated_data_state[aggregated_data_state['Years'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_count'], hole=.3)])
                        fig.update_layout(
                            title=f'Transaction Count Distribution for {year} - All Quarters',
                            height=550,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown(f'### Aggregated Transaction Count for All Four Quarters Combined Across All Years - {states}')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    aggregated_total = aggregated_data_state.groupby(['Quarter'])['Transaction_count'].sum().reset_index()
                    fig_total = go.Figure(data=[go.Pie(labels=aggregated_total['Quarter'], values=aggregated_total['Transaction_count'], hole=.3)])
                    fig_total.update_layout(
                        title='Aggregated Transaction Count for All Quarters Combined',
                        height=550,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)

#------------------------------------------------------STATE INSIGHTS: INSIGHT-3----------------------------------------------------------------- 

        
        if selected_insight == f'3. Yearly Growth of Insurance Premium amount in {states}':
            st.markdown(f'#### Yearly Growth of Insurance Premium Amount in {states}')
            query7 = '''SELECT  Years, 
                    SUM(Transaction_amount) AS Transaction_amount
                    FROM map_insurance
                    WHERE years != 2024 and states = %s                  
                    GROUP BY Years
                    ORDER BY Years'''
            cursor.execute(query7,(states,))
            mydb.commit()
            table7= cursor.fetchall()
            map_ins_yearly = pd.DataFrame(table7, columns=["Years","Transaction_amount"])             
            map_ins_yearly['Transaction_amount']=map_ins_yearly['Transaction_amount'].apply(format_amount)
            fig = px.line(map_ins_yearly, x='Years', y='Transaction_amount', 
                    labels={'Years': 'Years', 'Transaction_amount': 'Insurance Premium Amount'}, 
                    title=f'Yearly Growth of Insurance Premium Amount in {states}', markers=True)
            fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True) 
            
                            
            on4 = st.toggle("Advanced Insights",key="states_toggle4")

            if on4:
                st.markdown(f"#### Quarterly Distribution of Insurance Premium Amount by Year in {states}")
                map3 , table3 = st.columns((5,2),gap= 'large')   
                query8 = '''SELECT  Years, Quarter, 
                    SUM(Transaction_amount) AS Transaction_amount 
                    FROM map_insurance
                    WHERE STATEs = %s                
                    GROUP BY Years,Quarter
                    '''
                cursor.execute(query8,(states,))
                mydb.commit()
                table8 = cursor.fetchall()
                map_ins_data1 = pd.DataFrame(table8, columns=["Years","Quarter","Transaction_amount"])                
                map_ins_data1['Transaction_amount']=map_ins_data1['Transaction_amount'].apply(format_amount)
                
                map_ins_data1['Years'] = map_ins_data1['Years'].astype(str)
                with map3:   

                    fig = px.box(map_ins_data1, x='Years', y='Transaction_amount', color='Quarter',
                                title=f'Box Plot of Quarterly Insurance Premium Amount by Year in {states}',
                                points='all')  
                               

                    st.plotly_chart(fig, use_container_width=True)
                with table3:  
                    df_agg_ins_data1=map_ins_data1
                   
                    df_agg_ins_data1.rename(columns={"Transaction_amount": "Transaction Amount"}, inplace=True)
                    st.markdown('#### Quarterly Insurance Premium Amount Distribution')
                    st.dataframe(df_agg_ins_data1, use_container_width=True, hide_index=True)



                query9 = '''SELECT  Years, Quarter, 
                        SUM(Transaction_amount) AS Transaction_amount
                        FROM map_insurance
                        WHERE years != 2024 and states = %s                     
                        GROUP BY Years,Quarter'''
                cursor.execute(query9,(states,))
                mydb.commit()
                table9 = cursor.fetchall()
                map_ins_state = pd.DataFrame(table9, columns=["Years","Quarter","Transaction_amount"])   
                st.markdown(f'#### Quarterly Transaction Amount Distribution by Insurance Premium Amount for Each Year - {states}')
                years = map_ins_state['Years'].unique()
                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = map_ins_state[map_ins_state['Years'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_amount'], hole=.3)])
                        fig.update_layout(
                            title=f'Premium Amount Distribution for {year} - All Quarters',
                            height=550,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown(f'### Insurance Premium Amount for All Four Quarters Combined Across All Years - {states}')            
                co1,co2,co3 = st.columns(3)
                with co2:

                    map_ins_total = map_ins_state.groupby(['Quarter'])['Transaction_amount'].sum().reset_index()
                
                    
                    fig_total = go.Figure(data=[go.Pie(labels=map_ins_total['Quarter'], values=map_ins_total['Transaction_amount'], hole=.3)])
                    fig_total.update_layout(
                        title='Insurance Premium Amount for All Quarters Combined',
                        height=550,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)    

#------------------------------------------------------STATE INSIGHTS: INSIGHT-4----------------------------------------------------------------- 

        if selected_insight == f'4. Yearly Growth of Insurance Premium Count in {states}':
            st.markdown(f'#### Yearly Growth of Insurance Premium Count in {states}')
            query10 = '''SELECT  Years, 
                    SUM(Transaction_count) AS Transaction_count
                    FROM map_insurance
                    WHERE years != 2024 and states = %s                     
                    GROUP BY Years
                    ORDER BY Years'''
            cursor.execute(query10,(states,))
            mydb.commit()
            table10= cursor.fetchall()
            map_ins_data_yearly_count = pd.DataFrame(table10, columns=["Years","Transaction_count"])                 
            map_ins_data_yearly_count['Transaction_count']=map_ins_data_yearly_count['Transaction_count'].apply(format_number)
            fig = px.line(map_ins_data_yearly_count, x='Years', y='Transaction_count', 
                            labels={'Year': 'Years', 'Transaction_count': 'Insurance Premium Count'}, 
                            title=f'Yearly Growth of Insurance Premium Count in {states}',markers=True)
            fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True)   
            
            on5 = st.toggle("Advanced Insights", key="states_toggle5")

            if on5:
                map4 , table4 = st.columns((5,2),gap= 'large')   
                query11 = '''SELECT  Years, Quarter, 
                    SUM(Transaction_count) AS Transaction_count
                    FROM map_insurance
                    where states = %s                    
                    GROUP BY Years,Quarter'''
                cursor.execute(query11,(states,))
                mydb.commit()
                table11 = cursor.fetchall()
                aggregated_data1 = pd.DataFrame(table11, columns=["Years","Quarter","Transaction_count"])                
                
                aggregated_data1['Transaction_count']=aggregated_data1['Transaction_count'].apply(format_number)
                aggregated_data1['Years'] = aggregated_data1['Years'].astype(str)
                with map4:   
                    st.markdown(f'#### Box Plot of Quarterly Insurance Premium Count by Year in {states}')
                    fig = px.box(aggregated_data1, x='Years', y='Transaction_count', color='Quarter',
                                title=f'Box Plot of Quarterly Insurance Premium Count by Year in {states}',
                                points='all')
                               

                    st.plotly_chart(fig, use_container_width=True)
                with table4:  
                    df_aggregated_data1=aggregated_data1
                    
                    df_aggregated_data1.rename(columns={"Transaction_count": "Transaction Count"}, inplace=True)
                    st.markdown('#### Quarterly Insurance Premium Count Distribution')
                    st.dataframe(df_aggregated_data1, use_container_width=True, hide_index=True)
                    

                query12 = '''SELECT  Years, Quarter, 
                        SUM(Transaction_count) AS Transaction_count
                        FROM map_insurance
                        WHERE years != 2024 and states = %s                      
                        GROUP BY Years,Quarter'''
                cursor.execute(query12,(states,))
                mydb.commit()
                table12 = cursor.fetchall()
                aggregated_data_state = pd.DataFrame(table12, columns=["Years","Quarter","Transaction_count"])                
                st.markdown(f'#### Quarterly Distribution by Insurance Premium Count for Each Year - {states}')
                years = aggregated_data_state['Years'].unique()
                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = aggregated_data_state[aggregated_data_state['Years'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['Transaction_count'], hole=.3)])
                        fig.update_layout(
                            title=f'Premium Count Distribution for {year} - All Quarters',
                            height=550,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown(f'### Insurance Premium Count for All Four Quarters Combined Across All Years - {states}')            
                co1,co2,co3 = st.columns(3)
                with co2:

                    aggregated_total = aggregated_data_state.groupby(['Quarter'])['Transaction_count'].sum().reset_index()

                    
                    fig_total = go.Figure(data=[go.Pie(labels=aggregated_total['Quarter'], values=aggregated_total['Transaction_count'], hole=.3)])
                    fig_total.update_layout(
                        title='Insurance Premium Count for All Quarters Combined',
                        height=550,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)



#------------------------------------------------------STATE INSIGHTS: INSIGHT-5-----------------------------------------------------------------         
        if selected_insight == f"5. Yearly Growth of Registered User in {states}":
    
            st.markdown(f'#### Yearly Growth of Registered User in {states}')
            query13 = '''SELECT  Years, 
                    SUM(RegisteredUsers) AS RegisteredUsers
                    FROM map_user
                    WHERE years != 2024 and states = %s                  
                    GROUP BY Years
                    ORDER BY Years'''
            cursor.execute(query13,(states,))
            mydb.commit()
            table13= cursor.fetchall()
            map_user_yearly = pd.DataFrame(table13, columns=["Years","RegisteredUsers"])              
            map_user_yearly['RegisteredUsers']=map_user_yearly['RegisteredUsers'].apply(format_number)
            fig = px.line(map_user_yearly, x='Years', y='RegisteredUsers',
                            labels={'Years': 'Years', 'RegisteredUsers': 'Registered User'}, title=f'Yearly Growth of Registered User in {states}',markers=True)
            fig.update_xaxes(tickmode='array', tickvals=[2018,2019,2020,2021,2022,2023,2024])
            st.plotly_chart(fig, use_container_width=True)
            
            on6 = st.toggle("Advanced Insights", key="states_toggle6")

            if on6:            
                st.markdown(f'#### Area chart Quarter-wise Growth of Registered User in {states} ')
                query14 = '''SELECT  Years, Quarter, 
                    SUM(RegisteredUsers) AS RegisteredUsers
                    FROM map_user
                    WHERE years !=2024 and states = %s                   
                    GROUP BY Years,Quarter'''
                cursor.execute(query14,(states,))
                mydb.commit()
                table14 = cursor.fetchall()
                map_data1 = pd.DataFrame(table14, columns=["Years","Quarter","RegisteredUsers"])      
                map5 , table5 = st.columns((5,2),gap= 'large')   
                with map5:                             
                    map_data = map_user[map_user['Years'] != 2024].groupby(['Years', 'Quarter'])['RegisteredUsers'].sum().reset_index()
                    fig = px.area(
                        map_data,
                        x='Quarter',
                        y='RegisteredUsers',
                        color='Years',
                        title=f"Quarter-wise Growth of Registered User in {states}",
                        labels={'Quarter': 'Quarter', 'RegisteredUsers': 'Registered User'},
                        hover_data={'RegisteredUsers': ':.2f'}
                    )
                    fig.update_layout(margin=dict(t=50, b=50, l=50, r=50))
                    fig.update_xaxes(tickmode='array', tickvals=[1,2,3,4])
                    st.plotly_chart(fig, use_container_width=True)
                with table5:
                    df_map_data=map_data
                    df_map_data['Years'] = df_map_data['Years'].apply(lambda x: '{:.0f}'.format(x))
                    df_map_data["RegisteredUsers"]=df_map_data["RegisteredUsers"].apply(format_number)
                    df_map_data.rename(columns={"RegisteredUsers": "RegisteredUsers Users"}, inplace=True)
                    st.markdown('#### Quarterly Registered User in India')
                    st.dataframe(df_map_data, use_container_width=True, hide_index=True)
                                    

                st.markdown(f'#### Quarterly Distribution by Registered User for Each Year - {states}')
                years = map_data1['Years'].unique()
                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = map_data1[map_data1['Years'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['RegisteredUsers'], hole=.3)])
                        fig.update_layout(
                            title=f'Registered User Distribution for {year} - All Quarters',
                            height=550,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown(f'### Registered User for All Four Quarters Combined Across All Years -states')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    map_user_total = map_data1.groupby(['Quarter'])['RegisteredUsers'].sum().reset_index()

                    fig_total = go.Figure(data=[go.Pie(labels=map_user_total['Quarter'], values=map_user_total['RegisteredUsers'], hole=.3)])
                    fig_total.update_layout(
                        title='Registered User for All Quarters Combined',
                        height=550,
                    )
                    st.plotly_chart(fig_total, use_container_width=True)



#------------------------------------------------------STATE INSIGHTS: INSIGHT-6----------------------------------------------------------------- 
        if selected_insight == f"6. Yearly Growth of App Open in {states}":
            st.markdown(f'#### Yearly Growth of App Opens in {states}')
            query15 = '''SELECT  Years, 
                    SUM(AppOpens) AS AppOpens
                    FROM map_user
                    WHERE years NOT IN (2018,2024) and states = %s            
                    GROUP BY Years
                    ORDER BY Years'''
            cursor.execute(query15,(states,))
            mydb.commit()
            table15= cursor.fetchall()
            map_user_years_appopens = pd.DataFrame(table15, columns=["Years","AppOpens"])             
            map_user_years_appopens['AppOpens']=map_user_years_appopens['AppOpens'].apply(format_number)
            fig = px.line(map_user_years_appopens, x='Years', y='AppOpens', 
                            labels={'Years': 'Years', 'AppOpens': 'App Opens'},title=f'Yearly Growth of App Opens in {states}',markers=True)
            fig.update_xaxes(tickmode='array', tickvals=[2019,2020,2021,2022,2023])
            st.plotly_chart(fig, use_container_width=True) 
            
            on5 = st.toggle("Advanced Insights", key="states_toggle5")

            if on5:            
                st.markdown(f'#### Area chart Quarter-wise Growth of App Opens in {states} ')
                map6 , table6 = st.columns((5,2),gap= 'large')  
                with map6:                
                    map_data = map_user[~map_user['Years'].isin([2024, 2018])].groupby(['Years', 'Quarter'])['AppOpens'].sum().reset_index()
                    fig = px.area(
                        map_data,
                        x='Quarter',
                        y='AppOpens',
                        color='Years',
                        title=f"Quarter-wise Growth of App Opens in {states}",
                        labels={'Quarter': 'Quarter', 'AppOpens': 'App Opens'},
                        hover_data={'AppOpens': ':.2f'}
                    )
                    fig.update_layout(margin=dict(t=50, b=50, l=50, r=50))
                    fig.update_xaxes(tickmode='array', tickvals=[1,2,3,4])
                    st.plotly_chart(fig, use_container_width=True)
                with table6:
                    df_map_data=map_data
                    df_map_data['Years'] = df_map_data['Years'].apply(lambda x: '{:.0f}'.format(x))
                    df_map_data["AppOpens"]=df_map_data["AppOpens"].apply(format_number)
                    df_map_data.rename(columns={"AppOpens": "App Opens"}, inplace=True)
                    st.markdown('#### Quarterly App Opens in India')
                    st.dataframe(df_map_data, use_container_width=True, hide_index=True)
                                        
                query16 = '''SELECT  Years, quarter, 
                    SUM(AppOpens) AS AppOpens
                    FROM map_user
                    WHERE years NOT IN (2024, 2018) and states = %s           
                    GROUP BY Years,quarter'''
                cursor.execute(query16,(states,))
                mydb.commit()
                table16 = cursor.fetchall()
                map_user_state = pd.DataFrame(table16, columns=["Years","Quarter","AppOpens"]) 
                                
                st.markdown(f'#### Quarterly Distribution by App Opens for Each Year - {states}')

                years = map_user_state['Years'].unique()

                num_columns = 3
                columns = st.columns(num_columns)

                for i, year in enumerate(years):
                    df_year_quarter = map_user_state[map_user_state['Years'] == year]
                    if not df_year_quarter.empty:
                        fig = go.Figure(data=[go.Pie(labels=df_year_quarter['Quarter'], values=df_year_quarter['AppOpens'], hole=.3)])
                        fig.update_layout(
                            title=f'App Opens Distribution for {year} - All Quarters',
                            height=550,
                        )
                        with columns[i % num_columns]:
                            st.markdown(f"### Year: {year}")
                            st.plotly_chart(fig, use_container_width=True)
                                
                st.markdown(f'### App Opens for All Four Quarters Combined Across All Years - {states}')            
                co1,co2,co3 = st.columns(3)
                with co2:
                    map_user_total = map_user_state.groupby(['Quarter'])['AppOpens'].sum().reset_index()
                    fig_total = go.Figure(data=[go.Pie(labels=map_user_total['Quarter'], values=map_user_total['AppOpens'], hole=.3)])
                    fig_total.update_layout(
                        title='App Opens for All Quarters Combined',
                        height=550,
                    )
                    st.plotly_chart(fig_total, use_container_width=True) 


#------------------------------------------------------STATE INSIGHTS: INSIGHT-7-----------------------------------------------------------------    
        if selected_insight == f'7. {states} - Transaction Amount by District':
            st.markdown(f'#### Total Transaction Amount by District in {states}')
            query17 = '''SELECT Districts , 
                                SUM(Transaction_amount) AS Transaction_amount 
                        FROM map_transaction
                        where states = %s                      
                        GROUP BY Districts'''
            cursor.execute(query17,(states,))
            mydb.commit()
            table17 = cursor.fetchall()
            aggregated_data_state = pd.DataFrame(table17, columns=["Districts","Transaction_amount"])             
            fig = px.bar(aggregated_data_state, x='Districts', y='Transaction_amount', height=700,
                        title=f'Transaction Amount by District in {states}',
                        labels={'Transaction_amount': 'Transaction Amount', 'Districts': 'District'},
                        color='Districts', color_discrete_sequence=px.colors.qualitative.Pastel1)
            fig.update_layout(legend_title="District List")
            st.plotly_chart(fig, use_container_width=True)



#------------------------------------------------------STATE INSIGHTS: INSIGHT-8-----------------------------------------------------------------   
        if selected_insight == f'8. {states} - Transaction Count by District':    
            st.markdown(f'#### Total Transaction Count by District in {states}')
            query18 = '''SELECT Districts , 
                                SUM(transaction_count) AS transaction_count 
                        FROM map_transaction
                        where states = %s              
                        GROUP BY Districts'''
            cursor.execute(query18,(states,))
            mydb.commit()
            table18 = cursor.fetchall()
            aggregated_data_state = pd.DataFrame(table18, columns=["Districts","Transaction_count"])             
            fig = px.bar(aggregated_data_state, x='Districts', y='Transaction_count', 
                        title=f'Total Transaction Count by District in {states}',
                        labels={'Transaction_count': 'Transaction Count', 'Districts': 'District'},
                        color='Districts', color_discrete_sequence=px.colors.qualitative.Pastel1,height=700)
            fig.update_layout(legend_title="District List")
            st.plotly_chart(fig, use_container_width=True)



#------------------------------------------------------STATE INSIGHTS: INSIGHT-9-----------------------------------------------------------------   
        if selected_insight == f'9. {states} - Insurance Premium Amount by District':
            st.markdown(f'#### Total Insurance Premium Amount by District in {states}')
            query19 = '''SELECT Districts , 
                                SUM(Transaction_amount) AS Transaction_amount 
                        FROM map_insurance
                        where states = %s            
                        GROUP BY Districts'''
            cursor.execute(query19,(states,))
            mydb.commit()
            table19 = cursor.fetchall()
            aggregated_data_state = pd.DataFrame(table19, columns=["Districts","Transaction_amount"])               
            fig = px.bar(aggregated_data_state, x='Districts', y='Transaction_amount', height=700,
                        title=f'Insurance Premium Amount by District in {states}',
                        labels={'Transaction_amount': 'Insurance Premium Amount', 'Districts': 'District'},
                        color='Districts', color_discrete_sequence=px.colors.qualitative.Pastel1)
            fig.update_layout(legend_title="District List")
            st.plotly_chart(fig, use_container_width=True)



#------------------------------------------------------STATE INSIGHTS: INSIGHT-10-----------------------------------------------------------------   
        if selected_insight ==f'10. {states} - Insurance Premium Count by District':    
            st.markdown(f'#### Total Insurance Premium Count by District in {states}')
            query20 = '''SELECT Districts , 
                                SUM(transaction_count) AS transaction_count 
                        FROM map_insurance
                        where States = %s
                        GROUP BY Districts'''
            cursor.execute(query20,(states,))
            mydb.commit()
            table20 = cursor.fetchall()
            aggregated_data_state = pd.DataFrame(table20, columns=["Districts","Transaction_count"])               
            fig = px.bar(aggregated_data_state, x='Districts', y='Transaction_count', 
                        title=f'Total Insurance Premium Count by District in {states}',
                        labels={'Transaction_count': 'Insurance Premium Count', 'Districts': 'Districts'},
                        color='Districts', color_discrete_sequence=px.colors.qualitative.Pastel1,height=700)
            fig.update_layout(legend_title="District List")
            st.plotly_chart(fig, use_container_width=True) 



#------------------------------------------------------STATE INSIGHTS: INSIGHT-11----------------------------------------------------------------- 
        if selected_insight == f'11. {states} - Registered User by District':
            st.markdown(f'#### Total Registered User Count by District in {states}')
            query21 = '''SELECT Districts , 
                                SUM(RegisteredUsers) AS RegisteredUsers 
                        FROM map_user
                        where states = %s                    
                        GROUP BY Districts'''
            cursor.execute(query21,(states,))
            mydb.commit()
            table21 = cursor.fetchall()
            map_data_state = pd.DataFrame(table21, columns=["Districts","RegisteredUsers"])               
            fig = px.bar(map_data_state, x='Districts', y='RegisteredUsers',
                        title=f'Total Registered User by District in {states}',
                        labels={'RegisteredUsers': 'Registered User', 'Districts': 'District'},
                        color='Districts', color_discrete_sequence=px.colors.qualitative.Pastel1,height=700)
            fig.update_layout(legend_title="District List")
            st.plotly_chart(fig, use_container_width=True)



#------------------------------------------------------STATE INSIGHTS: INSIGHT-12-----------------------------------------------------------------       
        if selected_insight == f'12. {states} - App Opens by District':

            st.markdown(f'#### Total App Opens Count by District in {states}')
            query22 = '''SELECT Districts , 
                                SUM(AppOpens) AS AppOpens 
                        FROM map_user
                        where states = %s                      
                        GROUP BY Districts'''
            cursor.execute(query22,(states,))
            mydb.commit()
            table22 = cursor.fetchall()          
            map_data_state = map_user.groupby('Districts')['AppOpens'].sum().reset_index()
            fig = px.bar(map_data_state, x='Districts', y='AppOpens',
                        title=f'Total App Opens by District in {states}',
                        labels={'AppOpens': 'App Opens', 'Districts': 'District'},
                        color='Districts', color_discrete_sequence=px.colors.qualitative.Pastel1,height=700)
            fig.update_layout(legend_title="District List")
            st.plotly_chart(fig, use_container_width=True)



#------------------------------------------------------STATE INSIGHTS: INSIGHT-13----------------------------------------------------------------- 
        if selected_insight==f'13. {states} - Average Transaction Amount by Quarter by District':
            st.markdown(f'### Average Transaction Amount by Quarter in {states}')
            query23 = '''SELECT Quarter, 
                                AVG(Transaction_amount) AS Transaction_amount 
                        FROM map_transaction
                        where states = %s                        
                        GROUP BY Quarter'''
            cursor.execute(query23,(states,))
            mydb.commit()
            table23 = cursor.fetchall()
            avg_trans_amount_data = pd.DataFrame(table23, columns=["Quarter","Transaction_amount"])            
            c1, c2 = st.columns((5,2),gap="large")
            with c1:
                avg_trans_amount_data['Transaction_amount']=avg_trans_amount_data['Transaction_amount'].apply(format_amount)
                fig16 = px.bar(avg_trans_amount_data, x='Quarter', y='Transaction_amount', title='Average Transaction Amount by Quarter')
                fig16.update_xaxes(tickmode='array', tickvals=[1,2,3,4])
                st.plotly_chart(fig16)
            with c2:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                avg_trans_amount_data.rename(columns={"Transaction_amount": "Transaction Amount"}, inplace=True)
                st.dataframe(avg_trans_amount_data, use_container_width=True, hide_index=True)


#-------------------------------------------------------------END OF THE PROJECT------------------------------------------------------------------------

