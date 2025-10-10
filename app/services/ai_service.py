import openai
from app.config import OPENAI_API_KEY
import json

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_blog_metadata(prompt: str):
    system_prompt = (
        "You are a helpful assistant for WordPress blogging. "
        "When given a prompt, generate an SEO blog post, a catchy SEO title, a DALL·E image suggestion, and meta description. "
        "Respond in a valid JSON object with keys: title, featured_image_prompt, meta_description, content."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1200,
        temperature=0.7
    )
    ai_text = response.choices[0].message.content.strip()
    try:
        ai_json = json.loads(ai_text)
    except Exception:
        ai_json = {"raw": ai_text}
    return ai_json

def generate_featured_image(prompt: str):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url
    return image_url

def generate_blog_with_image(prompt: str):
    ai_json = generate_blog_metadata(prompt)
    featured_prompt = ai_json.get("featured_image_prompt", "")
    if featured_prompt:
        image_url = generate_featured_image(featured_prompt)
        ai_json["featured_image_url"] = image_url
    return ai_json
