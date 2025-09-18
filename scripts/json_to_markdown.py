#!/usr/bin/env python3
"""
JSON to Markdown converter for Tempo.co scraped articles.

This script converts categorized JSON article files to individual Markdown files
with simplified metadata format and clean directory structure.

Features:
- Converts articles to Markdown format with proper metadata
- Organizes output by category in separate directories
- Sanitizes filenames for cross-platform compatibility
- Adds tempo.co domain to premium article URLs
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any


def sanitize_filename(title: str) -> str:
    """
    Create a filesystem-safe filename from article title.
    
    Args:
        title: Article title
        
    Returns:
        Sanitized filename without extension
    """
    # Remove " | tempo.co" suffix if present
    if " | tempo.co" in title:
        title = title.split(" | tempo.co")[0]
    
    # Keep alphanumeric characters, spaces, and some punctuation
    # Replace other characters with spaces
    filename = re.sub(r'[^a-zA-Z0-9\s\-_.]', ' ', title)
    
    # Replace multiple spaces/hyphens with single hyphen
    filename = re.sub(r'[\s\-_]+', '-', filename)
    
    # Remove leading/trailing hyphens
    filename = filename.strip('-')
    
    # Limit length to prevent filesystem issues
    filename = filename[:100] if len(filename) > 100 else filename
    
    # Ensure we have a valid filename
    if not filename or filename == "":
        filename = "untitled-article"
    
    return filename.lower()


def format_metadata(article: Dict[str, Any]) -> str:
    """
    Format article metadata in simplified key-value format.
    
    Args:
        article: Article data dictionary
        
    Returns:
        Formatted metadata string
    """
    metadata = article.get("metadata", {})
    
    # Extract metadata fields
    category = metadata.get("category", "")
    publication_date = metadata.get("publication_date", "")
    publication_time = metadata.get("publication_time", "")
    is_free = metadata.get("is_free", True)
    tags = article.get("tags", [])
    url = metadata.get("url", "")
    
    # For premium articles, add tempo.co domain if not already present
    if not is_free and url and not url.startswith("http"):
        url = "https://tempo.co" + url
    
    # Format date and time
    if publication_date and publication_time:
        # Convert YYYY-MM-DD to YYYY/MM/DD
        formatted_date = publication_date.replace("-", "/")
        published_at = f"{formatted_date} {publication_time}"
    else:
        published_at = ""
    
    # Format tags with #free or #premium first
    tag_list = []
    if is_free:
        tag_list.append("#free")
    else:
        tag_list.append("#premium")
    
    # Add article tags
    for tag in tags:
        # Clean and validate tag
        if isinstance(tag, str) and tag.strip():
            # Remove any non-alphanumeric characters except hyphens and underscores
            clean_tag = re.sub(r'[^a-zA-Z0-9_-]', '', tag)
            # Ensure it's not empty after cleaning
            if clean_tag:
                tag_list.append(f"#{clean_tag}")
    
    tags_str = " ".join(tag_list)
    
    # Format metadata without quotes
    metadata_lines = [
        f"Category: {category}",
        f"Published at: {published_at}",
        f"Tags: {tags_str}",
        f"URL: {url}"
    ]
    
    return "\n".join(metadata_lines)


def create_markdown_content(article: Dict[str, Any]) -> str:
    """
    Create complete Markdown content for an article.
    
    Args:
        article: Article data dictionary
        
    Returns:
        Complete Markdown content with proper line breaks
    """
    metadata = format_metadata(article)
    
    # Extract title and clean it
    title = article.get("metadata", {}).get("title", "Untitled Article")
    if " | tempo.co" in title:
        clean_title = title.split(" | tempo.co")[0]
    else:
        clean_title = title
    
    # Get content paragraphs
    content_paragraphs = article.get("content", [])
    
    # Build Markdown content as a list of lines
    md_content = []
    md_content.append(metadata)
    md_content.append("")  # Blank line after metadata
    md_content.append(f"# {clean_title}")
    md_content.append("")  # Blank line after title
    
    # Add content paragraphs as separate lines (one paragraph per line)
    for paragraph in content_paragraphs:
        if paragraph.strip():  # Only add non-empty paragraphs
            md_content.append(paragraph.strip())
            md_content.append("")  # Add blank line after each paragraph
    
    # Join all lines with actual newlines (not \n characters)
    return "\n".join(md_content)


def process_json_file(json_file_path: Path, output_dir: Path) -> int:
    """
    Process a single JSON file and convert articles to Markdown.
    
    Args:
        json_file_path: Path to JSON file
        output_dir: Output directory for Markdown files
        
    Returns:
        Number of articles processed
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {json_file_path}: {e}")
        return 0
    
    # Get category name from filename (without .json extension)
    category = json_file_path.stem
    
    # Create category directory
    category_dir = output_dir / category
    category_dir.mkdir(parents=True, exist_ok=True)
    
    # Get articles from the category key
    articles = data.get(category, [])
    
    if not isinstance(articles, list):
        print(f"Warning: Expected list of articles in {category}, got {type(articles)}")
        return 0
    
    article_count = 0
    for i, article in enumerate(articles):
        try:
            # Create Markdown content
            md_content = create_markdown_content(article)
            
            # Generate filename
            title = article.get("metadata", {}).get("title", f"article-{i}")
            filename = sanitize_filename(title) + ".md"
            
            # Handle duplicate filenames
            md_file_path = category_dir / filename
            counter = 1
            original_filename = filename
            while md_file_path.exists():
                # Extract name without extension
                name_without_ext = original_filename[:-3]  # Remove .md
                # Create new filename with counter
                filename = f"{name_without_ext}-{counter}.md"
                md_file_path = category_dir / filename
                counter += 1
            
            # Write to file
            with open(md_file_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            article_count += 1
            print(f"  Created: {md_file_path.name}")
            
        except Exception as e:
            print(f"  Error processing article {i} in {category}: {e}")
            continue
    
    return article_count


def main():
    """Main function to process JSON files and convert to Markdown.
    
    Features:
    - Converts articles to Markdown format with proper metadata
    - Organizes output by category in separate directories
    - Sanitizes filenames for cross-platform compatibility
    - Adds tempo.co domain to premium article URLs
    """
    if len(sys.argv) < 3:
        print("Usage: python json_to_markdown.py <input_directory> <output_directory>")
        print("Example: python json_to_markdown.py data/saved/berita_16_september_2025 data/output/markdown")
        sys.exit(1)
    
    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    
    if not input_dir.exists():
        print(f"Error: Input directory {input_dir} does not exist")
        sys.exit(1)
    
    if not input_dir.is_dir():
        print(f"Error: {input_dir} is not a directory")
        sys.exit(1)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Converting JSON articles to Markdown...")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Process all JSON files except metadata.json
    json_files = list(input_dir.glob("*.json"))
    json_files = [f for f in json_files if f.name != "metadata.json"]
    
    if not json_files:
        print("No JSON files found to process (excluding metadata.json)")
        return
    
    total_articles = 0
    for json_file in json_files:
        print(f"Processing {json_file.name}...")
        article_count = process_json_file(json_file, output_dir)
        total_articles += article_count
        print(f"  Converted {article_count} articles")
        print()
    
    print(f"Conversion complete!")
    print(f"Total articles converted: {total_articles}")
    print(f"Output files saved to: {output_dir}")


if __name__ == "__main__":
    main()