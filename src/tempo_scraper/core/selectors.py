"""HTML selectors configuration for Tempo.co scraper.

This module centralizes all HTML selectors and attributes used by the scraper,
making it easy to update when the website structure changes.
"""

# CSS Selectors for Index Pages
INDEX_SELECTORS = {
    # Main container for article listings
    "article_list_container": "flex flex-col divide-y divide-neutral-500",
    
    # Article elements within the container
    "article_item": "div",  # Direct child divs of the container
    "article_figure": "figure",
    "article_figcaption": "figcaption",
    "article_paragraph": "p",
    "article_link": "a",
    
    # Premium article indicator
    "premium_indicator": "inline-flex bg-primary-main p-[1.7px] rounded-[1px]"
}

# CSS Selectors for Article Pages
ARTICLE_SELECTORS = {
    # Main article container
    "article_container": "grow space-y-6 overflow-x-clip z-10",
    
    # Metadata selectors
    "title": "title",
    "published_time_meta": "article:published_time",
    "publish_date_meta": "publish-date",
    "author_meta": "author",
    
    # Content selectors
    "content_wrapper": "content-wrapper",
    "content_paragraph": "p",
    "editor_pick_indicator": "Pilihan Editor:",
    
    # Tags and images
    "tags_container": "article-tags",
    "tag_link": "a",
    "image": "img",
    
    # Ads logo to filter out
    "ads_logo": "/img/logo-tempo-ads.svg",
    
    # Premium content indicators
    "premium_indicator": "inline-flex bg-primary-main p-[1.7px] rounded-[1px]"
}

# HTTP Headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Base URL
BASE_URL = "https://tempo.co/indeks"