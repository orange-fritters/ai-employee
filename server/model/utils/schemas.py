from typing import List, TypedDict
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


class Context(BaseModel):
    title: str
    content: str


class RankTitle(BaseModel):
    title: str
    rank: int


class Search(BaseModel):
    query: str
    titles: List[RankTitle]
