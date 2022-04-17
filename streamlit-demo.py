from ast import alias
from calendar import week
from re import A
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

#plt.rcParams["figure.figsize"] = (12, 9)

#--------------------------------------------------------
# Headers

original_header = '<p style="font-family:Courier; color:White; font-size: 48px;">Dashboard</p>'
st.markdown(original_header, unsafe_allow_html=True)

original_header = '<p style="font-family:Courier; color:#2BB3A0; font-size: 24px;">Data Analysis on Energy Consumption</p>'
st.markdown(original_header, unsafe_allow_html=True)


#--------------------------------------------------------
# Component: File Uploader

uploaded_file = st.sidebar.file_uploader("Choose a CSV file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['timestamp'] = pd.DatetimeIndex(df["timestamp"])
    #df.set_index("timestamp", inplace=True)



#--------------------------------------------------------
# Component: Select Box
add_selectbox = st.sidebar.selectbox(
    "Select the length of each timestamp",
        ("Quater-Hour", "Hourly", "Daily", "Weekly")
)

#--------------------------------------------------------
## Resampling

if uploaded_file is not None:
    df1 = df.set_index("timestamp")
    hourly_df = df1.resample("H", label="right", closed='right').sum()
    hourly_df.reset_index(inplace=True)
    day_df = df1.resample("D", label="left", closed='right').sum()
    day_df.reset_index(inplace=True)
    df_np = np.array(hourly_df['Energy in kWh'])
    df_np_2d = df_np.reshape(30, 24)
    

#--------------------------------------------------------
if uploaded_file is not None:
    if add_selectbox == "Quater-Hour":
        ## Data Visualization ----------
        c = alt.Chart(df, title='Quater-Hourly Energy Consumption').mark_line(color='#2BB3A0').encode(
            x='timestamp', y='Energy in kWh').properties(width=800, height=300)
        st.altair_chart(c, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1: 
            original_header = '<p style="font-family:Courier; color:White; font-size: 24px;">Dataframe</p>'
            st.markdown(original_header, unsafe_allow_html=True)
            st.dataframe(data=df, width=800, height=300)
            

        with col2:
            original_header = '<p style="font-family:Courier; color:White; font-size: 24px;">Statistics</p>'
            st.markdown(original_header, unsafe_allow_html=True) 
            st.write(df.describe())
    
    if add_selectbox == "Hourly":
        
        ## Data Visualization ----------
        c = alt.Chart(hourly_df, title='Hourly Energy Consumption').mark_line(color='#2BB3A0').encode(
            x='timestamp', y='Energy in kWh').properties(width=800, height=400)
        st.altair_chart(c, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1: 
            original_header = '<p style="font-family:Courier; color:White; font-size: 24px;">Dataframe</p>'
            st.markdown(original_header, unsafe_allow_html=True)
            st.dataframe(data=hourly_df, width=800, height=300)

        with col2:
            original_header = '<p style="font-family:Courier; color:White; font-size: 24px;">Statistics</p>'
            st.markdown(original_header, unsafe_allow_html=True) 
            st.write(hourly_df.describe()) 

    if add_selectbox == "Daily":
        
        ## Data Visualization --------
        c = alt.Chart(day_df, title='Daily Energy Consumption').mark_line(color='#2BB3A0').encode(
            x='timestamp', y='Energy in kWh').properties(width=400, height=300)
        st.altair_chart(c, use_container_width=True)

        slider_val = st.sidebar.slider("Select the day you want to analyse ", min_value=0, 
                                                    max_value=len(day_df)-1, value=None, step=1)
        day=slider_val
        plt_day = df_np[0+24*day:24*(day+1)]
        df2 = pd.DataFrame(plt_day)
        df2.reset_index(inplace=True)
        df2.rename(columns={"index":"Hour of the day", 0:"Energy in kWh"}, inplace=True)
        c1 = alt.Chart(df2, title='Hourly Consumption of the day').mark_line(color='#2BB3A0').encode(
            x='Hour of the day', y='Energy in kWh').properties(width=400, height=300)
        st.altair_chart(c1, use_container_width=True)   


        col1, col2 = st.columns(2)
        with col1: 
            original_header = '<p style="font-family:Courier; color:White; font-size: 24px;">Dataframe</p>'
            st.markdown(original_header, unsafe_allow_html=True)
            st.dataframe(data=day_df, width=800, height=300)

        with col2:
            original_header = '<p style="font-family:Courier; color:White; font-size: 24px;">Statistics</p>'
            st.markdown(original_header, unsafe_allow_html=True) 
            st.write(day_df.describe())
            # For spaces
            placeholder = st.empty()
            with placeholder.container():
                i=0
                while i<6:
                    st.write("")
                    i+=1 
                 
        
        with col1:
            original_header = '<p style="font-family:Courier; color:White; font-size: 24px;">Additional Insights</p>'
            st.markdown(original_header, unsafe_allow_html=True)
            fig, ax = plt.subplots()  
            ax = sns.heatmap(df_np_2d, cmap="viridis")
            plt.xlabel('Time of day')
            plt.ylabel('Day of month')          
            st.pyplot(fig, width=700, height=300)

        with col2:
            st.write()
            fig, ax = plt.subplots()  
            ax = plt.plot(df_np_2d.T, alpha=.3, color='#2BB3A0')
            plt.plot(np.mean(df_np_2d, axis=0), '*--', color='#172A3A')
            plt.xlabel('Time [hours]')
            plt.ylabel('Energy Consumption')
            plt.xticks(np.arange(0, len(plt_day), 1))
            st.pyplot(fig, width=700, height=300) 

        
#-----------------------------

    if add_selectbox == "Weekly":
        day_df.set_index("timestamp", inplace=True)
        day_np = np.array(day_df)
        week_np = day_np[0:28].reshape(4,7)
        week_df = pd.DataFrame(np.sum(week_np, axis =1))
        week_df.reset_index(inplace=True)
        week_df.rename(columns={"index":"Week", 0:"Energy in kWh"}, inplace=True)
        ## Resampling
        slider_val = st.sidebar.slider("Select the week you want to analyse ", min_value=0, 
                                                    max_value=(len(day_df)//7)-1, value=None, step=1)
        week_no=slider_val
        plt_week = df_np[0+7*week_no:7*(week_no+1)]
        df3 = pd.DataFrame(plt_week)
        df3.reset_index(inplace=True)
        df3.rename(columns={"index":"Day of the Week", 0:"Energy in kWh"}, inplace=True)

        ## Data Visualization --------
        c1 = alt.Chart(df3, title='Weekly Energy Consumption').mark_line(color='#2BB3A0').encode(
            x='Day of the Week', y='Energy in kWh').properties(width=400, height=300)
        st.altair_chart(c1, use_container_width=True) 
        
        col1, col2 = st.columns(2)
        with col1: 
            original_header = '<p style="font-family:Courier; color:White; font-size: 24px;">Dataframe</p>'
            st.markdown(original_header, unsafe_allow_html=True)
            st.dataframe(data=week_df, width=800, height=300)
            # For spaces
            i=0
            while i<6:
                st.write("")
                i+=1

            original_header = '<p style="font-family:Courier; color:White; font-size: 24px;">Additional Insights</p>'
            st.markdown(original_header, unsafe_allow_html=True)
            fig, ax = plt.subplots()  
            ax = sns.heatmap(week_np, cmap="viridis")
            plt.xlabel('Day of the week')
            plt.ylabel('week')          
            st.pyplot(fig, width=700, height=300)

            
            

        with col2:
            original_header = '<p style="font-family:Courier; color:White; font-size: 24px;">Statistics</p>'
            st.markdown(original_header, unsafe_allow_html=True) 
            st.write(week_df.describe())
            # For spaces
            placeholder = st.empty()
            with placeholder.container():
                i=0
                while i<3:
                    st.write("")
                    i+=1

        
            fig, ax = plt.subplots()  
            ax = plt.plot(week_np.T, alpha=.3, color='#2BB3A0')
            plt.plot(np.mean(week_np, axis=0), '*--', color='#172A3A')
            plt.xlabel('Time [days]')
            plt.ylabel('Energy Consumption')
            plt.xticks(np.arange(0, 7, 1))
            st.pyplot(fig, width=700, height=300) 
        

#--------------------------------------------------------
# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Select the length of each timestamp",
        ("Quater-Hour", "Hourly", "Daily", "Weekly")
    )




