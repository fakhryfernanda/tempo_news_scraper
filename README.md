# Tempo.co Scraper

A Python-based web scraper for the Indonesian news website [tempo.co](https://www.tempo.co). This tool allows you to scrape article index pages and extract full content from individual articles.

## Features

- Scrape article index pages with pagination support
- Filter articles by date range (with automatic 1-day difference creation)
- Filter articles by rubric/category
- Limit number of articles per page
- Extract full content from individual articles
- Automatically extract content for all articles found in index pages
- Filter out ads logo images (`/img/logo-tempo-ads.svg`)
- Filter out "Pilihan Editor:" content from article body
- Skip extraction for non-free articles (`is_free=false`)
- Prevent duplicate JSON exports when running from index scraper
- Save data in structured JSON format
- Categorize articles by category with separate output files per category

## Project Structure

```
tempo/
├── data/
│   └── output/            # Scraped data output directory
├── src/
│   └── tempo_scraper/     # Main package directory
│       ├── __init__.py
│       ├── __main__.py
│       ├── core/           # Core utilities (config, logging, etc.)
│       ├── extractors/     # Content extraction modules
│       ├── models/         # Data models
│       ├── scrapers/       # Main scraping logic
│       └── utils/          # Utility modules
├── tests/                 # Test files
├── scripts/               # Helper scripts
│   ├── json_to_markdown.py # JSON to Markdown converter
│   └── run_index_scraper.sh
├── AGENTS.md
├── README.md
└── requirements.txt
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd tempo-scraper
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

The scraper provides two main subcommands:

#### 1. Index Scraper (`indeks`)

Scrape article index pages from tempo.co:

```bash
# Basic usage - scrape pages 1-3
python -m src.tempo_scraper indeks

# Scrape specific page range
python -m src.tempo_scraper indeks --start-page 1 --end-page 5

# Scrape with delay between requests
python -m src.tempo_scraper indeks --start-page 1 --end-page 3 --delay 2

# Scrape with date filtering (creates 1-day difference by default)
python -m src.tempo_scraper indeks --start-date 2025-09-10

# Scrape with both start and end dates
python -m src.tempo_scraper indeks --start-date 2025-09-10 --end-date 2025-09-15

# Filter by rubric
python -m src.tempo_scraper indeks --rubric politik

# Note: Rubric and date filters are mutually exclusive. If both are provided, rubric takes precedence.

# Limit articles per page
python -m src.tempo_scraper indeks --article-per-page 10

# Extract full content for each article found
python -m src.tempo_scraper indeks --extract-content
```

#### 2. Article Extractor (`article`)

Extract full content from a specific article:

```bash
python -m src.tempo_scraper article --url https://www.tempo.co/article-url
```

### Command Line Options

#### Index Scraper Options
- `--start-page START_PAGE`: Starting page number (default: 1)
- `--end-page END_PAGE`: Ending page number (default: 3)
- `--delay DELAY`: Delay between requests in seconds (default: 1)
- `--start-date START_DATE`: Start date in YYYY-MM-DD format (default: None)
- `--end-date END_DATE`: End date in YYYY-MM-DD format (default: None)
- `--article-per-page ARTICLE_PER_PAGE`: Number of articles per page (default: 20)
- `--extract-content`: Extract full content for each article (default: False)
- `--rubric RUBRIC`: Filter articles by rubric (default: None)
- `--categorize`: Categorize articles by category in separate files (default: False)
- `--output-name OUTPUT_NAME`: Custom output name (without extension) (default: auto-generated)

#### Article Extractor Options
- `--url URL`: URL of the article to extract (required)
- `--output-name OUTPUT_NAME`: Custom output name (without extension) (default: auto-generated)

### Date Handling

The scraper has intelligent date handling:
- When only `--start-date` is provided, it automatically creates a 1-day range (start_date to start_date + 1 day)
- When only `--end-date` is provided, it automatically creates a 1-day range (end_date - 1 day to end_date)
- When both dates are provided, it uses the specified range

### Content Filtering

The scraper automatically filters out:
- Ads logo images (`/img/logo-tempo-ads.svg`)
- "Pilihan Editor:" content from article body
- Non-free articles (`is_free=false`) during content extraction

### Output

All output files are saved in the `data/output/` directory:
- Index scraping results: `indeks_{timestamp}.json` (when not using categorization)
- Index scraping results with custom name: `{custom_name}.json` (when `--output-name` is provided)
- Index scraping results with categorization: `indeks_{timestamp}/` directory containing:
  - `{category}.json` files for each article category
  - `metadata.json` with scraping information
- Index scraping results with categorization and custom name: `{custom_name}/` directory containing:
  - `{category}.json` files for each article category
  - `metadata.json` with scraping information
- Individual articles: `article_{timestamp}.json` (only when using standalone article extractor)
- Individual articles with custom name: `{custom_name}.json` (when `--output-name` is provided for article extraction)

## Examples

```bash
# Scrape the first page with 5 articles
python -m src.tempo_scraper indeks --start-page 1 --end-page 1 --article-per-page 5

# Scrape articles from September 10, 2025 (automatically creates 1-day range)
python -m src.tempo_scraper indeks --start-date 2025-09-10

# Scrape and extract full content for all articles found (skips non-free articles, no duplicate exports)
python -m src.tempo_scraper indeks --start-page 1 --end-page 1 --extract-content

# Scrape and categorize articles by category in separate files
python -m src.tempo_scraper indeks --start-page 1 --end-page 3 --categorize

# Scrape and categorize articles with full content extraction
python -m src.tempo_scraper indeks --start-page 1 --end-page 3 --categorize --extract-content

# Scrape with a custom output name
python -m src.tempo_scraper indeks --start-page 1 --end-page 1 --output-name my_scraped_articles

# Extract content from a specific article with a custom output name
python -m src.tempo_scraper article --url "https://www.tempo.co/teroka/synchronize-fest-2025-bakal-ada-guruh-gipsy-dan-elvy-sukaesih--2069043" --output-name my_article

# Count total articles and pages without extracting content (much faster)
./scripts/count_articles.sh
```

## Testing

The project includes a comprehensive test suite:

```bash
# Run all tests
python tests/run_all_tests.py

# Run individual test suites
python tests/test_comprehensive.py      # Unit tests
python tests/test_integration.py       # Integration tests
python tests/test_article_extractor.py # Article extractor tests
python tests/test_content_filtering.py # Content filtering tests
python tests/test_non_free_filtering.py # Non-free article filtering tests
```

## Development

### Code Structure

- **main.py**: Command-line interface entry point
- **core/**: Core utilities (config, logging, etc.)
- **extractors/**: Content extraction modules
- **models/**: Data models
- **scrapers/**: Main scraping logic
- **utils/**: Utility modules

### Key Features

1. **Automatic Date Range Creation**: When only one date is provided, the system automatically creates a 1-day difference
2. **Content Filtering**: 
   - Ads logo images (`/img/logo-tempo-ads.svg`) are automatically filtered out
   - "Pilihan Editor:" content is automatically filtered out
   - Non-free articles are automatically skipped during content extraction
3. **No Duplicate Exports**: When running from index scraper, individual JSON files are not created to prevent duplication
4. **Content Extraction**: Option to automatically extract full content during index scraping
5. **Flexible Filtering**: Support for page range, date range, and article count filtering
6. **Structured Output**: Data saved in consistent JSON format for easy processing
7. **Categorized Output**: Articles can be saved in separate files by category

## Article Filtering

The scraper now includes enhanced filtering capabilities:

### Access-Based Filtering
- **Anonymous mode** (default): Only free articles are processed

### Content Extraction
- Use `--extract-content` to extract full article content
- Non-free articles are automatically skipped in anonymous mode

### Filter Options
- `--rubric`: Filter articles by rubric/category
- `--start-date` / `--end-date`: Filter articles by date range
- `--article-per-page`: Limit number of articles per page

## Usage Examples

### Basic Index Scraping



## Requirements

- Python 3.6+
- requests
- beautifulsoup4
- lxml

See `requirements.txt` for detailed dependencies.

## JSON to Markdown Converter

The project includes a utility script to convert scraped JSON articles to Markdown format:

```bash
python scripts/json_to_markdown.py <input_directory> <output_directory>
```

### Features

- Converts articles to Markdown format with proper metadata
- Organizes output by category in separate directories
- Sanitizes filenames for cross-platform compatibility
- Adds tempo.co domain to premium article URLs
- Handles duplicate filenames by adding counters
- Preserves article content formatting with proper spacing

### Example

```bash
python scripts/json_to_markdown.py data/saved/berita_16_september_2025 data/output/markdown
```

This will convert all JSON files in the input directory to Markdown files in the output directory, organized by category.

### Special Handling

- Premium articles (where `is_free` is `false`) have the tempo.co domain prepended to their URLs
- Free articles (where `is_free` is `true`) retain their original URLs
- Filenames are sanitized to be filesystem-safe
- Duplicate filenames are handled by adding counters (e.g., `article.md`, `article-1.md`, `article-2.md`)

## Valid Rubrics

The following rubrics are available for use with the `--rubric` parameter (in lowercase with dashes for multi-word rubrics):

- politik
- hukum
- ekonomi
- lingkungan
- wawancara
- sains
- investigasi
- cekfakta
- kolom
- hiburan
- internasional
- arsip
- otomotif
- olahraga
- sepakbola
- digital
- gaya-hidup
- teroka
- prelude
- tokoh
- video
- foto
- data
- infografik
- pemilu
- newsletter
- info-tempo
- ramadan

## License

This project is licensed under the MIT License - see the LICENSE file for details.