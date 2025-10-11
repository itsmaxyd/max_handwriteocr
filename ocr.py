from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
import torch
from PIL import Image
import io

app = FastAPI()

# Load model and processor once at startup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name = "Qwen/Qwen2.5-VL-7B-Instruct"
processor = AutoProcessor.from_pretrained(model_name)
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(model_name).to(device)

templates = Jinja2Templates(directory="templates")

def image_to_markdown(image: Image.Image) -> str:
    # Prepare inputs for the model
    inputs = processor(image, return_tensors="pt").to(device)
    
    # Use a prompt to guide handwriting recognition
    prompt = "Transcribe the handwritten text accurately and output in markdown format:"
    input_text = processor.tokenizer(prompt, return_tensors="pt").to(device)
    
    # Generate output ids
    outputs = model.generate(**inputs, input_ids=input_text.input_ids, attention_mask=input_text.attention_mask, max_length=512)
    
    # Decode the generated text
    result = processor.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return result

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    markdown_text = image_to_markdown(image)

    return templates.TemplateResponse("result.html", {"request": request, "markdown": markdown_text})

@app.post("/api/transcribe")
async def api_transcribe(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    markdown_text = image_to_markdown(image)

    return JSONResponse(content={"markdown": markdown_text})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
