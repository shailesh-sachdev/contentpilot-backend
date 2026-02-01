"""
Ollama service for text generation using self-hosted LLM.
Handles all text generation requests via Ollama REST API.
"""
import logging
import json
from typing import Optional
import requests
from requests.auth import HTTPBasicAuth
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_USERNAME, OLLAMA_PASSWORD

logger = logging.getLogger(__name__)

# Timeout for Ollama API calls (in seconds)
OLLAMA_TIMEOUT = 300  # Increased to 5 minutes for remote server


def convert_chat_messages_to_prompt(messages: list[dict]) -> str:
    """
    Convert OpenAI-style messages (role/content format) into a single prompt string.
    
    Args:
        messages: List of message dicts with 'role' and 'content' keys
        
    Returns:
        A single prompt string suitable for Ollama
    """
    prompt_parts = []
    
    for message in messages:
        role = message.get("role", "").lower()
        content = message.get("content", "")
        
        if role == "system":
            prompt_parts.append(f"{content}")
        elif role == "user":
            prompt_parts.append(f"User: {content}")
        elif role == "assistant":
            prompt_parts.append(f"Assistant: {content}")
    
    return "\n".join(prompt_parts)


def generate_text(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048
) -> str:
    """
    Call Ollama API to generate text based on a prompt.
    
    Args:
        prompt: The main prompt/query
        system_prompt: Optional system prompt to set context
        temperature: Sampling temperature (0.0 to 2.0)
        max_tokens: Maximum tokens in response
        
    Returns:
        Generated text from Ollama
        
    Raises:
        Exception: If Ollama API call fails
    """
    try:
        # Build the full prompt with system context if provided
        full_prompt = ""
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        else:
            full_prompt = prompt
        
        # Call Ollama API
        url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": full_prompt,
            "stream": False,
            "temperature": temperature,
            "num_predict": max_tokens
        }
        
        logger.debug(f"Calling Ollama at {url} with model {OLLAMA_MODEL}")
        
        # Use Basic Auth
        auth = HTTPBasicAuth(OLLAMA_USERNAME, OLLAMA_PASSWORD) if OLLAMA_PASSWORD else None
        
        response = requests.post(url, json=payload, timeout=OLLAMA_TIMEOUT, auth=auth)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result.get("response", "").strip()
        
        logger.debug(f"Ollama generation successful, tokens used: {result.get('eval_count', 'unknown')}")
        
        return generated_text
        
    except requests.exceptions.Timeout:
        error_msg = f"Ollama API timeout after {OLLAMA_TIMEOUT} seconds"
        logger.error(error_msg)
        raise Exception(error_msg)
    except requests.exceptions.RequestException as e:
        error_msg = f"Ollama API request failed: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)
    except (KeyError, json.JSONDecodeError) as e:
        error_msg = f"Failed to parse Ollama response: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)


def generate_text_from_chat_messages(
    messages: list[dict],
    temperature: float = 0.7,
    max_tokens: int = 2048
) -> str:
    """
    Generate text from OpenAI-style chat messages using Ollama.
    
    Args:
        messages: List of message dicts with 'role' and 'content' keys
        temperature: Sampling temperature
        max_tokens: Maximum tokens in response
        
    Returns:
        Generated text from Ollama
    """
    prompt = convert_chat_messages_to_prompt(messages)
    return generate_text(prompt, temperature=temperature, max_tokens=max_tokens)


def generate_json_response(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048
) -> dict:
    """
    Generate a JSON response from Ollama.
    Attempts to parse the response as JSON.
    
    Args:
        prompt: The main prompt/query
        system_prompt: Optional system prompt to set context
        temperature: Sampling temperature
        max_tokens: Maximum tokens in response
        
    Returns:
        Parsed JSON dict, or dict with 'raw' key if parsing fails
        
    Raises:
        Exception: If Ollama API call fails
    """
    generated_text = generate_text(prompt, system_prompt, temperature, max_tokens)
    
    # Clean up markdown code blocks if present
    text_clean = generated_text.strip()
    if text_clean.startswith("```json"):
        text_clean = text_clean[7:]
    if text_clean.startswith("```"):
        text_clean = text_clean[3:]
    if text_clean.endswith("```"):
        text_clean = text_clean[:-3]
    text_clean = text_clean.strip()
    
    try:
        return json.loads(text_clean)
    except (json.JSONDecodeError, ValueError):
        logger.warning("Failed to parse JSON from Ollama response, returning as raw text")
        return {"raw": generated_text}

def enhance_image_prompt(basic_prompt: str) -> str:
    """
    Enhance a basic image prompt using Ollama to create a detailed, high-quality DALL-E prompt.
    This function generates a comprehensive image description optimized for DALL-E-3.
    
    Args:
        basic_prompt: A basic or simple image description (e.g., "A professional workspace")
        
    Returns:
        An enhanced, detailed prompt optimized for DALL-E image generation
    """
    try:
        enhancement_prompt = (
            "You are an expert visual designer and DALL-E prompt engineer. "
            "Transform the following basic image description into a DETAILED, PROFESSIONAL, and HIGHLY SPECIFIC image prompt "
            "optimized for DALL-E-3 to generate stunning, publication-quality images.\n\n"
            "ENHANCEMENT REQUIREMENTS:\n"
            "1. Be VERY specific about visual elements, composition, lighting, colors, and mood\n"
            "2. Include style references (e.g., 'photographic', 'cinematic', 'professional photography', 'minimalist design')\n"
            "3. Specify camera angle and perspective (e.g., 'wide-angle shot', 'overhead view', 'close-up')\n"
            "4. Include lighting details (e.g., 'soft natural light', 'golden hour', 'dramatic shadows')\n"
            "5. Add texture and material descriptions (e.g., 'glossy', 'matte', 'metallic', 'natural textures')\n"
            "6. Include mood/atmosphere (e.g., 'professional', 'warm', 'modern', 'elegant')\n"
            "7. Specify resolution/quality (e.g., '4K resolution', 'high detail', 'sharp focus')\n"
            "8. Keep it under 150 words but make every word count\n"
            "9. Make it WordPress/blog-ready for featured images\n\n"
            f"BASIC PROMPT TO ENHANCE:\n{basic_prompt}\n\n"
            "ENHANCED PROMPT:\n"
            "Return ONLY the enhanced prompt text, nothing else. No quotes, no labels, just the improved prompt."
        )
        
        enhanced_prompt = generate_text(
            enhancement_prompt,
            temperature=0.7,
            max_tokens=300
        )
        
        logger.debug(f"Image prompt enhanced: {len(enhanced_prompt)} characters")
        return enhanced_prompt
        
    except Exception as e:
        logger.warning(f"Failed to enhance image prompt, using original: {str(e)}")
        # Fallback to original prompt if enhancement fails
        return basic_prompt