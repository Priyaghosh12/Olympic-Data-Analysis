import streamlit as st
import pandas as pd
import Olympic_Preprocessor
import helper
from helper import medal_tally

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
    medal_tally = helper.medal_tally(df)
    st.dataframe(medal_tally)

