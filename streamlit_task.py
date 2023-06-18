import streamlit as st
import pandas as pd
from collections import defaultdict
from transformers import pipeline
import numpy as np

sentiment_analysis = pipeline("sentiment-analysis")

# Создание списка доступных фильмов и персонажей для каждого из них
df = pd.read_csv('replicas.csv')
df_heroes_by_movies = df[['char_id1', 'movie_id2', 'mName', 'chName_1']].drop_duplicates(subset=['char_id1','movie_id2'])
movies = defaultdict(list)

for index, row in df_heroes_by_movies.iterrows():
    movie_name = row['mName']
    character_name = row['chName_1']
    character_id = row['char_id1']
    #replicas = eval(row['replicas'].replace('nan,', '').replace('nan', ''))

    for character in movies[movie_name]:
        if character['Id'] == character_id:
            break
    else:
        movies[movie_name].append({'Id': character_id, 'Name': character_name})

# Функция для классификации текста при помощи Hugging Face Transformers
def classify_sentiment(text):
    result = sentiment_analysis(text)[0]
    return result["label"]

def get_dialogue_data(movie, character = True):
    heroes = [d['Id'] for d in movies[movie]]
    df_heroes_replics = df[(df['mName'] == movie) & (df['char_id1'].isin(heroes))].groupby('char_id1').head(10)
    result = []
    for index, row in df_heroes_replics.iterrows():
        character_id = row['char_id1']
        replicas = eval(row['replicas'].replace('nan,', '').replace('nan', ''))
        for i in range(0, len(result)):
            if(result[i]['Speaker'] == character_id):
                result[i]['Text'] += replicas
                break
        else:
            result.append({'Speaker': character_id, 'Text': replicas})

    return result

# Интерфейс пользователя на Streamlit
st.title("Emotion Analysis")

movie_choice = st.selectbox("Choose a movie:", list(movies.keys()))
character_choice = st.selectbox("Choose a character:", [{'Id': 'All', 'Name' : "All Characters"}] + movies[movie_choice], format_func=lambda hero: hero["Name"])

if character_choice['Id'] == "All":
    dialogue_data = get_dialogue_data(movie_choice) # Получение диалоговых данных из файла
    
    sentiment_score = {"POSITIVE":0, "NEGATIVE":0, "NEUTRAL":0}
    
    for speaker in dialogue_data:
        text_list = list(speaker["Text"])
        
        for text in text_list:
            sentiment_label=classify_sentiment(text)
            
            if sentiment_label=="POSITIVE":
                sentiment_score["POSITIVE"]+=1
            elif sentiment_label=="NEGATIVE":
                sentiment_score["NEGATIVE"]+=1
            else:
                sentiment_score["NEUTRAL"]+=1
                
    st.write("Sentiment analysis for all characters in", movie_choice)
    st.write("Positive:", sentiment_score["POSITIVE"])
    st.write("Negative:", sentiment_score["NEGATIVE"])
    st.write("Neutral:", sentiment_score["NEUTRAL"])

else:
    dialogue_data = get_dialogue_data(movie_choice, character_choice['Id']) # Получение диалоговых данных для выбранного персонажа из файла
    
    if len(dialogue_data)==0: # Проверка наличия диалоговых данных для выбранного персонажа
        st.write(f"No dialogue data found for {character_choice} in {movie_choice}.")
        
    else:
        text_list = list(dialogue_data["Text"])
    
        sentiment_score = {"POSITIVE":0, "NEGATIVE":0, "NEUTRAL":0}
    
        for text in text_list:
            sentiment_label=classify_sentiment(text)
            
            if sentiment_label=="POSITIVE":
                sentiment_score["POSITIVE"]+=1
            elif sentiment_label=="NEGATIVE":
                sentiment_score["NEGATIVE"]+=1
            else:
                sentiment_score["NEUTRAL"]+=1
                
        st.write(f"Sentiment analysis for {character_choice} in {movie_choice}")
        st.write("Positive:",sentiment_score['POSITIVE'])
        st.write("Negative:",sentiment_score['NEGATIVE'])
        st.write("Neutral:",sentiment_score['NEUTRAL'])