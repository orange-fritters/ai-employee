import json
import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from model.bm25.ensemble import Ensemble
from model.io_model import IOModel
from model.embed.multiturn_model import MultiTurn
from model.utils.schemas import Query, SingleString, Context
from model.utils.get_response_openai import get_response_openai, get_response_prompted
import model.utils.convert_prompt as get_prompt


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
    # recommendations = multiturn_model.get_recommendations(query.query)
    recommendations = ensemble.get_topN_title(query.query)
    return json.dumps(recommendations)

# Multi-turn


@app.post("/api/multi-turn/initial")
async def get_multi_turn(query: SingleString):
    recommendations = multiturn_model.get_recommendations(query.query)
    return json.dumps(recommendations)


@app.post("/api/multi-turn/decide-sufficiency")
async def decide_sufficiency(titles: List[str], history: List[Context]):
    result = multiturn_model.decide_information_sufficiency(titles, history)
    return json.dumps(result)


@app.post("/api/multi-turn/new-question")
async def get_new_question(titles: List[str], history: List[Context]):
    result = multiturn_model.generate_question_based_on_history(titles, history)
    return json.dumps(result)


@app.post("/api/multi-turn/new-recommendation")
async def get_new_recommendation(history: List[Context]):
    result = multiturn_model.get_recommendation_new_history(history)
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
