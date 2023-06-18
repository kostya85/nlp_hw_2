from starlette.requests import Request
from transformers import pipeline
from ray import serve

sentiment_analysis = pipeline("sentiment-analysis")


@serve.deployment(route_prefix="/classify")
class SentimentAnalisys:
    _model = pipeline("sentiment-analysis")

    async def __call__(self, request: Request) -> str:
        input_json = await request.json()
        text = input_json["text"]
        label = self._model(text)[0]["label"]
        return label


app = SentimentAnalisys.bind()

if __name__ == '__main__':
    serve.run(app)
