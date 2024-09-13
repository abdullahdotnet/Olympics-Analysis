import numpy as np

def medal_tally(data):
    medal_tally = data.drop_duplicates(subset = ['Team','NOC','Year','Games','City','Sport','Event','Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values(by='Gold',ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold']+medal_tally['Silver']+medal_tally['Silver']
    return medal_tally

def country_year_list(data):
    years = data['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    country = np.unique(data['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country


def fetch_medal_tally(data, year,country):
    medal_tally = data.drop_duplicates(subset = ['Team','NOC','Year','Games','City','Sport','Event','Medal'])
    flag = 0
    print(year,country)
    if year == 'Overall' and country == "Overall":
        temp = medal_tally
    elif year == 'Overall' and country != "Overall":
        flag = 1
        temp = medal_tally[medal_tally['region'] == country]
    elif year != 'Overall' and country == "Overall":
        temp = medal_tally[medal_tally['Year'] == year]
    elif year != 'Overall' and country != "Overall":
        temp = medal_tally[(medal_tally['region'] == country) & (medal_tally['Year'] == year)]
    
    if flag == 1:
        x = temp.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values(by='Year',ascending=True).reset_index()
    else:
        x = temp.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values(by='Gold',ascending=False).reset_index()
    x['total'] = x['Gold']+x['Silver']+x['Silver']

    return x

def data_over_time(data, param):
    nations_over_time = data.drop_duplicates(['Year',param])['Year'].value_counts().reset_index().sort_values(by='Year')
    nations_over_time.rename(columns = {'Year':'Edition','count': param},inplace=True)
    return nations_over_time

def most_successful_athletes(df, sport):
    temp = df.dropna(subset=['Medal'])
    
    if sport != 'Overall':
        temp = temp[temp['Sport'] == sport]
    
    top_athletes = temp['Name'].value_counts().reset_index().head(15)
    
    top_athletes.columns = ['Athlete', 'Medal Count']
    
    merged_df = top_athletes.merge(df, left_on='Athlete', right_on='Name', how='left')
    
    result = merged_df[['Athlete', 'Medal Count', 'Sport', 'region']].drop_duplicates(subset=['Athlete'])
    
    return result