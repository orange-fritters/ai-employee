import openai

openai.api_key_path = "model/files/config.txt"


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
