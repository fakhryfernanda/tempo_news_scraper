"""Main module for Tempo.co scraper."""

import argparse
import sys
import time
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .scrapers.index_scraper import scrape_index_page
from .scrapers.article_filters import filter_articles_by_access, extract_content_for_articles
from .extractors.article_extractor import extract_article_content
from .utils.url_builder import build_index_url
from .utils.validators import validate_date_format, validate_date_range, validate_page_range, process_dates
from .utils.file_handler import save_articles_to_json
from .models.article import Article, ArticleMetadata, ScrapingOptions
from .core.logging import logger

def scrape_index_pages(options: ScrapingOptions) -> str:
    """
    Scrape index pages with the given options.
    
    Args:
        options: Scraping options
        
    Returns:
        Path to the saved output file
    """
    # Process and validate dates
    options.start_date, options.end_date = process_dates(options.start_date, options.end_date)
    
    # Validate date range
    if not validate_date_range(options.start_date, options.end_date):
        sys.exit(1)
    
    # Collect all articles
    all_articles = []
    
    for page in range(options.start_page, options.end_page + 1):
        # Construct URL
        url = build_index_url(page, options.start_date, options.end_date, options.rubric)
        
        # Scrape the page
        articles = scrape_index_page(url, page, options.article_per_page)
        
        # Filter articles based on access rights
        filtered_articles = filter_articles_by_access(articles)
        
        # If extract_content is True, extract full content for each article
        if options.extract_content:
            articles_with_content = extract_content_for_articles(filtered_articles)
            all_articles.extend(articles_with_content)
        else:
            # Convert ArticleMetadata to Article objects (without content)
            articles_as_objects = [
                Article(
                    metadata=meta,
                    content=[],
                    tags=[]
                ) for meta in filtered_articles
            ]
            all_articles.extend(articles_as_objects)
        
        # Add delay between requests (except for the last page)
        if page < options.end_page:
            logger.info(f"Waiting {options.delay} seconds before next request...")
            time.sleep(options.delay)
    
    # Prepare scraping options for metadata
    scraping_options = {
        "extract_content": options.extract_content,
        "start_page": options.start_page,
        "end_page": options.end_page,
        "start_date": options.start_date or "",
        "end_date": options.end_date or "",
        "rubric": options.rubric or "",
        "article_per_page": options.article_per_page,
        "categorize": options.categorize
    }
    
    # Save articles to JSON file
    output_dir = "data/output"
    output_file = save_articles_to_json(
        all_articles, 
        output_dir, 
        is_index_scraping=True,
        scraping_options=scraping_options,
        categorize=options.categorize,
        output_filename=options.output_name
    )
    
    return output_file

def extract_single_article(url: str, output_name: Optional[str] = None) -> str:
    """
    Extract content from a single article.
    
    Args:
        url: URL of the article to extract
        output_name: Custom output name (without extension) (default: None)
        
    Returns:
        Path to the saved output file
    """
    # Extract article content
    article = extract_article_content(url)
    
    if not article:
        logger.error("Failed to extract article content")
        sys.exit(1)
    
    # Save to JSON file
    output_dir = "data/output"
    output_file = save_articles_to_json(
        [article], 
        output_dir, 
        is_index_scraping=False,
        output_filename=output_name
    )
    
    return output_file

def main():
    """Main entry point for the scraper."""
    parser = argparse.ArgumentParser(description="Tempo.co Scraper")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Subparser for index scraper
    index_parser = subparsers.add_parser('indeks', help='Scrape article index pages')
    
    # Add arguments for index scraper
    index_parser.add_argument("--start-page", type=int, default=1, help="Starting page number (default: 1)")
    index_parser.add_argument("--end-page", type=int, default=3, help="Ending page number (default: 3)")
    index_parser.add_argument("--delay", type=int, default=1, help="Delay between requests in seconds (default: 1)")
    index_parser.add_argument("--start-date", help="Start date in YYYY-MM-DD format (default: None)")
    index_parser.add_argument("--end-date", help="End date in YYYY-MM-DD format (default: None)")
    index_parser.add_argument("--article-per-page", type=int, default=20, help="Number of articles per page (default: 20)")
    index_parser.add_argument("--extract-content", action="store_true", help="Extract full content for each article (default: False)")
    index_parser.add_argument("--rubric", help="Rubric to filter by (default: None)")
    index_parser.add_argument("--categorize", action="store_true", help="Categorize articles by category (default: False)")
    index_parser.add_argument("--output-name", help="Custom output name (without extension) (default: auto-generated)")
    
    # Subparser for article extractor
    article_parser = subparsers.add_parser('article', help='Extract content from a single article')
    article_parser.add_argument("--url", type=str, required=True, help="URL of the article to extract")
    article_parser.add_argument("--output-name", help="Custom output name (without extension) (default: auto-generated)")
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    if args.command == 'indeks':
        # Validate date formats
        if not validate_date_format(args.start_date, "start-date"):
            sys.exit(1)
        
        if not validate_date_format(args.end_date, "end-date"):
            sys.exit(1)
        
        # Validate page range
        if not validate_page_range(args.start_page, args.end_page):
            sys.exit(1)
        
        # Create scraping options
        options = ScrapingOptions(
            start_page=args.start_page,
            end_page=args.end_page,
            delay=args.delay,
            start_date=args.start_date,
            end_date=args.end_date,
            article_per_page=args.article_per_page,
            extract_content=args.extract_content,
            rubric=args.rubric,
            categorize=args.categorize,
            output_name=args.output_name
        )
        
        # Run index scraper
        output_file = scrape_index_pages(options)
        logger.info(f"Index scraping completed. Output saved to: {output_file}")
        
    elif args.command == 'article':
        # Run article extractor
        output_file = extract_single_article(args.url, args.output_name)
        logger.info(f"Article extraction completed. Output saved to: {output_file}")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()