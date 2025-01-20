import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

#cricket data
# data=pd.read_csv("datasets/deliveries.csv")
# data2=pd.read_csv("datasets/matches.csv")
data=pd.read_excel("datasets/cricket_ipl.xlsb",engine='pyxlsb')
data=preprocessor.ipl(data)

#tornment data
data1=pd.read_csv("datasets/tornament.csv")
data1=preprocessor.tornmet(data1)


def cricket_main():
    st.title("IPL Analysis")
    user_menu = st.sidebar.radio(
        'Select an Option',
        ('IPL Winners and Losers: A Historical Overview', 'Overall Analysis', 'Playercard', 'Teams in every Season')
    )
    if user_menu == 'IPL Winners and Losers: A Historical Overview':
        data2 = pd.read_csv("datasets/tornament.csv")
        st.table(data2)
    
    elif user_menu == "Overall Analysis":
        Seasons = data["season"].nunique()
        Total_Teams = data["team1"].nunique()
        Total_Batters = data["batter"].nunique()
        Total_Bowlers = data["bowler"].nunique()
        venues = data["venue"].nunique()
        cities = data["city"].nunique()

        st.title("Top Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Seasons")
            st.title(Seasons)
        with col2:
            st.header("Teams")
            st.title(Total_Teams)
        with col3:
            st.header("Batters")
            st.title(Total_Batters)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Bowlers")
            st.title(Total_Bowlers)
        with col2:
            st.header("Cities")
            st.title(cities)
        with col3:
            st.header("Venues")
            st.title(venues)
        



        winning_team_new = helper.winning_team(data1)
        fig = px.bar(winning_team_new, x="Winner", y="count", 
             labels={"Winner": "Team", "count": "Number of Wins"},
             color="Winner",  
             text="count") 
        st.title("IPL Teams with the Highest Number of Titles")
        st.plotly_chart(fig)


        lossing_team_new = helper.loosing_team(data1)
        fig = px.bar(lossing_team_new, x="Runner-up", y="count",
                     labels={"Runner-up": "Team", "count": "Number of lost"},
                     color="Runner-up"
                     )
        st.title("Most Runner-Up Finishes in IPL")
        st.plotly_chart(fig)

        Ipl_team_statics=pd.read_csv("datasets/Statics_team.csv")
        st.title("Win-Loss Ratios and Performance Percentages of IPL Teams (2008-2024)")
        st.table(Ipl_team_statics)

        #Barchats
        #loss
        fig = px.bar(Ipl_team_statics, x="Team",y="Lost",
                     labels={"Team": "Teams", "Lost": "Number of lost by a team"},
                     color="Team",  
                     text="Lost"
                     )
        st.title("Most Matches Lost by Teams in IPL")
        st.plotly_chart(fig)
       #Win
        fig = px.bar(Ipl_team_statics, x="Team",y="Won",
                     labels={"Team": "Teams", "Win": "Number of wins by a team"},
                     color="Team",  
                     text="Won"
                     )
        st.title("Most Matches Won by Teams in IPL")
        st.plotly_chart(fig)
         #lost percentage
        fig = px.bar(Ipl_team_statics, x="Team",y="%L",
                     labels={"Team": "Teams", "%L": "Loss Percentage"},
                     color="Team",  
                     text="%L"
                     )
        st.title("Loss Percentage of Teams in IPL")
        st.plotly_chart(fig)
        #win percentage
        fig = px.bar(Ipl_team_statics, x="Team",y="%W",
                     labels={"Team": "Teams", "%W": "Win Percentage"},
                     color="Team",  
                     text="%W"
                     )
        st.title("Win Percentage of Teams in IPL")
        st.plotly_chart(fig)

            
    elif user_menu == "Playercard":
        player= helper.list(data)
        selected_player = st.sidebar.selectbox("Select Player", player)
        player2= helper.calculate_player_card67(data, selected_player)
        st.title(f"Player Card: {selected_player}")
        st.table(player2)

    elif user_menu == 'Teams in every Season':
        year, team = helper.list2(data)  # Ensure helper.list2 returns proper values
        selected_team = st.sidebar.selectbox("Select Team", team)
        selected_year = st.sidebar.selectbox("Select Season", year)

    # Fetch team-wise data
        team_data = helper.teams(data, selected_year, selected_team)
        st.title(f"{selected_team}: in : {selected_year}")
        st.table(team_data )
