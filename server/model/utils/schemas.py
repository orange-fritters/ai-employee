from typing import List
from pydantic import BaseModel


class Query(BaseModel):
    query: str
    title: str


class SingleString(BaseModel):
    query: str


class History(BaseModel):
    # history = [{"role" : "user", "content" : ...},
    #            {"role" : "bot", "content" : ...}, ...]
    role: str
    content: str


class RankTitle(BaseModel):
    title: str
    rank: int


class Search(BaseModel):
    query: str
    titles: List[RankTitle]


class Option(BaseModel):
    title: str
    content: str


class Recommendation(BaseModel):
    rank: int
    title: str
