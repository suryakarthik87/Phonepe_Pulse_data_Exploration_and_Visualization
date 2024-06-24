#---------------------------------------------IMPORTING PACKAGES---------------------------------------------
import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import json
import requests
from PIL import Image


#------------------------------------------------SQL CONNECTION-----------------------------------------------

mydb = psycopg2.connect(host = "localhost",
                        port = "5432",
                        user = "postgres",
                        password = "karthik",
                        database = "phonepe")

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

#---------------------------------------FUNCTION FOR TRANSACTION AMOUNT AND COUNT USING YEARLY-------------------------------------------------

def transaction_amount_count_Y(df,year):
    tacy = df[df["Years"] == year]
    tacy.reset_index(drop=True, inplace = True)

    tacyg = tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    st.write(f" TRANSACTION DETAILS FOR THE YEAR {year}")
    st.dataframe(tacyg)
    
    col1,col2 = st.columns(2)
    with col1:

        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount", title = f" TRANSACTION AMOUNT FOR THE YEAR {year}",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count = px.bar(tacyg, x="States", y="Transaction_count", title = f"TRANSACTION COUNT FOR THE YEAR {year}",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600)
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)

    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        states_name = []
        data1 = json.loads(response.content)
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                    color = "Transaction_amount", color_continuous_scale = "Rainbow",
                                    range_color = (tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max() ),
                                    hover_name = "States", title = f"TRANSACTION AMOUNT FOR THE YEAR {year}", fitbounds="locations",
                                    height = 600, width = 600)
        
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(tacyg, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                    color = "Transaction_count", color_continuous_scale = "Rainbow",
                                    range_color = (tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max() ),
                                    hover_name = "States", title = f"TRANSACTION COUNT FOR THE YEAR {year} ", fitbounds="locations",
                                    height = 600, width = 600)
        
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)

    return tacy

#--------------------------------------FUNCTION FOR TRANSACTION AMOUNT AND COUNT USING QUARTERLY-----------------------------------
def transaction_amount_count_Y_Q(df,quarter):
    tacy = df[df["Quarter"] == quarter]
    tacy.reset_index(drop=True, inplace = True)

    tacyg = tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    st.write(f"Q{quarter}: TRANSACTION DETAILS FOR THE YEAR {tacy['Years'].min()} ")
    st.dataframe(tacyg)
    col1,col2 = st.columns(2)
    
    with col1:
    
        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount", title = f"Q{quarter}: TRANSACTION AMOUNT FOR THE YEAR {tacy['Years'].min()} ",
                            color_discrete_sequence=px.colors.sequential.PuBu, height=650, width=600)
        st.plotly_chart(fig_amount)
    
    with col2:

        fig_count = px.bar(tacyg, x="States", y="Transaction_count", title = f"Q{quarter}: TRANSACTION COUNT FOR THE YEAR {tacy['Years'].min()}",
                            color_discrete_sequence=px.colors.sequential.PuBu, height=650, width=600)
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        states_name = []
        data1 = json.loads(response.content)
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                    color = "Transaction_amount", color_continuous_scale = "Rainbow",
                                    range_color = (tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max() ),
                                    hover_name = "States", title = f"Q{quarter}: TRANSACTION AMOUNT FOR THE YEAR {tacy['Years'].min()}",
                                    fitbounds="locations",height = 600, width = 600)
        
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2 = px.choropleth(tacyg, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                    color = "Transaction_count", color_continuous_scale = "Rainbow",
                                    range_color = (tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max() ),
                                    hover_name = "States", title = f"Q{quarter}: TRANSACTION COUNT FOR THE YEAR {tacy['Years'].min()}",
                                    fitbounds="locations",height = 600, width = 600)
        
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)

    return tacy

#-----------------------------------------------FUNCTION FOR AGGREGATED TRANSACTION USING TRANSACTION TYPE------------------------------
def Agg_trans_trans_type(df,state):

    tacy = df[df["States"] == state]
    tacy.reset_index(drop=True, inplace = True)
    
    tacyg = tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    st.write(f"{state.upper()}: TRANSACTION TYPE DETAILS")
    st.dataframe(tacyg)
    col1,col2 = st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_amount",
                        width=600, title=f"{state.upper()}: TRANSACTION TYPE AND AMOUNT", hole=0.5)
        st.plotly_chart(fig_pie_1)
    with col2:
        fig_pie_2 = px.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_count",
                        width=600, title=f"{state.upper()}: TRANSACTION TYPE AND COUNT", hole=0.5)
        st.plotly_chart(fig_pie_2)


#--------------------------FUNCTION FOR AGGREGATED USER ANALYSIS FOR BRANDS AND TRANSACTION COUNT YEARLY----------------------------
def Agg_user_plot_1(df,year):
    aguy= df[df["Years"] == year]
    aguy.reset_index(drop=True, inplace=True)
    
    aguyg =pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)
    col1,col2 = st.columns(2)
    with col2:
        st.write(f"TRANSACTION COUNT OF BRANDS FOR THE YEAR {year}")
        st.dataframe(aguyg,use_container_width=True,)
       
    with col1:   
        fig_bar_1 = px.bar(aguyg, x = "Brands", y = "Transaction_count", title=f"TRANSACTION COUNT OF BRANDS FOR THE YEAR {year}",
                        width = 1500, color_discrete_sequence= px.colors.sequential.Bluyl_r, hover_name="Brands")
        st.plotly_chart(fig_bar_1)

    return aguy

#--------------------------FUNCTION FOR AGGREGATED USER ANALYSIS FOR BRANDS AND TRANSACTION COUNT QUARTERLY----------------------------

def Agg_user_plot_2(df,quarter):
    aguyq= df[df["Quarter"] == quarter]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col2:
        st.write(f"Q{quarter}: TRANSACTION COUNT OF BRANDS")
        st.dataframe(aguyqg,use_container_width=True,)
       
    with col1:
        fig_bar_1 = px.bar(aguyqg, x = "Brands", y = "Transaction_count", title=f"Q{quarter}: TRANSACTION COUNT OF BRANDS",
                            width = 1000, color_discrete_sequence= px.colors.sequential.Bluyl_r, hover_name="Brands")
        st.plotly_chart(fig_bar_1)

    return aguyq

#--------------------------FUNCTION FOR AGGREGATED USER ANALYSIS PERCENTAGE FOR BRANDS AND TRANSACTION COUNT STATE WISE----------------------------
def Agg_user_plot_3(df, state):
    auyqs= df[df["States"]== state]
    auyqs.reset_index(drop=True,inplace=True)

    auyqsg=pd.DataFrame(auyqs.groupby("Brands")["Percentage"].sum())
    auyqsg.reset_index(inplace=True)
    
    col1,col2 = st.columns(2)
    with col2:
        st.write(f"{state.upper()}: PERCENTAGE OF BRANDS")
        st.dataframe(auyqsg,use_container_width=True,)
       
    with col1:
        fig_line_1 = px.line(auyqs, x= "Brands", y = "Transaction_count", hover_data= "Percentage",
                            title = f"{state.upper()}: PERCENTAGE OF BRANDS", width=1000, markers = True)

        st.plotly_chart(fig_line_1)
    

#-----------------------------FUNCTION FOR MAP INSURANCE TRANSACTION AMOUNT AND COUNT DISTRICT WISE-------------------------------------------------------
def map_ins_dist(df,state):

    tacy = df[df["States"] == state]
    tacy.reset_index(drop=True, inplace = True)

    tacyg = tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    st.write(f"{state.upper()}: DISTRICT WISE TRANSACTION DETAILS")
    st.dataframe(tacyg)
    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(tacyg, x= "Transaction_amount", y = "Districts", orientation="h",height=600,
                        title=f"{state.upper()}: DISTRICT WISE TRANSACTION AMOUNT",
                        color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2 = px.bar(tacyg, x= "Transaction_count", y = "Districts", orientation="h", height=600,
                        title=f"{state.upper()}: DISTRICT WISE TRANSACTION COUNT",
                        color_discrete_sequence= px.colors.sequential.Burg_r)
        st.plotly_chart(fig_bar_2)


#-------------------------------------FUNCTION FOR MAP USERS REGISTERED USER AND APPOPENS STATE WISE YEARLY-----------------------------------------
def map_user_plot_1(df,year):
    muy= df[df["Years"] == year]
    muy.reset_index(drop=True, inplace=True)
    
    muyg =muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace=True)
    col1,col2 = st.columns(2)
    with col2:
        st.write(f" APPOPENS OF REGISTERED USERS IN {year}")
        st.dataframe(muyg,use_container_width=True)
    with col1:
        fig_line_1 = px.line(muyg, x= "States", y = ["RegisteredUsers", "AppOpens"] ,
                                title =f" APPOPENS OF REGISTERED USERS IN {year}", width=800, height=600, markers = True)

        st.plotly_chart(fig_line_1)

    return muy


#-------------------------------------FUNCTION FOR MAP USERS REGISTERED USER AND APPOPENS STATE WISE QUARTELY-----------------------------------------
def map_user_plot_2(df,quarter):
    muyq= df[df["Quarter"] == quarter]
    muyq.reset_index(drop=True, inplace=True)
    
    muyqg =muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace=True)
    col1,col2 = st.columns(2)
    with col2:

        st.dataframe(muyqg,use_container_width=True)
    with col1:
        fig_line_1 = px.line(muyqg, x= "States", y = ["RegisteredUsers", "AppOpens"] ,
                                title =f"Q{quarter}:APPOPENS OF REGISTERED USERS IN {df['Years'].min()}", width=700, height=600, markers = True,
                                color_discrete_sequence=px.colors.sequential.Rainbow_r)

        st.plotly_chart(fig_line_1)

    return muyq



#-------------------------------------FUNCTION FOR MAP USERS REGISTERED USER AND APPOPENS BY DISTRICTS-----------------------------------------
def map_user_plot_3(df,states):
    muyqs= df[df["States"] == states]
    muyqs.reset_index(drop=True, inplace=True)
    
    muyqsg =muyqs.groupby("Districts")[["RegisteredUsers", "AppOpens"]].sum()
    muyqsg.reset_index(inplace=True)
    st.write(f"{states.upper()}: REGISTERED USERS AND APPOPENS")
    st.dataframe(muyqsg)
    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(muyqs, x= "RegisteredUsers",y="Districts",orientation="h",
                        title=f"{states.upper()}: REGISTERED USERS", height=800, color_discrete_sequence= px.colors.sequential.Rainbow_r)

        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2 = px.bar(muyqs, x= "AppOpens",y="Districts",orientation="h",
                        title=f"{states.upper()}: APPOPENS", height=800, color_discrete_sequence= px.colors.sequential.Rainbow)

        st.plotly_chart(fig_bar_2)


#------------------------------------FUNCTION FOR TOP INSURANCE TRANSACTION AMOUNT AND COUNT BY QUARTER AND PINCODE-------------------------------
def top_ins_plot_1(df,state):
    tiy= df[df["States"] ==state]
    tiy.reset_index(drop=True, inplace=True)

    tiyg =tiy.groupby("Pincode")[["Transaction_count", "Transaction_amount"]].sum()
    tiyg.reset_index(inplace=True)
    
    st.write("PINCODE WISE TRANSACTION DETAILS")
    st.dataframe(tiyg)
    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(tiy, x= "Quarter",y="Transaction_amount", hover_data="Pincode",
                        title="TRANSACTION AMOUNT", height=650, width=600, color_discrete_sequence= px.colors.sequential.GnBu_r)
    
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2 = px.bar(tiy, x= "Quarter",y="Transaction_count", hover_data="Pincode",
                        title="TRANSACTION COUNT", height=650, width=600, color_discrete_sequence= px.colors.sequential.Cividis_r)

        st.plotly_chart(fig_bar_2)


#------------------------------------FUNCTION FOR TOP USERS REGISTERED QUARTELY USING STATES---------------------------------------------
def top_user_plot_1(df,year):
    tuy= df[df["Years"] == year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg =pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)
    
    fig_plot_1 = px.bar(tuyg, x = "States", y = "RegisteredUsers", color = "Quarter", width=1000, height=800,
                        color_discrete_sequence=px.colors.sequential.Burgyl_r, hover_name= "States",
                        title= f"REGISTERED USERS FOR THE {year}")
    st.plotly_chart(fig_plot_1)

    return tuy


#-------------------------------------FUNCTION FOR TOP USERS REGISTERED QUARTELY BY PINCODES--------------------------------------------
def top_user_plot_2(df,state):
    tuys= df[df["States"] == state]
    tuys.reset_index(drop=True, inplace=True)

    fig_plot_1 = px.bar(tuys, x = "Quarter", y="RegisteredUsers", title= "REGISTERED USERS, QUARTER AND PINCODES",
                        width=1000, height=800, color="RegisteredUsers", hover_data="Pincode",
                        color_continuous_scale=px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_plot_1)

#---------------------------------------CHARTS FOR TOP TEN, LAST TEN AND PERCENTAGE OF TRANSACTION AMOUNT----------------------------------------
def top_chart_trans_amt(table_name):
    mydb = psycopg2.connect(host = "localhost",
                            port = "5432",
                            user = "postgres",
                            password = "karthik",
                            database = "phonepe")

    cursor = mydb.cursor()
    #plot_1
    query_1 = f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("states", "transaction_amount")) 

    col1,col2 = st.columns(2)
    with col1:
        fig_df_1 = px.bar(df_1, x="states", y="transaction_amount", title = "TOP 10 STATES: TRANSACTION AMOUNT", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=600)
        st.plotly_chart(fig_df_1)


    #plot_2
    query_2 = f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount
                LIMIT 10;'''

    cursor.execute(query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states", "transaction_amount")) 

    with col2:
        fig_df_2 = px.bar(df_2, x="states", y="transaction_amount", title = " LAST 10 STATES: TRANSACTION AMOUNT", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Agsunset_r, height=650, width=600)
        st.plotly_chart(fig_df_2)

    #plot_3
    query_3 = f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''

    cursor.execute(query_3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states", "transaction_amount")) 

    fig_df_3 = px.bar(df_3, y="states", x="transaction_amount", title = "AVERAGE TRANSACTION AMOUNT BY STATES", hover_name= "states",
                            orientation="h",color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
    st.plotly_chart(fig_df_3)


#---------------------------------------CHARTS FOR TOP TEN, LAST TEN AND PERCENTAGE OF TRANSACTION COUNT----------------------------------------
def top_chart_trans_count(table_name):
    mydb = psycopg2.connect(host = "localhost",
                            port = "5432",
                            user = "postgres",
                            password = "karthik",
                            database = "phonepe")

    cursor = mydb.cursor()
    #plot_1
    query_1 = f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''

    cursor.execute(query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("states", "transaction_count")) 

    col1,col2 = st.columns(2)
    with col1:
        fig_df_1 = px.bar(df_1, x="states", y="transaction_count", title = " TOP 10 STATES: TRANSACTION COUNT", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=600)
        st.plotly_chart(fig_df_1)


    #plot_2
    query_2 = f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count
                LIMIT 10;'''

    cursor.execute(query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states", "transaction_count")) 

    with col2:
        fig_df_2 = px.bar(df_2, x="states", y="transaction_count", title = " LAST 10 STATES: TRANSACTION COUNT", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Agsunset_r, height=650, width=600)
        st.plotly_chart(fig_df_2)

    #plot_3
    query_3 = f'''SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''

    cursor.execute(query_3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states", "transaction_count")) 

    fig_df_3 = px.bar(df_3, y="states", x="transaction_count", title = " AVERAGE TRANSACTION COUNT BY STATES", hover_name= "states",
                            orientation="h",color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
    st.plotly_chart(fig_df_3)



#---------------------------------------CHARTS FOR TOP TEN, LAST TEN AND PERCENTAGE OF REGISTERED USERS DISTRICT WISE----------------------------------------
def top_chart_registered_user(table_name, state):
    mydb = psycopg2.connect(host = "localhost",
                            port = "5432",
                            user = "postgres",
                            password = "karthik",
                            database = "phonepe")

    cursor = mydb.cursor()
    #plot_1
    query_1 = f'''SELECT districts,SUM(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("districts", "registeredusers")) 

    col1,col2 = st.columns(2)
    with col1:
        fig_df_1 = px.bar(df_1, x="districts", y="registeredusers", title = "TOP 10 DISTRICTS: REGISTERED USERS", hover_name= "districts",
                                color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=600)
        st.plotly_chart(fig_df_1)


    #plot_2
    query_2 = f'''SELECT districts,SUM(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts
                ORDER BY registeredusers
                LIMIT 10;'''

    cursor.execute(query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("districts", "registeredusers")) 

    with col2:
        fig_df_2 = px.bar(df_2, x="districts", y="registeredusers", title = " LAST 10 DISTRICTS: REGISTERED USER", hover_name= "districts",
                                color_discrete_sequence=px.colors.sequential.Agsunset_r, height=650, width=600)
        st.plotly_chart(fig_df_2)

    #plot_3
    query_3 = f'''SELECT districts,AVG(registeredusers) AS registeredusers
                    FROM {table_name}
                    WHERE states = '{state}'
                    GROUP BY districts
                    ORDER BY registeredusers;'''

    cursor.execute(query_3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("districts", "registeredusers")) 

    fig_df_3 = px.bar(df_3, y="districts", x="registeredusers", title = " AVERAGE REGISTERED USER BY DISTRICTS", hover_name= "districts",
                            orientation="h",color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
    st.plotly_chart(fig_df_3)



#---------------------------------------CHARTS FOR TOP TEN, LAST TEN AND PERCENTAGE OF APP OPENS DISTRICT WISE----------------------------------------
def top_chart_appopens(table_name, state):
    mydb = psycopg2.connect(host = "localhost",
                            port = "5432",
                            user = "postgres",
                            password = "karthik",
                            database = "phonepe")

    cursor = mydb.cursor()
    #Plot_1
    query_1 = f'''SELECT districts,SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''

    cursor.execute(query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("districts", "appopens")) 
    
    col1,col2 = st.columns(2)
    with col1:
        fig_df_1 = px.bar(df_1, x="districts", y="appopens", title = "TOP 10 OF APP OPENS", hover_name= "districts",
                                color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=600)
        st.plotly_chart(fig_df_1)


    #Plot_2
    query_2 = f'''SELECT districts,SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts
                ORDER BY appopens
                LIMIT 10;'''

    cursor.execute(query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("districts", "appopens")) 

    with col2:
        fig_df_2 = px.bar(df_2, x="districts", y="appopens", title = " LAST 10 OF APP OPENS", hover_name= "districts",
                                color_discrete_sequence=px.colors.sequential.Agsunset_r, height=650, width=600)
        st.plotly_chart(fig_df_2)

    #plot_3
    query_3 = f'''SELECT districts,AVG(appopens) AS appopens
                    FROM {table_name}
                    WHERE states = '{state}'
                    GROUP BY districts
                    ORDER BY appopens;'''

    cursor.execute(query_3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("districts", "appopens")) 

    fig_df_3 = px.bar(df_3, y="districts", x="appopens", title = " AVERAGE OF APP OPENS", hover_name= "districts",
                            orientation="h",color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
    st.plotly_chart(fig_df_3)



#---------------------------------------CHARTS FOR TOP TEN, LAST TEN AND PERCENTAGE OF REGISTERED USERS STATE WISE----------------------------------------
def top_chart_registered_users(table_name):
    mydb = psycopg2.connect(host = "localhost",
                            port = "5432",
                            user = "postgres",
                            password = "karthik",
                            database = "phonepe")

    cursor = mydb.cursor()
    #Plot_1
    query_1 = f'''SELECT states,SUM(registeredusers) AS registeredusers
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY registeredusers DESC
                    LIMIT 10;'''

    cursor.execute(query_1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("states", "registeredusers")) 

    col1,col2 = st.columns(2)
    with col1:
        fig_df_1 = px.bar(df_1, x="states", y="registeredusers", title = "TOP 10 OF REGISTERED USERS", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=600)
        st.plotly_chart(fig_df_1)


    #Plot_2
    query_2 = f'''SELECT states,SUM(registeredusers) AS registeredusers
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY registeredusers
                    LIMIT 10;'''

    cursor.execute(query_2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states", "registeredusers")) 

    with col2:
        fig_df_2 = px.bar(df_2, x="states", y="registeredusers", title = " LAST 10 OF REGISTERED USERS", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Agsunset_r, height=650, width=600)
        st.plotly_chart(fig_df_2)

    #Plot_3
    query_3 = f'''SELECT states,AVG(registeredusers) AS registeredusers
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY registeredusers;'''

    cursor.execute(query_3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states", "registeredusers")) 

    fig_df_3 = px.bar(df_3, y="states", x="registeredusers", title = " AVERAGE OF REGISTERED USERS", hover_name= "states",
                            orientation="h",color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
    st.plotly_chart(fig_df_3)


#--------------------------------------------------------STREAMLIT USER INTERFACE----------------------------------------------------
st.set_page_config(layout='wide')
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

#--------------------------------------------------------OPTION MENU----------------------------------------------------------------
with st.sidebar:

    select = option_menu("Main Menu",["HOME","DATA EXPLORATION & GEO VISUALIZATION","TOP CHARTS"])

#---------------------------------------------------------OPTION: HOME-----------------------------------------------------------
if select == "HOME":
    
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
elif select == "DATA EXPLORATION & GEO VISUALIZATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])
#---------------------------------------------------------------TAB: AGGREGATED ANALYSIS--------------------------------------------------

    with tab1:

        method = st.radio("Select the Method",["Insurance Analysis", "Transaction Analysis", "User Analysis"])


        #----------------------------------------------------RADIO BUTTON: INSURANCE ANALYSIS-----------------------------------------
        if method == "Insurance Analysis":

            col1,col2 = st.columns(2)
            with col1:

                years= st.slider("Select the Year of Aggregated Insurance",Agg_ins_df["Years"].min(),Agg_ins_df["Years"].max(),Agg_ins_df["Years"].min())
                
            tac_Y = transaction_amount_count_Y(Agg_ins_df,years)

           
            col1,col2 = st.columns(2)
            with col1:

                quarters = st.selectbox("Select the Quarter", options=tac_Y["Quarter"].unique())
                #quarters= st.slider("Select the Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            transaction_amount_count_Y_Q(tac_Y,quarters)

        #----------------------------------------------------RADIO BUTTON: TRANSACTION ANALYSIS-------------------------------------------
        elif method == "Transaction Analysis":
            
            col1,col2 = st.columns(2)
            
            with col1:

                years= st.slider("Select the Year for Aggregated Transactions",Agg_trans_df["Years"].min(),Agg_trans_df["Years"].max(),Agg_trans_df["Years"].min())
                
            Agg_trans_tac_Y = transaction_amount_count_Y(Agg_trans_df,years)

            col1,col2 = st.columns(2)
            
            with col1:

                states = st.selectbox("Select the State for Aggregated Transactions_Type by yearly",Agg_trans_tac_Y["States"].unique())

            Agg_trans_trans_type(Agg_trans_tac_Y,states)

            col1,col2 = st.columns(2)
            with col1:

                
                quarters= st.slider("Select the Quarter for Aggregated Transactions_Type",Agg_trans_tac_Y["Quarter"].min(),Agg_trans_tac_Y["Quarter"].max(),Agg_trans_tac_Y["Quarter"].min())
            Agg_trans_tac_Y_Q= transaction_amount_count_Y_Q(Agg_trans_tac_Y,quarters)
            
            col1,col2 = st.columns(2)
            
            with col1:

                states = st.selectbox("Select the State for Aggregated Transactions_Type by quartely",Agg_trans_tac_Y_Q["States"].unique())

            Agg_trans_trans_type(Agg_trans_tac_Y_Q,states)
        
        
        #-------------------------------------------------------------RADIO BUTTON: USER ANALYSIS------------------------------------------
        elif method == "User Analysis":
            
            col1,col2 = st.columns(2)
            
            with col1:

                years= st.slider("Select the Year of Aggregated User",Agg_user_df["Years"].min(),Agg_user_df["Years"].max(),Agg_user_df["Years"].min())
                
            Agg_user_Y = Agg_user_plot_1(Agg_user_df,years)

            col1,col2 = st.columns(2)
            with col1:

                quarters= st.slider("Select the Quarter of Aggregated User",Agg_user_Y["Quarter"].min(),Agg_user_Y["Quarter"].max(),Agg_user_Y["Quarter"].min())
            Agg_user_Y_Q= Agg_user_plot_2(Agg_user_Y,quarters)

            col1,col2 = st.columns(2)
            
            with col1:

                states = st.selectbox("Select the State of Aggregated User",Agg_user_Y_Q["States"].unique())

            Agg_user_plot_3(Agg_user_Y_Q,states)


#-----------------------------------------------------------------TAB: MAP ANALYSIS------------------------------------------------------------------   
    with tab2:

        method_2 = st.radio("Select the Method",["Map Insurance", "Map Transactions", "Map User"])

        #----------------------------------------------------RADIO BUTTON: MAP INSURANCE-------------------------------------------------
        if method_2 == "Map Insurance":
            
            col1,col2 = st.columns(2)
            
            with col1:

                years= st.slider("Select the Year for Map Insurance",map_ins_df["Years"].min(),map_ins_df["Years"].max(),map_ins_df["Years"].min())
                
            map_ins_tac_Y = transaction_amount_count_Y(map_ins_df,years)

            col1,col2 = st.columns(2)
            
            with col1:

                states = st.selectbox("Select the State for Map Insurance",map_ins_tac_Y["States"].unique())

            map_ins_dist(map_ins_tac_Y,states)

            col1,col2 = st.columns(2)
            with col1:

                
                quarters= st.slider("Select the Quarter for Map Insurance",map_ins_tac_Y["Quarter"].min(),map_ins_tac_Y["Quarter"].max(),map_ins_tac_Y["Quarter"].min())
            map_ins_tac_Y_Q= transaction_amount_count_Y_Q(map_ins_tac_Y,quarters)

            col1,col2 = st.columns(2)
            
            with col1:

                states = st.selectbox("Select the State for Map Insurance by Quartely",map_ins_tac_Y_Q["States"].unique())

            map_ins_dist(map_ins_tac_Y_Q,states)

        #-------------------------------------------------RADIO BUTTON: MAP TRANSACTIONS---------------------------------------
        elif method_2 == "Map Transactions":
            
            col1,col2 = st.columns(2)
            
            with col1:

                years= st.slider("Select the Year for Map Transactions",map_trans_df["Years"].min(),map_trans_df["Years"].max(),map_trans_df["Years"].min())
                
            map_trans_tac_Y = transaction_amount_count_Y(map_trans_df,years)

            col1,col2 = st.columns(2)
            
            with col1:

                states = st.selectbox("Select the State for Map Transactions",map_trans_tac_Y["States"].unique())

            map_ins_dist(map_trans_tac_Y,states)

            col1,col2 = st.columns(2)
            with col1:

                
                quarters= st.slider("Select the Quarter for Map Transactions",map_trans_tac_Y["Quarter"].min(),map_trans_tac_Y["Quarter"].max(),map_trans_tac_Y["Quarter"].min())
            map_trans_tac_Y_Q= transaction_amount_count_Y_Q(map_trans_tac_Y,quarters)

            col1,col2 = st.columns(2)
            
            with col1:

                states = st.selectbox("Select the State for Map Transactions by Quartely",map_trans_tac_Y_Q["States"].unique())

            map_ins_dist(map_trans_tac_Y_Q,states)

        #--------------------------------------------------RADIO BUTTON: MAP USERS--------------------------------------------------
        elif method_2 == "Map User":
            
            col1,col2 = st.columns(2)
            
            with col1:

                years= st.slider("Select the Year for Map User",map_user_df["Years"].min(),map_user_df["Years"].max(),map_user_df["Years"].min())
                
            map_user_Y = map_user_plot_1(map_user_df,years)

            col1,col2 = st.columns(2)
            with col1:

                
                quarters= st.slider("Select the Quarter for Map User",map_user_Y["Quarter"].min(),map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            map_user_Y_Q= map_user_plot_2(map_user_Y,quarters)

            col1,col2 = st.columns(2)
            
            with col1:

                states = st.selectbox("Select the State for Map User_Quartely",map_user_Y_Q["States"].unique())

            map_user_plot_3(map_user_Y_Q,states)

#--------------------------------------------------------------------TAB: TOP ANALYSIS----------------------------------------------------------------    
    with tab3:

        method_3 = st.radio("Select the Method",["Top Insurance", "Top Transactions", "Top User"])

        #-----------------------------------------------RADIO BUTTON: TOP INSURANCE---------------------------------------------
        if method_3 == "Top Insurance":
            col1,col2 = st.columns(2)
            
            with col1:

                years= st.slider("Select the Year for Top Insurance",top_ins_df["Years"].min(),top_ins_df["Years"].max(),top_ins_df["Years"].min())
                
            top_ins_tac_Y = transaction_amount_count_Y(top_ins_df,years)

            col1,col2 = st.columns(2)
            
            with col1:

                states = st.selectbox("Select the State for Top Insurance",top_ins_tac_Y["States"].unique())

            top_ins_plot_1(top_ins_tac_Y,states)

            col1,col2 = st.columns(2)
            with col1:

                
                quarters= st.slider("Select the Quarter for Top Insurance",top_ins_tac_Y["Quarter"].min(),top_ins_tac_Y["Quarter"].max(),top_ins_tac_Y["Quarter"].min())
            top_ins_Y_Q= transaction_amount_count_Y_Q(top_ins_tac_Y,quarters)

        #-----------------------------------------------RADIO BUTTON: TOP TRANSACTIONS------------------------------------------
        elif method_3 == "Top Transactions":    
            col1,col2 = st.columns(2)
            
            with col1:

                years= st.slider("Select the Year for Top Trasactions",top_trans_df["Years"].min(),top_trans_df["Years"].max(),top_trans_df["Years"].min())
                
            top_trans_tac_Y = transaction_amount_count_Y(top_trans_df,years)

            col1,col2 = st.columns(2)
            
            with col1:

                states = st.selectbox("Select the State for Top Transactions",top_trans_tac_Y["States"].unique())

            top_ins_plot_1(top_trans_tac_Y,states)

            col1,col2 = st.columns(2)
            with col1:

                
                quarters= st.slider("Select the Quarter for Top Transactions",top_trans_tac_Y["Quarter"].min(),top_trans_tac_Y["Quarter"].max(),top_trans_tac_Y["Quarter"].min())
            top_trans_Y_Q= transaction_amount_count_Y_Q(top_trans_tac_Y,quarters)

        #-----------------------------------------------RADIO BUTTON: TOP USERS--------------------------------------------------
        elif method_3 == "Top User":
            col1,col2 = st.columns(2)
            
            with col1:

                years= st.slider("Select the Year for Top Users",top_user_df["Years"].min(),top_user_df["Years"].max(),top_user_df["Years"].min())
                
            top_user_Y = top_user_plot_1(top_user_df,years)

            col1,col2 = st.columns(2)
            
            with col1:

                states = st.selectbox("Select the State for Top Users",top_user_Y["States"].unique())

            top_user_plot_2(top_user_Y,states)


#------------------------------------------------------------------------OPTION: TOP CHARTS----------------------------------------------------
elif select == "TOP CHARTS":
        question = st.selectbox("Select the Question",["1.Transaction Amount and Count of Aggregated Insurance",
                                                       "2.Transaction Amount and Count of Map Insurance",
                                                       "3.Transaction Amount and Count of Top Insurance",
                                                       "4.Transaction Amount and Count of Aggregated Transactions",
                                                       "5.Trasanction Amount and Count of Map Transactions",
                                                       "6.Transaction Amoutn and Count of Top Transactions",
                                                       "7.Transaction Count of Aggregated User",
                                                       "8.Registered User of Map Users",
                                                       "9.App Opens of Map User",
                                                       "10.Registered Users of Top User"])
        #Question_1
        
        if question == "1.Transaction Amount and Count of Aggregated Insurance":
            
            st.subheader("TRANSACTION AMOUNT")
            top_chart_trans_amt("aggregated_insurance")
            
            st.subheader("TRANSACTION COUNT")
            top_chart_trans_count("aggregated_insurance")

        #Question_2

        elif question == "2.Transaction Amount and Count of Map Insurance":
            
            st.subheader("TRANSACTION AMOUNT")
            top_chart_trans_amt("map_insurance")
            
            st.subheader("TRANSACTION COUNT")
            top_chart_trans_count("map_insurance")

        #Question_3        

        elif question == "3.Transaction Amount and Count of Top Insurance":
            
            st.subheader("TRANSACTION AMOUNT")
            top_chart_trans_amt("top_insurance")
            
            st.subheader("TRANSACTION COUNT")
            top_chart_trans_count("top_insurance")

        #Question_4

        elif question == "4.Transaction Amount and Count of Aggregated Transactions":
            
            st.subheader("TRANSACTION AMOUNT")
            top_chart_trans_amt("aggregated_transaction")
            
            st.subheader("TRANSACTION COUNT")
            top_chart_trans_count("aggregated_transaction")

        #Question_5

        elif question == "5.Trasanction Amount and Count of Map Transactions":
            
            st.subheader("TRANSACTION AMOUNT")
            top_chart_trans_amt("map_transaction")
            
            st.subheader("TRANSACTION COUNT")
            top_chart_trans_count("map_transaction")

        #Question_6

        elif question == "6.Transaction Amoutn and Count of Top Transactions":
            
            st.subheader("TRANSACTION AMOUNT")
            top_chart_trans_amt("top_transaction")
            
            st.subheader("TRANSACTION COUNT")
            top_chart_trans_count("top_transaction")

        #Question_7

        elif question == "7.Transaction Count of Aggregated User":                       
                
            st.subheader("TRANSACTION COUNT")
            top_chart_trans_count("aggregated_user")

        #Question_8

        elif question == "8.Registered User of Map Users":                       

            states = st.selectbox("Select the State", map_user_df["States"].unique())    
            st.subheader("REGISTERED USERS")
            top_chart_registered_user("map_user", states)

        #Question_9

        elif question == "9.App Opens of Map User":                       

            states = st.selectbox("Select the State", map_user_df["States"].unique())    
            st.subheader("APP OPENS")
            top_chart_appopens("map_user", states)

        #Question_10

        elif question == "10.Registered Users of Top User":                       

            st.subheader("REGISTERED USERS")
            top_chart_registered_users("top_user")

#----------------------------------------------------------------END OF THE PROJECT------------------------------------------------------------------
