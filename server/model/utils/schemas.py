from typing import List
from pydantic import BaseModel


class Query(BaseModel):
    query: str
    title: str


class SingleString(BaseModel):
    query: str


class MultiTurnProp(BaseModel):
    input: str
    titles: List[str]
    context: List[str]
