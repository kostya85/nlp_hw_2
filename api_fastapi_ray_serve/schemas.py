from pydantic import BaseModel


class PerActorStatistics(BaseModel):
    actor: str
    positive_num: int = 0
    negative_num: int = 0
    neutral_num: int = 0


class ResponseModel(BaseModel):
    per_actor_stat: list[PerActorStatistics]


class ReplicaModel(BaseModel):
    actor: str
    text: str


class RequestModel(BaseModel):
    replicas_list: list[ReplicaModel]
