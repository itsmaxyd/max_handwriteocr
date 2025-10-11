# Handwritten Text Transcription with Qwen2.5VL

A user-friendly web application for transcribing handwritten text from images using the Qwen2.5VL-7B-Instruct model. The application supports both GPU and CPU inference with automatic fallback.

## Features

- 🖼️ **Multi-format Support**: PNG, JPG, JPEG, BMP, TIFF
- 🚀 **GPU Acceleration**: Automatic GPU detection and usage
- 💻 **CPU Fallback**: Works on systems without GPU
- 📝 **Markdown Output**: Clean, formatted text output
- ⬇️ **Download Results**: Save transcriptions as .md files
- 🐳 **Docker Ready**: Easy deployment with Docker
- 🎨 **User-Friendly UI**: Clean Streamlit interface

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ocr_project
   ```

2. **Build and run with GPU support:**
   ```bash
   docker-compose up --build
   ```

3. **For CPU-only mode:**
   ```bash
   # Edit docker-compose.yml and uncomment the CPU service
   docker-compose up ocr-app-cpu --build
   ```

4. **Access the application:**
   - Open your browser to `http://localhost:8501`
   - Upload an image and click "Transcribe Text"

### Manual Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## System Requirements

### Minimum Requirements
- Python 3.8+
- 8GB RAM
- 10GB free disk space

### Recommended for GPU
- NVIDIA GPU with 8GB+ VRAM
- CUDA 11.8+ or 12.0+
- 16GB+ RAM

### CPU-Only Mode
- 16GB+ RAM
- 20GB+ free disk space

## Usage Tips

For best transcription results:

1. **Image Quality**: Use high-resolution images (at least 300 DPI)
2. **Contrast**: Ensure good contrast between text and background
3. **Orientation**: Keep text upright and properly oriented
4. **Handwriting**: Clean, legible handwriting works best
5. **Format**: Supported formats: PNG, JPG, JPEG, BMP, TIFF

## Docker Configuration

### GPU Support
The application automatically detects and uses available GPUs. For NVIDIA GPUs, ensure you have:
- NVIDIA Container Toolkit installed
- Docker with GPU support enabled

### CPU-Only Mode
To force CPU-only mode, set the environment variable:
```bash
export CUDA_VISIBLE_DEVICES=""
```

## API Usage

The application also provides a simple API endpoint:

```python
import requests

# Upload an image and get transcription
with open('handwritten_image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8501/api/transcribe', files=files)
    result = response.json()
    print(result['markdown'])
```

## Troubleshooting

### Common Issues

1. **Out of Memory Error:**
   - Reduce image size before uploading
   - Use CPU-only mode if GPU memory is insufficient
   - Close other applications to free up memory

2. **Model Loading Issues:**
   - Ensure stable internet connection for model download
   - Check available disk space (model is ~14GB)
   - Try restarting the application
   - Install hf_transfer for faster downloads: `pip install hf_transfer`

3. **HF Transfer Issues:**
   - If you see "hf_transfer is not available" error, install it: `pip install hf_transfer`
   - The application will automatically fallback to standard download if hf_transfer fails
   - For Docker: hf_transfer is included in the container

4. **Docker Issues:**
   - Ensure Docker is running properly
   - Check Docker logs: `docker-compose logs`
   - Verify GPU support: `docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu20.04 nvidia-smi`
   - If Docker build fails, try: `./build-docker.sh`

### Performance Optimization

- **GPU Mode**: Significantly faster for large images
- **CPU Mode**: More memory efficient, slower processing
- **Image Preprocessing**: Resize large images to reasonable dimensions (max 2048x2048)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Qwen2.5VL](https://github.com/QwenLM/Qwen2-VL) for the vision-language model
- [Streamlit](https://streamlit.io/) for the web interface
- [Hugging Face Transformers](https://huggingface.co/transformers/) for model integration
