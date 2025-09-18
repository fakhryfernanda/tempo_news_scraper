"""File handling utilities for Tempo.co scraper."""

import logging
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from ..models.article import Article

logger = logging.getLogger('tempo_scraper')

def save_categorized_articles_to_files(
    articles: List[Article],
    output_dir: str,
    filename_timestamp: str,
    metadata_timestamp: str,
    scraping_options: Dict[str, Any] = None,
    extract_content: bool = False,
    output_filename: Optional[str] = None
) -> str:
    """
    Save categorized articles to separate files in a timestamped directory.
    
    Args:
        articles: List of articles to save
        output_dir: Base directory to save the files
        filename_timestamp: Timestamp for folder and filenames
        metadata_timestamp: Timestamp for metadata
        scraping_options: Options used for scraping
        extract_content: Whether full content was extracted
        output_filename: Custom output name (without extension) (default: None)
        
    Returns:
        Path to the created directory
    """
    # Create the directory with custom name or timestamped name
    if output_filename:
        category_dir = os.path.join(output_dir, output_filename)
    else:
        category_dir = os.path.join(output_dir, f"indeks_{filename_timestamp}")
    os.makedirs(category_dir, exist_ok=True)
    
    # Categorize articles
    categorized_articles = {}
    category_counts = {}
    
    # Process articles and group by category
    for article in articles:
        # Convert article to dictionary format based on whether we have full content or not
        if extract_content:
            # Full article data - convert the entire Article object to dict
            article_dict = {
                "metadata": article.metadata.__dict__,
                "content": article.content,
                "tags": article.tags
            }
            category = article.metadata.category
        else:
            # Simplified article data - just the metadata fields
            article_dict = {
                "url": article.metadata.url,
                "title": article.metadata.title,
                "category": article.metadata.category,
                "is_free": article.metadata.is_free
            }
            category = article.metadata.category
        
        if category not in categorized_articles:
            categorized_articles[category] = []
            category_counts[category] = 0
        categorized_articles[category].append(article_dict)
        category_counts[category] += 1
    
    # Save each category to a separate file
    for category, category_articles in categorized_articles.items():
        # Create category filename (sanitize for filesystem)
        category_filename = f"{category}.json"
        category_file_path = os.path.join(category_dir, category_filename)
        
        # Create the category data structure
        category_data = {category: category_articles}
        
        # Save category file
        with open(category_file_path, 'w', encoding='utf-8') as f:
            json.dump(category_data, f, ensure_ascii=False, indent=2)
    
    # Create and save metadata
    metadata = {
        "type": "index",
        "timestamp": metadata_timestamp,
        "scraping_options": scraping_options or {},
        "total_articles": len(articles),
        "categories": category_counts
    }
    
    metadata_file_path = os.path.join(category_dir, "metadata.json")
    with open(metadata_file_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Successfully saved {len(articles)} articles to {category_dir}")
    return category_dir

def save_articles_to_json(
    articles: List[Article],
    output_dir: str,
    is_index_scraping: bool = True,
    scraping_options: Dict[str, Any] = None,
    categorize: bool = False,
    output_filename: Optional[str] = None
) -> str:
    """
    Save articles data to a JSON file with timestamp-based naming.
    
    Args:
        articles: List of articles to save
        output_dir: Directory to save the file
        is_index_scraping: Whether this is index scraping or single article extraction
        scraping_options: Options used for scraping
        categorize: Whether to categorize articles by category
        output_filename: Custom output name (without extension) (default: None)
        
    Returns:
        Path to the saved file or directory
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamps
    now = datetime.now()
    filename_timestamp = now.strftime("%Y%m%d_%H%M%S")
    metadata_timestamp = now.strftime("%Y/%m/%d %H:%M:%S")
    
    # Handle categorization differently - create separate files
    if is_index_scraping and categorize:
        extract_content = scraping_options and scraping_options.get("extract_content", False)
        return save_categorized_articles_to_files(
            articles, 
            output_dir, 
            filename_timestamp, 
            metadata_timestamp, 
            scraping_options, 
            extract_content,
            output_filename
        )
    
    # Create filename with timestamp or custom name
    if output_filename:
        # Use custom filename, ensuring it has .json extension
        if not output_filename.endswith('.json'):
            output_filename = f"{output_filename}.json"
        output_file = os.path.join(output_dir, output_filename)
    else:
        # Generate filename with timestamp (current behavior)
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
            
            # Categorize articles if requested (old method - kept for backward compatibility)
            if categorize:
                categorized_articles = {}
                category_counts = {}
                for article in simplified_articles:
                    category = article["category"]
                    if category not in categorized_articles:
                        categorized_articles[category] = []
                        category_counts[category] = 0
                    categorized_articles[category].append(article)
                    category_counts[category] += 1
                
                output_data = {
                    "metadata": {
                        "type": "index",
                        "timestamp": metadata_timestamp,
                        "scraping_options": scraping_options or {},
                        "total_articles": len(articles),
                        "categories": category_counts
                    },
                    "articles": categorized_articles
                }
            else:
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
            # Categorize articles if requested (old method - kept for backward compatibility)
            if categorize:
                categorized_articles = {}
                category_counts = {}
                for article in articles:
                    category = article.metadata.category
                    if category not in categorized_articles:
                        categorized_articles[category] = []
                        category_counts[category] = 0
                    categorized_articles[category].append(article.__dict__)
                    category_counts[category] += 1
                
                output_data = {
                    "metadata": {
                        "type": "index",
                        "timestamp": metadata_timestamp,
                        "scraping_options": scraping_options or {},
                        "total_articles": len(articles),
                        "categories": category_counts
                    },
                    "articles": categorized_articles
                }
            else:
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
        
        logger.info(f"Successfully saved {len(articles)} articles to {output_file}")
        return output_file
    except Exception as e:
        logger.error(f"Error saving to JSON file: {e}")
        raise