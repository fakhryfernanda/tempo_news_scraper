# Tempo.co Scraper Test Suite

This directory contains comprehensive tests for the Tempo.co scraper application.

## Test Structure

1. **test_comprehensive.py** - Unit tests for core functionality including URL building and date processing
2. **test_integration.py** - Integration tests for the command-line interface
3. **test_article_extractor.py** - Unit tests for the article extractor module
4. **test_logo_filtering.py** - Specific tests for logo image filtering
5. **run_all_tests.py** - Master script to run all test suites

## Running Tests

### Run All Tests
```bash
cd /home/fakhry/dev/scraper/tempo
python tests/run_all_tests.py
```

### Run Individual Test Suites
```bash
# Run comprehensive unit tests
python tests/test_comprehensive.py

# Run integration tests
python tests/test_integration.py

# Run article extractor unit tests
python tests/test_article_extractor.py

# Run logo filtering verification
python tests/test_logo_filtering.py
```

## Test Coverage

The test suite covers:

- ✅ URL building with various parameters
- ✅ Date processing with automatic 1-day difference creation
- ✅ Command-line interface functionality
- ✅ Article extraction from Tempo.co
- ✅ Logo image filtering (`/img/logo-tempo-ads.svg`)
- ✅ File saving and output generation
- ✅ Error handling and edge cases

## Test Results

All tests are currently passing, ensuring the scraper works correctly with:
- Proper date range handling (1-day difference by default)
- Logo image filtering
- Content extraction
- File output generation
- Command-line argument parsing