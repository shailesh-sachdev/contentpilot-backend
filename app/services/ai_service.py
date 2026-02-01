"""
AI service for text and image generation.
Text generation: Uses Ollama (self-hosted LLM)
Image generation: Uses OpenAI DALL·E
Fresh data: Integrates RSS feeds for current topics
"""
import openai
import json
import logging
from app.config import OPENAI_API_KEY
from app.services import ollama_service
from app.services import fresh_data_service
from app.services.prompt_templates import PromptTemplates

logger = logging.getLogger(__name__)

# Initialize OpenAI client for image generation only
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def suggest_keywords_from_products_and_posts(products: list[str], posts: list[str]):
    """
    Given a list of product titles and posts, return a list of high-traffic keyword suggestions for ranking.
    Uses Ollama for text generation with SEO-optimized templates.
    """
    try:
        prompt = PromptTemplates.keyword_suggestions(products, posts)
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
    Integrates fresh data pipeline for current topics.
    """
    try:
        # Step 1: Check if topic needs fresh data
        needs_fresh = fresh_data_service.needs_fresh_data(keyword)
        fresh_context = None
        
        if needs_fresh:
            logger.info(f"Topic '{keyword}' requires fresh data - fetching RSS articles")
            try:
                articles = fresh_data_service.fetch_rss_articles(max_items=3)
                if articles:
                    fresh_context = fresh_data_service.build_fresh_context(articles, max_chars=1200)
                    logger.info(f"Fresh context built: {len(fresh_context)} characters")
                else:
                    logger.warning("No articles fetched, proceeding without fresh data")
            except Exception as e:
                logger.error(f"Failed to fetch fresh data: {str(e)} - proceeding without it")
        
        # Step 2: Build optimized prompt with or without fresh data
        if fresh_context:
            base_prompt = PromptTemplates.blog_post_with_fresh_data(keyword, fresh_context)
        else:
            base_prompt = PromptTemplates.blog_post_evergreen(keyword)
        
        # Add user-provided context if available
        if context:
            base_prompt += f"\n\nAdditional context to consider: {json.dumps(context)}"

        # Step 3: Generate blog metadata using the optimized prompt
        ai_json = generate_blog_metadata(base_prompt)
        
        # Step 4: Generate featured image
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
    Uses Ollama for text generation with SEO guidelines.
    """
    try:
        enhanced_prompt = PromptTemplates.general_content(prompt)
        content = ollama_service.generate_text(enhanced_prompt, temperature=0.7, max_tokens=1024)
        return {"content": content}
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        raise


def generate_blog_metadata(prompt: str):
    """
    Generate SEO-optimized blog metadata (title, featured image prompt, meta description, content) from a prompt.
    Uses Ollama for text generation with expert SEO templates. Returns JSON with keys: title, featured_image_prompt, meta_description, content.
    """
    try:
        system_prompt = PromptTemplates.blog_metadata_system_prompt()
        ai_json = ollama_service.generate_json_response(
            prompt,
            system_prompt=system_prompt,
            temperature=0.6,
            max_tokens=1000
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
    Integrates fresh data pipeline for current topics.
    """
    try:
        # Step 1: Extract topic from prompt for fresh data detection
        # Simple heuristic: use the prompt as the topic
        needs_fresh = fresh_data_service.needs_fresh_data(prompt)
        fresh_context = None
        
        if needs_fresh:
            logger.info(f"Prompt requires fresh data - fetching RSS articles")
            try:
                articles = fresh_data_service.fetch_rss_articles(max_items=3)
                if articles:
                    fresh_context = fresh_data_service.build_fresh_context(articles, max_chars=1200)
                    logger.info(f"Fresh context built: {len(fresh_context)} characters")
            except Exception as e:
                logger.error(f"Failed to fetch fresh data: {str(e)} - proceeding without it")
        
        # Step 2: Build optimized prompt
        if fresh_context:
            optimized_prompt = PromptTemplates.blog_post_with_fresh_data(prompt, fresh_context)
        else:
            optimized_prompt = PromptTemplates.blog_post_evergreen(prompt)
        
        # Step 3: Generate blog metadata
        ai_json = generate_blog_metadata(optimized_prompt)
        
        # Step 4: Generate featured image
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
            "You are an expert SEO strategist. Generate strategic keyword recommendations as an HTML table.\n\n"
            "REQUIREMENTS:\n"
            "- Create a simple HTML table (no <html>/<body>/<head> tags)\n"
            "- Columns: Keyword | Search Volume | Difficulty | Intent | Priority\n"
            "- 10 strategic recommendations\n"
            "- Commercial/Informational/Transactional intent\n"
            "- Priority scores 1-5\n"
            "- Clean, WordPress-ready HTML\n\n"
            f"BUSINESS CONTEXT: {prompt}\n\n"
            "Generate the table now:"
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

