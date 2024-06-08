#!/bin/bash

# Connect to the Django container
docker exec -it steganography-tool_api_1 /bin/bash << EOF

# Navigate to the Django project directory
cd /app

# Perform migration
python manage.py makemigrations api
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Check for errors during migration
python manage.py check --deploy

EOF