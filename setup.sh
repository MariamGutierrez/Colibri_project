#!/bin/bash

# Script to set up environment for Heroku deployment

# This will be executed on Heroku before the app starts
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python colibri/manage.py collectstatic --noinput

echo "Running migrations..."
python colibri/manage.py migrate

echo "Setup complete!"
