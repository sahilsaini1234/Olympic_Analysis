import streamlit as st
import pandas as pd
import helper
import preprocessor
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import os
import numpy as np
import plotly.figure_factory as ff
st.sidebar.header("Olympic Analysis")
st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8stG2LEGR7KKjYYKki_eVTtTowTI6i0vs4IFNRwu0wt2D1lgHMiuIhincEmP6uzSbd_U&usqp=CAU')
menu=st.sidebar.radio('Select an option',
         ('Medal_tally','Overall_Analysis','Player_Wise_Analysis','Country_Wise'))
data=pd.read_csv('data1.csv')
region_df=pd.read_csv('noc_regions.csv')
data=preprocessor.process(data,region_df)
medal_tally=helper.medal_tally(data)
if(menu=='Medal_tally'):
    year=helper.year(data)
    country=helper.country(data)
    selected_year=st.sidebar.selectbox(label='Year',options=year)
    selected_country=st.sidebar.selectbox(label='Country',options=country)
    medal_tally=helper.medal_data(data,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.header("Medal Tally Of All Country Over Year")
    if selected_year!='Overall' and selected_country=='Overall':
        st.header("Medal Tally Of Countries in Year "+selected_year)
    if selected_year=='Overall' and selected_country!='Overall':
        st.header("Medal Tally Of "+selected_country+"Over Year")
    if selected_year!='Overall' and selected_country!='Overall':
        st.header("Medal Tally Of "+selected_country+" In Year "+selected_year)           
    st.table(medal_tally)
if(menu=='Overall_Analysis'):
    st.title('Top Statistics')
    editions=data['Year'].unique().shape[0]-1
    cities=data['City'].unique().shape[0]
    sports=data['Sport'].unique().shape[0]
    event=data['Event'].unique().shape[0]
    athelete=data['Name'].unique().shape[0]
    Countries=data['region'].unique().shape[0]
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Edition')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Events')
        st.title(event)
    with col2:
        st.header('Athelete')
        st.title(athelete)
    with col3:
        st.header('Countries')
        st.title(Countries)
    df_new=helper.no_of_country_year(data)
    st.title("Participating countries over the year")
    fig=px.line(df_new, x="Year", y="No of Country")
    st.plotly_chart(fig)
    
    df_new2=helper.data_over_year(data)
    st.title("Events over the year")
    fig2=px.line(df_new2, x="Year", y="Events")
    st.plotly_chart(fig2)
    
    df_new3=helper.athlete_over_year(data)
    st.title("Athlete over the year")
    fig3=px.line(df_new3, x="Year", y="Name")
    st.plotly_chart(fig3)
    
    st.title("Sports event over the year")
    data_new=data.drop_duplicates(['Sport','Event','Year'])
    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(data_new.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)
    
    st.title('Top 10 sports-person of paticular/overall sports')
    sport_list=helper.sport(data)
    selected_sport=st.selectbox(label='Select sport',options=sport_list)
    sport_df=helper.most_succesfull(data,selected_sport)
    st.table(sport_df)
if(menu=='Country_Wise'):
    st.title('Country_wise_Analysis')
    country_list=data['region']
    country_list=country_list.dropna()
    country_list=country_list.unique()
    np.sort(country_list)
    selected_country=st.selectbox(label='Select a country',options=country_list)
    st.header('Number of medals by '+selected_country+' over Year')
    temp_df_2=helper.year_wise_tally(data,selected_country)
    fig4=px.line(temp_df_2, x="Year", y="Medal") 
    st.plotly_chart(fig4)
    
    st.header(selected_country+' performance in different sports over year')
    temp_df_3=helper.counrty_event_heatmap(data,selected_country)
    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(temp_df_3.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)
    
    st.header('Top 10 sports-person of particular country')
    country_top_df=helper.most_succesfull_country(data,selected_country)
    st.table(country_top_df)
if menu == 'Player_Wise_Analysis':
    x=data.drop_duplicates(subset=['Name','region'])
    x1=x['Age'].dropna()
    x2=x[x['Medal']=='Gold']['Age'].dropna()
    x3=x[x['Medal']=='Silver']['Age'].dropna()
    x4=x[x['Medal']=='Bronze']['Age'].dropna()
    l=[]
    l.append(x)
    fig=ff.create_distplot([x1,x2,x3,x4],['Overall','Gold','Silver','Bronze'],show_hist=False,show_rug=False)
    st.header('Age Distribution of Athlete')
    st.plotly_chart(fig)
    
    sport_list = data['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(data,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)
    
    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(data)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=800, height=400)
    st.plotly_chart(fig)   
    

    
