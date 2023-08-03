from fastapi import HTTPException
import openai
import tiktoken
openai.api_key_path = "model/files/config.txt"


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

        async for chunk in response:
            current_content = chunk["choices"][0]["delta"].get("content", "")
            if current_content:
                yield current_content

    except Exception as e:
        print("OpenAI Response (Streaming) Error: " + str(e))
        raise HTTPException(503, "OpenAI server is busy, try again later")


async def get_response_prompted(prompt):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = 0
    for context in prompt:
        for role, content in context.items():
            tokens += len(encoding.encode(content))

    try:
        if tokens < 4000:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=prompt,
                stream=True,
            )
        else:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo-16k",
                messages=prompt,
                stream=True,
            )

        async for chunk in response:
            current_content = chunk["choices"][0]["delta"].get("content", "")
            if current_content:
                yield current_content

    except Exception as e:
        print("OpenAI Response (Streaming) Error: " + str(e))
        raise HTTPException(503, "OpenAI server is busy, try again later")
