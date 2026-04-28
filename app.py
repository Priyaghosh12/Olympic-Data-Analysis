import streamlit as st
import pandas as pd
import Olympic_Preprocessor
import helper
from helper import medal_tally
st.set_page_config(layout="wide")

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = Olympic_Preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
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
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal TAlly in "+str(selected_year)+" olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country+" Overall Performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(f" {selected_country} performance in {selected_year}")
    st.table(medal_tally)


