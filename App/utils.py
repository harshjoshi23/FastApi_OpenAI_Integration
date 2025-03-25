import openai
from dotenv import load_dotenv
import os

load_dotenv()  # load env variables
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_description(input):
    messages = [
        {"role": "user",
         "content": """As a Product Description Generator, Generate multi paragraph rich text product description with emojis from the information provided to you' \n"""},
    ]
    messages.append({"role": "user", "content": f"{input}"})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = completion.choices[0].message.content
    return reply