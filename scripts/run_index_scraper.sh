# Simple script to run the Tempo.co index scraper with all parameters
# Example: ./run_index_scraper.sh

# Multi-line version showing all parameters with default values
# Uncomment the lines below to add additional parameters

python -m src.tempo_scraper indeks \
  --start-page 1 \
  --end-page 25 \
  --delay 1 \
  --start-date 2025-09-16 \
  --end-date 2025-09-17 \
  --extract-content \
  --categorize
  # --rubric politik \
  # --article-per-page 20

# Available parameters for the indeks command:
# --start-page N        Starting page number (default: 1)
# --end-page N          Ending page number (default: 3)
# --delay N             Delay between requests in seconds (default: 1)
# --start-date YYYY-MM-DD Start date (default: None)
# --end-date YYYY-MM-DD   End date (default: None)
# --article-per-page N  Number of articles per page (default: 20)
# --extract-content     Extract full content for each article (default: False)
# --rubric RUBRIC       Rubric to filter by (default: None)
# --categorize          Categorize articles by category in separate files (default: False)

# Valid rubrics on tempo.co (in lowercase with dashes for multi-word rubrics):
# politik
# hukum
# ekonomi
# lingkungan
# wawancara
# sains
# investigasi
# cekfakta
# kolom
# hiburan
# internasional
# arsip
# otomotif
# olahraga
# sepakbola
# digital
# gaya-hidup
# teroka
# prelude
# tokoh
# video
# foto
# data
# infografik
# pemilu
# newsletter
# info-tempo
# ramadan