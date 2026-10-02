from huggingface_hub import InferenceClient

from config import HF_TOKEN

import base64
import io
import urllib.request

from PIL import Image


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
                            "text": (
                                "descreva o que está acontecendo nessa imagem "
                                "de forma simples e objetiva."
                            )
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

    async def describe_gif(self, gif_url):

        with urllib.request.urlopen(gif_url, timeout=10) as response:
            gif_data = response.read()

        gif = Image.open(io.BytesIO(gif_data))

        total_frames = getattr(gif, "n_frames", 1)

        if total_frames <= 3:
            frame_indexes = list(range(total_frames))
        else:
            frame_indexes = [
                0,
                total_frames // 2,
                total_frames - 1
            ]

        images = []

        for index in frame_indexes:
            gif.seek(index)

            frame = gif.convert("RGB")

            buffer = io.BytesIO()
            frame.save(buffer, format="JPEG", quality=75)

            encoded = base64.b64encode(
                buffer.getvalue()
            ).decode("utf-8")

            images.append(
                f"data:image/jpeg;base64,{encoded}"
            )

        content = [
            {
                "type": "text",
                "text": (
                    "essas são imagens de diferentes momentos de um GIF. "
                    "analise os frames juntos e descreva o que está acontecendo "
                    "na animação, incluindo movimentos ou mudanças perceptíveis. "
                    "seja simples e objetivo."
                )
            }
        ]

        for image in images:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": image
                }
            })

        response = self.client.chat_completion(
            model="Qwen/Qwen2.5-VL-3B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            max_tokens=300
        )

        return response.choices[0].message.content


vision = Vision()