# Projet_Data_Visualization

# Requirements

## I.5 Project Assignment: Build Your Own Interactive Application

- **Group Size**: Maximum of 3 students
- **Deadline**: Last Session, October 26th

## Overview

For this project, you are required to build an interactive web application utilizing the Streamlit library alongside one data visualization library (matplotlib, seaborn, altair, bokeh, or plotly).

The core objective is to select a dataset from data.gouv.fr (or alternatively, use [MovieLens](https://grouplens.org/datasets/movielens/)) and develop a data visualization web application. This app should offer insightful answers to relevant questions, enabling users to interact with the data effectively.

Although not mandatory, it is recommended to choose a dataset related to the RSE theme. For more information on RSE, visit [Responsabilité Sociétale des Entreprises (RSE)](https://www.economie.gouv.fr/entreprises/responsabilite-societale-entreprises-rse).

## Technical Guidelines

Your Streamlit application must adhere to the following technical requirements:

- **Code Organization**: All code should be function-based, with modular blocks for data processing and workflow steps. Comments and modularity are highly encouraged for clarity and maintenance.
- **Streamlit Visualizations**: Include at least four internal Streamlit plots (`st.line`, `st.bar_chart`, `st.scatter_chart`, `st.map`).
- **External Library Plots**: Integrate four different types of plots (histograms, bar charts, scatter plots, or pie charts) using external libraries such as matplotlib, seaborn, plotly, or Altair.
- **Interactive Elements**: Incorporate four interactive elements (e.g., checkboxes, sliders).
- **Caching**: Utilize caching for data loading and preprocessing to enhance performance.
- **Optional**: Implement a decorator to log execution time intervals (e.g., 30 seconds, 2 seconds, 0.01 seconds) and timestamps of function calls.
- **Optional**: Organize function calls within a main function to establish a clear application workflow.

## Objective

The primary goal is to provide meaningful insights and narrate a compelling story through your data. Initially, dedicate time to explore, conceptualize, and structure your dashboard. Decide on the questions you aim to answer and the insights you wish to convey to your users.

## Choice

For this project, we have chosen to use a dataset found on [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/accidents-de-velo/) related to bicycle accidents for the period 2005-2021.
