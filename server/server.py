import json
import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from model.io_model import IOModel
from model.bm25.ensemble import Ensemble
from model.embed.multiturn_model import MultiTurn

from model.embed.embed_prompt import get_answer_from_question
import model.utils.convert_prompt as get_prompt
from model.utils.schemas import Query, Search, SingleString, History, RankTitle
from model.utils.get_response_openai import get_response_openai, get_response_prompted


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

io_model = IOModel('model/files/info_sheet.csv')
multiturn_model = MultiTurn()
ensemble = Ensemble()

# Single-turn


@app.post("/api/summary")
async def get_summary(query: SingleString):
    return io_model.get_summary(query.query)


@app.post("/api/gpt-summary")
async def get_chat(title: SingleString):
    content, target = io_model.get_content_target(title.title)

    prompt = get_prompt.get_summary(target, content, title.title)
    return StreamingResponse(get_response_openai(prompt), media_type="text/event-stream")


@app.post("/api/query")
async def get_chat_response(query: Query):
    filename = io_model.get_filename(query.title)
    filedir = os.path.join('articles', filename)
    with open(filedir, 'r', encoding='utf-8') as f:
        document = f.read()

    prompt = get_prompt.get_answer_from_document(document, query.query)
    return StreamingResponse(get_response_openai(prompt), media_type="text/event-stream")


@app.post("/api/recommendation")
async def get_recommendation(query: SingleString):
    recommendations = ensemble.get_topN_title(query.query)
    return json.dumps(recommendations)


@app.post("/api/search")
async def get_search(search: Search):
    titles = ensemble.get_topN_title(search.query)
    # titles [{"rank": i + 1, "title": title} for i, title in enumerate(top_titles)]
    titles = [RankTitle(**title) for title in titles]
    options = multiturn_model.get_contents_from_title(titles)
    prompt = get_answer_from_question(search.query, options)
    return StreamingResponse(get_response_prompted(prompt), media_type="text/event-stream")

# Multi-turn


@app.post("/api/multi-turn/decide-sufficiency")
async def decide_sufficiency(titles: List[RankTitle],
                             history: List[History]):
    # titles : [RankTitle(title='title_of_service', rank=0), RankTitle...]
    # history : [History(role='uesr', content='query_from_user'), History...]
    result = multiturn_model.decide_information_sufficiency(titles, history)
    print("server 80 line, check decision result as json: ", json.dumps(result))
    return json.dumps(result)


@app.post("/api/multi-turn/question")
async def get_new_question(titles: List[RankTitle],
                           history: List[History]):
    result = multiturn_model.get_question_from_history(titles, history)
    return json.dumps(result)


@app.post("/api/multi-turn/recommendation")
async def get_new_recommendation(titles: List[RankTitle],
                                 history: List[History]):
    result = multiturn_model.get_recommendation_new_history(history)
    print(result)
    return json.dumps(result)


@app.post("/api/multi-turn/answer")
async def get_answer(titles: List[RankTitle],
                     history: List[History]):
    result = multiturn_model.get_answer_from_history(titles, history)
    return json.dumps(result)


# View document


@app.get("/api/articles/view/{id}")
async def view_article(id: str):
    return RedirectResponse(url=f'/articles/{id}')


@app.get("/articles/{id}")
async def get_article(id: str):
    filename = io_model.data.iloc[int(id)]['filename']
    filepath = os.path.join('articles', filename)
    return FileResponse(filepath, media_type='text/html')


app.mount("/", StaticFiles(directory="../frontend/build", html=True), name="build")
