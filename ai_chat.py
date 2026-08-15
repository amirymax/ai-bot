from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'),)

history: dict[int, list] = {}

SYSTEM_PROMPT = 'Tу ёрдамчии хушмуомила ҳастӣ. Кӯтоҳ ва фаҳмо ҷавоб деҳ'

def chat(user_id: int, text: str) -> str:
    if user_id not in history:
        history[user_id] = [
            {'role': 'system', 'content': SYSTEM_PROMPT}
        ]

    history[user_id].append({'role':'user','content': text})

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=history[user_id]
    )
    answer = response.choices[0].message.content
    history[user_id].append({'role':'assistant', 'content': answer})

    return answer

def generate_image(user_id, prompt: str) -> str:
    response = client.images.generate(
        model='gpt-image-2',
        prompt=prompt,
        size='1024x1024'
    )

    image_bytes64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_bytes64)

    filename = f"generated_{user_id}.png"

    with open(filename, 'wb') as f:
        f.write(image_bytes)

    return filename

def search(query: str) -> str:
    response = client.responses.create(
        model='gpt-4o-mini',
        tools = [
            {'type': 'web_search'}
        ],
        instructions='Ба забони тоҷикӣ ҷавоб деҳ. кӯтоҳ ва фаҳмо',
        input=query
    )

    return response.output_text
