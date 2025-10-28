# Lightweight Handwritten OCR with OpenAI GPT-4o

A simple command-line tool for transcribing handwritten text from images using OpenAI's GPT-4o Vision API.

## Features

- 🖼️ **Simple CLI**: Easy to use command-line interface
- 🤖 **OpenAI GPT-4o**: Powered by the latest vision model
- 📝 **Terminal Output**: Prints transcribed text directly to terminal
- 🐳 **Docker Ready**: Easy deployment with Docker
- 🔒 **Basic Obfuscation**: API key obfuscated with base64 encoding

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd max_handwriteocr
   ```

2. **Build the Docker container:**
   ```bash
   cd max_handwriteocr
   docker-compose build
   ```

3. **Start the container:**
   ```bash
   docker-compose up -d
   ```

4. **Run the OCR script:**
   ```bash
   # Enter the container
   docker-compose exec ocr-app bash
   
   # Run the script (inside container)
   python handwrite_ocr.py /path/to/image.jpg
   ```

### Manual Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the OCR script:**
   ```bash
   python handwrite_ocr.py image.jpg
   ```

## System Requirements

- Python 3.8+
- OpenAI API key (embedded in the script)
- Docker (optional, for containerized deployment)

## Usage

Run the script with an image path:

```bash
python handwrite_ocr.py path/to/your/image.jpg
```

The transcribed text will be printed to the terminal.

### Usage Tips

For best transcription results:

1. **Image Quality**: Use clear, high-resolution images
2. **Contrast**: Ensure good contrast between text and background
3. **Orientation**: Keep text upright and properly oriented
4. **Handwriting**: Clean, legible handwriting works best
5. **Format**: Supported formats: PNG, JPG, JPEG, BMP, TIFF

## Docker Configuration

The container runs interactively, allowing you to process multiple images:

```bash
# Build the container
docker-compose build

# Start the container
docker-compose up -d

# Enter the container
docker-compose exec ocr-app bash

# Inside container, run:
python handwrite_ocr.py /path/to/image.jpg
```

## GitHub Deployment

To push updates to GitHub:

1. **Create a GitHub repository** (if not already done):
   - Go to https://github.com/new
   - Create a new repository
   - Copy the repository URL

2. **Initialize git** (if not already done):
   ```bash
   cd max_handwriteocr
   git init
   git remote add origin <your-repo-url>
   ```

3. **Push updates:**
   ```bash
   ./push-to-github.sh
   ```

## Troubleshooting

### Common Issues

1. **API Key Issues:**
   - If you get authentication errors, verify the API key in the script
   - The API key is base64 encoded for basic obfuscation

2. **Image Not Found:**
   - Ensure the image path is correct
   - Use absolute paths if relative paths fail

3. **Docker Issues:**
   - Ensure Docker is running: `sudo systemctl start docker`
   - Check container status: `docker-compose ps`
   - View logs: `docker-compose logs`

4. **Import Errors:**
   - Install dependencies: `pip install -r requirements.txt`
   - Verify Python version: `python --version` (needs 3.8+)

### Tips

- Works with handwritten text in images
- Best results with clear, readable handwriting
- No GPU required (uses OpenAI API)

## Security Note

The API key is base64-encoded in the source code for basic obfuscation. This prevents casual viewing but is not encryption. For production use, consider using environment variables or secure vaults.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OpenAI GPT-4o](https://openai.com/) for the vision model
- Python PIL/Pillow for image processing
