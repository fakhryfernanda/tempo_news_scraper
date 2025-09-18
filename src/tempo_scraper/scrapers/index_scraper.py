"""Index scraping module for Tempo.co scraper."""

import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from urllib.parse import urlparse
from ..core.session import create_session
from ..core.logging import logger
from ..core.selectors import INDEX_SELECTORS, HEADERS
from ..models.article import ArticleMetadata

def scrape_index_page(
    url: str,
    page_num: int,
    article_per_page: int = 20
) -> List[ArticleMetadata]:
    """
    Scrape a single index page and return article metadata.
    
    Args:
        url: URL of the index page to scrape
        page_num: Page number (for logging)
        article_per_page: Maximum number of articles to extract per page
        
    Returns:
        List of article metadata
    """
    logger.info(f"Fetching URL: {url}")
    
    try:
        # Create session
        session = create_session()
        
        # Send GET request
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the div with class "flex flex-col divide-y divide-neutral-500"
        target_div = soup.find('div', class_=INDEX_SELECTORS["article_list_container"])
        
        articles = []
        
        if target_div:
            # Find all child divs
            child_divs = target_div.find_all(INDEX_SELECTORS["article_item"], recursive=False)
            
            # Limit the number of articles based on article_per_page parameter
            child_divs = child_divs[:article_per_page]
            
            # Extract href and text from each div > figure > figcaption > p > a
            for child_div in child_divs:
                figure = child_div.find(INDEX_SELECTORS["article_figure"])
                if figure:
                    figcaption = figure.find(INDEX_SELECTORS["article_figcaption"])
                    if figcaption:
                        p = figcaption.find(INDEX_SELECTORS["article_paragraph"])
                        if p:
                            link = p.find(INDEX_SELECTORS["article_link"])
                            if link and link.get('href'):
                                href = link['href']
                                title = link.get_text(strip=True).strip()
                                
                                # Extract category from the URL
                                category = extract_category_from_url(href)
                                
                                # Check if the article is free or not
                                is_free = is_article_free(link)
                                
                                articles.append(ArticleMetadata(
                                    url=href,
                                    title=title,
                                    category=category,
                                    is_free=is_free
                                ))
            
            logger.info(f"Page {page_num}: Found {len(articles)} articles (limited to {article_per_page} per page)")
        else:
            logger.warning(f"Page {page_num}: Div with class '{INDEX_SELECTORS['article_list_container']}' not found")
        
        return articles
    
    except requests.RequestException as e:
        logger.error(f"Error fetching page {page_num}: {e}")
        return []
    except Exception as e:
        logger.error(f"Error parsing HTML for page {page_num}: {e}")
        return []

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

def is_article_free(link_element: BeautifulSoup) -> bool:
    """
    Check if an article is free based on its link element.
    
    If premium indicators are found, the article is not free.
    If no premium indicators are found, the article is free.
    
    Args:
        link_element: BeautifulSoup element of the article link
        
    Returns:
        True if free, False if premium
    """
    # Look for span with class "inline-flex bg-primary-main p-[1.7px] rounded-[1.7px]"
    span_tag = link_element.find('span', class_=INDEX_SELECTORS["premium_indicator"])
    
    # If premium indicator is found, article is not free
    # If no premium indicator is found, article is free
    return span_tag is None