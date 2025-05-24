# app/model_infer.py
from dotenv import load_dotenv
load_dotenv()
from transformers import ViTFeatureExtractor, ViTForImageClassification
from PIL import Image
import torch
import os
import numpy as np

# Load model and extractor
model_path = os.path.join(os.path.dirname(__file__), "model")
feature_extractor = ViTFeatureExtractor.from_pretrained(model_path)
model = ViTForImageClassification.from_pretrained(model_path)
model.eval()

# Load label mapping
label_to_idx = np.load(os.path.join(model_path, "label_to_idx.npy"), allow_pickle=True).item()
idx_to_label = {v: k for k, v in label_to_idx.items()}

def predict(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = feature_extractor(images=image, return_tensors="pt", padding=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        
    predicted_class_idx = logits.argmax(-1).item()
    confidence = probabilities[0][predicted_class_idx].item()
    
    return {
        "species": idx_to_label[predicted_class_idx],
        "confidence": f"{confidence:.2%}"
    }

