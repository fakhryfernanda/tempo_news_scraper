"""File handling utilities for Tempo.co scraper."""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
from ..models.article import Article

def save_articles_to_json(
    articles: List[Article],
    output_dir: str,
    is_index_scraping: bool = True,
    scraping_options: Dict[str, Any] = None
) -> str:
    """
    Save articles data to a JSON file with timestamp-based naming.
    
    Args:
        articles: List of articles to save
        output_dir: Directory to save the file
        is_index_scraping: Whether this is index scraping or single article extraction
        scraping_options: Options used for scraping
        
    Returns:
        Path to the saved file
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamps
    now = datetime.now()
    filename_timestamp = now.strftime("%Y%m%d_%H%M%S")
    metadata_timestamp = now.strftime("%Y/%m/%d %H:%M:%S")
    
    # Create filename with timestamp
    if is_index_scraping:
        output_filename = f"indeks_{filename_timestamp}.json"
    else:
        output_filename = f"article_{filename_timestamp}.json"
    
    output_file = os.path.join(output_dir, output_filename)
    
    if is_index_scraping:
        # Index scraping - include filter info
        # If extract_content is false, only include specific fields
        if scraping_options and not scraping_options.get("extract_content", False):
            # Create simplified article data with only the required fields
            simplified_articles = []
            for article in articles:
                simplified_article = {
                    "url": article.metadata.url,
                    "title": article.metadata.title,
                    "category": article.metadata.category,
                    "is_free": article.metadata.is_free
                }
                simplified_articles.append(simplified_article)
            
            output_data = {
                "metadata": {
                    "type": "index",
                    "timestamp": metadata_timestamp,
                    "scraping_options": scraping_options or {},
                    "total_articles": len(articles)
                },
                "articles": simplified_articles
            }
        else:
            # Include full article data
            output_data = {
                "metadata": {
                    "type": "index",
                    "timestamp": metadata_timestamp,
                    "scraping_options": scraping_options or {},
                    "total_articles": len(articles)
                },
                "articles": [article.__dict__ for article in articles]
            }
    else:
        # Single article extraction
        output_data = articles[0].__dict__ if articles else {}
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2, default=lambda o: o.__dict__)
        
        print(f"Successfully saved {len(articles)} articles to {output_file}")
        return output_file
    except Exception as e:
        print(f"Error saving to JSON file: {e}")
        raise