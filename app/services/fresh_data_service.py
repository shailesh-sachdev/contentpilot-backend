"""
Fresh Data Service for SEO Blog Generation
Fetches recent data from RSS feeds and integrates it into Ollama prompts.
"""
import logging
import re
from typing import Optional
import feedparser
from datetime import datetime

logger = logging.getLogger(__name__)

# RSS feeds for fresh content
RSS_FEEDS = [
    "https://wordpress.org/news/feed/",
    "https://developers.google.com/search/blog/rss.xml",
    "https://www.searchenginejournal.com/feed/",
    "https://www.searchenginewatch.com/feed/"
]

# Keywords that indicate need for fresh data (conservative list)
FRESH_DATA_KEYWORDS = [
    "latest", "recent", "update", "updates", "trends",
    "new", "2024", "2025", "2026",
    "current", "now", "today", "breaking", "news"
]


def needs_fresh_data(topic: str) -> bool:
    """
    Determine if a topic requires fresh data based on keyword detection.
    
    Args:
        topic: The blog topic or keyword to analyze
        
    Returns:
        True if topic requires fresh data, False for evergreen content
    """
    if not topic:
        return False
    
    topic_lower = topic.lower()
    
    # Check if any fresh data keyword is present
    for keyword in FRESH_DATA_KEYWORDS:
        if keyword in topic_lower:
            logger.debug(f"Fresh data needed for topic '{topic}' - matched keyword: '{keyword}'")
            return True
    
    # Check for year patterns (2024, 2025, 2026)
    if re.search(r'\b(202[4-9]|203[0-9])\b', topic_lower):
        logger.debug(f"Fresh data needed for topic '{topic}' - contains year")
        return True
    
    logger.debug(f"No fresh data needed for topic '{topic}'")
    return False


def fetch_rss_articles(max_items: int = 5) -> list[dict]:
    """
    Fetch recent articles from multiple RSS feeds.
    
    Args:
        max_items: Maximum number of articles to fetch from each feed
        
    Returns:
        List of article dicts with keys: title, summary, link, published
    """
    all_articles = []
    
    for feed_url in RSS_FEEDS:
        try:
            logger.debug(f"Fetching RSS feed: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:
                logger.warning(f"RSS feed parsing issue for {feed_url}: {feed.bozo_exception}")
                continue
            
            # Extract articles from feed
            for entry in feed.entries[:max_items]:
                article = {
                    "title": entry.get("title", "").strip(),
                    "summary": entry.get("summary", entry.get("description", "")).strip(),
                    "link": entry.get("link", "").strip(),
                    "published": entry.get("published", entry.get("updated", ""))
                }
                
                # Only add if we have at least title and summary
                if article["title"] and article["summary"]:
                    all_articles.append(article)
                    
        except Exception as e:
            logger.error(f"Failed to fetch RSS feed {feed_url}: {str(e)}")
            continue
    
    logger.info(f"Fetched {len(all_articles)} articles from {len(RSS_FEEDS)} RSS feeds")
    return all_articles


def build_fresh_context(articles: list[dict], max_chars: int = 800) -> str:
    """
    Build a clean, readable context string from fetched articles.
    
    Args:
        articles: List of article dicts from fetch_rss_articles
        max_chars: Maximum characters to include in context
        
    Returns:
        Formatted context string, truncated safely to max_chars
    """
    if not articles:
        return ""
    
    context_parts = ["=== RECENT DATA ===\n"]
    
    for idx, article in enumerate(articles, 1):
        # Clean HTML tags from summary if present
        summary = re.sub(r'<[^>]+>', '', article["summary"])
        summary = re.sub(r'\s+', ' ', summary).strip()
        
        # Truncate long summaries
        if len(summary) > 100:
            summary = summary[:97] + "..."
        
        article_text = (
            f"\n{idx}. {article['title']}\n"
            f"{summary}\n"
        )
        
        # Check if adding this article exceeds max_chars
        current_length = len("".join(context_parts))
        if current_length + len(article_text) > max_chars:
            context_parts.append("\n[Additional articles omitted due to length constraints]")
            break
        
        context_parts.append(article_text)
    
    context_parts.append("\n=== END DATA ===\n")
    
    final_context = "".join(context_parts)
    logger.debug(f"Built fresh context: {len(final_context)} characters, {len(articles)} articles")
    
    return final_context


def build_prompt(topic: str, fresh_context: Optional[str] = None) -> str:
    """
    Build an optimized prompt for Ollama, with or without fresh data.
    
    Args:
        topic: The blog topic or keyword
        fresh_context: Optional fresh data context from RSS feeds
        
    Returns:
        Complete prompt string for Ollama
    """
    if fresh_context:
        # Prompt with fresh data - enforce factual accuracy
        prompt = (
            f"Write an SEO blog post about '{topic}' using this data:\n\n"
            f"{fresh_context}\n\n"
            f"RULES:\n"
            f"- Use ONLY the data above for facts\n"
            f"- Don't invent dates or stats\n"
            f"- 3-4 H2 sections\n"
            f"- Include keyword naturally\n"
            f"- Short paragraphs\n"
            f"- 700-800 words total\n"
        )
    else:
        # Evergreen prompt - no fresh data required
        prompt = (
            f"Write an SEO blog post about '{topic}'.\n\n"
            f"RULES:\n"
            f"- 3-4 H2 sections\n"
            f"- Include keyword naturally\n"
            f"- Short paragraphs\n"
            f"- Timeless advice\n"
            f"- 700-800 words total\n"
        )
    
    return prompt
