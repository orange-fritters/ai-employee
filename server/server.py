import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from model.sample import Model
from model.utils.get_response_openai import get_response_openai
from model.ir.recommendation import Recommendation


class Query(BaseModel):
    query: str
    title: str


class SingleString(BaseModel):
    query: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/{full_path:path}", include_in_schema=False)
# async def catch_all(full_path: str):
#     return FileResponse('../frontend/build/index.html')

model = Model('model/info_sheet.csv')
rec = Recommendation('model/info_sheet.csv',
                     'articles/')


@app.post("/api/summary")
async def get_summary(query: SingleString):
    return model.get_summary(query.query)


@app.post("/api/recommendation")
async def get_recommendation(query: SingleString):
    return rec.get_bm25(query.query)


@app.post("/api/query")
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


@app.get("/articles/{id}")
async def get_article(id: str):
    filename = model.data.iloc[int(id)]['filename']
    filepath = os.path.join('articles', filename)
    return FileResponse(filepath, media_type='text/html')


@app.get("/api/articles/view/{id}")
async def view_article(id: str):
    filename = model.data.iloc[int(id)]['filename']
    return RedirectResponse(url=f'/articles/{id}')


app.mount("/", StaticFiles(directory="../frontend/build", html=True), name="build")
