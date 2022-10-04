from tkinter.tix import COLUMN
import numpy as np
def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    medal_tally['Gold']=medal_tally['Gold'].astype(int)
    medal_tally['Silver']=medal_tally['Silver'].astype(int)
    medal_tally['Bronze']=medal_tally['Bronze'].astype(int)
    medal_tally['total']=medal_tally['total'].astype(int)
    return medal_tally
def year(df):
    year=df['Year']
    year=year.unique()
    year=np.sort(year)
    year=year.astype(str)
    year=np.insert(year,0,'Overall')
    return year
def sport(df):
    sport=df['Sport']
    sport=sport.unique()
    sport=np.sort(sport)
    sport=np.insert(sport,0,'Overall')
    return sport
def country(df):
    country=df['region']
    country=country.dropna()
    country=country.unique()
    country=np.sort(country)
    country=np.insert(country,0,'Overall')
    return country
def medal_data(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year=='Overall' and country=='Overall':
        temp_df=medal_df
    if year!='Overall' and country=='Overall':
        temp_df=medal_df[medal_df['Year']==int(year)]
    if year=='Overall' and country!='Overall':
        flag=1
        temp_df=medal_df[medal_df['region']==country]
    if year!='Overall' and country!='Overall':
        temp_df=medal_df[(medal_df['Year']==int(year))&(medal_df['region']==country)]
    if(flag==1):
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['total']=x['Gold']+x['Silver']+x['Bronze']
    return x
def no_of_country_year(df):
    data_new=df.drop_duplicates(subset=['Year','region'])
    data_new=data_new['Year'].value_counts().reset_index()
    data_new=data_new.sort_values('index')
    data_new.rename(columns={'index':'Year','Year':'No of Country'},inplace=True)
    return data_new
def data_over_year(df):
    data_new=df.drop_duplicates(subset=['Year','Event'])
    data_new=data_new['Year'].value_counts().reset_index()
    data_new=data_new.sort_values('index')
    data_new.rename(columns={'index':'Year','Year':'Events'},inplace=True)
    return data_new
def athlete_over_year(df):
    data_new=df.drop_duplicates(subset=['Year','Name'])
    data_new=data_new['Year'].value_counts().reset_index()
    data_new=data_new.sort_values('index')
    data_new.rename(columns={'index':'Year','Year':'Name'},inplace=True)
    return data_new
def most_succesfull(df,sport):
    temp_df=df.dropna(subset=['Medal'])
    if(sport!='Overall'):
        temp_df=temp_df[temp_df['Sport']==sport]
    x=temp_df['Name'].value_counts().reset_index().merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates(['index']).head(10)
    x.rename({'index':'Name','Name_x':'Medal'},inplace=True)
    return x
def year_wise_tally(df,country):
    x=df.dropna(subset=['Medal'])
    x=x.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    x=x[x['region']==country]
    x=x.groupby('Year').count()['Medal'].reset_index()
    return x
def counrty_event_heatmap(df,country):
    x=df.dropna(subset=['Medal'])
    x=x.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    x=x[x['region']==country]
    return x
def most_succesfull_country(df,country):
    temp_df=df.dropna(subset=['Medal'])
    if(country!='Overall'):
        temp_df=temp_df[temp_df['region']==country]
    x=temp_df['Name'].value_counts().reset_index().merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates(['index']).head(10)
    x.rename({'index':'Name','Name_x':'Medal'},inplace=True)
    return x
def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df
def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
    
    