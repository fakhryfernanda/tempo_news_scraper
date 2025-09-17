"""Data models for Tempo.co scraper."""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime

@dataclass
class Image:
    """Represents an image in an article."""
    src: str
    alt: str

@dataclass
class ArticleMetadata:
    """Metadata for an article."""
    url: str
    title: str
    category: str
    is_free: bool = True
    publication_date_raw: str = ""
    publication_date: str = ""
    publication_time: str = ""
    timezone: str = ""
    author: str = ""

@dataclass
class Article:
    """Represents a complete article with content."""
    metadata: ArticleMetadata
    content: List[str]
    tags: List[str]
    images: List[Image]

@dataclass
class ScrapingOptions:
    """Options for scraping operations."""
    start_page: int = 1
    end_page: int = 3
    delay: int = 1
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    article_per_page: int = 20
    extract_content: bool = False
    rubric: Optional[str] = None
    use_auth: bool = False
    categorize: bool = False

@dataclass
class ScrapingResult:
    """Result of a scraping operation."""
    articles: List[Article]
    metadata: Dict[str, Any]
    output_file: str