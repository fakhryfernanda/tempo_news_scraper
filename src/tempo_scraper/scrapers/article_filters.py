"""Article filtering module for Tempo.co scraper."""

from typing import List
from ..models.article import ArticleMetadata, Article
from ..extractors.article_extractor import extract_article_content

def filter_articles_by_access(articles: List[ArticleMetadata], use_auth: bool) -> List[ArticleMetadata]:
    """
    Filter articles based on access rights.
    
    Args:
        articles: List of article metadata
        use_auth: Whether authentication is being used
        
    Returns:
        Filtered list of articles
    """
    # The index scraper should list all articles (free and non-free)
    # Only the article extractor should skip non-free articles
    return articles

def extract_content_for_articles(articles: List[ArticleMetadata], use_auth: bool) -> List[Article]:
    """
    Extract full content for a list of articles.
    
    Args:
        articles: List of article metadata
        use_auth: Whether to use authentication for premium content
        
    Returns:
        List of articles with full content
    """
    articles_with_content = []
    
    for i, article_meta in enumerate(articles, 1):
        print(f"  Extracting content for article {i}/{len(articles)}: {article_meta.url}")
        
        # Convert relative URLs to absolute URLs
        if article_meta.url.startswith('/'):
            full_url = 'https://www.tempo.co' + article_meta.url
        else:
            full_url = article_meta.url
            
        # Check if article is free or if we're using authentication
        if not article_meta.is_free and not use_auth:
            # Non-free article without authentication
            print(f"    Article is not free and no authentication provided: {article_meta.url}")
            # Create article with empty content and reason
            empty_article = Article(
                metadata=article_meta,
                content=["[Content not available: Non-free article and no authentication provided]"],
                tags=[],
                images=[]
            )
            articles_with_content.append(empty_article)
            continue
            
        # Extract full content
        article = extract_article_content(full_url, use_auth)
        if article:
            articles_with_content.append(article)
        else:
            # Failed to extract content (likely photo/video archive)
            print(f"    Failed to extract content (likely photo/video archive): {article_meta.url}")
            # Create article with empty content and reason
            empty_article = Article(
                metadata=article_meta,
                content=["[Content not available: Article structure not found (likely photo/video archive)]"],
                tags=[],
                images=[]
            )
            articles_with_content.append(empty_article)
    
    return articles_with_content