#!/bin/bash

# Exit on error
set -e

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Always run the database initialization script.
# The script is idempotent and safe to run on every build.
# It will create tables if they don't exist and won't duplicate data.
echo "Initializing database..."
python init_db.py