#!/usr/bin/env python3
"""
Unit tests for the categorization feature in Tempo.co scraper
"""

import sys
import os
import json
import tempfile
import glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tempo_scraper.models.article import Article, ArticleMetadata, Image
from tempo_scraper.utils.file_handler import save_articles_to_json

def test_categorization_disabled():
    """Test that categorization is disabled by default and produces flat structure"""
    print("Testing categorization disabled (default behavior)...")
    
    # Create mock articles with different categories
    articles = [
        Article(
            metadata=ArticleMetadata(
                url='https://www.tempo.co/politik/article1',
                title='Political Article 1',
                category='politik',
                is_free=True
            ),
            content=['Content 1'],
            tags=['politik'],
            images=[]
        ),
        Article(
            metadata=ArticleMetadata(
                url='https://www.tempo.co/hukum/article2',
                title='Legal Article 1',
                category='hukum',
                is_free=True
            ),
            content=['Content 2'],
            tags=['hukum'],
            images=[]
        ),
        Article(
            metadata=ArticleMetadata(
                url='https://www.tempo.co/politik/article3',
                title='Political Article 2',
                category='politik',
                is_free=True
            ),
            content=['Content 3'],
            tags=['politik'],
            images=[]
        )
    ]
    
    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save articles with categorization disabled (default)
        output_file = save_articles_to_json(
            articles, 
            temp_dir, 
            is_index_scraping=True,
            scraping_options={"extract_content": False}
        )
        
        # Read the output file
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check that articles are in flat structure
        assert "articles" in data, "Expected 'articles' key in output"
        assert isinstance(data["articles"], list), "Expected articles to be a list when categorization is disabled"
        assert len(data["articles"]) == 3, f"Expected 3 articles, got {len(data['articles'])}"
        
        # Check that there's no categories metadata when categorization is disabled
        assert "categories" not in data["metadata"], "Expected no categories metadata when categorization is disabled"
        
        print("✓ Categorization disabled test passed")
        
def test_categorization_enabled():
    """Test that categorization works correctly when enabled"""
    print("Testing categorization enabled...")
    
    # Create mock articles with different categories
    articles = [
        Article(
            metadata=ArticleMetadata(
                url='https://www.tempo.co/politik/article1',
                title='Political Article 1',
                category='politik',
                is_free=True
            ),
            content=['Content 1'],
            tags=['politik'],
            images=[]
        ),
        Article(
            metadata=ArticleMetadata(
                url='https://www.tempo.co/hukum/article2',
                title='Legal Article 1',
                category='hukum',
                is_free=True
            ),
            content=['Content 2'],
            tags=['hukum'],
            images=[]
        ),
        Article(
            metadata=ArticleMetadata(
                url='https://www.tempo.co/politik/article3',
                title='Political Article 2',
                category='politik',
                is_free=True
            ),
            content=['Content 3'],
            tags=['politik'],
            images=[]
        ),
        Article(
            metadata=ArticleMetadata(
                url='https://www.tempo.co/olahraga/article4',
                title='Sports Article 1',
                category='olahraga',
                is_free=True
            ),
            content=['Content 4'],
            tags=['olahraga'],
            images=[]
        )
    ]
    
    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save articles with categorization enabled
        output_file = save_articles_to_json(
            articles, 
            temp_dir, 
            is_index_scraping=True,
            scraping_options={"extract_content": False},
            categorize=True
        )
        
        # Read the output file
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check that articles are in categorized structure
        assert "articles" in data, "Expected 'articles' key in output"
        assert isinstance(data["articles"], dict), "Expected articles to be a dict when categorization is enabled"
        
        # Check categories
        categories = data["articles"]
        assert "politik" in categories, "Expected 'politik' category"
        assert "hukum" in categories, "Expected 'hukum' category"
        assert "olahraga" in categories, "Expected 'olahraga' category"
        
        # Check article counts per category
        assert len(categories["politik"]) == 2, f"Expected 2 political articles, got {len(categories['politik'])}"
        assert len(categories["hukum"]) == 1, f"Expected 1 legal article, got {len(categories['hukum'])}"
        assert len(categories["olahraga"]) == 1, f"Expected 1 sports article, got {len(categories['olahraga'])}"
        
        # Check category counts in metadata
        assert "categories" in data["metadata"], "Expected categories metadata when categorization is enabled"
        category_counts = data["metadata"]["categories"]
        assert category_counts["politik"] == 2, f"Expected politik count to be 2, got {category_counts['politik']}"
        assert category_counts["hukum"] == 1, f"Expected hukum count to be 1, got {category_counts['hukum']}"
        assert category_counts["olahraga"] == 1, f"Expected olahraga count to be 1, got {category_counts['olahraga']}"
        
        print("✓ Categorization enabled test passed")

def test_categorization_with_full_content():
    """Test that categorization works correctly with full article content"""
    print("Testing categorization with full content...")
    
    # Create mock articles with full content
    articles = [
        Article(
            metadata=ArticleMetadata(
                url='https://www.tempo.co/politik/article1',
                title='Political Article 1',
                category='politik',
                is_free=True,
                publication_date='2025-09-12'
            ),
            content=['Paragraph 1', 'Paragraph 2'],
            tags=['politik', 'election'],
            images=[Image(src='image1.jpg', alt='Image 1')]
        ),
        Article(
            metadata=ArticleMetadata(
                url='https://www.tempo.co/hukum/article2',
                title='Legal Article 1',
                category='hukum',
                is_free=True,
                publication_date='2025-09-13'
            ),
            content=['Legal content paragraph 1'],
            tags=['hukum', 'court'],
            images=[Image(src='image2.jpg', alt='Image 2')]
        )
    ]
    
    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save articles with categorization enabled and full content
        output_file = save_articles_to_json(
            articles, 
            temp_dir, 
            is_index_scraping=True,
            scraping_options={"extract_content": True},
            categorize=True
        )
        
        # Read the output file
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check that articles are in categorized structure
        assert "articles" in data, "Expected 'articles' key in output"
        assert isinstance(data["articles"], dict), "Expected articles to be a dict when categorization is enabled"
        
        # Check categories
        categories = data["articles"]
        assert "politik" in categories, "Expected 'politik' category"
        assert "hukum" in categories, "Expected 'hukum' category"
        
        # Check article counts per category
        assert len(categories["politik"]) == 1, f"Expected 1 political article, got {len(categories['politik'])}"
        assert len(categories["hukum"]) == 1, f"Expected 1 legal article, got {len(categories['hukum'])}"
        
        # Check that full content is preserved
        politik_article = categories["politik"][0]
        assert "content" in politik_article, "Expected content in political article"
        assert len(politik_article["content"]) == 2, "Expected 2 paragraphs in political article"
        
        hukum_article = categories["hukum"][0]
        assert "content" in hukum_article, "Expected content in legal article"
        assert len(hukum_article["content"]) == 1, "Expected 1 paragraph in legal article"
        
        # Check category counts in metadata
        assert "categories" in data["metadata"], "Expected categories metadata when categorization is enabled"
        category_counts = data["metadata"]["categories"]
        assert category_counts["politik"] == 1, f"Expected politik count to be 1, got {category_counts['politik']}"
        assert category_counts["hukum"] == 1, f"Expected hukum count to be 1, got {category_counts['hukum']}"
        
        print("✓ Categorization with full content test passed")

def main():
    """Run all categorization tests"""
    print("Running categorization feature tests for Tempo.co scraper")
    print("=" * 60)
    
    try:
        test_categorization_disabled()
        test_categorization_enabled()
        test_categorization_with_full_content()
        print("\n✓ All categorization tests passed")
        return True
    except Exception as e:
        print(f"\n✗ Categorization tests failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)