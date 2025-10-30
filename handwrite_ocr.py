#!/usr/bin/env python3
"""
Lightweight Handwritten OCR using OpenAI GPT-4o Vision API
Takes an image path as command-line argument and outputs transcribed text to terminal.
"""

import sys
import base64
import argparse
from pathlib import Path
from PIL import Image
from openai import OpenAI

_ENCODED_KEY = "c2stcHJvai11QTJ2dGFpdzIwc1RIWlVoOEoxMzVtZzJvV0JZbEo4R1VicUpaRzJ1aTFMVFVxck84ejNCOWZJMDdnXzUwTVA0cXlGVkF1bU8xTlQzQmxia0ZKYlJEc1F0UWJRel9kUDJQVFRleXpldGw5QmlYemlhT1BxWFFPeUd3WU1QMWoya3NJeVVEdEdrUjNuUFRLeHNyQlFjaFRnbHI2WUEK"

def get_api_key():
    """Decode and return the API key"""
    return base64.b64decode(_ENCODED_KEY).decode('utf-8')

def encode_image(image_path):
    """Convert image to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def transcribe_handwriting(image_path):
    """Process image with OpenAI GPT-4o vision model"""
    # Initialize OpenAI client
    client = OpenAI(api_key=get_api_key())
    
    # Read and encode image
    base64_image = encode_image(image_path)
    
    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Transcribe all handwritten text from this image accurately. Preserve line breaks and formatting as closely as possible."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000
    )
    
    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(
        description='Transcribe handwritten text from an image using OpenAI GPT-4o'
    )
    parser.add_argument(
        'image_path',
        type=str,
        help='Path to the image file to transcribe'
    )
    
    args = parser.parse_args()
    
    # Validate image path
    image_path = Path(args.image_path)
    if not image_path.exists():
        print(f"Error: File '{image_path}' not found.", file=sys.stderr)
        sys.exit(1)
    
    if not image_path.is_file():
        print(f"Error: '{image_path}' is not a file.", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Transcribe the image
        result = transcribe_handwriting(image_path)
        
        # Print to terminal
        print("\n" + "="*60)
        print("TRANSCRIBED TEXT:")
        print("="*60)
        print(result)
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"Error processing image: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

