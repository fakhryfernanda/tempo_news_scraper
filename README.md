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
- **Authentication support** for accessing premium content (Subscribed users)

## Project Structure

```
tempo/
├── data/
│   └── output/            # Scraped data output directory
├── src/
│   └── tempo_scraper/     # Main package directory
│       ├── __init__.py
│       ├── __main__.py
│       ├── article_extractor.py
│       ├── article_filters.py
│       ├── file_handler.py
│       ├── indeks_scraper.py
│       ├── main.py
│       ├── scraper.py
│       ├── url_builder.py
│       └── validator.py
├── tests/                 # Test files
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
- `--login`: Use authentication for premium content access (default: False)
- `--categorize`: Categorize articles by category in output (default: False)

#### Article Extractor Options
- `--url URL`: URL of the article to extract (required)
- `--login`: Use authentication for premium content access (default: False)

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
- Index scraping results: `articles_{start_page}_{end_page}[_{start_date}_to_{end_date}].json`
- Individual articles: `article_{category}_{article-title}.json` (only when using standalone article extractor)

## Examples

```bash
# Scrape the first page with 5 articles
python -m src.tempo_scraper indeks --start-page 1 --end-page 1 --article-per-page 5

# Scrape articles from September 10, 2025 (automatically creates 1-day range)
python -m src.tempo_scraper indeks --start-date 2025-09-10

# Scrape and extract full content for all articles found (skips non-free articles, no duplicate exports)
python -m src.tempo_scraper indeks --start-page 1 --end-page 1 --extract-content

# Extract content from a specific article (creates individual JSON file)
python -m src.tempo_scraper article --url "https://www.tempo.co/teroka/synchronize-fest-2025-bakal-ada-guruh-gipsy-dan-elvy-sukaesih--2069043"
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

- **indeks_scraper.py**: Main index scraping functionality
- **article_extractor.py**: Article content extraction
- **url_builder.py**: URL construction with intelligent date handling
- **validator.py**: Input validation and processing
- **scraper.py**: Core HTML parsing for index pages
- **file_handler.py**: JSON file saving functionality
- **article_filters.py**: Additional filtering capabilities
- **main.py**: Command-line interface entry point

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

## Article Filtering

The scraper now includes enhanced filtering capabilities:

### Access-Based Filtering
- **Anonymous mode** (default): Only free articles are processed
- **Authenticated mode** (`--login`): All articles (including premium content) are processed

### Content Extraction
- Use `--extract-content` to extract full article content
- When combined with `--login`, premium content is accessible
- Non-free articles are automatically skipped in anonymous mode

### Filter Options
- `--rubric`: Filter articles by rubric/category
- `--start-date` / `--end-date`: Filter articles by date range
- `--article-per-page`: Limit number of articles per page

## Authentication (Premium Content Access)

Subscribed users can access premium content by setting their REMP session ID in a `.env` file:

### Getting Your REMP_SESSION_ID

1. Login to [tempo.co](https://tempo.co) in your browser
2. Open Developer Tools (F12 or Ctrl+Shift+I)
3. Go to the Application/Storage tab
4. Find Cookies for "https://tempo.co"
5. Look for `remp_session_id` cookie
6. Copy the value

### Setting REMP_SESSION_ID

Create a `.env` file in the project root directory with your REMP session ID:

```bash
echo "REMP_SESSION_ID=your-remp-session-id-here" > .env
```

Or manually create a `.env` file with the following content:
```
REMP_SESSION_ID=your-remp-session-id-here
```

### Checking Your Login Status

You can verify if your REMP_SESSION_ID is properly configured:

```bash
# Check .env file and test authentication with tempo.co
python scripts/auth_check.py
```

### Using Authentication

By default, the scraper runs in anonymous mode. To access premium content, use the `--login` flag:

```bash
# Index scraper with authentication
python -m src.tempo_scraper indeks --login

# Article extractor with authentication
python -m src.tempo_scraper article --url https://www.tempo.co/article-url --login
```

The REMP_SESSION_ID will be automatically loaded from the `.env` file when `--login` is used, allowing access to premium content.

**Note**: Session IDs may expire and require periodic renewal.

### Limitations with Premium Content Access

Despite using authentication with a valid REMP_SESSION_ID, some premium content may still be inaccessible due to server-side paywalls. In such cases, only article metadata and a preview of the content may be available, with the full article content remaining behind a subscription paywall. This is a limitation of the website's architecture and not an issue with the scraper itself.

For more details about this limitation, see:
- [AUTH_LIMITATIONS.md](AUTH_LIMITATIONS.md) - Detailed documentation of authentication limitations
- [scripts/auth_limitation_demo.py](scripts/auth_limitation_demo.py) - Script to demonstrate the limitation

## Requirements

- Python 3.6+
- requests
- beautifulsoup4
- lxml

See `requirements.txt` for detailed dependencies.

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