#!/bin/bash

# Function to ensure dependencies are installed
ensure_dependencies() {
  if [ ! -f "uv.lock" ]; then
    echo "uv.lock file not found. Creating project with uv..."
    uv init
  fi
  
  echo "Syncing dependencies with uv..."
  uv sync
}

# Function to run scraping for a given date range
run_scraping() {
  local start_date=$1
  local end_date=$2
  
  echo "Starting scraping for date range: $start_date to $end_date"
  
  current_date=$start_date

  # Function to convert date to seconds since epoch for comparison
  date_to_seconds() {
      date -d "$1" +%s
  }

  while [[ $(date_to_seconds "$current_date") -le $(date_to_seconds "$end_date") ]]; do
    # Format the date for the output name (YYYYMMDD)
    output_name=$(date -d "$current_date" +"%Y%m%d")
    
    # Extract year, month, and day for directory structure
    year=$(date -d "$current_date" +"%Y")
    month=$(date -d "$current_date" +"%m")
    day=$(date -d "$current_date" +"%d")
    
    # Calculate the next day for the end-date parameter
    next_day=$(date -d "$current_date + 1 day" +"%Y-%m-%d")
    
    echo "==============================================="
    echo "Scraping articles for $current_date..."
    echo "==============================================="
    
    uv run python -m src.tempo_scraper indeks \
      --start-page 1 \
      --end-page 30 \
      --delay 1 \
      --start-date "$current_date" \
      --end-date "$next_day" \
      --categorize \
      --extract-content \
      --output-name "$output_name"
    
    # Check if the scraping was successful
    if [ $? -eq 0 ]; then
      echo "Scraping completed successfully for $current_date."
      
      # Define input directory for markdown conversion
      input_dir="data/output/$output_name"
      
      # Define output directory with the specified structure
      output_dir="/home/fakhry/dev/obsidian/news/$year/$month/$day"
      
      echo "Converting JSON files to Markdown for $current_date..."
      echo "Output directory: $output_dir"
      uv run python scripts/json_to_markdown.py "$input_dir" "$output_dir"
      
      # Check if the conversion was successful
      if [ $? -eq 0 ]; then
        echo "Markdown conversion completed successfully for $current_date."
      else
        echo "Error: Markdown conversion failed for $current_date."
      fi
    else
      echo "Error: Scraping failed for $current_date."
    fi
    
    # Move to the next day
    current_date=$(date -d "$current_date + 1 day" +"%Y-%m-%d")
    
    echo "Completed processing for $current_date. Moving to the next day."
    echo ""
  done

  echo "==============================================="
  echo "All scraping and conversion completed for the date range $start_date to $end_date."
  echo "==============================================="
}

# Ensure dependencies are installed before running
ensure_dependencies

run_scraping "2025-10-23" "2025-10-24"

echo "==============================================="
echo "All scraping periods completed!"
echo "==============================================="
