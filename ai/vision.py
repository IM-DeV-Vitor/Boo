from huggingface_hub import InferenceClient

from config import HF_TOKEN


class Vision:

    def __init__(self):
        self.client = InferenceClient(
            api_key=HF_TOKEN
        )

    async def describe_image(self, image_url):

        response = self.client.chat_completion(
            model="Qwen/Qwen2.5-VL-7B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "descreva o que está acontecendo nessa imagem de forma simples e objetiva."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )

        return response.choices[0].message.content


vision = Vision()