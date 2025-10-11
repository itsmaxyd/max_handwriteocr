#!/bin/bash

# Script to push handwritten text transcription code to GitHub
# Repository: https://github.com/itsmaxyd/max_handwriteocr

echo "🚀 Pushing Handwritten Text Transcription to GitHub"
echo "Repository: https://github.com/itsmaxyd/max_handwriteocr"
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the project directory."
    exit 1
fi

# Check git status
echo "📋 Current git status:"
git status
echo ""

# Add all files
echo "📁 Adding all files to git..."
git add .

# Check what's staged
echo "📋 Staged files:"
git status --porcelain
echo ""

# Create a comprehensive commit
echo "💾 Creating commit..."
git commit -m "Complete Handwritten Text Transcription Application

🎯 Features:
- Streamlit web interface for handwritten text transcription
- Qwen2.5VL-7B model with GPU/CPU fallback support
- Markdown output format with download functionality
- Multi-format image support (PNG, JPG, JPEG, BMP, TIFF)
- Docker containerization with build scripts
- GitHub Actions workflow for automated builds

🔧 Technical Details:
- Uses Qwen2.5VL-7B-Instruct model (8.3B parameters)
- Automatic GPU detection and CPU fallback
- hf_transfer for faster model downloads
- Optimized memory usage with low_cpu_mem_usage
- Trust remote code enabled for Qwen2.5VL compatibility

📦 Files Included:
- app.py: Main Streamlit application
- requirements.txt: Python dependencies
- Dockerfile & Dockerfile.simple: Container configurations
- docker-compose.yml: Multi-service setup
- build-docker.sh: Docker build script
- setup.sh: Local testing script
- test_model.py: Model testing script
- README.md: Comprehensive documentation
- .github/workflows/: GitHub Actions CI/CD

🚀 Ready for deployment and use!"

# Push to GitHub
echo "📤 Pushing to GitHub..."
echo "Note: You may need to authenticate with GitHub"
echo ""

# Try to push
if git push origin main --force; then
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 Repository: https://github.com/itsmaxyd/max_handwriteocr"
    echo ""
    echo "📋 Next steps:"
    echo "1. Visit your repository: https://github.com/itsmaxyd/max_handwriteocr"
    echo "2. Check the GitHub Actions tab for automated builds"
    echo "3. Use the Docker images from GitHub Container Registry"
    echo "4. Share the repository with others!"
else
    echo "❌ Push failed. This might be due to authentication issues."
    echo ""
    echo "🔧 Manual steps to push:"
    echo "1. Run: git push origin main --force"
    echo "2. Enter your GitHub username and personal access token when prompted"
    echo "3. Or set up SSH keys for authentication"
    echo ""
    echo "📋 Alternative: You can also:"
    echo "1. Download the files from this directory"
    echo "2. Upload them manually to GitHub"
    echo "3. Or use GitHub Desktop/GitKraken for GUI push"
fi

echo ""
echo "🎉 Your handwritten text transcription application is ready!"
