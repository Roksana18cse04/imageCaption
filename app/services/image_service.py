import base64
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = "openai/gpt-4.1"  # Must support vision input

def generate_caption_from_image_and_instruction(image_path, instruction):
    system_prompt = """
You are a smart caption creation assistant. A user will give you an image and a free-form instruction describing what kind of content they want to post (e.g., "write a LinkedIn post about this photo", "create an Instagram caption", etc).

Your job is to:
- Analyze the image content
- Understand the platform or tone implied by the instruction (LinkedIn, Instagram, etc.)
- Generate a high-quality, engaging caption that aligns with the visual and instruction
- Include emojis, hashtags, and formatting only if appropriate for the platform
- Write in first person unless told otherwise
- Behave like multilingual
"""

    # Convert image to base64
    with open(image_path, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
        image_url = f"data:image/jpeg;base64,{encoded_image}"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",  # Change to your domain if deploying
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt.strip()},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instruction},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        caption = result["choices"][0]["message"]["content"]
        print("Result Caption:\n", caption)
        return caption
    else:
        print("Error:", response.status_code, response.text)
        return "Failed to generate caption"
