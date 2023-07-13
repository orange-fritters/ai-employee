import uvicorn
import openai
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import JSONResponse
from urllib.parse import unquote


class Query(BaseModel):
    query: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("config.json") as config_file:
    config_data = json.load(config_file)
    openai.api_key = config_data["chatgpt"]["secret"]


@app.post("/query")
async def get_chat_response(query: Query):
    documents = ['articles/취업지원_1.html',
                 'articles/취업지원_2.html',
                 'articles/취업지원_3.html',
                 'articles/취업지원_4.html',
                 'articles/취업지원_5.html']

    html_url = documents[-1]
    with open(html_url, 'r', encoding='utf-8') as f:
        document = f.read()

    prompt = f"""
    오로지 아래 내용에만 기반하여 질문에 대해 답해주십시오.
    내용에 없는 내용은 생성하지 말아주십시오.

    ### 내용 :
    {document}

    ### 질문 :
    {query.query}
    """
    print(prompt)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return JSONResponse({"response": response['choices'][0]['message']['content']})

app.mount("/", StaticFiles(directory="../frontend/build", html=True), name="build")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
