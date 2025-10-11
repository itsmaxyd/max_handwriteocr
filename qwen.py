from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = Qwen2_5_VLForConditionalGeneration.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct").to(device)
processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct")
