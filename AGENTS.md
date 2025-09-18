# AGENTS.md - Tempo.co Multi-Tool Scraper

## Project Overview

This is a Python-based web scraper for the Indonesian news website tempo.co. The project provides functionality to:
1. Scrape article index pages with various filters
2. Extract full content from individual articles
3. Process articles with automatic content extraction

The project follows Python packaging best practices with a clear separation between the core package and utility modules.

## Project Structure

```
tempo/
├── data/                  # Data files and scraped output
│   └── output/            # Scraped data output directory
├── src/                   # Source code (main package)
│   └── tempo_scraper/     # Main package directory
│       ├── __init__.py
│       ├── __main__.py
│       ├── core/           # Core utilities (config, logging, etc.)
│       ├── extractors/     # Content extraction modules
│       ├── models/         # Data models
│       ├── scrapers/       # Main scraping logic
│       └── utils/          # Utility modules
├── tests/                 # Test files
│   ├── test_comprehensive.py
│   ├── test_integration.py
│   ├── test_article_extractor.py
│   ├── test_content_filtering.py
│   ├── test_non_free_filtering.py
│   ├── run_all_tests.py
│   └── README.md
├── scripts/               # Helper scripts
├── AGENTS.md
├── README.md
└── requirements.txt
```

## Technologies Used

- **Python 3.6+**: Main programming language
- **requests**: HTTP library for making web requests
- **beautifulsoup4**: HTML parsing library
- **lxml**: XML/HTML parser

## Core Package Components

### Main Module (`src/tempo_scraper/main.py`)
- Entry point for the package with command-line argument parsing
- Implements subcommands for different functionalities:
  1. `indeks` - Scrape article index pages
  2. `article` - Extract full article content

### Index Scraper Module (`src/tempo_scraper/indeks_scraper.py`)
- Main functionality for scraping index pages
- Supports filtering by page range, date range, and number of articles per page
- Option to automatically extract full content for each article found
- Skips extraction for non-free articles (`is_free=false`)
- Prevents duplicate JSON exports when running from index scraper

### Article Extractor Module (`src/tempo_scraper/article_extractor.py`)
- Implements functionality for extracting full article content
- Extracts title, authors, publication date, article body, tags, and images
- Automatically filters out ads logo images (`/img/logo-tempo-ads.svg`)
- Automatically filters out "Pilihan Editor:" content from article body

### URL Builder Module (`src/tempo_scraper/url_builder.py`)
- Builds URLs for index page scraping
- Automatically creates 1-day date ranges when only one date is provided

### Validator Module (`src/tempo_scraper/validator.py`)
- Validates and processes input parameters
- Handles date validation and automatic date range creation

### Scraper Module (`src/tempo_scraper/scraper.py`)
- Core scraping functionality for parsing index pages
- Extracts article metadata from index pages
- Identifies free vs non-free articles

### File Handler Module (`src/tempo_scraper/utils/file_handler.py`)
- Handles saving scraped data to JSON files
- Manages output directory creation and file naming
- Implements categorized article saving with separate files per category

### Article Filters Module (`src/tempo_scraper/article_filters.py`)
- Provides additional functionality for listing articles with various filter options
- Contains functions for building index URLs with filters

## Building and Running

### Installation
```bash
pip install -r requirements.txt
```

### Using the Core Package

#### As a Module
```bash
# Scrape index pages
python -m src.tempo_scraper indeks --start-page 1 --end-page 3

# Scrape with date filtering (creates 1-day difference by default)
python -m src.tempo_scraper indeks --start-date 2025-09-10

# Scrape with content extraction (skips non-free articles, no duplicate exports)
python -m src.tempo_scraper indeks --extract-content

# Scrape with categorization (saves articles in separate files per category)
python -m src.tempo_scraper indeks --categorize

# Scrape with categorization and content extraction
python -m src.tempo_scraper indeks --categorize --extract-content

# Extract content from specific article (creates individual JSON file)
python -m src.tempo_scraper article --url https://www.tempo.co/article-url
```

### Command Line Options

#### Index Scraper
```bash
python -m src.tempo_scraper indeks [--start-page START_PAGE] [--end-page END_PAGE]
                          [--delay DELAY] [--start-date START_DATE]
                          [--end-date END_DATE] [--article-per-page ARTICLE_PER_PAGE]
                          [--extract-content] [--categorize]
```

#### Article Extractor
```bash
python -m src.tempo_scraper article --url URL
```

### Running Tests
```bash
# Run all tests
python tests/run_all_tests.py

# Run individual test suites
python tests/test_comprehensive.py
python tests/test_integration.py
python tests/test_article_extractor.py
python tests/test_content_filtering.py
python tests/test_non_free_filtering.py
```

## Development Conventions

1. **Code Structure**: Follows the Python src-layout pattern for package organization
2. **Imports**: Uses relative imports within the package and absolute imports for external dependencies
3. **Error Handling**: Implements proper exception handling for network requests and parsing
4. **Testing**: Comprehensive test suite with unit and integration tests
5. **Documentation**: Clear documentation in code and README files

## Key Features

1. **Automatic Date Range Creation**: When only one date is provided, automatically creates a 1-day difference
2. **Content Filtering**: 
   - Automatically filters out ads logo images (`/img/logo-tempo-ads.svg`)
   - Automatically filters out "Pilihan Editor:" content from article body
3. **Non-Free Article Handling**: Automatically skips extraction for non-free articles (`is_free=false`)
4. **No Duplicate Exports**: When running from index scraper, individual JSON files are not created to prevent duplication
5. **Content Extraction**: Can extract full article content during index scraping
6. **Flexible Filtering**: Support for page range, date range, and article count filtering
7. **JSON Output**: Structured JSON output for easy data processing
8. **Categorized Output**: Articles can be saved in separate files by category
9. **Authentication Support**: Can use REMP session ID for accessing premium content

## Output Files

All output files are saved in the `data/output/` directory:
- JSON files for article index data (when not using categorization)
- Directory with categorized output (when using `--categorize`):
  - Separate JSON files for each article category
  - Metadata file with scraping information
- Individual JSON files for each article's full content (only when using standalone article extractor)

## Limitations with Premium Content Access

Despite using authentication with a valid REMP_SESSION_ID, some premium content may still be inaccessible due to server-side paywalls. In such cases, only article metadata and a preview of the content may be available, with the full article content remaining behind a subscription paywall. This is a limitation of the website's architecture and not an issue with the scraper itself.