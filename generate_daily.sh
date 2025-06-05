#!/bin/bash
export PATH="/usr/local/bin:/usr/bin:/bin"
PROJECT_DIR="$HOME/ai-blog-generator-interview--Giovanny-Rodriguez-"
cd "$PROJECT_DIR" || exit 1
source venv/bin/activate
export $(cat .env | xargs)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
echo "[$TIMESTAMP] Starting daily blog generation..."
KEYWORD="${1:-wireless earbuds}"
RESPONSE=$(curl -s -X GET "http://localhost:5000/generate?keyword=${KEYWORD// /%20}")
if [ $? -eq 0 ]; then
    echo "[$TIMESTAMP] Successfully generated blog post"
    echo "Response: $RESPONSE" | head -c 200
    echo "[$TIMESTAMP] $RESPONSE" >> daily_generation.log
else
    echo "[$TIMESTAMP] Error generating blog post"
fi
deactivate