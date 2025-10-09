import openai
from app.config import OPENAI_API_KEY

print(f"DEBUG: OPENAI_API_KEY = '{OPENAI_API_KEY}'")  # Add this line


client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_content(prompt: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes high-quality SEO blog posts."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800,
        temperature=0.7
    )
    content = response.choices[0].message.content.strip()
    return {"content": content}


print(f"DEBUG: OPENAI_API_KEY = '{OPENAI_API_KEY}'")  # Add this line
