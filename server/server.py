import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from model.sample import Model
from model.utils.get_response_openai import get_response_openai


class Query(BaseModel):
    query: str
    title: str


class Situation(BaseModel):
    query: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = Model('model/info_sheet.csv')


@app.post("/recommendation")
async def get_recommendation(query: Situation):
    return model.get_recommendation(query.query)


@app.post("/query")
async def get_chat_response(query: Query):
    document = model.get_filename(query.title)
    document = os.path.join('articles', document)
    with open(document, 'r', encoding='utf-8') as f:
        document = f.read()

    prompt = f"""
    오로지 아래 내용에만 기반하여 질문에 대해 답해주십시오.
    내용에 없는 내용은 생성하지 말아주십시오.

    ### 내용 :
    {document}

    ### 질문 :
    {query.query}
    """
    return StreamingResponse(get_response_openai(prompt), media_type="text/event-stream")

app.mount("/", StaticFiles(directory="../frontend/build", html=True), name="build")
