"""
AI service for text and image generation.
Text generation: Uses Ollama (self-hosted LLM)
Image generation: Uses OpenAI DALL·E
"""
import openai
import json
import logging
from app.config import OPENAI_API_KEY
from app.services import ollama_service

logger = logging.getLogger(__name__)

# Initialize OpenAI client for image generation only
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def suggest_keywords_from_products_and_posts(products: list[str], posts: list[str]):
    """
    Given a list of product titles and posts, return a list of high-traffic keyword suggestions for ranking.
    Uses Ollama for text generation.
    """
    try:
        prompt = (
            "You are an SEO expert. Analyze these products and posts to suggest 10 high-traffic, low-competition keywords. "
            "Products: " + ", ".join(products) + "\n"
            "Posts: " + ", ".join(posts) + "\n\n"
            "Return ONLY valid JSON array with format: [{\"keyword\": \"example keyword\", \"explanation\": \"why it ranks\", \"search_volume\": \"5000\", \"difficulty\": 30, \"intent\": \"commercial\"}]"
        )
        
        keywords = ollama_service.generate_json_response(prompt, temperature=0.5, max_tokens=800)
        return keywords
    except Exception as e:
        logger.error(f"Error generating keywords from products and posts: {str(e)}")
        raise


def generate_detailed_blog(keyword: str, context: dict = None):
    """
    Given a keyword, generate a detailed blog post (at least 1000 words) with comprehensive information,
    including SEO title, meta description, and a featured image.
    Optionally, include any context (such as previous blog data) for more detail.
    Uses Ollama for text generation and DALL-E for featured image.
    """
    try:
        base_prompt = (
            f"You are an expert SEO copywriter. Write a well-structured, SEO-optimized blog post about: '{keyword}'. \n\n"
            f"STRUCTURE:\n"
            f"1. Introduction (100-150 words): Hook, establish authority\n"
            f"2. 3-4 main H2 sections (150-200 words each)\n"
            f"3. Conclusion (100 words): Summary + CTA\n\n"
            f"SEO REQUIREMENTS:\n"
            f"- Naturally use the keyword in title, first paragraph, and headings\n"
            f"- Include 2-3 long-tail keyword variations\n"
            f"- Use short paragraphs (2-3 sentences)\n"
            f"- Include bullet points and lists\n"
            f"- 7th-grade reading level\n"
            f"- Provide actionable insights\n"
        )
        if context:
            base_prompt += f"\n\nHere is some context or previous blog data to expand upon: {json.dumps(context)}"

        # Use the same metadata generation logic as generate_blog_with_image
        ai_json = generate_blog_metadata(base_prompt)
        featured_prompt = ai_json.get("featured_image_prompt", "")
        if featured_prompt:
            try:
                image_url = generate_featured_image(featured_prompt)
                ai_json["featured_image_url"] = image_url
            except Exception as e:
                logger.warning(f"Could not generate featured image for keyword '{keyword}': {str(e)}")
                ai_json["featured_image_url"] = None

        # Attach the keyword for reference
        ai_json["keyword"] = keyword
        return {"keyword": keyword, "blog": json.dumps(ai_json)}
    except Exception as e:
        logger.error(f"Error generating detailed blog for keyword '{keyword}': {str(e)}")
        raise


def generate_content(prompt: str):
    """
    Generate general content based on a prompt.
    Uses Ollama for text generation.
    """
    try:
        content = ollama_service.generate_text(prompt, temperature=0.7, max_tokens=1024)
        return {"content": content}
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        raise


def generate_blog_metadata(prompt: str):
    """
    Generate SEO-optimized blog metadata (title, featured image prompt, meta description, content) from a prompt.
    Uses Ollama for text generation with expert SEO guidelines. Returns JSON with keys: title, featured_image_prompt, meta_description, content.
    """
    try:
        system_prompt = (
            "You are an expert SEO content strategist and WordPress optimization specialist. "
            "Generate a RANK-WINNING blog post with optimal SEO metadata following these strict rules:\n\n"
            "TITLE: 50-60 characters, includes primary keyword, compelling, click-worthy (CTR optimized)\n"
            "META_DESCRIPTION: 150-160 characters, summarizes content value, includes keyword, includes CTA (e.g., 'Learn how...', 'Discover...')\n"
            "FEATURED_IMAGE_PROMPT: Detailed DALL-E prompt (50+ words) for visually compelling, professional image matching content\n"
            "CONTENT: 1200+ word SEO-optimized blog post with H2/H3 structure, keyword integration, and actionable insights\n\n"
            "Respond ONLY as a valid JSON object with EXACTLY these keys: 'title', 'featured_image_prompt', 'meta_description', 'content'. "
            "No markdown, no code blocks, just valid JSON."
        )
        
        ai_json = ollama_service.generate_json_response(
            prompt,
            system_prompt=system_prompt,
            temperature=0.6,
            max_tokens=1200
        )
        return ai_json
    except Exception as e:
        logger.error(f"Error generating blog metadata: {str(e)}")
        raise


def generate_featured_image(prompt: str):
    """
    Generate a featured image using DALL-E (OpenAI) with Ollama-enhanced prompts.
    First uses Ollama to enhance the image prompt for maximum quality, then sends to DALL-E.
    
    Args:
        prompt: Basic or detailed image generation prompt
        
    Returns:
        URL to the generated image
    """
    try:
        # Enhance the prompt using Ollama for better DALL-E output
        logger.debug(f"Enhancing image prompt using Ollama...")
        enhanced_prompt = ollama_service.enhance_image_prompt(prompt)
        
        logger.debug(f"Original prompt: {prompt[:100]}...")
        logger.debug(f"Enhanced prompt: {enhanced_prompt[:100]}...")
        
        # Generate image using DALL-E with enhanced prompt
        response = client.images.generate(
            model="dall-e-3",
            prompt=enhanced_prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        logger.debug(f"DALL-E image generated successfully with enhanced prompt")
        return image_url
    except Exception as e:
        logger.error(f"Failed to generate DALL-E image: {str(e)}")
        raise


def generate_blog_with_image(prompt: str):
    """
    Generate a complete blog with metadata and featured image.
    Uses Ollama for text and DALL-E for image.
    """
    try:
        ai_json = generate_blog_metadata(prompt)
        featured_prompt = ai_json.get("featured_image_prompt", "")
        if featured_prompt:
            try:
                image_url = generate_featured_image(featured_prompt)
                ai_json["featured_image_url"] = image_url
            except Exception as e:
                logger.warning(f"Could not generate featured image: {str(e)}")
                ai_json["featured_image_url"] = None
        return ai_json
    except Exception as e:
        logger.error(f"Error generating blog with image: {str(e)}")
        raise


def generate_keyword_plan(prompt: str):
    """
    Generate an SEO-focused keyword research plan with strategic targeting recommendations.
    Uses Ollama for text generation. Returns an HTML table with comprehensive metrics and priorities.
    """
    try:
        ai_prompt = (
            "You are an SEO expert. Based on this business info, suggest the top 10 best keywords to target.\n\n"
            "Return ONLY as a simple HTML table (no <html>/<body>/<head> tags) with columns:\n"
            "- Keyword\n"
            "- Search Volume\n"
            "- Difficulty (1-100)\n"
            "- Intent (Commercial/Informational/Transactional)\n"
            "- Priority (1-5)\n\n"
            "Make it clean and WordPress-ready.\n\n"
            "Business: " + prompt
        )

        result = ollama_service.generate_text(
            ai_prompt,
            temperature=0.5,
            max_tokens=800
        )
        
        return result
    except Exception as e:
        logger.error(f"Error generating keyword plan: {str(e)}")
        raise

