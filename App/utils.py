import openai
from dotenv import load_dotenv
import os

load_dotenv()  # load env variables
class DescriptionNotConfigured(RuntimeError):
    """Raised when product generation has no configured provider key."""


def generate_description(input):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise DescriptionNotConfigured("Product description generation is not configured.")
    messages = [
        {"role": "user",
         "content": """As a Product Description Generator, Generate multi paragraph rich text product description with emojis from the information provided to you' \n"""},
    ]
    messages.append({"role": "user", "content": f"{input}"})
    with openai.OpenAI(api_key=api_key) as client:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return completion.choices[0].message.content
