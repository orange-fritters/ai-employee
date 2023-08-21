import json
import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from model.io_model import IOModel
from server.model.bm25.model import Model

import model.utils.convert_prompt as get_prompt
from model.neural_model.prompts import get_answer_from_question
from model.utils.schemas import Query, Search, SingleString, RankTitle
from model.utils.get_response_openai import get_response_openai, get_response_prompted

# App Setting Section

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

io_model = IOModel('model/files/info_sheet.csv')
ensemble = Model()


# Single-turn Section

@app.post("/api/summary")
async def get_summary(query: SingleString):
    """From a title, return a pre-generated summary of the article. """
    return io_model.get_summary(query.query)


@app.post("/api/query")
async def get_chat_response(query: Query):
    """ Endpoint for retrieve a documentand answer a query. """
    filename = io_model.get_filename(query.title)
    filedir = os.path.join('articles', filename)
    with open(filedir, 'r', encoding='utf-8') as f:
        document = f.read()

    prompt = get_prompt.get_answer_from_document(document, query.query)
    return StreamingResponse(get_response_openai(prompt), media_type="text/event-stream")


@app.post("/api/recommendation")
async def get_recommendation(query: SingleString):
    """ from query, return a list of titles of recommended service. """
    recommendations = ensemble.get_topN_title(query.query)
    return json.dumps(recommendations)


@app.post("/api/search")
async def get_search(search: Search):
    """
    Endpoint for retrieve and answer a search query.

    Args:
        search (Search): A Pydantic model representing the search query.
    Returns:
        StreamingResponse: A streaming response containing the search results.
    """
    # Function code here
    titles = ensemble.get_topN_title(search.query)
    titles = [RankTitle(**title) for title in titles]
    options = io_model.get_contents_from_title(titles)
    prompt = get_answer_from_question(search.query, options)
    return StreamingResponse(get_response_prompted(prompt), media_type="text/event-stream")


# View document Section

@app.get("/api/articles/view/{id}")
async def view_article(id: str):
    """ Redirection for viewing a document. """
    return RedirectResponse(url=f'/articles/{id}')


@app.get("/articles/{id}")
async def get_article(id: str):
    """ Endpoint for viewing a document. """
    filename = io_model.data.iloc[int(id)]['filename']
    filepath = os.path.join('articles', filename)
    return FileResponse(filepath, media_type='text/html')


# Static Section

app.mount("/", StaticFiles(directory="../frontend/build", html=True), name="build")
