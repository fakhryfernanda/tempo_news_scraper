#!/usr/bin/env python3
"""
Comprehensive unit tests for refactored Tempo.co scraper
"""

import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tempo_scraper.models.article import Article, ArticleMetadata, Image
from tempo_scraper.utils.date_parser import parse_publication_datetime
from tempo_scraper.utils.validators import validate_date_format, validate_date_range
from tempo_scraper.utils.url_builder import build_index_url

def test_date_parsing():
    """Test date parsing functionality"""
    print("Testing date parsing...")
    
    # Test normal case
    result = parse_publication_datetime("12 September 2025 | 15.22 WIB")
    assert result["date"] == "2025-09-12", f"Expected '2025-09-12', got '{result['date']}'"
    assert result["time"] == "15:22:00", f"Expected '15:22:00', got '{result['time']}'"
    assert result["timezone"] == "WIB", f"Expected 'WIB', got '{result['timezone']}'"
    
    # Test edge cases
    result = parse_publication_datetime("")
    assert result["date"] == "", f"Expected empty date, got '{result['date']}'"
    
    result = parse_publication_datetime("invalid format")
    assert result["date"] == "", f"Expected empty date, got '{result['date']}'"
    
    print("✓ Date parsing tests passed")

def test_date_validation():
    """Test date validation functionality"""
    print("Testing date validation...")
    
    # Test valid dates
    assert validate_date_format("2025-09-12", "test") == True
    assert validate_date_format(None, "test") == True
    
    # Test invalid dates
    assert validate_date_format("invalid", "test") == False
    assert validate_date_format("12-09-2025", "test") == False
    
    # Test date range validation
    assert validate_date_range("2025-09-12", "2025-09-15") == True
    assert validate_date_range("2025-09-15", "2025-09-12") == False
    
    print("✓ Date validation tests passed")

def test_url_building():
    """Test URL building functionality"""
    print("Testing URL building...")
    
    # Test basic URL
    url = build_index_url(1)
    assert "page=1" in url, f"Expected page parameter in URL: {url}"
    
    # Test with rubric
    url = build_index_url(1, rubric="politik")
    assert "rubric_slug=politik" in url, f"Expected rubric parameter in URL: {url}"
    
    # Test with dates
    url = build_index_url(1, "2025-09-12", "2025-09-15")
    assert "start_date=2025-09-12" in url, f"Expected start_date parameter in URL: {url}"
    assert "end_date=2025-09-15" in url, f"Expected end_date parameter in URL: {url}"
    
    print("✓ URL building tests passed")

def test_data_models():
    """Test data models functionality"""
    print("Testing data models...")
    
    # Test ArticleMetadata
    metadata = ArticleMetadata(
        url="https://www.tempo.co/test",
        title="Test Article",
        category="test",
        is_free=True
    )
    
    assert metadata.url == "https://www.tempo.co/test"
    assert metadata.title == "Test Article"
    assert metadata.category == "test"
    assert metadata.is_free == True
    
    # Test Image
    image = Image(src="test.jpg", alt="Test Image")
    assert image.src == "test.jpg"
    assert image.alt == "Test Image"
    
    # Test Article
    article = Article(
        metadata=metadata,
        content=["Paragraph 1", "Paragraph 2"],
        tags=["test", "article"],
        images=[image]
    )
    
    assert len(article.content) == 2
    assert len(article.tags) == 2
    assert len(article.images) == 1
    
    print("✓ Data models tests passed")

def main():
    """Run all comprehensive tests"""
    print("Running comprehensive unit tests for refactored Tempo.co scraper")
    print("=" * 60)
    
    try:
        test_date_parsing()
        test_date_validation()
        test_url_building()
        test_data_models()
        print("\n✓ All comprehensive unit tests passed")
        return True
    except Exception as e:
        print(f"\n✗ Comprehensive unit tests failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)