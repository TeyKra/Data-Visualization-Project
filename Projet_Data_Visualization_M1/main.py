import pandas as pd
import numpy as np
import missingno as msno
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
import altair as alt
from matplotlib import colors
from streamlit_folium import folium_static
from folium import plugins
from folium.plugins import FastMarkerCluster, HeatMap
import folium
import plotly.express as px
import plotly.graph_objects as go
import altair_viewer
import json

st.title("Bike accidents and injuries in France")

st.write("cache memory is used to make your computation faster")


@st.cache_data
def load_data():
    return pd.read_csv('accidentsVelo.csv', delimiter=",")

print("Here is our cleared database")
df = load_data()
print(df)
print(df.shape)
print(df.describe())

print("We have to drop rows with missing values:")
df = df.dropna().reset_index(drop=True)
print("DataFrame after removing rows with missing values:")
print(df.head(5))
print(df.shape)
print("Number of missing values per column after the changes:")
print(df.isnull().sum().head(5))

print("Removing Duplicate Values")
duplicate_rows = df[df.duplicated()]
print("Duplicate Rows:")
df = df.drop_duplicates(keep='first').reset_index(drop=True)
print("DataFrame after removing duplicates:")
print(df.head(5))
print(df.shape)


print("Reformatting Some Columns:")
df["date"] = pd.to_datetime(df["date"]).dt.strftime("%d/%m/%Y")
df['an'] = df['an'].astype(str).str.replace(',', '')
print("DataFrame after reformatting 'date' and 'an' columns:")
print(df.head(5))


print("droping useless datas:")
df = df.drop(columns=["plan", "lartpc", "larrout", "Num_Acc", "int", "secuexist", "vehiculeid", "manoeuvehicules"])
print("DataFrame after dropping columns:")
print(df.head(5))
print(df.shape)

# Convert latitude and longitude columns to numeric type.
df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
df['long'] = pd.to_numeric(df['long'], errors='coerce')
# Remove rows with missing latitude and longitude values.
df.dropna(subset=['lat', 'long'], inplace=True)


print("Remake the column 'age':")
# Filter the DataFrame based on age and hour conditions.
df = df[(df['age'] >= 0) & (df['age'] <= 120)]
df['hrmn'] = df['hrmn'].str.split(':').str[0]
df = df[df['hrmn'].astype(int).between(0, 23)]
print(df.head(5))
df.shape

def display_Project():
    st.header('Why did i choose this subject ? ')
    st.write('Bike accidents can occur at every moment of our lives. My first injury, and the first injury of many of us was during a bike accident that was meant to be a travel in family. In this dataset, we will find bike accident that occurs from 2005 to 2021 with at least one person going to the hospital.')
    st.write('In order to indentify the potential risks for me and my family of aciddents, i wanted to analyse this dataset in all of his aspects. This page may look empty at the first look, but will go bigger as you will explore his content.')
    st.write('Please find the original dataset at this link: https://www.data.gouv.fr/fr/datasets/accidents-de-velo/ .')
    st.write("lets explore  together the dataset, you will here see only the visualisation of the dataset, don't hesitate to check the read-me file to have further informations." )

    st.header("Visualization")
    # Creating a dropdown menu for the user to select the type of chart they'd like to see.
    option = st.selectbox(
        "Select a chart",
        ('Distribution by Month', 'Distribution by Day of the Week',
        'Age Distribution', 'Lighting Conditions',
        'Atmospheric Conditions'))

    # Checking the user's selection and plotting the corresponding chart.
    if option == 'Distribution by Month':
        st.write("This visualization shows a distribution of accidents by month. The warmer months, namely June, July, and August, have a higher number of accidents compared to other months. Maybe because of an increase in travel or outdoor activities. The winter months, particularly November and December, record the lowest accident numbers of the year, maybe because it's to cold to go outside.")

        # Grouping accidents by month and counting them.
        month_counts = df.groupby('mois').size().reset_index(name='counts')
        # Ordering the months.
        month_order = ["janvier", "février", "mars", "avril", "mai", "juin",
                       "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
        # Organizing the month counts in the correct order.
        month_counts['mois'] = pd.Categorical(month_counts['mois'], categories=month_order, ordered=True)
        month_counts = month_counts.sort_values('mois')
        # Plotting the distribution of accidents by month.
        fig = px.bar(month_counts, x='mois', y='counts', title='Accident Distribution by Month')
        st.plotly_chart(fig)

    elif option == 'Distribution by Day of the Week':
        st.write("Distribution of accidents by day of the week: Accidents are fairly evenly distributed from Monday to Friday, with a slight decrease on Saturday and a more significant drop on Sunday. We can maybe say that people are more carefull on the week end or maybe they just doesn't take their bike.")

        # Grouping accidents by day of the week and counting them.
        day_counts = df.groupby('jour').size().reset_index(name='counts')
        # Ordering the days.
        day_order = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi",
                       "dimanche"]
        # Organizing the day counts in the correct order.
        day_counts['jour'] = pd.Categorical(day_counts['jour'], categories=day_order, ordered=True)
        day_counts = day_counts.sort_values('jour')
        # Plotting the distribution of accidents by day of the week.
        fig = px.bar(day_counts, x='jour', y='counts', title='Accident Distribution by Day of the Week')
        st.plotly_chart(fig)


    elif option == 'Age Distribution':

        st.write("Most of accident is at 20 YO.")

        # Grouping accidents by age and counting them.
        age_counts = df.groupby('age').size().reset_index(name='counts')
        # Organizing the age counts in order.
        age_counts['age'] = pd.Categorical(age_counts['age'],  ordered=True)
        age_counts = age_counts.sort_values('age')
        # Plotting the distribution of accidents by age.
        fig = px.bar(age_counts, x='age', y='counts', title='Accident Distribution by Age')
        st.plotly_chart(fig)

    elif option == 'Lighting Conditions':

        st.write("The majority of accidents heppend during daytime")

        # Grouping accidents by lighting conditions and counting them.
        lum_counts = df.groupby('lum').size().reset_index(name='counts')
        lum_counts['lum'] = pd.Categorical(lum_counts['lum'], ordered=True)
        lum_counts = lum_counts.sort_values('lum')
        # Creating a mapping for the lighting conditions.
        lum_mapping = {
            1: "Full daylight",
            2: "Dusk or dawn",
            3: "Night without public lighting",
            4: "Night with public lighting off",
            5: "Night with public lighting on"
        }
        # Applying the mapping to the 'lum' column.
        lum_counts['lum_label'] = lum_counts['lum'].map(lum_mapping)

        # Plotting the distribution of accidents by lighting condition.
        fig = px.bar(lum_counts, x='lum_label', y='counts',
                     title='Accident Distribution by Lighting Conditions')

        st.plotly_chart(fig)

    elif option == 'Atmospheric Conditions':

        # Grouping accidents by atmospheric conditions and counting them.
        atm_counts = df.groupby('atm').size().reset_index(name='counts')
        atm_counts['atm'] = pd.Categorical(atm_counts['atm'], ordered=True)
        atm_counts = atm_counts.sort_values('atm')
        # Creating a mapping for the atmospheric conditions.
        atm_mapping = {
            -1: "Not specified",
            1: "Normal",
            2: "Light rain",
            3: "Heavy rain",
            4: "Snow - hail",
            5: "Fog - smoke",
            6: "Strong wind - storm",
            7: "Dazzling weather",
            8: "Overcast",
            9: "Other"
        }
        # Applying the mapping to the 'atm' column.
        atm_counts['atm_label'] = atm_counts['atm'].map(atm_mapping)
        # Plotting the distribution of accidents by atmospheric condition.
        fig = px.bar(atm_counts, x='atm_label', y='counts',
                     title='Accident Distribution by Atmospheric Conditions')
        st.plotly_chart(fig)

        st.write("Despite normal being first, because this is the major weather. Light rain is first after we have overcast and dazzling weather.")


    viz_radio = st.radio("Choose a visualisation :",
        ("Heatmap of the accident frequencies by hours", "Bar plot of the injuries by genders", "Pie chart of accident during time"))

    if viz_radio == "Heatmap of the accident frequencies by hours":

        df['hrmn'] = df['hrmn'].astype(int)
        # Create a pivot table to represent data for heatmap (hour vs. day of the week).
        pivot_df = df.groupby(['hrmn', 'jour']).size().reset_index(name='counts')
        heatmap_data = pivot_df.pivot_table(values='counts', index='jour', columns='hrmn', fill_value=0)
        heatmap_data = heatmap_data.sort_index(axis=1)
        plt.figure(figsize=(12, 7))
        heatmap = sns.heatmap(heatmap_data, cmap="YlGnBu", linewidths=.5)
        # Information about heatmap.
        plt.title('Heatmap by Hour (hr) and Weekdays (jour)', fontsize=15)
        heatmap.set_yticklabels(('Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'), rotation='horizontal')
        st.pyplot(plt)
        st.write("Heatmap by hour and day of the week: Darker shades (blue) indicate hours and days with a high concentration of accidents. It appears that weekday afternoons have the highest number of accidents.")

    elif viz_radio == "Bar plot of the injuries by genders":
        # Creating a plot to represent distribution of accident severity by gender.
        df_sexe = df.copy()
        df_sexe['sexe'] = df_sexe['sexe'].map({1: 'Male', 2: 'Female'})
        plt.figure(figsize=(5, 3))
        sns.histplot(x='grav', data=df_sexe, kde=True, hue='sexe', bins=20)
        plt.title("Distribution of Severity by Sexe of cyclist")
        st.pyplot(plt)
        # Information about the severity plot.
        st.write("Severity Distribution by Gender: Both males and females exhibit similar accident trends, with severity level 4 (likely minor injuries) being the most common for both genders, with a male predominance across all severity levels.")

    elif viz_radio == "Pie chart of accident during time":
        # Allow users to select a year and month to filter data for a pie chart.
        selected_year = st.selectbox('Select a year:', sorted(df['an'].unique(), reverse=True))
        df_year = df[df['an'] == selected_year]
        selected_month = st.selectbox('Select a month:', sorted(df_year['mois'].unique()))
        # Plotting the pie chart for selected year and month.
        df_month = df_year[df_year['mois'] == selected_month]
        fig = px.pie(df_month, values=df_month['jour'].value_counts().values,
                     names=df_month['jour'].value_counts().index,
                     title=f"Distribution of Accidents by Day for {selected_month}/{selected_year}")
        st.plotly_chart(fig)
        st.write(
            "Pie Chart: Displays accident distribution by day, you can modify the month")

    number_choice = st.number_input("1: bubble chart, 2: superposed maping",value=None, placeholder="Please enter a number 1, 2")

    if number_choice ==1:

        # The size of each point is determined by the severity of the accident.
        fig = px.scatter(df, x='lat', y='long', size='grav', color='atm',
                         hover_data=['typevehicules', 'manv'],
                         title='Bubble Chart of Latitude vs Longitude by Severity and Atmospheric Conditions',
                         labels={'lat': 'Latitude', 'long': 'Longitude', 'grav': 'Severity',
                                 'atm': 'Atmospheric Conditions'})
        st.plotly_chart(fig)
        st.write("We can see a strong concentration on the right of the graph, this longitude/latitude/Atmospherique condition are favorable to accidents")


    elif number_choice == 2:
        # Defining order for days of the week and months.
        jours_order = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
        mois_order = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
                      "novembre", "décembre"]
        # Converting 'jour' and 'mois' columns to ordered categorical data types.
        df['jour'] = pd.Categorical(df['jour'], categories=jours_order, ordered=True)
        df['mois'] = pd.Categorical(df['mois'], categories=mois_order, ordered=True)
        # Mapping integers in the 'trajet' column to their corresponding descriptive strings.
        trajet_mapping = {
            0: "Not specified",
            1: "Home – work",
            2: "Home – school",
            3: "Grocery shopping – errands",
            4: "Professional use",
            5: "Leisure – recreational",
            9: "Other"
        }
        # Applying the mapping to a copy of the original dataframe.
        df_trajet = df.copy()
        df_trajet['trajet'] = df_trajet['trajet'].replace(trajet_mapping)
        # Creating a dropdown box for users to select a time dimension.

        options = ['mois', 'an', 'jour']
        selected_option = st.selectbox('Choose a time dimension', options)
        if selected_option == "mois":
            st.write("Monthly Trajectory Chart: Peaks occur around mid-year, with 'Leisure – recreational' having the most incidents")
        elif selected_option == "an":
            st.write("A slight decrease over time, with 'Leisure – recreational' consistently highest")
        elif selected_option == "jour":
            st.write("same visualisation than in another plot, we have more accidents in the middle of the week")

        # Grouping the data by the selected time dimension and 'trajet'.
        grouped_df = df_trajet.groupby([selected_option, 'trajet']).size().reset_index(name='nombre')
        # Setting a specified order for the 'trajet' column.
        trajet_order = ["Grocery shopping – errands", "Professional use", "Home – school", "Other", "Home – work",
                        "Not specified", "Leisure – recreational"]
        grouped_df['trajet'] = pd.Categorical(grouped_df['trajet'], categories=trajet_order, ordered=True)
        grouped_df = grouped_df.sort_values(by=[selected_option, 'trajet'])
        fig = px.area(grouped_df, x=selected_option, y="nombre", color="trajet",
                      title=f"Number of Incidents by {selected_option} and according to the Trajectory",
                      labels={"nombre": "Number of Incidents", selected_option: selected_option.capitalize(),
                              "trajet": "Trajectory"})
        st.plotly_chart(fig, use_container_width=True)

        blessed_leger = df[df['grav'] == 4].groupby('an').size()
        blessed_hospitalise = df[df['grav'] == 3].groupby('an').size()
        indemne = df[df['grav'] == 1].groupby('an').size()
        tue = df[df['grav'] == 2].groupby('an').size()


def display_introduction():
    st.header('Why did i choose this subject ? ')
    st.write('Bike accidents can occur at every moment of our lives. My first injury, and the first injury of many of us was during a bike accident that was meant to be a travel in family. In this dataset, we will find bike accident that occurs from 2005 to 2021 with at least one person going to the hospital.')
    st.write('Please find the original dataset at this link: https://www.data.gouv.fr/fr/datasets/accidents-de-velo/ .')
    st.write("lets explore  together the dataset, you will here see only the visualisation of the dataset, don't hesitate to check the read-me file to have further informations")


def display_datavisualizations():
    st.header("Visualization")
    # Creating a dropdown menu for the user to select the type of chart they'd like to see.
    option = st.selectbox(
        "Select a chart",
        ('Distribution by Month', 'Distribution by Day of the Week',
         'Age Distribution', 'Lighting Conditions',
         'Atmospheric Conditions'))

    # Checking the user's selection and plotting the corresponding chart.
    if option == 'Distribution by Month':
        st.write(
            "This visualization shows a distribution of accidents by month. The warmer months, namely June, July, and August, have a higher number of accidents compared to other months. Maybe because of an increase in travel or outdoor activities. The winter months, particularly November and December, record the lowest accident numbers of the year, maybe because it's to cold to go outside.")

        # Grouping accidents by month and counting them.
        month_counts = df.groupby('mois').size().reset_index(name='counts')
        # Ordering the months.
        month_order = ["janvier", "février", "mars", "avril", "mai", "juin",
                       "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
        # Organizing the month counts in the correct order.
        month_counts['mois'] = pd.Categorical(month_counts['mois'], categories=month_order, ordered=True)
        month_counts = month_counts.sort_values('mois')
        # Plotting the distribution of accidents by month.
        fig = px.bar(month_counts, x='mois', y='counts', title='Accident Distribution by Month')
        st.plotly_chart(fig)

    elif option == 'Distribution by Day of the Week':
        st.write(
            "Distribution of accidents by day of the week: Accidents are fairly evenly distributed from Monday to Friday, with a slight decrease on Saturday and a more significant drop on Sunday. We can maybe say that people are more carefull on the week end or maybe they just doesn't take their bike.")

        # Grouping accidents by day of the week and counting them.
        day_counts = df.groupby('jour').size().reset_index(name='counts')
        # Ordering the days.
        day_order = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi",
                     "dimanche"]
        # Organizing the day counts in the correct order.
        day_counts['jour'] = pd.Categorical(day_counts['jour'], categories=day_order, ordered=True)
        day_counts = day_counts.sort_values('jour')
        # Plotting the distribution of accidents by day of the week.
        fig = px.bar(day_counts, x='jour', y='counts', title='Accident Distribution by Day of the Week')
        st.plotly_chart(fig)


    elif option == 'Age Distribution':

        st.write(
            "Distribution of accidents by age: There is a clear peak for individuals under 20 years old, followed by a gradual decline up to the age of 80 and older.")

        # Grouping accidents by age and counting them.
        age_counts = df.groupby('age').size().reset_index(name='counts')
        # Organizing the age counts in order.
        age_counts['age'] = pd.Categorical(age_counts['age'], ordered=True)
        age_counts = age_counts.sort_values('age')
        # Plotting the distribution of accidents by age.
        fig = px.bar(age_counts, x='age', y='counts', title='Accident Distribution by Age')
        st.plotly_chart(fig)

    elif option == 'Lighting Conditions':

        st.write(
            "Distribution of accidents by lighting conditions: The majority of accidents occur during daylight, followed at a distance by accidents happening at night with public lighting on. Other lighting conditions are significantly less common.")

        # Grouping accidents by lighting conditions and counting them.
        lum_counts = df.groupby('lum').size().reset_index(name='counts')
        lum_counts['lum'] = pd.Categorical(lum_counts['lum'], ordered=True)
        lum_counts = lum_counts.sort_values('lum')
        # Creating a mapping for the lighting conditions.
        lum_mapping = {
            1: "Full daylight",
            2: "Dusk or dawn",
            3: "Night without public lighting",
            4: "Night with public lighting off",
            5: "Night with public lighting on"
        }
        # Applying the mapping to the 'lum' column.
        lum_counts['lum_label'] = lum_counts['lum'].map(lum_mapping)

        # Plotting the distribution of accidents by lighting condition.
        fig = px.bar(lum_counts, x='lum_label', y='counts',
                     title='Accident Distribution by Lighting Conditions')

        st.plotly_chart(fig)

    elif option == 'Atmospheric Conditions':

        # Grouping accidents by atmospheric conditions and counting them.
        atm_counts = df.groupby('atm').size().reset_index(name='counts')
        atm_counts['atm'] = pd.Categorical(atm_counts['atm'], ordered=True)
        atm_counts = atm_counts.sort_values('atm')
        # Creating a mapping for the atmospheric conditions.
        atm_mapping = {
            -1: "Not specified",
            1: "Normal",
            2: "Light rain",
            3: "Heavy rain",
            4: "Snow - hail",
            5: "Fog - smoke",
            6: "Strong wind - storm",
            7: "Dazzling weather",
            8: "Overcast",
            9: "Other"
        }
        # Applying the mapping to the 'atm' column.
        atm_counts['atm_label'] = atm_counts['atm'].map(atm_mapping)
        # Plotting the distribution of accidents by atmospheric condition.
        fig = px.bar(atm_counts, x='atm_label', y='counts',
                     title='Accident Distribution by Atmospheric Conditions')
        st.plotly_chart(fig)

        st.write(
            "Despite normal being first, because this is the major weather. Light rain is first after we have overcast and dazzling weather.")

    viz_radio = st.radio("Choose a visualisation :",
                         ("Heatmap of the accident frequencies by hours", "Bar plot of the injuries by genders",
                          "Pie chart of accident during time"))

    if viz_radio == "Heatmap of the accident frequencies by hours":

        df['hrmn'] = df['hrmn'].astype(int)
        # Create a pivot table to represent data for heatmap (hour vs. day of the week).
        pivot_df = df.groupby(['hrmn', 'jour']).size().reset_index(name='counts')
        heatmap_data = pivot_df.pivot_table(values='counts', index='jour', columns='hrmn', fill_value=0)
        heatmap_data = heatmap_data.sort_index(axis=1)
        plt.figure(figsize=(12, 7))
        heatmap = sns.heatmap(heatmap_data, cmap="YlGnBu", linewidths=.5)
        # Information about heatmap.
        plt.title('Heatmap by Hour (hr) and Weekdays (jour)', fontsize=15)
        heatmap.set_yticklabels(('Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'), rotation='horizontal')
        st.pyplot(plt)
        st.write(
            "Heatmap by hour and day of the week: Darker shades (blue) indicate hours and days with a high concentration of accidents. It appears that weekday afternoons have the highest number of accidents.")

    elif viz_radio == "Bar plot of the injuries by genders":
        # Creating a plot to represent distribution of accident severity by gender.
        df_sexe = df.copy()
        df_sexe['sexe'] = df_sexe['sexe'].map({1: 'Male', 2: 'Female'})
        plt.figure(figsize=(5, 3))
        sns.histplot(x='grav', data=df_sexe, kde=True, hue='sexe', bins=20)
        plt.title("Distribution of Severity by Sexe of cyclist")
        st.pyplot(plt)
        # Information about the severity plot.
        st.write(
            "Severity Distribution by Gender: Both males and females exhibit similar accident trends, with severity level 4 (likely minor injuries) being the most common for both genders, with a male predominance across all severity levels.")

    elif viz_radio == "Pie chart of accident during time":
        # Allow users to select a year and month to filter data for a pie chart.
        selected_year = st.selectbox('Select a year:', sorted(df['an'].unique(), reverse=True))
        df_year = df[df['an'] == selected_year]
        selected_month = st.selectbox('Select a month:', sorted(df_year['mois'].unique()))
        # Plotting the pie chart for selected year and month.
        df_month = df_year[df_year['mois'] == selected_month]
        fig = px.pie(df_month, values=df_month['jour'].value_counts().values,
                     names=df_month['jour'].value_counts().index,
                     title=f"Distribution of Accidents by Day for {selected_month}/{selected_year}")
        st.plotly_chart(fig)
        st.write(
            "Pie Chart: Displays accident distribution by day, you can modify the month")

    number_choice = st.number_input("1: bubble chart, 2: superposed maping", value=None,
                                    placeholder="Please enter a number 1, 2")

    if number_choice == 1:

        # The size of each point is determined by the severity of the accident.
        fig = px.scatter(df, x='lat', y='long', size='grav', color='atm',
                         hover_data=['typevehicules', 'manv'],
                         title='Bubble Chart of Latitude vs Longitude by Severity and Atmospheric Conditions',
                         labels={'lat': 'Latitude', 'long': 'Longitude', 'grav': 'Severity',
                                 'atm': 'Atmospheric Conditions'})
        st.plotly_chart(fig)
        st.write(
            "We can see a strong concentration on the right of the graph, this longitude/latitude/Atmospherique condition are favorable to accidents")


    elif number_choice == 2:
        # Defining order for days of the week and months.
        jours_order = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
        mois_order = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
                      "novembre", "décembre"]
        # Converting 'jour' and 'mois' columns to ordered categorical data types.
        df['jour'] = pd.Categorical(df['jour'], categories=jours_order, ordered=True)
        df['mois'] = pd.Categorical(df['mois'], categories=mois_order, ordered=True)
        # Mapping integers in the 'trajet' column to their corresponding descriptive strings.
        trajet_mapping = {
            0: "Not specified",
            1: "Home – work",
            2: "Home – school",
            3: "Grocery shopping – errands",
            4: "Professional use",
            5: "Leisure – recreational",
            9: "Other"
        }
        # Applying the mapping to a copy of the original dataframe.
        df_trajet = df.copy()
        df_trajet['trajet'] = df_trajet['trajet'].replace(trajet_mapping)
        # Creating a dropdown box for users to select a time dimension.

        options = ['mois', 'an', 'jour']
        selected_option = st.selectbox('Choose a time dimension', options)
        if selected_option == "mois":
            st.write(
                "Monthly Trajectory Chart: Peaks occur around mid-year, with 'Leisure – recreational' having the most incidents")
        elif selected_option == "an":
            st.write("A slight decrease over time, with 'Leisure – recreational' consistently highest")
        elif selected_option == "jour":
            st.write("same visualisation than in another plot, we have more accidents in the middle of the week")

        # Grouping the data by the selected time dimension and 'trajet'.
        grouped_df = df_trajet.groupby([selected_option, 'trajet']).size().reset_index(name='nombre')
        # Setting a specified order for the 'trajet' column.
        trajet_order = ["Grocery shopping – errands", "Professional use", "Home – school", "Other", "Home – work",
                        "Not specified", "Leisure – recreational"]
        grouped_df['trajet'] = pd.Categorical(grouped_df['trajet'], categories=trajet_order, ordered=True)
        grouped_df = grouped_df.sort_values(by=[selected_option, 'trajet'])
        fig = px.area(grouped_df, x=selected_option, y="nombre", color="trajet",
                      title=f"Number of Incidents by {selected_option} and according to the Trajectory",
                      labels={"nombre": "Number of Incidents", selected_option: selected_option.capitalize(),
                              "trajet": "Trajectory"})
        st.plotly_chart(fig, use_container_width=True)

        blessed_leger = df[df['grav'] == 4].groupby('an').size()
        blessed_hospitalise = df[df['grav'] == 3].groupby('an').size()
        indemne = df[df['grav'] == 1].groupby('an').size()
        tue = df[df['grav'] == 2].groupby('an').size()

def main_display_map():

    st.subheader("Mapping of Bicycle Accidents between 2005 and 2021 based on severals variables of the accident")

    from streamlit_folium import folium_static

    grav_options = ["Unharmed", "Killed", "Hospitalized injured", "Slightly injured"]
    grav_selected = st.multiselect("Select the gravity.", options=grav_options)
    # Create a dictionary to map the string representation of severity to its numerical value.
    grav_mapping = {
        "Unharmed": 1,
        "Killed": 2,
        "Hospitalized injured": 3,
        "Slightly injured": 4
    }
    # Convert the selected severity levels from string to their corresponding numerical values.
    grav_values = [grav_mapping[grav] for grav in grav_selected]
    sex_options = ["Male", "Female"]
    sex_selected = st.multiselect('Select the gender', options=sex_options)
    sex_mapping = {
        "Male": 1,
        "Female": 2
    }
    sex_values = [sex_mapping[sex] for sex in sex_selected]
    col_options = [
        "Not specified",
        "Two vehicles - head-on",
        "Two vehicles - rear-end",
        "Two vehicles - side impact",
        "Three or more vehicles - chain reaction",
        "Three or more vehicles - multiple collisions",
        "Other collision",
        "No collision"
    ]
    col_selected = st.multiselect("Select the type of collision", options=col_options)
    col_mapping = {
        "Not specified": -1,
        "Two vehicles - head-on": 1,
        "Two vehicles - rear-end": 2,
        "Two vehicles - side impact": 3,
        "Three or more vehicles - chain reaction": 4,
        "Three or more vehicles - multiple collisions": 5,
        "Other collision": 6,
        "No collision": 7
    }
    col_values = [col_mapping[col] for col in col_selected]
    trajet_options = [
        "Not specified",
        "Home - work",
        "Home - school",
        "Errands - shopping",
        "Professional use",
        "Leisure - recreation",
        "Other"
    ]
    trajet_selected = st.multiselect("Reason for the trip", options=trajet_options)
    trajet_mapping = {
        "Not specified": -1,
        "Home - work": 1,
        "Home - school": 2,
        "Errands - shopping": 3,
        "Professional use": 4,
        "Leisure - recreation": 5,
        "Other": 9
    }
    trajet_values = [trajet_mapping[trajet] for trajet in trajet_selected]
    lum_options = [
        "Full daylight",
        "Dusk or dawn",
        "Night without public lighting",
        "Night with public lighting off",
        "Night with public lighting on"
    ]
    lum_selected = st.multiselect("Lighting conditions", options=lum_options)
    lum_mapping = {
        "Full daylight": 1,
        "Dusk or dawn": 2,
        "Night without public lighting": 3,
        "Night with public lighting off": 4,
        "Night with public lighting on": 5
    }
    lum_values = [lum_mapping[lum] for lum in lum_selected]
    atm_options = [
        "Not specified",
        "Normal",
        "Light rain",
        "Heavy rain",
        "Snow - hail",
        "Fog - smoke",
        "Strong wind - storm",
        "Dazzling weather",
        "Overcast",
        "Other"
    ]
    atm_selected = st.multiselect('Atmospheric conditions', options=atm_options)
    atm_mapping = {
        "Not specified": -1,
        "Normal": 1,
        "Light rain": 2,
        "Heavy rain": 3,
        "Snow - hail": 4,
        "Fog - smoke": 5,
        "Strong wind - storm": 6,
        "Dazzling weather": 7,
        "Overcast": 8,
        "Other": 9
    }
    atm_values = [atm_mapping[atm] for atm in atm_selected]

    df_filtered = df.copy()

    if grav_selected:
        df_filtered = df_filtered[df_filtered['grav'].isin(grav_values)]
    if sex_selected:
        df_filtered = df_filtered[df_filtered['sexe'].isin(sex_values)]
    if col_selected:
        df_filtered = df_filtered[df_filtered['col'].isin(col_values)]
    if trajet_selected:
        df_filtered = df_filtered[df_filtered['trajet'].isin(trajet_values)]
    if lum_selected:
        df_filtered = df_filtered[df_filtered['lum'].isin(lum_values)]
    if atm_selected:
        df_filtered = df_filtered[df_filtered['atm'].isin(atm_values)]

    def display_map(df_to_display):

        initial_location = [46.603354, 1.888334]
        initial_zoom = 6
        m = folium.Map(location=initial_location, zoom_start=initial_zoom)

        # Define a dictionary to map severity levels to corresponding colors.
        colors = {
            1: "green",
            2: "red",
            3: "orange",
            4: "yellow"
        }
        # Iterate over each row in the dataframe.
        for _, row in df_to_display.iterrows():
            # Assign the color corresponding to the severity of the incident.
            color = colors[row["grav"]]
            # Create a CircleMarker for each incident using its latitude and longitude.
            folium.CircleMarker(
                location=[row["lat"], row["long"]],  # Define the location of the marker.
                radius=row['numVehicules'],
                # Set the size of the circle marker based on the number of vehicles involved.
                color=color,  # Set the color of the circle based on the severity.
                fill=True,  # Enable fill.
                fill_color=color,  # Set the fill color of the circle.
                fill_opacity=0.2
            ).add_to(m)  # Add the marker to the map

        folium_static(m)
    display_map(df_filtered)
    st.write(
        "This map can be filtered to see with more precision who, where and why people have accidents.")


option = st.sidebar.selectbox('To travel faster, you can select the disered topic :',['Project','Introduction', 'Visualizations', 'Map'])
#show_map = st.sidebar.text_input('Please input map in order to see the final map of France', 'I am empty :(')

if option == 'Project':
    #show_map = " "
    display_Project()
elif option == 'Introduction':
    #show_map = " "
    display_introduction()
elif option == 'Visualizations':
    #show_map = " "
    display_datavisualizations()
elif option == "Map":
    main_display_map()

#if show_map == "map":
    #option = "Map"

with st.sidebar:
        st.write(" ------------------------ ")
        st.write("SENECHAL Morgan M1 APP BDML")
        st.write(" ------------------------ ")











