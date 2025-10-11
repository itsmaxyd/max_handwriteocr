#!/bin/bash

# Docker Build Script for Handwritten Text Transcription

echo "🐳 Building Docker container for Handwritten Text Transcription"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Try different Docker build approaches
echo "🔨 Attempting Docker build..."

# Method 1: Try with buildx
if docker buildx version > /dev/null 2>&1; then
    echo "📦 Using Docker Buildx..."
    docker buildx build -f Dockerfile.simple -t ocr-handwriting-app --load .
    if [ $? -eq 0 ]; then
        echo "✅ Build successful with Buildx!"
        exit 0
    fi
fi

# Method 2: Try standard build with different options
echo "📦 Trying standard Docker build..."
docker build -f Dockerfile.simple -t ocr-handwriting-app --no-cache .
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    exit 0
fi

# Method 3: Try with different storage driver
echo "📦 Trying with VFS storage driver..."
DOCKER_BUILDKIT=0 docker build -f Dockerfile.simple -t ocr-handwriting-app .
if [ $? -eq 0 ]; then
    echo "✅ Build successful with VFS!"
    exit 0
fi

echo "❌ All build methods failed"
echo "💡 Try running: sudo dockerd --storage-driver=vfs --data-root=/tmp/docker-data"
exit 1

