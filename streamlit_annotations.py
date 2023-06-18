import os
import random
import pandas as pd
import streamlit as st


def show():
    df = pd.read_csv('replicas.csv')
    movies = df['mName'].unique()


    def get_replics(movie):
        df_replics_by_movie = df[(df['mName'] == movie)].head(3)
        result = []
        for index, row in df_replics_by_movie.iterrows():
            character_from = row['chName_1']
            character_to = row['chName_2']
            replicas = eval(row['replicas'].replace('nan,', '').replace('nan', ''))
            for replic in replicas:
                result.append(f'{character_from} to {character_to}: {replic}')
        return result

    st.write(
        """
        ## 📚 Text Annotation

        Welcome to the text annotation tool! Label some text and all of your
        annotations will be preserved in `st.session_state`!
        """
    )

    st.write("")

    movie_choice = st.selectbox("Choose a movie:", movies)

    data = get_replics(movie_choice)

    if "annotations" not in st.session_state or st.session_state.movie != movie_choice:
        st.session_state.movie = movie_choice
        st.session_state.annotations = {}
        st.session_state.data = data.copy()
        st.session_state.current_text = data[0]

    def annotate(label):
        st.session_state.annotations[st.session_state.current_text] = label
        if st.session_state.data:
            st.session_state.current_text = random.choice(st.session_state.data)
            st.session_state.data.remove(st.session_state.current_text)

    if st.session_state.data:
        st.write(
            "Annotated:",
            len(st.session_state.annotations),
            "– Remaining:",
            len(st.session_state.data),
        )
        st.write("### Text")
        st.write(st.session_state.current_text)
        st.button("Positive 😄", on_click=annotate, args=("positive",))
        st.button("Negative 😞", on_click=annotate, args=("negative",))
        st.button("Neutral 😐", on_click=annotate, args=("neutral",))
    else:
        st.success(
            f"🎉 Done! All {len(st.session_state.annotations)} texts annotated."
        )

    st.write("### Annotations")
    st.write(st.session_state.annotations)
        
if __name__ == "__main__":
    show()