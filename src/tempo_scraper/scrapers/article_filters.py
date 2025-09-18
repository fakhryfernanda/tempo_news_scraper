"""Article filtering module for Tempo.co scraper."""

from typing import List
from ..models.article import ArticleMetadata, Article
from ..extractors.article_extractor import extract_article_content
from ..core.logging import logger

def filter_articles_by_access(articles: List[ArticleMetadata]) -> List[ArticleMetadata]:
    """
    Filter articles based on access rights.
    
    Args:
        articles: List of article metadata
        
    Returns:
        Filtered list of article metadata
    """
    # The index scraper should list all articles (free and non-free)
    # Only the article extractor should skip non-free articles
    return articles

def extract_content_for_articles(articles: List[ArticleMetadata]) -> List[Article]:
    """
    Extract full content for a list of articles.
    
    Args:
        articles: List of article metadata
        
    Returns:
        List of articles with full content
    """
    articles_with_content = []
    
    for i, article_meta in enumerate(articles, 1):
        logger.info(f"Extracting content for article {i}/{len(articles)}: {article_meta.url}")
        
        # Convert relative URLs to absolute URLs
        if article_meta.url.startswith('/'):
            full_url = 'https://www.tempo.co' + article_meta.url
        else:
            full_url = article_meta.url
            
        # Check if article is free (authentication is no longer supported)
        if not article_meta.is_free:
            # Non-free article without authentication
            logger.info(f"  Article is not free and no authentication provided: {article_meta.url}")
            # Create article with empty content and reason
            empty_article = Article(
                metadata=article_meta,
                content=["[Content not available: Non-free article and no authentication provided]"],
                tags=[]
            )
            articles_with_content.append(empty_article)
            continue
            
        # Extract full content
        article = extract_article_content(full_url)
        if article:
            articles_with_content.append(article)
        else:
            # Failed to extract content (likely photo/video archive)
            logger.info(f"  Failed to extract content (likely photo/video archive): {article_meta.url}")
            # Create article with empty content and reason
            empty_article = Article(
                metadata=article_meta,
                content=["[Content not available: Article structure not found (likely photo/video archive)]"],
                tags=[]
            )
            articles_with_content.append(empty_article)
    
    return articles_with_content