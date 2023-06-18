# Задание 1. Анализ диалогов с Gradio

## Работа с данными

Предобработку данных можно найти в файле dataset-preparation.ipynb
Данные после предобработки находятся в replicas.csv

## Sentiment
### API с Ray Serve лежит тут: ```api_ray_serve/```

### API FastAPI + Ray Serve лежит тут: ```api_fastapi_ray_serve/```

### Визуализация статистики по репликам диалога лежит тут: ```dialog_analysis_client/```
#### Запуск:
##### Для начала записываем диалог в виде списка реплик в переменную DIALOG файла main.py
##### После этого командой ```streamlit run <path_to_main_file>``` запускаем визуализацию


## Genre + Emotions

Визуализация данных реализована в gradio_genre_emotions.py

# Задание 2. Streamlit

## Speaker + Emotions

Алгоритм находится в файле streamlit_speaker_emotions.py

## Интерфейс для аннотации

Алгоритм находится в файле streamlit_annotations.py