from transformers import pipeline
from fastapi import FastAPI
from ray import serve

from schemas import ResponseModel, RequestModel, PerActorStatistics

sentiment_analysis = pipeline("sentiment-analysis")

app = FastAPI()


@serve.deployment(route_prefix="/", num_replicas=2, ray_actor_options={"num_cpus": 0.2, "num_gpus": 0})
@serve.ingress(app)
class SentimentAnalysis:
    _model = pipeline("sentiment-analysis")

    @app.put("/classify", response_model=ResponseModel)
    async def classify(self, body: RequestModel) -> ResponseModel:
        actor_dict = {}
        for replica in body.replicas_list:
            if replica.actor not in actor_dict:
                actor_dict.update({replica.actor: PerActorStatistics(actor=replica.actor)})
                label = self._model(replica.text)[0]["label"]
                if label == "POSITIVE":
                    actor_dict[replica.actor].positive_num += 1
                elif label == "NEGATIVE":
                    actor_dict[replica.actor].negative_num += 1
                else:
                    actor_dict[replica.actor].neutral_num += 1
        return ResponseModel(per_actor_stat=[v for _, v in actor_dict.items()])


if __name__ == '__main__':
    serve.start()
    SentimentAnalysis.deploy()
