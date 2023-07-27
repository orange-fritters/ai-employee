import openai
import json

with open("model/utils/config.json") as config_file:
    config_data = json.load(config_file)
    openai.api_key = config_data["chatgpt"]["secret"]


def get_direct_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            temperature=0
        )
        return response['choices'][0]['text']
    except Exception as e:
        print("OpenAI Response (Streaming) Error: " + str(e))
        return "Error"
