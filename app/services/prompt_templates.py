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
            "You are an expert SEO strategist specializing in high-ROI keyword research.\n\n"
            "TASK: Analyze the following products and content to suggest 10 highly targeted keywords.\n\n"
            "PRODUCTS TO ANALYZE:\n"
            f"{', '.join(products)}\n\n"
            "EXISTING POSTS:\n"
            f"{', '.join(posts)}\n\n"
            "KEYWORD CRITERIA:\n"
            "• High commercial intent (business-focused)\n"
            "• Low-to-medium keyword difficulty\n"
            "• Aligned with products/services\n"
            "• Realistic search volume (100+ monthly searches)\n"
            "• Specific and actionable (avoid generic terms)\n\n"
            "RESPONSE FORMAT:\n"
            "Return ONLY a valid JSON array with exactly 10 objects. Each object must have:\n"
            "{\n"
            '  "keyword": "exact keyword phrase",\n'
            '  "explanation": "why this ranks for your products",\n'
            '  "search_volume": "estimated monthly searches",\n'
            '  "difficulty": 25,\n'
            '  "intent": "commercial|informational|navigational"\n'
            "}\n\n"
            "NO MARKDOWN, NO EXPLANATION TEXT. Return ONLY the JSON array."
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
            "You are an expert SEO content strategist writing for business decision-makers.\n\n"
            f"TOPIC: {topic}\n\n"
            f"RECENT DATA YOU MUST USE:\n"
            f"{fresh_context}\n\n"
            "CRITICAL RULES:\n"
            "• Use ONLY facts and data provided above\n"
            "• Do NOT invent dates, statistics, or claims\n"
            "• If information is incomplete, acknowledge it\n"
            "• Cite recent developments naturally\n"
            "• Maintain an authoritative, current tone\n\n"
            "CONTENT STRUCTURE:\n"
            "• H2 Heading 1: Introduction and relevance (100-150 words)\n"
            "• H2 Heading 2: Key insight #1 (150-200 words)\n"
            "• H2 Heading 3: Key insight #2 (150-200 words)\n"
            "• H2 Heading 4: Takeaway/implementation (100-150 words)\n\n"
            "SEO REQUIREMENTS:\n"
            "• Naturally include the primary keyword 2-3 times\n"
            "• Use 2-3 long-tail keyword variations\n"
            "• Short paragraphs (2-3 sentences max)\n"
            "• Use bullet points for data/statistics\n"
            "• Professional tone, 7th-grade reading level\n"
            "• Total: 700-800 words\n\n"
            "Write the blog post now (H2/H3 headings included, no introductory text):"
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
            "You are an expert SEO content strategist writing timeless content for business readers.\n\n"
            f"TOPIC: {topic}\n\n"
            "CONTENT STRUCTURE:\n"
            "• H2 Heading 1: Why this matters (100-150 words)\n"
            "• H2 Heading 2: Core concept/strategy (150-200 words)\n"
            "• H2 Heading 3: Practical implementation (150-200 words)\n"
            "• H2 Heading 4: Common mistakes to avoid (100-150 words)\n\n"
            "SEO REQUIREMENTS:\n"
            "• Naturally include the primary keyword 2-3 times\n"
            "• Use 2-3 long-tail keyword variations\n"
            "• Short paragraphs (2-3 sentences max)\n"
            "• Use numbered lists and bullet points\n"
            "• Professional tone, 7th-grade reading level\n"
            "• Provide timeless, actionable strategies\n"
            "• Avoid dates, trends, or time-specific references\n"
            "• Total: 700-800 words\n\n"
            "Write the blog post now (H2/H3 headings included, no introductory text):"
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
            "You are an expert SEO content strategist and conversion rate optimization specialist.\n\n"
            "TASK: Generate SEO-optimized metadata for a blog post.\n\n"
            "OUTPUT REQUIREMENTS:\n"
            "Generate exactly 4 JSON fields:\n\n"
            "1. title (50-60 characters)\n"
            "   • Include primary keyword naturally\n"
            "   • Create curiosity or promise value\n"
            "   • Optimize for click-through rate (CTR)\n"
            "   • Avoid clickbait or exaggeration\n\n"
            "2. meta_description (150-160 characters)\n"
            "   • Summarize content value clearly\n"
            "   • Include primary keyword\n"
            "   • Include call-to-action (e.g., 'Learn how...', 'Discover...')\n"
            "   • Compelling, specific, benefit-driven\n\n"
            "3. featured_image_prompt (50+ words)\n"
            "   • Detailed DALL-E image prompt\n"
            "   • Professional, visually compelling\n"
            "   • Matches content theme and topic\n"
            "   • Include style descriptors (clean, modern, professional)\n\n"
            "4. content (700-800 words)\n"
            "   • SEO-optimized blog post\n"
            "   • H2/H3 heading structure\n"
            "   • Keyword integration throughout\n"
            "   • Actionable, specific insights\n"
            "   • Short paragraphs (2-3 sentences)\n\n"
            "RESPONSE FORMAT:\n"
            "Return ONLY valid JSON with these exact keys: 'title', 'meta_description', 'featured_image_prompt', 'content'.\n"
            "NO MARKDOWN, NO CODE BLOCKS, NO EXTRA TEXT. Valid JSON only."
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
