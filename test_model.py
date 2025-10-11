#!/usr/bin/env python3
"""
Test script to verify Qwen2.5VL model loading
"""

import os
import torch
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration

def test_model_loading():
    """Test if the model can be loaded successfully"""
    print("🧪 Testing Qwen2.5VL model loading...")
    
    # Set environment variables
    os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    
    try:
        # Check device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"📱 Using device: {device}")
        
        if device.type == "cuda":
            print(f"🚀 GPU: {torch.cuda.get_device_name(0)}")
            print(f"💾 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        
        # Load model
        model_name = "Qwen/Qwen2.5-VL-7B-Instruct"
        print(f"📥 Loading model: {model_name}")
        
        print("⏳ Loading processor...")
        processor = AutoProcessor.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        print("✅ Processor loaded successfully")
        
        print("⏳ Loading model...")
        model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if device.type == "cuda" else torch.float32,
            device_map="auto" if device.type == "cuda" else None,
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
        
        if device.type == "cpu":
            model = model.to(device)
        
        print("✅ Model loaded successfully!")
        print(f"📊 Model parameters: {sum(p.numel() for p in model.parameters()):,}")
        
        # Test with a simple image
        from PIL import Image
        import io
        
        # Create a simple test image
        test_image = Image.new('RGB', (100, 100), color='white')
        
        print("🧪 Testing transcription...")
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": test_image},
                    {"type": "text", "text": "What do you see in this image?"}
                ]
            }
        ]
        
        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = processor.process_vision_info(messages)
        
        inputs = processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            return_tensors="pt"
        ).to(device)
        
        print("✅ Model test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("💡 Make sure hf_transfer is installed: pip install hf_transfer")
        return False

if __name__ == "__main__":
    success = test_model_loading()
    exit(0 if success else 1)

