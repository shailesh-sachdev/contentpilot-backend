"""
SEO-Optimized Prompt Templates for Ollama
All templates designed for qwen2.5:7b with focus on clarity, structure, and commercial intent.
"""
from typing import Optional


class PromptTemplates:
    """Collection of SEO-optimized prompt templates for Ollama text generation."""
    
    @staticmethod
    def keyword_suggestions(products: list[str], posts: list[str]) -> str:
        """
        Generate prompt for SEO keyword research and suggestions.
        
        Args:
            products: List of product names to analyze
            posts: List of blog post titles to analyze
            
        Returns:
            Formatted prompt string
        """
        return (
            f"Generate 10 SEO keywords for: {', '.join(products)}\n"
            f"Existing posts: {', '.join(posts)}\n"
            "JSON array only: [{\"keyword\": \"phrase\", \"difficulty\": 30, \"volume\": \"500\", \"intent\": \"commercial\"}]"
        )
    
    @staticmethod
    def blog_post_with_fresh_data(topic: str, fresh_context: str) -> str:
        """
        Generate prompt for blog post using fresh/current data.
        
        Args:
            topic: Blog topic or primary keyword
            fresh_context: Context from RSS feeds (recent articles/data)
            
        Returns:
            Formatted prompt string
        """
        return (
            f"Write SEO blog about: {topic}\n"
            f"Data:\n{fresh_context}\n"
            "3 H2 sections, 500 words max, keyword natural, short paragraphs."
        )
    
    @staticmethod
    def blog_post_evergreen(topic: str) -> str:
        """
        Generate prompt for evergreen (timeless) blog post without fresh data.
        
        Args:
            topic: Blog topic or primary keyword
            
        Returns:
            Formatted prompt string
        """
        return (
            f"Write SEO blog about: {topic}\n"
            "3 H2 sections, 500 words max, keyword natural, timeless, short paragraphs."
        )
    
    @staticmethod
    def blog_metadata_system_prompt() -> str:
        """
        System prompt for generating SEO metadata (title, meta description, featured image prompt).
        Used with generate_blog_metadata in the content generation pipeline.
        
        Returns:
            System prompt string for Ollama
        """
        return (
            "Generate SEO blog JSON: title (50-60 chars), "
            "meta_description (150-160 chars with CTA), "
            "featured_image_prompt (50+ words), "
            "content (500 words, H2 headings). "
            "Valid JSON only."
        )
    
    @staticmethod
    def outline_structure(topic: str, fresh_context: Optional[str] = None) -> str:
        """
        Generate prompt for blog post outline with H2/H3 structure.
        
        Args:
            topic: Blog topic or primary keyword
            fresh_context: Optional context from RSS feeds
            
        Returns:
            Formatted prompt string
        """
        context_note = ""
        if fresh_context:
            context_note = (
                f"RECENT DATA (use naturally):\n"
                f"{fresh_context}\n\n"
            )
        
        return (
            "You are an expert content strategist specializing in SEO structure.\n\n"
            f"TOPIC: {topic}\n\n"
            f"{context_note}"
            "TASK: Create a detailed outline with proper heading hierarchy.\n\n"
            "OUTLINE STRUCTURE:\n"
            "H2: Main Section 1 (Introduction or overview)\n"
            "  H3: Subsection 1a\n"
            "  H3: Subsection 1b\n\n"
            "H2: Main Section 2 (Core concept)\n"
            "  H3: Subsection 2a\n"
            "  H3: Subsection 2b\n\n"
            "H2: Main Section 3 (Implementation or strategy)\n"
            "  H3: Subsection 3a\n"
            "  H3: Subsection 3b\n\n"
            "H2: Main Section 4 (Takeaway or conclusion)\n\n"
            "REQUIREMENTS:\n"
            "• Include primary keyword in at least 2 H2 headings\n"
            "• Each section should be specific and actionable\n"
            "• Use natural language (avoid awkward phrasing)\n"
            "• Target business decision-makers\n\n"
            "Return the outline with proper heading format (H2 = ##, H3 = ###):"
        )
    
    @staticmethod
    def seo_title_and_description(topic: str) -> str:
        """
        Generate prompt for SEO title and meta description only (lighter weight).
        
        Args:
            topic: Page topic or primary keyword
            
        Returns:
            Formatted prompt string
        """
        return (
            "You are an expert SEO copywriter.\n\n"
            f"TOPIC: {topic}\n\n"
            "TASK: Create an SEO-optimized title and meta description.\n\n"
            "TITLE GUIDELINES:\n"
            "• 50-60 characters including spaces\n"
            "• Include the primary keyword\n"
            "• Compelling and click-worthy\n"
            "• No clickbait or exaggeration\n"
            "• Benefit-driven if possible\n\n"
            "META DESCRIPTION GUIDELINES:\n"
            "• 150-160 characters including spaces\n"
            "• Summarize the content value\n"
            "• Include the primary keyword\n"
            "• Include a clear call-to-action\n"
            "• Specific and benefit-focused\n\n"
            "RESPONSE FORMAT:\n"
            "Return ONLY valid JSON:\n"
            "{\n"
            '  "title": "Your SEO title here",\n'
            '  "meta_description": "Your meta description here"\n'
            "}\n\n"
            "NO EXTRA TEXT. Valid JSON only."
        )
    
    @staticmethod
    def general_content(prompt: str) -> str:
        """
        Generate prompt for general-purpose content (passed through with minimal modification).
        
        Args:
            prompt: Original user prompt for content generation
            
        Returns:
            Enhanced prompt string with SEO guidelines
        """
        return (
            "You are an expert business content writer.\n\n"
            f"REQUEST: {prompt}\n\n"
            "GUIDELINES:\n"
            "• Write for business professionals and decision-makers\n"
            "• Use clear, direct language\n"
            "• Keep paragraphs short (2-3 sentences)\n"
            "• Include specific examples or data where relevant\n"
            "• Avoid jargon, fluff, or exaggeration\n"
            "• Focus on delivering clear value\n\n"
            "Begin writing:"
        )
