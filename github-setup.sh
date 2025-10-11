#!/bin/bash

# GitHub Setup Script for Handwritten Text Transcription

echo "🐙 Setting up GitHub repository for Handwritten Text Transcription"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Handwritten Text Transcription with Qwen2.5VL

- Streamlit web interface for handwritten text transcription
- Qwen2.5VL-7B model with GPU/CPU fallback support
- Docker containerization with multi-architecture support
- Markdown output format
- User-friendly interface with image upload and download

Features:
- Multi-format image support (PNG, JPG, JPEG, BMP, TIFF)
- Automatic GPU detection and CPU fallback
- Clean markdown output
- Download results as .md files
- Docker Compose for easy deployment
- GitHub Actions for automated builds"

echo ""
echo "🎉 Git repository ready!"
echo ""
echo "Next steps:"
echo "1. Create a new repository on GitHub"
echo "2. Add the remote origin:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
echo "3. Push to GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "The GitHub Actions workflow will automatically build and push Docker images to GitHub Container Registry."
echo "You can then pull and run the image with:"
echo "   docker pull ghcr.io/YOUR_USERNAME/YOUR_REPO_NAME:latest"

