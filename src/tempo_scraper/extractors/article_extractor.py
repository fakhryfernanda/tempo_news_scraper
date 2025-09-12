"""Article extraction module for Tempo.co scraper."""

import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, List
from urllib.parse import urljoin, urlparse
from ..core.session import create_session
from ..core.logging import logger
from ..core.selectors import ARTICLE_SELECTORS, HEADERS
from ..models.article import Article, ArticleMetadata, Image
from ..utils.date_parser import parse_publication_datetime

def extract_article_content(url: str, use_auth: bool = False) -> Optional[Article]:
    """
    Extract article content from a Tempo.co article page.
    
    Args:
        url: URL of the article to extract
        use_auth: Whether to use authentication for premium content
        
    Returns:
        Article object with extracted content, or None if extraction fails
    """
    logger.info(f"Fetching URL: {url}")
    
    try:
        # Create session
        session = create_session(use_auth)
        
        # Send GET request with headers
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the article element
        article_element = soup.find('article', class_=ARTICLE_SELECTORS["article_container"])
        
        if not article_element:
            logger.warning("Article element not found")
            return None
        
        # Extract title
        title = ""
        title_tag = soup.find(ARTICLE_SELECTORS["title"])
        if title_tag:
            title = title_tag.get_text().strip()
        
        # Extract publication date
        pub_date = ""
        published_meta = soup.find('meta', property=ARTICLE_SELECTORS["published_time_meta"])
        publish_date_meta = soup.find('meta', attrs={'name': ARTICLE_SELECTORS["publish_date_meta"]})
        date_meta = published_meta or publish_date_meta
        if date_meta and date_meta.get('content'):
            pub_date = date_meta.get('content')
        
        # Extract author
        author = ""
        author_meta = soup.find('meta', attrs={'name': 'author'})
        if author_meta and author_meta.get('content'):
            author = author_meta.get('content')
        
        # Extract category from URL
        category = extract_category_from_url(url)
        
        # Extract article body content
        content_paragraphs = []
        content_wrappers = article_element.find_all('div', id=ARTICLE_SELECTORS["content_wrapper"])
        for wrapper in content_wrappers:
            paragraphs = wrapper.find_all(ARTICLE_SELECTORS["content_paragraph"])
            for p in paragraphs:
                # Skip empty paragraphs and editor picks
                text = p.get_text().strip()
                if text and not text.startswith(ARTICLE_SELECTORS["editor_pick_indicator"]):
                    content_paragraphs.append(text)
        
        # Extract tags
        tags = []
        tag_links = article_element.find('div', id=ARTICLE_SELECTORS["tags_container"])
        if tag_links:
            tag_elements = tag_links.find_all(ARTICLE_SELECTORS["tag_link"])
            for tag_elem in tag_elements:
                tag_text = tag_elem.get_text().strip()
                if tag_text:
                    tags.append(tag_text)
        
        # Extract images
        images = []
        img_tags = article_element.find_all(ARTICLE_SELECTORS["image"])
        for img in img_tags:
            src = img.get('src', '')
            alt = img.get('alt', '')
            # Only add if src is not empty and not the ads logo
            if src and src != ARTICLE_SELECTORS["ads_logo"]:
                images.append(Image(src=src, alt=alt))
        
        # Parse publication datetime
        pub_datetime = parse_publication_datetime(pub_date)
        
        # Create metadata
        metadata = ArticleMetadata(
            url=url,
            title=title,
            category=category,
            publication_date_raw=pub_date,
            publication_date=pub_datetime["date"],
            publication_time=pub_datetime["time"],
            timezone=pub_datetime["timezone"],
            author=author
        )
        
        # Create article object
        article = Article(
            metadata=metadata,
            content=content_paragraphs,
            tags=tags,
            images=images
        )
        
        return article
    
    except requests.RequestException as e:
        logger.error(f"Error fetching the page: {e}")
        return None
    except Exception as e:
        logger.error(f"Error parsing HTML: {e}")
        return None

def extract_category_from_url(url: str) -> str:
    """
    Extract category from URL path.
    
    Args:
        url: Article URL
        
    Returns:
        Category name
    """
    # Handle relative URLs by adding a base
    if url.startswith('/'):
        url = 'https://tempo.co' + url
    
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    if path_parts and path_parts[0]:
        return path_parts[0]
    return "indeks"  # Default category if none found

