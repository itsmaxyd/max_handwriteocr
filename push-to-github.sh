#!/bin/bash

# Script to push code to GitHub
# Usage: ./push-to-github.sh

set -e

echo "=== Adding files to git ==="
git add .

echo "=== Committing changes ==="
read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Update OCR script with OpenAI GPT-4o"
fi

git commit -m "$commit_msg"

echo "=== Pushing to GitHub ==="
git push

echo "=== Done ==="
echo "Note: Make sure you have created the GitHub repository first:"
echo "1. Go to https://github.com/new"
echo "2. Create a new repository"
echo "3. Set the remote: git remote add origin <your-repo-url>"
echo "4. Push: git push -u origin master"
