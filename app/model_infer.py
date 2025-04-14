# app/model_infer.py
from transformers import ViTFeatureExtractor, ViTForImageClassification
from PIL import Image # type: ignore
import torch # type: ignore

import os 
your_token =os.environ("HF_TOKEN")
model_name = 'google/vit-base-patch16-224'

# Load model and extractor once (not every time user uploads)
feature_extractor = ViTFeatureExtractor.from_pretrained(model_name, use_auth_token=your_token)
model = ViTForImageClassification.from_pretrained(model_name, use_auth_token=your_token)
model.eval()

def predict(image_path):
    image = Image.open(image_path)
    inputs = feature_extractor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    return model.config.id2label[predicted_class_idx]
