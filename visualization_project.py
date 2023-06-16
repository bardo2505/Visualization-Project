# -*- coding: utf-8 -*-
"""Visualization Final Project.ipynb
"""


import streamlit as st

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots







st.set_page_config(page_title="PROJECT",
                   page_icon=":bar_chart:",
                  layout="wide")
st.title('PROJECT')

# OUR GRAPHS #


    

df = pd.read_csv('mxmh_survey_results.csv') # read csv
df = df.sort_values('Fav genre')

genres_to_remove = ['Jazz', 'Lofi', 'Gospel', 'Latin','Rap','Country','K pop'] # remove genres with num of records < 30
df = df[~df['Fav genre'].isin(genres_to_remove)]


genres_to_keep = ['Rock','Pop','Metal','Classical','Video game music','EDM','R&B','Hip hop','Folk']  # remove people that are not listening to thier fav genre (112 records removed)
for idx, row in df.iterrows():
    fav = row['Fav genre']
    if row[f'Frequency [{fav}]'] not in ['Sometimes','Very frequently']:
      df = df.drop(idx)

def apply_bins_hours(time): # divide to hour bins for graph number 4
  if time <= 2:
    return "[0-2]"
  if time < 3:
    return "(2-3]"
  if time < 5:
    return "(3-4]"
  return "(4-24]"
df['Hours bins'] = df['Hours per day'].apply(apply_bins_hours)

# calculate the mean of targets for graph number 4
df['targets_mean'] = df.apply(lambda row: row[['Anxiety', 'Depression', 'Insomnia', 'OCD']].mean(), axis=1)

# make a DF for graph number 3 : 
third_graph_df = pd.DataFrame(columns=['Genre','Target', 'Average Score'])
targets = ['Anxiety','Depression','Insomnia','OCD']
names = sorted(['Rock','Video game music','R&B','EDM', 'Hip hop','Pop','Classical', 'Metal', 'Folk'])
j=0
for name in names:
    curr_df = df[df['Fav genre']==name]
    for target in targets:
        j+=1
        curr_avg = np.mean(curr_df[target])
        third_graph_df.loc[j] = [name ,target, curr_avg]

    
    
    

# First Graph:
st.subheader('Scatter Plot for Age Vs. Mental Health Scores')
st.text("Would you like to see how age affects the average of the scores? Or compare between specific scores?")
comparison = st.selectbox('Choose one of:', ['None', 'Average', 'Comparison'], key=0)

if comparison == 'Comparison':
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        checkbox1 = col1.checkbox('Anxiety', key=1)
        checkbox2 = col2.checkbox('Depression', key=2)
        checkbox3 = col3.checkbox('Insomnia', key=3)    
        checkbox4 = col4.checkbox('OCD', key=4) 
   
    list_of_trues = [False, False, False, False]
    if (checkbox1):
        list_of_trues[0] = True
    else:
        list_of_trues[0] = False
        
    if (checkbox2):
        list_of_trues[1] = True
    else:
        list_of_trues[1] = False
        
    if (checkbox3):
        list_of_trues[2] = True
    else:
        list_of_trues[2] = False
        
    if (checkbox4):
        list_of_trues[3] = True
    else:
        list_of_trues[3] = False
        
    true_indices = [index for index, value in enumerate(list_of_trues) if value]
    graphs_amount = sum(list_of_trues)
    
    Anxiety = px.scatter(df,x="Age", y = 'Anxiety',
                        color="Fav genre",
                        title="Age Vs. Anxiety")

    
    Depression = px.scatter(df,x="Age", y = 'Depression',
                        color="Fav genre",
                        title="Age Vs. Depression")
    
    Insomnia = px.scatter(df,x="Age", y = 'Insomnia',
                        color="Fav genre",
                        title="Age Vs. Insomnia")
    
    OCD = px.scatter(df,x="Age", y = 'OCD',
                        color="Fav genre",
                        title="Age Vs. OCD")
    
    graphs = [Anxiety, Depression, Insomnia, OCD]
    for g in graphs:
        g.update_xaxes(tickmode='linear', dtick=10)
        for trace in g.data:
            trace.update(marker=dict(size=10, opacity=0.7))
    if graphs_amount == 0:
        pass
    
    elif graphs_amount == 1:
        for i in range(len(list_of_trues)):
            if list_of_trues[i]:
                st.plotly_chart(graphs[i], use_container_width=True)
                
    elif graphs_amount == 2:
         col1, col2 = st.columns(2, gap="large")
         g1_idx = true_indices[0]
         g2_idx = true_indices[1]
         with col1:
            st.plotly_chart(graphs[g1_idx], use_container_width=False)
         with col2:
            st.plotly_chart(graphs[g2_idx], use_container_width=False)
    elif graphs_amount == 3:
         col1, col2 = st.columns(2, gap="large")
         g1_idx = true_indices[0]
         g2_idx = true_indices[1]
         g3_idx = true_indices[2]
         with col1:
            st.plotly_chart(graphs[g1_idx], use_container_width=False)
         with col2:
            st.plotly_chart(graphs[g2_idx], use_container_width=False)
         col3, _ = st.columns(2, gap="large")
         with col3:
            st.plotly_chart(graphs[g3_idx], use_container_width=False)

    elif graphs_amount == 4:
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.plotly_chart(graphs[0], use_container_width=False)
        with col2:
            st.plotly_chart(graphs[1], use_container_width=False)
            
        col3, col4 = st.columns(2, gap="large")
        with col3:
            st.plotly_chart(graphs[2], use_container_width=False)   
        with col4:
            st.plotly_chart(graphs[3], use_container_width=False)   


elif comparison == 'Average':
    g = px.scatter(df, x="Age", y="targets_mean",
                         color="Fav genre",
                         title="Scatterplot Matrix with Colors as Legend")
    for trace in g.data:
            trace.update(marker=dict(size=10, opacity=0.7))
    g.update_layout(yaxis_title='Average of Mental Health Scores')
    g.update_xaxes(range=[-0.5, 90.5], tickmode='linear', dtick=10)  
    st.plotly_chart(g, use_container_width=True)

st.markdown("---") 
    
# Second Graph:
st.subheader('Scatter Plot for Hours of listening per day Vs. Mental Health Scores')
st.text("Would you like to see how hours of listening per day affects the average of the scores? Or compare between specific scores?")
comparison = st.selectbox('Choose one of:', ['None', 'Average', 'Comparison'], key=-1)
if comparison == 'Comparison':
    
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        checkbox5 = col1.checkbox('Anxiety', key=5)
        checkbox6 = col2.checkbox('Depression', key=6)
        checkbox7 = col3.checkbox('Insomnia', key=7)    
        checkbox8 = col4.checkbox('OCD', key=8) 
        
    list_of_trues = [False, False, False, False]
    if (checkbox5):
        list_of_trues[0] = True
    else:
        list_of_trues[0] = False
        
    if (checkbox6):
        list_of_trues[1] = True
    else:
        list_of_trues[1] = False
        
    if (checkbox7):
        list_of_trues[2] = True
    else:
        list_of_trues[2] = False
        
    if (checkbox8):
        list_of_trues[3] = True
    else:
        list_of_trues[3] = False
        
    true_indices = [index for index, value in enumerate(list_of_trues) if value]
    graphs_amount = sum(list_of_trues)
    Anxiety = px.scatter(df,x="Hours per day", y = 'Anxiety',
                        color="Fav genre",
                        title="Hours per day Vs. Anxiety")
    Depression = px.scatter(df,x="Hours per day", y = 'Depression',
                        color="Fav genre",
                        title="Hours per day Vs. Depression")
    Insomnia = px.scatter(df,x="Hours per day", y = 'Insomnia',
                        color="Fav genre",
                        title="Hours per day Vs. Insomnia")
    OCD = px.scatter(df,x="Hours per day", y = 'OCD',
                        color="Fav genre",
                        title="Hours per day Vs. OCD")
    OCD.update_xaxes(range=[-0.5, 24.5], tickmode='linear', dtick=1)
    graphs = [Anxiety, Depression, Insomnia, OCD]
    for g in graphs:
      g.update_xaxes(range=[-0.5, 24.5], tickmode='linear', dtick=2)  
      for trace in g.data:
          trace.update(marker=dict(size=10, opacity=0.7))
    if graphs_amount == 0:
        pass
    
    elif graphs_amount == 1:
        for i in range(len(list_of_trues)):
            if list_of_trues[i]:
                st.plotly_chart(graphs[i], use_container_width=True)
                
    elif graphs_amount == 2:
         col1, col2 = st.columns(2, gap="large")
         g1_idx = true_indices[0]
         g2_idx = true_indices[1]
         with col1:
            st.plotly_chart(graphs[g1_idx], use_container_width=False)
         with col2:
            st.plotly_chart(graphs[g2_idx], use_container_width=False)
    elif graphs_amount == 3:
         col1, col2 = st.columns(2, gap="large")
         g1_idx = true_indices[0]
         g2_idx = true_indices[1]
         g3_idx = true_indices[2]
         with col1:
            st.plotly_chart(graphs[g1_idx], use_container_width=False)
         with col2:
            st.plotly_chart(graphs[g2_idx], use_container_width=False)
         col3, _ = st.columns(2, gap="large")
         with col3:
            st.plotly_chart(graphs[g3_idx], use_container_width=False)

    elif graphs_amount == 4:
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.plotly_chart(graphs[0], use_container_width=False)
        with col2:
            st.plotly_chart(graphs[1], use_container_width=False)
            
        col3, col4 = st.columns(2, gap="large")
        with col3:
            st.plotly_chart(graphs[2], use_container_width=False)   
        with col4:
            st.plotly_chart(graphs[3], use_container_width=False)   


elif comparison == 'Average':
    g = px.scatter(df, x="Hours per day", y="targets_mean",
                         color="Fav genre",
                         title="Scatterplot Matrix with Colors as Legend")
    for trace in g.data:
        trace.update(marker=dict(size=10, opacity=0.7))
    g.update_layout(yaxis_title='Average of Mental Health Scores')
    g.update_xaxes(range=[-0.5, 24.5], tickmode='linear', dtick=1)
    st.plotly_chart(g, use_container_width=True)


st.markdown("---") 
    
# Graph 3 #
st.subheader('Bar Plot for Genres Vs. Mental Health Scores')
st.text("Use the checkboxes to observe specific genres")
with st.container():
    col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
    classical = col1.checkbox('Classical', key=9)
    edm = col2.checkbox('EDM', key=10)
    folk = col3.checkbox('Folk', key=11)    
    hiphop = col4.checkbox('Hip hop', key=12) 
    metal = col5.checkbox('Metal', key=13)
    pop = col6.checkbox('Pop', key=14)
    rnb = col7.checkbox('R&B', key=15)    
    rock = col8.checkbox('Rock', key=16) 
    videogame = col9.checkbox('Video game music', key=17) 

check_box_booleans = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
to_show =[]
for i in range(len(genres)):
    if check_box_booleans[i]:
        to_show.append(genres[i])
 

to_show_df = third_graph_df[third_graph_df["Genre"].isin(to_show)]
color_map = {
    "Anxiety": "#FF0000",  # Red
    "Depression": "#00FF00",  # Green
    "Insomnia": "#0000FF",  # Blue
    "OCD": "#FF8000",  # Orange
}



third_graph_fig1 = px.histogram(to_show_df, x="Genre", y='Average Score',
             color='Target', barmode='group',
             histfunc='avg',
             height=400,
             color_discrete_map=color_map)
st.plotly_chart(third_graph_fig1, use_container_width=True)


st.markdown("---") 

# Graph 4 #
st.subheader('Heatmap for Hours of listening per day Vs. Mental Health Scores')

hours_bins_order = ["[0-2]","(2-3]","(3-4]","(4-24]"]
df["Hours bins"] = pd.Categorical(df["Hours bins"], categories=hours_bins_order, ordered=True)

df_avg = df.groupby(["Hours bins", "Fav genre"]).mean().reset_index()
fourth_graph_fig1 = px.density_heatmap(df_avg, x="Fav genre", y="Hours bins", z="targets_mean",
                         labels=dict(x="Favorite Genre", y="Hours Bins", z="Average Score"),
                         color_continuous_scale="RdYlBu_r")
fourth_graph_fig1.update_layout(title="Average Mental Health Score by Hours Bins and Favorite Genre")
st.plotly_chart(fourth_graph_fig1, use_container_width=True)







# df = pd.read_csv('Sleep_Efficiency.csv')
# df['Alcohol consumption'] = df['Alcohol consumption'].fillna(0.0)
# df['Caffeine consumption'] = df['Alcohol consumption'].fillna(0.0)
# df['Awakenings'] = df['Awakenings'].fillna(0.0)
# df['Exercise frequency'] = df['Exercise frequency'].fillna(0.0)
# # Convert bedtime and wakeup time columns to datetime format
# df['Bedtime'] = pd.to_datetime(df['Bedtime'])
# df['Wakeup time'] = pd.to_datetime(df['Wakeup time'])
# df['DayOfWeek'] = df['Bedtime'].dt.day_name()
# # "DayType" column based on weekdays and weekends
# df['DayType'] = df['DayOfWeek'].apply(lambda x: 'Weekday' if x in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] else 'Weekend')
# # Convert 'Wakeup time' column to datetime format
# df['Wakeup time'] = pd.to_datetime(df['Wakeup time'])
# # Extract the hour number into a new column
# df['Wakeup Hour'] = df['Wakeup time'].dt.hour
# df['Sleep efficiency'] = pd.to_numeric(df['Sleep efficiency'], errors='coerce')

# #First Graph
# st.subheader('Sleep Efficiency by Wakeup Hour')
# # Filter the data based on the selected gender
# selected_gender = st.selectbox('Select Gender', ['Male', 'Female'])
# filtered_data = df[df['Gender'] == selected_gender]

# # Create the box plot using plotly express
# fig = px.box(filtered_data, x='Wakeup Hour', y='Sleep efficiency', color='Wakeup Hour', hover_data=['Wakeup time'],
#             category_orders={'Wakeup Hour': sorted(df['Wakeup Hour'].unique())})
# fig.update_traces(hovertemplate="<b>Wakeup Hour:</b> %{x}<br><b>Sleep Efficiency:</b> %{y}<br><b>Wakeup Time:</b> %{customdata[0]}")


# # Show the plot
# st.plotly_chart(fig)


# #Second Graph
# st.subheader('Sleep Type by Average Percentage')
# # Get the age range from the user using number input fields
# min_age = st.number_input('Minimum Age', min_value=int(df['Age'].min()), max_value=int(df['Age'].max()), value=int(df['Age'].min()), step=10)
# max_age = st.number_input('Maximum Age', min_value=int(df['Age'].min()), max_value=int(df['Age'].max()), value=int(df['Age'].max()), step=10)

# # Filter the dataframe based on the selected age range
# filtered_df = df[(df['Age'] >= min_age) & (df['Age'] <= max_age)]

# # Calculate the average percentage of each type of sleep
# avg_sleep_perc = filtered_df[[ 'REM sleep percentage', 'Deep sleep percentage',
#     'Light sleep percentage' ]].mean()
# # Define a custom color palette for the bars
# color_scale = ["purple", "skyblue", "orange"]
# # Create a bar plot using Plotly Express
# fig = px.bar(avg_sleep_perc, y=avg_sleep_perc.index, x=avg_sleep_perc.values,
#              labels={'x': 'Sleep Type', 'y': 'Average Percentage'},
#              color=avg_sleep_perc.index, color_discrete_sequence=color_scale)


# # Customize the plot as needed
# fig.update_layout(yaxis_title='Sleep Type',
#                   xaxis_title='Average Percentage')

# # Display the plot
# st.plotly_chart(fig, use_container_width=True)

# #Third Graph
# # Define the columns for the line plot
# st.subheader('Sleep Efficiency by Number of Sleep Hours and Weekly Habits')
# x_column = 'Sleep duration'
# y_column = 'Sleep efficiency'

# # Get unique values for the condition columns
# awakenings_values = df['Awakenings'].unique()
# alcohol_values = df['Alcohol consumption'].unique()
# smoking_values = df['Smoking status'].unique()
# exercise_values = df['Exercise frequency'].unique()

# # User inputs for conditions
# #selected_awakenings = st.selectbox('Select Awakenings', awakenings_values)
# selected_alcohol = st.selectbox('Select Alcohol Consumption', alcohol_values)
# selected_smoking = st.selectbox('Select Smoking Status', smoking_values)
# selected_exercise = st.selectbox('Select Exercise Frequency', exercise_values)

# # Filter the dataframe based on user-selected conditions
# filtered_df = df[(df['Alcohol consumption'] == selected_alcohol) &
#                 (df['Smoking status'] == selected_smoking) &
#                 (df['Exercise frequency'] == selected_exercise)]

# # Create a scatter plot using Plotly Express
# fig = px.density_heatmap(filtered_df, x=x_column, y=y_column,
#                 labels={'x': 'Sleep Duration', 'y': 'Sleep Efficiency'})

# # Customize the plot as needed
# fig.update_layout(legend_title_text='Conditions')

# # Display the plot
# st.plotly_chart(fig, use_container_width=True)


# # Sleep efficiency comparison between weekdays and weekends
# st.subheader('Density Sleep Efficiency Comparison: Weekdays vs. Weekends')

# # Get unique values for the 'DayType' column
# day_values = df['DayType'].unique()

# # User selects the weekdays and weekends
# selected_days = st.multiselect('Select Weekdays/Weekends', day_values)

# # Filter the data based on the selected days
# selected_data = df[df['DayType'].isin(selected_days)]
# fig, ax = plt.subplots()
# for day in selected_days:
#     data = selected_data[selected_data['DayType'] == day]
#     density = data['Sleep efficiency'].plot.kde()
#     density.set_label(day)

# ax.set_xlabel('Sleep Efficiency')
# ax.set_ylabel('Density')
# # ax.set_title('Sleep Efficiency Distribution: Weekdays vs. Weekends')
# ax.legend(labels=['Weekend','Weekday'])
# st.pyplot(fig)



#OLD PREPROC
# preprocess:

# df = pd.read_csv('mxmh_survey_results.csv')

# genres_to_remove = ['Jazz', 'Lofi', 'Gospel', 'Latin','Rap','Country','K pop']
# df = df[~df['Fav genre'].isin(genres_to_remove)]

# genres_to_keep = ['Rock','Pop','Metal','Classical','Video game music','EDM','R&B','Hip hop','Folk']
# for idx, row in df.iterrows():
#     fav = row['Fav genre']
#     if row[f'Frequency [{fav}]'] not in ['Sometimes','Very frequently']:
#       df = df.drop(idx)

# third_graph_df = pd.DataFrame(columns=['Genre','Target', 'Average Score'])
# targets = ['Anxiety','Depression','Insomnia','OCD']
# names = sorted(['Rock','Video game music','R&B','EDM', 'Hip hop','Pop','Classical', 'Metal', 'Folk'])
# j=0
# for name in names: 
#     curr_df = df[df['Fav genre']==name]
#     for target in targets:
#         j+=1
#         curr_avg = np.mean(curr_df[target])
#         third_graph_df.loc[j] = [name ,target, curr_avg]
    
# df['targets_mean'] = df.apply(lambda row: row[['Anxiety', 'Depression', 'Insomnia', 'OCD']].mean(), axis=1)    

