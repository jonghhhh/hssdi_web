#!/bin/bash

# Exit on error
set -e

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Define the data directory for Render's persistent disk
DATA_DIR="/data"
DB_FILE="$DATA_DIR/hssdi.db"

# Check if the database file exists
if [ ! -f "$DB_FILE" ]; then
  echo "Database not found. Initializing..."
  # Run the database initialization script
  python init_db.py
else
  echo "Database already exists. Skipping initialization."
fi
