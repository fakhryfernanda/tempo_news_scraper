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

from tempo_scraper.models.article import Article, ArticleMetadata
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
            tags=['politik']
        ),
        Article(
            metadata=ArticleMetadata(
                url='https://www.tempo.co/hukum/article2',
                title='Legal Article 1',
                category='hukum',
                is_free=True
            ),
            content=['Content 2'],
            tags=['hukum']
        ),
        Article(
            metadata=ArticleMetadata(
                url='https://www.tempo.co/politik/article3',
                title='Political Article 2',
                category='politik',
                is_free=True
            ),
            content=['Content 3'],
            tags=['politik']
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
            tags=['politik']
        ),
        Article(
            metadata=ArticleMetadata(
                url='https://www.tempo.co/hukum/article2',
                title='Legal Article 1',
                category='hukum',
                is_free=True
            ),
            content=['Content 2'],
            tags=['hukum']
        ),
        Article(
            metadata=ArticleMetadata(
                url='https://www.tempo.co/politik/article3',
                title='Political Article 2',
                category='politik',
                is_free=True
            ),
            content=['Content 3'],
            tags=['politik']
        ),
        Article(
            metadata=ArticleMetadata(
                url='https://www.tempo.co/olahraga/article4',
                title='Sports Article 1',
                category='olahraga',
                is_free=True
            ),
            content=['Content 4'],
            tags=['olahraga']
        )
    ]
    
    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save articles with categorization enabled
        output_dir = save_articles_to_json(
            articles, 
            temp_dir, 
            is_index_scraping=True,
            scraping_options={"extract_content": False},
            categorize=True
        )
        
        # Check that a directory was returned
        assert os.path.isdir(output_dir), "Expected a directory path when categorization is enabled"
        
        # Read the metadata file
        metadata_file_path = os.path.join(output_dir, "metadata.json")
        with open(metadata_file_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Check metadata
        assert metadata["type"] == "index", "Expected type to be 'index'"
        assert "categories" in metadata, "Expected categories metadata when categorization is enabled"
        category_counts = metadata["categories"]
        assert category_counts["politik"] == 2, f"Expected politik count to be 2, got {category_counts['politik']}"
        assert category_counts["hukum"] == 1, f"Expected hukum count to be 1, got {category_counts['hukum']}"
        assert category_counts["olahraga"] == 1, f"Expected olahraga count to be 1, got {category_counts['olahraga']}"
        
        # Read each category file and collect all articles
        all_categorized_articles = {}
        for category in ["politik", "hukum", "olahraga"]:
            category_file_path = os.path.join(output_dir, f"{category}.json")
            assert os.path.exists(category_file_path), f"Expected category file {category_file_path} to exist"
            
            with open(category_file_path, 'r', encoding='utf-8') as f:
                category_data = json.load(f)
            
            assert category in category_data, f"Expected category key '{category}' in {category_file_path}"
            all_categorized_articles[category] = category_data[category]
        
        # Check categories
        assert "politik" in all_categorized_articles, "Expected 'politik' category"
        assert "hukum" in all_categorized_articles, "Expected 'hukum' category"
        assert "olahraga" in all_categorized_articles, "Expected 'olahraga' category"
        
        # Check article counts per category
        assert len(all_categorized_articles["politik"]) == 2, f"Expected 2 political articles, got {len(all_categorized_articles['politik'])}"
        assert len(all_categorized_articles["hukum"]) == 1, f"Expected 1 legal article, got {len(all_categorized_articles['hukum'])}"
        assert len(all_categorized_articles["olahraga"]) == 1, f"Expected 1 sports article, got {len(all_categorized_articles['olahraga'])}"
        
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
            tags=['politik', 'election']
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
            tags=['hukum', 'court']
        )
    ]
    
    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save articles with categorization enabled and full content
        output_dir = save_articles_to_json(
            articles, 
            temp_dir, 
            is_index_scraping=True,
            scraping_options={"extract_content": True},
            categorize=True
        )
        
        # Check that a directory was returned
        assert os.path.isdir(output_dir), "Expected a directory path when categorization is enabled"
        
        # Read the metadata file
        metadata_file_path = os.path.join(output_dir, "metadata.json")
        with open(metadata_file_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Check metadata
        assert metadata["type"] == "index", "Expected type to be 'index'"
        assert "categories" in metadata, "Expected categories metadata when categorization is enabled"
        category_counts = metadata["categories"]
        assert category_counts["politik"] == 1, f"Expected politik count to be 1, got {category_counts['politik']}"
        assert category_counts["hukum"] == 1, f"Expected hukum count to be 1, got {category_counts['hukum']}"
        
        # Read each category file and collect all articles
        all_categorized_articles = {}
        for category in ["politik", "hukum"]:
            category_file_path = os.path.join(output_dir, f"{category}.json")
            assert os.path.exists(category_file_path), f"Expected category file {category_file_path} to exist"
            
            with open(category_file_path, 'r', encoding='utf-8') as f:
                category_data = json.load(f)
            
            assert category in category_data, f"Expected category key '{category}' in {category_file_path}"
            all_categorized_articles[category] = category_data[category]
        
        # Check categories
        assert "politik" in all_categorized_articles, "Expected 'politik' category"
        assert "hukum" in all_categorized_articles, "Expected 'hukum' category"
        
        # Check article counts per category
        assert len(all_categorized_articles["politik"]) == 1, f"Expected 1 political article, got {len(all_categorized_articles['politik'])}"
        assert len(all_categorized_articles["hukum"]) == 1, f"Expected 1 legal article, got {len(all_categorized_articles['hukum'])}"
        
        # Check that full content is preserved
        politik_article = all_categorized_articles["politik"][0]
        assert "content" in politik_article, "Expected content in political article"
        assert len(politik_article["content"]) == 2, "Expected 2 paragraphs in political article"
        
        hukum_article = all_categorized_articles["hukum"][0]
        assert "content" in hukum_article, "Expected content in legal article"
        assert len(hukum_article["content"]) == 1, "Expected 1 paragraph in legal article"
        
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