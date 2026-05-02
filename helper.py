import numpy as np

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                             ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df

    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]

    elif year != 'Overall' and country == 'Overall':
        year = int(year)
        temp_df = medal_df[medal_df['Year'] == year]

    else:
        year = int(year)
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == year)]

    if flag == 1:
        x = temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Year',
                                                                                    ascending=True).reset_index()

    else:
        x = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values(
        'Year')
    nations_over_time.rename(columns={'Year': 'Editions', 'count':col}, inplace=True)

    return nations_over_time

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    top = temp_df['Name'].value_counts().reset_index()
    top.columns = ['Name', 'Medals']

    result = top.head(15).merge(df, on='Name', how='left')

    return result[['Name', 'Sport', 'region']].drop_duplicates('Name')

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal']).copy()

    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    final_df = temp_df[temp_df['region'] == country]

    if final_df.empty:
        return None

    final_df = final_df.groupby('Year').count()['Medal'].reset_index()
    if final_df.empty:
        return None

    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal']).copy()

    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    final_df = temp_df[temp_df['region'] == country]

    if final_df.empty:
        return None
    pt = final_df.pivot_table(
        index='Sport',
        columns='Year',
        values='Medal',
        aggfunc='count'
    ).fillna(0)

    if pt.empty:
        return None

    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    top = temp_df['Name'].value_counts().reset_index()
    top.columns = ['Name', 'Medals']
    result = top.head(10).merge(df, on='Name', how='left')

    return result[['Name', 'Medals', 'Sport']].drop_duplicates('Name')

def weight_vs_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'] = athlete_df['Medal'].fillna('No Medal')
    if sport!= 'Overall':
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