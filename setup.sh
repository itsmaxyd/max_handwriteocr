#!/bin/bash

# Handwritten Text Transcription Setup Script

echo "🚀 Setting up Handwritten Text Transcription Application"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -f Dockerfile.simple -t ocr-handwriting-app .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi

# Test the container
echo "🧪 Testing the container..."
docker run -d --name ocr-test -p 8501:8501 ocr-handwriting-app

sleep 10

# Check if container is running
if docker ps | grep -q ocr-test; then
    echo "✅ Container is running successfully"
    
    # Test the web interface
    if curl -s http://localhost:8501 > /dev/null; then
        echo "✅ Web interface is accessible"
    else
        echo "⚠️  Web interface might not be ready yet"
    fi
    
    # Clean up test container
    docker stop ocr-test
    docker rm ocr-test
    echo "🧹 Test container cleaned up"
else
    echo "❌ Container failed to start"
    docker logs ocr-test
    docker rm ocr-test
    exit 1
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To run the application:"
echo "  docker run -d --name ocr-app -p 8501:8501 ocr-handwriting-app"
echo ""
echo "To run with CPU-only mode:"
echo "  docker run -d --name ocr-app-cpu -p 8502:8501 -e CUDA_VISIBLE_DEVICES=\"\" ocr-handwriting-app"
echo ""
echo "To stop the application:"
echo "  docker stop ocr-app"
echo "  docker rm ocr-app"
echo ""
echo "Access the application at: http://localhost:8501"

