import os
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from model.embed import Model
from model.utils.get_response_openai import get_response_openai, get_response_prompted
from model.utils.get_chat import get_direct_response
from model.ir.recommendation import Recommendation


class Query(BaseModel):
    query: str
    title: str


class SingleString(BaseModel):
    query: str


class MultiTurn(BaseModel):
    input: str
    titles: List[str]
    context: List[str]


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
    return model.get_gpt_recommendation(query.query)
    # return rec.get_bm25(query.query)


@app.post("/api/gpt-summary")
async def get_chat(title: SingleString):
    content, target = model.get_content_target(title.title)

    prompt = f"""
    ### 대상 : {target}
    ### 내용 : {content}
          {title}의 대상과 내용에 대해 쉬운 말로 세 문장 이내로 요약하시오.
        - 마침표 이후에는 \n을 사용하시오.
        - 오로지 요약문만 출력하시오.
        - 문의 방법은 절대 포함하지 마시오.
        - 존댓말을 사용하시오 (습니다. 입니다. ~입니다.)
    """
    return StreamingResponse(get_response_openai(prompt), media_type="text/event-stream")


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


@app.post("/api/multi-turn")
async def get_multi_turn(body: MultiTurn):
    user_input = body.input
    titles: List[str] = body.titles
    target_explanation = [f"{title}의 대상: " + model.get_target(title) for title in titles]
    target_explanation = '\n'.join(target_explanation)
    history: List[str] = body.context
    history = '\n'.join(history)
    prompt = [
        {"role": "assistant",
         "content":
            f"""
            target : {target_explanation}
            """},
        {"role": "assistant",
         "content":
            f"""
            history : {history}
            """},
        {"role": "user", "content": user_input},
        {"role": "system", "content": f"""
            You are a counselor to answer the question from the user. 
            You should re-ask a question to pick one service to recommend. 
            Write a question to ask a  counsellee to get more information and verify which might fit him most.
            Question should be in Korean.
            Reference the previous history and (1) ask more or (2) choose service and explain.
            You should never use information that is not in the above passage.
            What is your response to the question?
         """},
    ]
    return StreamingResponse(get_response_prompted(prompt), media_type="text/event-stream")


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
