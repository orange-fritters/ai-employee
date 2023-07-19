from fastapi import HTTPException
import openai
import json

with open("model/utils/config.json") as config_file:
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

        async for chunk in response:
            current_content = chunk["choices"][0]["delta"].get("content", "")
            if current_content:
                yield current_content

    except Exception as e:
        print("OpenAI Response (Streaming) Error: " + str(e))
        raise HTTPException(503, "OpenAI server is busy, try again later")
