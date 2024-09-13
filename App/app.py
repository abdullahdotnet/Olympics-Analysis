import matplotlib.pyplot as plt
import streamlit as st
import preprocessor as pr
import helper as hp
import pandas as pd
import plotly.express as px
import seaborn as sns

df = pd.read_csv('E:\\Projects\\OlympicsAnalysis\\App\\athlete_events.csv')
regions = pd.read_csv('E:\\Projects\\OlympicsAnalysis\\App\\noc_regions.csv')

st.sidebar.title('Olymics Analysis')

df =pr.preprocess(df,regions)

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Athlete wise','Country wise','Overall Analysis')
)


if user_menu == 'Medal Tally':

    
    years,country = hp.country_year_list(df)
    st.sidebar.title('Medal Tally')
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Year",country)

    # st.header(f'Medal Tally \nYear: {selected_year} Country: {selected_country}')
    # st.header('Medal Tally')
    medal_tally = hp.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Medal Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in "+str(selected_year)+" Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(str(selected_country)+" overall performance")
    elif selected_year!= 'Overall' and selected_country != 'Overall':
        st.title(str(selected_country)+" performance in "+ str(selected_year))
    # medal_tally = hp.medal_tally(df)
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] -1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Edtions")
        st.title(editions)
    with col3:
        st.header("Hosts")
        st.title(cities)
    with col2:
        st.header("Sports")
        st.title(sports)
    
    col4,col5,col6 = st.columns(3)
    with col4:
        st.header("Events")
        st.title(events)
    with col5:
        st.header("Nations")
        st.title(nations)
    with col6:
        st.header("Athletes")
        st.title(athletes)
    

    st.title("Participating nations over the years")
    nations = hp.data_over_time(df,'region')
    fig = px.line(nations,x="Edition",y= 'region')
    st.plotly_chart(fig)

    st.title("No. of Events over the years")
    nations = hp.data_over_time(df,'Event')
    fig = px.line(nations,x="Edition",y="Event")
    st.plotly_chart(fig)


    st.title("No. of Athletes over the years")
    nations = hp.data_over_time(df,'Name')
    fig = px.line(nations,x="Edition",y="Name")
    st.plotly_chart(fig)


    st.title('No. of Events (Sports wise)')
    x = df.drop_duplicates(['Year','Sport','Event'])
    x_pivot = x.pivot_table(index='Sport',columns='Year',values = 'Event',aggfunc = 'count').fillna(0).astype('int')
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(x_pivot,annot=True)
    st.pyplot(fig)


    st.title('Top performing Athletes')
    top_athletes = hp.most_successful_athletes(df,'Overall')
    st.table(top_athletes)