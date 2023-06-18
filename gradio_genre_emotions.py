import gradio as gr
import pandas as pd
from transformers import pipeline

sentiment_analysis = pipeline("sentiment-analysis")

df = pd.read_csv('replicas.csv')
genres = df['genres'].unique()
genres_values = []
for genre_array in genres:
    for genre in eval(genre_array.replace("' '", "', '")):
        if(genre not in genres_values):
            genres_values.append(genre)

# создание Gradio интерфейса
genres_dropdown = gr.inputs.Dropdown(genres_values, label="Choose movie genre")
count_rows_outputtext = gr.outputs.Textbox(label="Number of dialogues labels:")

def classify_sentiment(text):
    result = sentiment_analysis(text)[0]
    return result["label"]

def analyze_dialogues(genre):
    if(genre == ''):
        return 'Choose genre'
    sentiment_score = {"POSITIVE":0, "NEGATIVE":0, "NEUTRAL":0}
    df_movies_by_genre = df[df['genres'].str.contains(genre)].groupby('movie_id2').head(1).sample(n=30)
    for index, row in df_movies_by_genre.iterrows():
        replicas = eval(row['replicas'].replace('nan,', '').replace('nan', ''))
        for replic in replicas:
            sentiment_label=classify_sentiment(replic)
            sentiment_score[sentiment_label] +=1
    return sentiment_score


gr.Interface(fn=analyze_dialogues,
             inputs=[genres_dropdown],
             outputs=[count_rows_outputtext],
             title='Movie Dialogue Emotion Analysis',
             description='Analyze emotion distribution in movie dialogues by genre'
            ).launch()