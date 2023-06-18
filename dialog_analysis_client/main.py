import requests
import streamlit as st
import pandas as pd
import altair as alt


# Define the API endpoint URL
URL = "http://localhost:8000/classify"

# Set the replicas of dialog
DIALOG = [
        {
            "actor": "bod",
            "text": "Hi Glad to see you!!"
        },
        {
            "actor": "Ann",
            "text": "Oh NO!!"
        }
    ]

st.set_page_config(page_title="FastAPI + Ray Server Visualization", page_icon=":bar_chart:", layout="wide")
st.sidebar.title("Options")

response = requests.put(URL, json={"replicas_list": DIALOG})
data = response.json()["per_actor_stat"]
selected_actor = st.sidebar.selectbox("Select Actor", [el["actor"] for el in data])

pd_data = pd.DataFrame({"actor": [el["actor"] for el in data],
                        "positive_num": [el["positive_num"] for el in data],
                        "negative_num": [el["negative_num"] for el in data],
                        "neutral_num": [el["neutral_num"] for el in data],
                        })

chart_figure_pos = alt.Chart(pd_data.query(f"actor == '{selected_actor}'")).mark_bar().encode(
    x='actor',
    y='positive_num'
)
chart_figure_neg = alt.Chart(pd_data.query(f"actor == '{selected_actor}'")).mark_bar().encode(
    x='actor',
    y='negative_num'
)
chart_figure_neutral = alt.Chart(pd_data.query(f"actor == '{selected_actor}'")).mark_bar().encode(
    x='actor',
    y='neutral_num'
)

st.altair_chart(chart_figure_pos, use_container_width=True)
st.altair_chart(chart_figure_neg, use_container_width=True)
st.altair_chart(chart_figure_neutral, use_container_width=True)
