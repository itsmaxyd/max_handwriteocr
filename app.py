import streamlit as st
import torch
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
from PIL import Image
import io
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Handwritten Text Transcription",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load the Qwen2.5VL model with GPU/CPU fallback"""
    try:
        # Check device availability
        if torch.cuda.is_available():
            device = torch.device("cuda")
            st.sidebar.success(f"🚀 Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            device = torch.device("cpu")
            st.sidebar.warning("⚠️ Using CPU (GPU not available)")
        
        # Load model and processor
        model_name = "Qwen/Qwen2.5-VL-7B-Instruct"
        
        with st.spinner("Loading Qwen2.5VL model... This may take a few minutes."):
            # Set environment variable for hf_transfer if available
            import os
            os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
            
            try:
                processor = AutoProcessor.from_pretrained(
                    model_name,
                    trust_remote_code=True
                )
                model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16 if device.type == "cuda" else torch.float32,
                    device_map="auto" if device.type == "cuda" else None,
                    trust_remote_code=True,
                    low_cpu_mem_usage=True
                )
            except Exception as hf_error:
                st.sidebar.warning(f"⚠️ HF Transfer not available, using standard download: {str(hf_error)}")
                # Fallback to standard download
                os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"
                processor = AutoProcessor.from_pretrained(
                    model_name,
                    trust_remote_code=True
                )
                model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16 if device.type == "cuda" else torch.float32,
                    device_map="auto" if device.type == "cuda" else None,
                    trust_remote_code=True,
                    low_cpu_mem_usage=True
                )
            
            if device.type == "cpu":
                model = model.to(device)
        
        st.sidebar.success("✅ Model loaded successfully!")
        return model, processor, device
    
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        st.error("💡 Try running: pip install hf_transfer")
        return None, None, None

def transcribe_handwriting(image, model, processor, device):
    """Transcribe handwritten text from image to markdown"""
    try:
        # Convert image to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Prepare the prompt for handwriting transcription
        prompt = "Please transcribe the handwritten text in this image accurately. Output the text in markdown format, preserving any formatting like lists, headers, or emphasis that you can identify from the handwriting."
        
        # Process the image and text
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
        
        # Apply chat template
        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = processor.process_vision_info(messages)
        
        # Prepare inputs
        inputs = processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            return_tensors="pt"
        ).to(device)
        
        # Generate response
        with torch.no_grad():
            generated_ids = model.generate(
                **inputs,
                max_new_tokens=1024,
                do_sample=True,
                temperature=0.1,
                top_p=0.9,
                pad_token_id=processor.tokenizer.eos_token_id
            )
        
        # Decode the response
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, generated_ids)
        ]
        
        response = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return response.strip()
    
    except Exception as e:
        logger.error(f"Error in transcription: {str(e)}")
        return f"Error during transcription: {str(e)}"

def main():
    # Header
    st.markdown('<h1 class="main-header">✍️ Handwritten Text Transcription</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload handwritten images and get accurate text transcription in markdown format</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("⚙️ Settings")
    
    # Load model
    model, processor, device = load_model()
    
    if model is None:
        st.error("❌ Failed to load model. Please check the error messages above.")
        return
    
    # Device info
    st.sidebar.markdown("### 🔧 System Info")
    st.sidebar.write(f"**Device:** {device}")
    if device.type == "cuda":
        st.sidebar.write(f"**GPU Memory:** {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload Image")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            help="Supported formats: PNG, JPG, JPEG, BMP, TIFF"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Image info
            st.info(f"**Image Info:** {image.size[0]}x{image.size[1]} pixels, Mode: {image.mode}")
    
    with col2:
        st.markdown("### 📝 Transcription Result")
        
        if uploaded_file is not None:
            if st.button("🚀 Transcribe Text", type="primary", use_container_width=True):
                with st.spinner("Transcribing handwritten text... This may take a moment."):
                    start_time = time.time()
                    result = transcribe_handwriting(image, model, processor, device)
                    end_time = time.time()
                
                if result.startswith("Error"):
                    st.markdown(f'<div class="error-box">{result}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="success-box">✅ Transcription completed in {end_time - start_time:.2f} seconds</div>', unsafe_allow_html=True)
                    
                    # Display result
                    st.markdown("**Transcribed Text (Markdown):**")
                    st.code(result, language="markdown")
                    
                    # Download button
                    st.download_button(
                        label="📥 Download as .md file",
                        data=result,
                        file_name=f"transcription_{int(time.time())}.md",
                        mime="text/markdown"
                    )
        else:
            st.info("👆 Please upload an image to get started")
    
    # Footer
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This application uses the **Qwen2.5VL-7B-Instruct** model to transcribe handwritten text from images.
    
    **Features:**
    - 🖼️ Support for multiple image formats
    - 🚀 GPU acceleration when available
    - 💻 CPU fallback for systems without GPU
    - 📝 Output in markdown format
    - ⬇️ Download results as .md files
    
    **Tips for best results:**
    - Use high-resolution images
    - Ensure good contrast between text and background
    - Avoid heavily skewed or rotated text
    - Clean, legible handwriting works best
    """)

if __name__ == "__main__":
    main()
