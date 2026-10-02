from huggingface_hub import InferenceClient
from config import HF_TOKEN
from .personality import PERSONALITY

class Brain:
    def __init__(self):
        self.client = InferenceClient(api_key=HF_TOKEN)

    async def generate_response(self, context):
        messages=[
            {
                "role": "system",
                "content": PERSONALITY
            }
        ]

        for message in context:

            if message["is_bot"]:
                messages.append({
                    "role": "assistant",
                    "content": message["content"]
            })

            else:
                messages.append({
                    "role": "user",
                    "content": f'{message["author"]}: {message["content"]}'
             })

        response = self.client.chat_completion(
        model="openai/gpt-oss-20b",
        messages=messages,
        max_tokens=500
        )  
        return response.choices[0].message.content

brain = Brain()