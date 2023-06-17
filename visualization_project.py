# -*- coding: utf-8 -*-
"""Visualization Final Project.ipynb
"""

# Imports #
import streamlit as st

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots



# Intro #
st.set_page_config(page_title="Streamlit Project",
                   page_icon=":bar_chart:",
                  layout="wide")
st.title('PROJECT')

color_blind = st.radio("Are you color blind?",['No','Yes'],key=51) # Did you know that 9% of men are color blind?
if color_blind == 'Yes': 

  cmap_graph_4 = "balance" # graph 4
  color_map_graphs12 = {
        "Classical": px.colors.qualitative.Dark24[19], # Deep Blue
        "EDM":  px.colors.qualitative.Dark24[21], # Brown
        "Folk":  px.colors.qualitative.T10[9], # Grey
        "Hip hop": px.colors.qualitative.Alphabet[6], # Light Green
        "Metal": px.colors.qualitative.Alphabet[24], # Yellow
        "Pop": px.colors.qualitative.Set1[0], # Red
        "R&b": px.colors.qualitative.Dark24[5], # Black
        "Rock": px.colors.qualitative.Alphabet[5], # Dark Green
        "Video game music":  px.colors.qualitative.Set1[4], # Orange
    }
  color_map_graph3 = {
        "Anxiety": px.colors.qualitative.Bold[2],  # Blue
        "Depression": px.colors.qualitative.Bold[3],  # Pink
        "Insomnia": px.colors.qualitative.Bold[4],  # Yellow
        "OCD": px.colors.qualitative.Bold[5]  # Green
    } 
else:

  cmap_graph_4 = "Tempo" # graph 4
  color_map_graphs12 = {
        "Classical": px.colors.qualitative.Dark24[19], # Deep Blue
        "EDM":  px.colors.qualitative.D3[5], # Brown
        "Folk":  px.colors.qualitative.T10[9], # Grey
        "Hip hop": px.colors.qualitative.Alphabet[6], # Light Green
        "Metal": px.colors.qualitative.Alphabet[24], # Yellow
        "Pop": px.colors.qualitative.Light24[0], # Red
        "R&B": px.colors.qualitative.Dark24[5], # Black
        "Rock": px.colors.qualitative.Dark2[0], # Dark Green
        "Video game music":  px.colors.qualitative.Prism[6], # Orange
      }
  color_map_graph3 = {
        "Anxiety": px.colors.qualitative.Bold[2],  # Blue
        "Depression": px.colors.qualitative.Bold[3],  # Pink
        "Insomnia": px.colors.qualitative.Bold[4],  # Yellow
        "OCD": px.colors.qualitative.Bold[5]  # Green
    } 

     
  
  


# Pre-Process #

df = pd.read_csv('mxmh_survey_results.csv') # read csv
df = df.sort_values('Fav genre')
df = df.rename(columns={"Fav genre": "Favorite Genre"})

genres_to_remove = ['Jazz', 'Lofi', 'Gospel', 'Latin','Rap','Country','K pop'] # remove genres with num of records < 30
df = df[~df['Favorite Genre'].isin(genres_to_remove)]


genres_to_keep = ['Rock','Pop','Metal','Classical','Video game music','EDM','R&B','Hip hop','Folk']  # remove people that are not listening to thier fav genre (112 records removed)
for idx, row in df.iterrows():
    fav = row['Favorite Genre']
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
df['Average Score'] = df.apply(lambda row: row[['Anxiety', 'Depression', 'Insomnia', 'OCD']].mean(), axis=1)
          
# make a DF for graph number 3 : 
third_graph_df = pd.DataFrame(columns=['Genre','Target', 'Average Score'])
targets = ['Anxiety','Depression','Insomnia','OCD']
names = sorted(['Rock','Video game music','R&B','EDM', 'Hip hop','Pop','Classical', 'Metal', 'Folk'])
j=0
for name in names:
    curr_df = df[df['Favorite Genre']==name]
    for target in targets:
        j+=1
        curr_avg = np.mean(curr_df[target])
        third_graph_df.loc[j] = [name ,target, curr_avg]

    
    
    
    
    
    
    
    
    
# OUR GRAPHS # 


##################################### First Graph #####################################
st.subheader('Scatter Plot for Age Vs. Mental Health Scores')
comparison = st.radio("Would you like to see how age affects the average of the scores? Or compare between specific scores?, Choose one of:", ['None', 'Average', 'Comparison'], key=50)

if comparison == 'Comparison':
    st.text("Please choose Mental health scores to observe (target values)")
    with st.container():
        col1, col2, col3, col4 = st.columns([0.1, 0.1, 0.1, 0.7])
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
    
   

    if sum(list_of_trues) > 0:
      st.text("Please choose Genres to observe - ")
      bool_genres = st.radio("Choose view method for genres:",['I prefer to choose the genres manually','Select all genres'])
      if bool_genres=='I prefer to choose the genres manually':
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
      elif bool_genres=='Select all genres':
        with st.container():
          col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
          classical = col1.checkbox('Classical',value=True, key=956555)
          edm = col2.checkbox('EDM',value=True, key=10555)
          folk = col3.checkbox('Folk',value=True, key=155551)    
          hiphop = col4.checkbox('Hip hop',value=True, key=125555) 
          metal = col5.checkbox('Metal',value=True, key=1555553)
          pop = col6.checkbox('Pop',value=True, key=145555)  
          rnb = col7.checkbox('R&B',value=True, key=15555)    
          rock = col8.checkbox('Rock',value=True, key=165555) 
          videogame = col9.checkbox('Video game music',value=True, key=15557) 
      check_box_booleans_graph_1 = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
      genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
      to_show_graph1 =[]
      for i in range(len(genres)):
          if check_box_booleans_graph_1[i]:
              to_show_graph1.append(genres[i])
 

      to_show_df_graph1 = df[df["Favorite Genre"].isin(to_show_graph1)]

  
      Anxiety = px.scatter(to_show_df_graph1,x="Age", y = 'Anxiety',
                        color="Favorite Genre",
                        title="Age Vs. Anxiety",
                        color_discrete_map = color_map_graphs12)

    
      Depression = px.scatter(to_show_df_graph1,x="Age", y = 'Depression',
                        color="Favorite Genre",
                        title="Age Vs. Depression",
                        color_discrete_map = color_map_graphs12)
    
      Insomnia = px.scatter(to_show_df_graph1,x="Age", y = 'Insomnia',
                        color="Favorite Genre",
                        title="Age Vs. Insomnia",
                        color_discrete_map = color_map_graphs12)
    
      OCD = px.scatter(to_show_df_graph1,x="Age", y = 'OCD',
                        color="Favorite Genre",
                        title="Age Vs. OCD",
                        color_discrete_map = color_map_graphs12)
    
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

    st.text("Please choose Genres to observe - ")
    with st.container():
        col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
        classical = col1.checkbox('Classical', key=90)
        edm = col2.checkbox('EDM', key=100)
        folk = col3.checkbox('Folk', key=110)    
        hiphop = col4.checkbox('Hip hop', key=120) 
        metal = col5.checkbox('Metal', key=130)
        pop = col6.checkbox('Pop', key=140)
        rnb = col7.checkbox('R&B', key=150)    
        rock = col8.checkbox('Rock', key=160) 
        videogame = col9.checkbox('Video game music', key=170) 

    check_box_booleans_graph_12 = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
    genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
    to_show_graph12 =[]
    for i in range(len(genres)):
      if check_box_booleans_graph_12[i]:
          to_show_graph12.append(genres[i])
 

    to_show_df_graph12 = df[df["Favorite Genre"].isin(to_show_graph12)]


      
    g = px.scatter(to_show_df_graph12, x="Age", y="Average Score",
                         color="Favorite Genre",
                         title="Scatterplot Matrix with Colors as Legend",
                        color_discrete_map = color_map_graphs12)
    for trace in g.data:
            trace.update(marker=dict(size=10, opacity=0.7))
    g.update_layout(yaxis_title='Average of Mental Health Scores')
    g.update_xaxes(range=[-0.5, 90.5], tickmode='linear', dtick=10)  
    st.plotly_chart(g, use_container_width=True)

st.markdown("---") 
    
  
  
  
  
  
  
##################################### Second Graph #####################################
st.subheader('Scatter Plot for Hours of listening per day Vs. Mental Health Scores')

comparison = st.radio("Would you like to see how age affects the average of the scores? Or compare between specific scores?, Choose one of:", ['None', 'Average', 'Comparison'], key=52)
if comparison == 'Comparison':
    
    with st.container():
        col1, col2, col3, col4 = st.columns([0.1, 0.1, 0.1, 0.7])
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



    st.text("Please choose Genres to observe - ")
    with st.container():
      col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
      classical = col1.checkbox('Classical', key=39)
      edm = col2.checkbox('EDM', key=310)
      folk = col3.checkbox('Folk', key=311)    
      hiphop = col4.checkbox('Hip hop', key=312) 
      metal = col5.checkbox('Metal', key=313)
      pop = col6.checkbox('Pop', key=314)
      rnb = col7.checkbox('R&B', key=315)    
      rock = col8.checkbox('Rock', key=316) 
      videogame = col9.checkbox('Video game music', key=317) 

    check_box_booleans_graph_2 = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
    genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
    to_show_graph2 =[]
    for i in range(len(genres)):
        if check_box_booleans_graph_2[i]:
            to_show_graph2.append(genres[i])
 

    to_show_df_graph2 = df[df["Favorite Genre"].isin(to_show_graph2)]

    
    
    Anxiety = px.scatter(to_show_df_graph2,x="Hours per day", y = 'Anxiety',
                        color="Favorite Genre",
                        title="Hours per day Vs. Anxiety",
                        color_discrete_map = color_map_graphs12)
    Depression = px.scatter(to_show_df_graph2,x="Hours per day", y = 'Depression',
                        color="Favorite Genre",
                        title="Hours per day Vs. Depression",
                        color_discrete_map = color_map_graphs12)
    Insomnia = px.scatter(to_show_df_graph2,x="Hours per day", y = 'Insomnia',
                        color="Favorite Genre",
                        title="Hours per day Vs. Insomnia",
                        color_discrete_map = color_map_graphs12)
    OCD = px.scatter(to_show_df_graph2,x="Hours per day", y = 'OCD',
                        color="Favorite Genre",
                        title="Hours per day Vs. OCD",
                        color_discrete_map = color_map_graphs12)

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


    st.text("Please choose Genres to observe - ")
    with st.container():
      col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
      classical = col1.checkbox('Classical', key=439)
      edm = col2.checkbox('EDM', key=4310)
      folk = col3.checkbox('Folk', key=4311)    
      hiphop = col4.checkbox('Hip hop', key=4312) 
      metal = col5.checkbox('Metal', key=4313)
      pop = col6.checkbox('Pop', key=4314)
      rnb = col7.checkbox('R&B', key=4315)    
      rock = col8.checkbox('Rock', key=4316) 
      videogame = col9.checkbox('Video game music', key=4317) 

    check_box_booleans_graph_22 = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
    genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
    to_show_graph22 =[]
    for i in range(len(genres)):
        if check_box_booleans_graph_22[i]:
            to_show_graph22.append(genres[i])
 

    to_show_df_graph22 = df[df["Favorite Genre"].isin(to_show_graph22)]
    g = px.scatter(to_show_df_graph22, x="Hours per day", y="Average Score",
                         color="Favorite Genre",
                         title="Scatterplot Matrix with Colors as Legend",
                        color_discrete_map = color_map_graphs12)
    for trace in g.data:
        trace.update(marker=dict(size=10, opacity=0.7))
    g.update_layout(yaxis_title='Average of Mental Health Scores')
    g.update_xaxes(range=[-0.5, 24.5], tickmode='linear', dtick=1)
    g.update_xaxes(title_font=dict(size=20), tickfont=dict(size=14))
    g.update_yaxes(title_font=dict(size=20), tickfont=dict(size=14))

    st.plotly_chart(g, use_container_width=True)#fix this

st.markdown("---") 
    
  
  
  
  
  
##################################### Third Graph #####################################
st.subheader('Bar Plot for Genres Vs. Mental Health Scores')
st.text("Use the checkboxes to observe specific genres")
select_all = st.radio("Would you like to view all Genres at once?",['Yes please.','No, I will choose myself.'])
if select_all == 'Yes please.': 
  with st.container():
      col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
      classical = col1.checkbox('Classical',value=True, key=9999699)
      edm = col2.checkbox('EDM',value=True, key=10999999)
      folk = col3.checkbox('Folk',value=True, key=11999999)    
      hiphop = col4.checkbox('Hip hop',value=True, key=12999999) 
      metal = col5.checkbox('Metal',value=True, key=139999999)
      pop = col6.checkbox('Pop',value=True, key=1499999)
      rnb = col7.checkbox('R&B',value=True, key=159999999)    
      rock = col8.checkbox('Rock',value=True, key=16999999) 
      videogame = col9.checkbox('Video game music',value=True, key=17999999) 
else:
  with st.container():
      col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
      classical = col1.checkbox('Classical', key=97777777777)
      edm = col2.checkbox('EDM', key=1077777777)
      folk = col3.checkbox('Folk', key=117777777777)    
      hiphop = col4.checkbox('Hip hop', key=12777777) 
      metal = col5.checkbox('Metal', key=1377777777)
      pop = col6.checkbox('Pop', key=14777777777)
      rnb = col7.checkbox('R&B', key=159595)    
      rock = col8.checkbox('Rock', key=1677777777) 
      videogame = col9.checkbox('Video game music', key=7777777717) 

check_box_booleans = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
to_show =[]
for i in range(len(genres)):
    if check_box_booleans[i]:
        to_show.append(genres[i])
 

to_show_df = third_graph_df[third_graph_df["Genre"].isin(to_show)]


third_graph_fig1 = px.histogram(to_show_df, x="Genre", y='Average Score',
             color='Target', barmode='group',
             histfunc='avg',
             height=400,
             color_discrete_map=color_map_graph3)
third_graph_fig1.update_layout(title="Put title here",
                               xaxis=dict(
                                       tickfont=dict(size=17),  # Set font size for x-axis tick numbers
                                       title=dict(text="Favorite Genre",font=dict(size=20))  # Set font size for x-axis label
                                        ),
                               yaxis=dict(
                                       tickfont=dict(size=17),  # Set font size for y-axis tick numbers
                                       title=dict(text="Mental Health Score", font=dict(size=20))  # Set font size for y-axis label
                                        ))


st.plotly_chart(third_graph_fig1, use_container_width=True)#









st.markdown("---") 

##################################### Fourth Graph #####################################

st.subheader('Heatmap for Hours of listening per day Vs. Mental Health Scores')

hours_bins_order = ["[0-2]","(2-3]","(3-4]","(4-24]"]
df["Hours bins"] = pd.Categorical(df["Hours bins"], categories=hours_bins_order, ordered=True)

df_avg = df.groupby(["Hours bins", "Favorite Genre"]).mean().reset_index()
df_avg['Average Score'] = df_avg['Average Score'].apply(lambda x: round(x, 2))
fourth_graph_fig1 = px.density_heatmap(df_avg, x="Favorite Genre", y="Hours bins", z="Average Score",
                         labels=dict(x="Favorite Genre", y="Hours Bins", z="Average Score"),
                         text_auto ="Average Score",
                         color_continuous_scale=cmap_graph_4
                                      )
                                      
fourth_graph_fig1.update_layout(title="Average Mental Health Score by Hours Bins and Favorite Genre",
                               xaxis=dict(
                                       tickfont=dict(size=17),  # Set font size for x-axis tick numbers
                                       title=dict(text="Favorite Genre",font=dict(size=20))  # Set font size for x-axis label
                                        ),
                               yaxis=dict(
                                       tickfont=dict(size=17),  # Set font size for y-axis tick numbers
                                       title=dict(text="Hours of listening (Daily)", font=dict(size=20))  # Set font size for y-axis label
                                        ),
                               coloraxis=dict(
                                      colorbar=dict(
                                            title="Mental Health Average Score",
                                            titleside="top",
                                            titlefont=dict(size=15),
                                            tickfont=dict(size=15))
                                              ),
                                font=dict(
                                      size=32  # Set the font size here
                                          )
                                 )

#fourth_graph_fig1.update_layout(uniformtext_minsize=20, uniformtext_mode='hide')      
st.plotly_chart(fourth_graph_fig1, use_container_width=True)

