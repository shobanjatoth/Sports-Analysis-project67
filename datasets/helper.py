from datetime import date
from turtle import st
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import streamlit as st




def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def data_over_time(df,col):

    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('count')
    nations_over_time.rename(columns={'count': 'Edition', 'Year': col}, inplace=True)
    return nations_over_time


def most_successful(df,sport=None):
    
    grouped = df.groupby(["Name", "Sport", "region", "Medal"]).size().reset_index(name="Number of Medals")

    # Filter by sport if provided
    if sport:
        grouped = grouped[grouped["Sport"] == sport]

    # Sort by the number of medals in descending order
    sorted_grouped = grouped.sort_values(by="Number of Medals", ascending=False).reset_index(drop=True).head(10)

    return sorted_grouped



def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df, country):
    # Drop rows with missing medals and remove duplicates
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    # Filter data for the selected country
    new_df = temp_df[temp_df['region'] == country]

    if new_df.empty:
        return pd.DataFrame()  # Return an empty DataFrame if no data for the country

    # Create the pivot table
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt



def most_successful_countrywise(df,country):
    new_data=df[df["Team"]==country]
    new_data= new_data.dropna(subset=['Medal'])
    filtered=new_data.groupby(["Name","Sport"])["Medal"].count().reset_index().sort_values(by="Medal",ascending=False).head(10)
    return filtered


    

def weight_v_height(df, sport):
    # Remove duplicate athletes
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Fill missing Medal values
    athlete_df['Medal'] = athlete_df['Medal'].fillna('No Medal')

    # Filter based on sport
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
    else:
        temp_df = athlete_df

    # Check if temp_df is empty
    if temp_df.empty:
        return None, f"No data available for the selected sport: {sport}"

    # Check if required columns exist
    if 'Weight' not in temp_df.columns or 'Height' not in temp_df.columns:
        return None, "Required columns ('Weight' and/or 'Height') are missing from the dataset."

    # Handle missing data
    temp_df = temp_df.dropna(subset=['Weight', 'Height'])
    if temp_df.empty:
        return None, f"No valid data available for the selected sport: {sport}"

    # Return valid DataFrame and no error
    return temp_df, None



def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final




#Cricket data
def list(data):
    player = data['batter'].unique().tolist()
    player.sort()
    return player


def calculate_player_card67(data, player_name):
    import pandas as pd

    # Filter data for the player as a batter and bowler
    batter_data = data[data["batter"] == player_name]
    bowler_data = data[data["bowler"] == player_name]

    # Batting Stats
    total_runs = batter_data["batsman_runs"].sum()
    balls_faced = batter_data["ball"].count()
    strike_rate = (total_runs / balls_faced) * 100 if balls_faced > 0 else 0

    # Calculate 50s and 100s
    match_scores = batter_data.groupby("id")["batsman_runs"].sum()
    fifty_plus = match_scores[match_scores >= 50].count()
    hundred_plus = match_scores[match_scores >= 100].count()
    highest_match_runs = match_scores.max() if not match_scores.empty else 0

    # Bowling Stats
    total_runs_conceded = bowler_data["total_runs"].sum()
    balls_bowled = bowler_data["ball"].count()
    overs_bowled = f"{balls_bowled // 6}.{balls_bowled % 6}"
    wickets_taken = bowler_data["is_wicket"].sum()
    economy_rate = total_runs_conceded / (balls_bowled / 6) if balls_bowled > 0 else 0

    # Latest Match and Team
    batter_latest_match_id = batter_data["id"].max() if not batter_data.empty else None
    bowler_latest_match_id = bowler_data["id"].max() if not bowler_data.empty else None
    latest_match_id = max(filter(None, [batter_latest_match_id, bowler_latest_match_id]), default=-1)

    # Get data for the latest match
    latest_batter_data = data[(data["batter"] == player_name) & (data["id"] == latest_match_id)]
    latest_bowler_data = data[(data["bowler"] == player_name) & (data["id"] == latest_match_id)]

    # Determine the current team based on the latest match
    current_team = ""
    if not latest_batter_data.empty:
        current_team = latest_batter_data.iloc[0]["batting_team"]
    elif not latest_bowler_data.empty:
        current_team = latest_bowler_data.iloc[0]["bowling_team"]

    # Calculate the number of matches played
    matches_played = len(batter_data["id"].unique())

    # Create the player card
    player_card = [
        ["Player Name", player_name],
        ["Current Team", current_team],
        ["Total Runs Scored", total_runs],
        ["Balls Faced", balls_faced],
        ["Strike Rate (%)", round(strike_rate, 2)],
        ["Half-Centuries", fifty_plus],
        ["Centuries", hundred_plus],
        ["Highest Match Runs", highest_match_runs],
        ["Matches Played", matches_played],
        ["Runs Conceded", total_runs_conceded],
        ["Balls Bowled", balls_bowled],
        ["Overs Bowled", overs_bowled],
        ["Wickets Taken", wickets_taken],
        ["Economy Rate (Runs/Over)", round(economy_rate, 2)],
    ]

    # Return as DataFrame with cricket-specific headers
    return pd.DataFrame(player_card, columns=["Stat Description", "Cricket Data"])



def list2(data):
    data['season'] = pd.to_numeric(data['season'], errors='coerce')  # Converts to numeric; invalid values become NaN
    data = data.dropna(subset=['season'])  # Drop rows where 'season' could not be converted
    data['season'] = data['season'].astype(int)  # Ensure the column is of integer type

    year = data['season'].unique().tolist()
    year.sort()
    # year.insert(0, 'Overall')

    team=data["batting_team"].unique().tolist()
    team.sort()
    return year,team



def teams(data,year,team):
    data['season'] = pd.to_numeric(data['season'], errors='coerce')  # Converts to numeric; invalid values become NaN
    data = data.dropna(subset=['season'])  # Drop rows where 'season' could not be converted
    data['season'] = data['season'].astype(int) 
    teams_by_year=data.groupby(["season","batting_team"])["batter"].unique().reset_index()
    filtered_data = teams_by_year[(teams_by_year["season"] == year) & (teams_by_year["batting_team"] == team)]
    return filtered_data

def winning_team(data1):
    df=data1.rename(columns={"Winner ":"Winner"})
    winner=df["Winner"].value_counts().reset_index()
    return winner

def loosing_team(data1):
    runner=data1["Runner-up"].value_counts().reset_index()
    return runner
