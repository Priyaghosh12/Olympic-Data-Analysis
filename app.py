import streamlit as st
import pandas as pd
import Olympic_Preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

st.set_page_config(layout="wide")

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = Olympic_Preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image("https://miro.medium.com/0*n4NPUUqqkVYCUWgt.png")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete-Wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("select Year",years)
    selected_country = st.sidebar.selectbox("select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.header("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.header("Medal TAlly in "+str(selected_year)+" olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.header(selected_country+" Overall Performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.header(f" {selected_country} performance in {selected_year}")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.header("Top Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Editions", editions)
        st.metric("Events", events)

    with col2:
        st.metric("Hosts", cities)
        st.metric("Nations", nations)

    with col3:
        st.metric("Sports", sports)
        st.metric("Athletes", f"{athletes:,}")

    nations_over_time = helper.data_over_time(df, 'region')
    st.header("Participating Nations Over Time")
    st.metric("Max Nations (Year)", int(nations_over_time['region'].max()))
    fig = px.line(
        nations_over_time,
        x='Editions',
        y='region'
    )
    fig.update_layout(template='simple_white',height=450,margin=dict(l=10, r=10, t=30, b=10),xaxis_title="Year",yaxis_title="Number of countries")
    fig.update_traces(line=dict(width=2),hovertemplate="Year: %{x}<br>Events: %{y}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

    events_over_time = helper.data_over_time(df, 'Event')
    st.header("Events Over Time")
    st.metric("Max Events (Year)", int(events_over_time['Event'].max()))
    fig = px.line(events_over_time,x='Editions',y='Event')
    fig.update_layout(template='simple_white',height=450,margin=dict(l=10, r=10, t=30, b=10),xaxis_title="Year",yaxis_title="Number of Events")
    fig.update_traces(line=dict(width=2),hovertemplate="Year: %{x}<br>Events: %{y}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

    athletes_over_time = helper.data_over_time(df, 'Name')
    st.header("Athletes over the years")
    st.metric("Max Athletes participated(Year)", int(events_over_time['Event'].max()))
    fig = px.line(athletes_over_time,x='Editions',y='Name')
    fig.update_layout(template='simple_white',height=450,margin=dict(l=10, r=10, t=30, b=10),xaxis_title="Year",yaxis_title="Number of Athletes")
    fig.update_traces(line=dict(width=2),hovertemplate="Year: %{x}<br>Events: %{y}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

    st.header("Number of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)


    st.header("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a  Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-Wise Analysis':

    st.sidebar.title("Country-Wise Analysis")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)

    st.header(selected_country + " Medal Tally over the years")

    if country_df is None:
        st.info(f"{selected_country} has no recorded medal history.")
    else:
        fig = px.line(country_df,x='Year',y='Medal')
        fig.update_layout(template='simple_white',height=450,margin=dict(l=10, r=10, t=30, b=10),xaxis_title="Year",yaxis_title="Medal")
        fig.update_traces(
            line=dict(width=2),
            hovertemplate="Year: %{x}<br>Medals: %{y}<extra></extra>"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.header(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    if pt is None:
        st.warning("No medal data available for this country")
    else:
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.heatmap(pt, annot=True, ax=ax)
        st.pyplot(fig)

    st.title("Top 10 Athletes of "+selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete-Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.show()
    fig.update_layout(autosize=False,width=1000,height=600)
    st.header("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming',
                     'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions', 'Handball',
                     'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Equestrianism', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving',
                     'Canoeing', 'Tennis', 'Modern Pentathlon', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining', 'Beach Volleyball',
                     'Triathlon', 'Rugby', 'Lacrosse', 'Polo', 'Cricket', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.header("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = sorted(df['Sport'].dropna().unique().tolist())
    sport_list.insert(0, 'Overall')
    st.header("Height vs Weight")
    selected_sport = st.selectbox('Select a Sport', sport_list)
    filtered_df = helper.weight_vs_height(df, selected_sport)
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_df,x='Weight',y='Height',hue='Medal',style='Sex',s=60,ax=ax)
    ax.set_title(f'Height vs Weight Analysis ({selected_sport})')
    ax.set_xlabel('Weight (kg)')
    ax.set_ylabel('Height (cm)')
    ax.legend(title='Legend', bbox_to_anchor=(1.05, 1), loc='upper left')

    st.pyplot(fig)

    st.header("Men vs Women Participation Over the Year")
    final = helper.men_vs_women(df)
    fig = px.line(final, x = 'Year', y = ['Male','Female'])
    st.plotly_chart(fig)