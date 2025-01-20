
import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df=pd.read_excel("datasets/olympic1.xlsb",engine='pyxlsb')
df = preprocessor.preprocess(df)


def app_main():
    # Check if the selected sport is Olympics
    # if st.session_state.selected_sport == "Olympics":
        st.title("Olympics Analysis")

        # User menu with options
        user_menu = st.sidebar.radio(
        'Select an Option',
        ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
         )
       
        # Medal Tally Analysis
        if user_menu == 'Medal Tally':
            st.header("Medal Tally")
            years, country = helper.country_year_list(df)

            selected_year = st.sidebar.selectbox("Select Year", years)
            selected_country = st.sidebar.selectbox("Select Country", country)

            medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

            # Display appropriate titles based on user selections
            if selected_year == 'Overall' and selected_country == 'Overall':
                st.title("Overall Tally")
            elif selected_year != 'Overall' and selected_country == 'Overall':
                st.title(f"Medal Tally in {selected_year} Olympics")
            elif selected_year == 'Overall' and selected_country != 'Overall':
                st.title(f"{selected_country} Overall Performance")
            else:
                st.title(f"{selected_country} Performance in {selected_year} Olympics")

            st.table(medal_tally)

        # Overall Analysis
        elif user_menu == "Overall Analysis":
            editions = df["Year"].unique().shape[0] - 1
            cities = df["City"].unique().shape[0]
            sports = df["Sport"].unique().shape[0]
            events = df["Event"].unique().shape[0]
            athletes = df["Name"].unique().shape[0]
            nations = df["region"].unique().shape[0]

            st.title("Top Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.header("Editions")
                st.title(editions)
            with col2:
                st.header("Cities")
                st.title(cities)
            with col3:
                st.header("Sports")
                st.title(sports)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.header("Events")
                st.title(events)
            with col2:
                st.header("Athletes")
                st.title(athletes)
            with col3:
                st.header("Nations")
                st.title(nations)

            # Participating Nations Over Time
            nations_over_time = helper.data_over_time(df, 'region')
            fig = px.line(nations_over_time, x="Edition", y="region")
            st.title("Participating Nations Over the Years")
            st.plotly_chart(fig)

            # Events Over Time
            events_over_time = helper.data_over_time(df, 'Event')
            fig = px.line(events_over_time, x="Edition", y="Event")
            st.title("Events Over the Years")
            st.plotly_chart(fig)

            # Athletes Over Time
            athlete_over_time = helper.data_over_time(df, 'Name')
            fig = px.line(athlete_over_time, x="Edition", y="Name")
            st.title("Athletes Over the Years")
            st.plotly_chart(fig)

            # Heatmap of Events Per Sport
            st.title("Number of Events Over Time (Every Sport)")
            fig, ax = plt.subplots(figsize=(20, 20))
            event_pivot = (
                df.drop_duplicates(['Year', 'Sport', 'Event'])
                .pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count')
                .fillna(0)
                .astype('int')
            )
            sns.heatmap(event_pivot, annot=True, ax=ax)
            st.pyplot(fig)

            # Most Successful Athletes
            st.title("Most Successful Athletes")
            sport_list = sorted(df['Sport'].unique().tolist())
            sport_list.insert(0, 'Overall')

            selected_sport = st.selectbox('Select a Sport', sport_list)
            most_successful = helper.most_successful(df, selected_sport)
            st.table(most_successful)

        # Country-wise Analysis
        elif user_menu == 'Country-wise Analysis':
            st.header("Country-wise Analysis")
            country_list = sorted(df['region'].dropna().unique().tolist())

            selected_country = st.selectbox('Select a Country', country_list)
            country_df = helper.yearwise_medal_tally(df, selected_country)

            fig = px.line(country_df, x="Year", y="Medal")
            st.title(f"{selected_country} Medal Tally Over the Years")
            st.plotly_chart(fig)

            st.title(f"{selected_country} Excels in the Following Sports")
            pt = helper.country_event_heatmap(df, selected_country)
            if pt.empty:
                st.warning(f"No data available for {selected_country} to plot the heatmap.")
            else:
                fig, ax = plt.subplots(figsize=(20, 20))
                sns.heatmap(pt, annot=True, ax=ax)
                st.pyplot(fig)

            st.title(f"Top 10 Athletes of {selected_country}")
            top10_df = helper.most_successful_countrywise(df, selected_country)
            st.table(top10_df)

        # Athlete-wise Analysis
        elif user_menu == 'Athlete wise Analysis':
            athlete_df = df.drop_duplicates(subset=['Name', 'region'])

            # Age Distribution
            st.title("Distribution of Age")
            x1 = athlete_df['Age'].dropna()
            x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
            x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
            x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

            fig = ff.create_distplot(
                [x1, x2, x3, x4],
                ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                show_hist=False, show_rug=False,
            )
            fig.update_layout(autosize=False, width=1000, height=600)
            st.plotly_chart(fig)

            # Height vs Weight
            st.title('Height vs Weight')
            sport_list = sorted(df['Sport'].unique().tolist())
            sport_list.insert(0, 'Overall')
            selected_sport = st.selectbox('Select a Sport', sport_list)

            temp_df, error_message = helper.weight_v_height(df, selected_sport)
            if error_message:
                st.warning(error_message)
            elif isinstance(temp_df, pd.DataFrame):
                fig, ax = plt.subplots()
                sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=60, ax=ax)
                st.pyplot(fig)
            else:
                st.warning("Something went wrong. Data unavailable.")

            # Men vs Women Participation
            st.title("Men vs Women Participation Over the Years")
            final = helper.men_vs_women(df)
            fig = px.line(final, x="Year", y=["Male", "Female"])
            fig.update_layout(autosize=False, width=1000, height=600)
            st.plotly_chart(fig)




