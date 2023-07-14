import uvicorn
import openai
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


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


async def get_response_openai(prompt):
    try:
        prompt = prompt
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )

        print("Got response from OpenAI")
        async for chunk in response:
            current_content = chunk["choices"][0]["delta"].get("content", "")
            print(current_content)
            if current_content:
                yield current_content

    except Exception as e:
        print("OpenAI Response (Streaming) Error: " + str(e))
        raise HTTPException(503, "OpenAI server is busy, try again later")


@app.post("/query")
async def get_chat_response(query: Query):
    document = "articles/취업지원_1.html"
    with open(document, 'r', encoding='utf-8') as f:
        document = f.read()[:1000]

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
