def suggest_keywords_from_products_and_posts(products: list[str], posts: list[str]):
    """
    Given a list of product titles and posts, return a list of high-traffic keyword suggestions for ranking.
    """
    prompt = (
        "You are an SEO expert. Given the following product titles and post titles, suggest a list of 20 high-traffic, low-competition keywords that can help these products and posts rank better. "
        "Return the result as a JSON array of objects, each with keys: 'keyword', 'explanation', and 'search_volume'. "
        "Products: " + ", ".join(products) + ". Posts: " + ", ".join(posts)
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt}
        ],
        max_tokens=800,
        temperature=0.7
    )
    ai_text = response.choices[0].message.content.strip()
    # Remove code block markers if present
    if ai_text.startswith("```json"):
        ai_text = ai_text[7:]
    if ai_text.startswith("```"):
        ai_text = ai_text[3:]
    if ai_text.endswith("```"):
        ai_text = ai_text[:-3]
    ai_text = ai_text.strip()
    try:
        keywords = json.loads(ai_text)
    except Exception:
        keywords = {"raw": ai_text}
    return keywords

def generate_detailed_blog(keyword: str, context: dict = None):
    """
    Given a keyword, generate a detailed blog post (at least 1000 words) with comprehensive information,
    including SEO title, meta description, and a featured image.
    Optionally, include any context (such as previous blog data) for more detail.
    """
    base_prompt = (
        f"Write a comprehensive, in-depth blog post of at least 1000 words about the keyword: '{keyword}'. "
        "The blog should be highly informative, well-structured, and provide as much value as possible to the reader. "
        "Include sections, examples, tips, and actionable advice. "
    )
    if context:
        base_prompt += f"\n\nHere is some context or previous blog data to expand upon: {json.dumps(context)}"

    # Use the same metadata generation logic as generate_blog_with_image
    ai_json = generate_blog_metadata(base_prompt)
    featured_prompt = ai_json.get("featured_image_prompt", "")
    if featured_prompt:
        image_url = generate_featured_image(featured_prompt)
        ai_json["featured_image_url"] = image_url

    # Attach the keyword for reference
    ai_json["keyword"] = keyword
    return {"keyword": keyword, "blog": json.dumps(ai_json)}
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

def generate_keyword_plan(prompt: str):
    # Instruct the AI to generate keywords in an HTML table format, with monthly search volume
    ai_prompt = (
        "Act as an SEO expert. Based on the following business info, suggest the 20 best keywords to target. "
        "For each keyword, show monthly search volume, difficulty, and a related keyword. "
        "Return the result ONLY as an HTML table. DO NOT return any <html>, <body>, or <head> tags. "
        "OPTIONAL: Include a <style> block above the table for table formatting."
    ) + "\n\n" + prompt

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ai_prompt}
        ],
        max_tokens=1200,
        temperature=0.7
    )
    result = response.choices[0].message.content.strip()
    # Return the HTML table (or render as safe HTML in the plugin)
    return result
