import os
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from transformers import ViTFeatureExtractor, ViTForImageClassification, TrainingArguments, Trainer
from datasets import load_dataset
import numpy as np
from sklearn.model_selection import train_test_split

class BirdDataset(Dataset):
    def __init__(self, image_paths, labels, feature_extractor):
        self.image_paths = image_paths
        self.labels = labels
        self.feature_extractor = feature_extractor

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert('RGB')
        encoding = self.feature_extractor(images=image, return_tensors="pt")
        encoding['labels'] = torch.tensor(self.labels[idx])
        return {k: v.squeeze() for k, v in encoding.items()}

def prepare_dataset(data_dir):
    # Load dataset from directory structure
    image_paths = []
    labels = []
    label_to_idx = {}
    
    for class_idx, class_name in enumerate(sorted(os.listdir(data_dir))):
        class_dir = os.path.join(data_dir, class_name)
        if os.path.isdir(class_dir):
            label_to_idx[class_name] = class_idx
            for img_name in os.listdir(class_dir):
                if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_paths.append(os.path.join(class_dir, img_name))
                    labels.append(class_idx)
    
    return image_paths, labels, label_to_idx

def main():
    # Configuration
    data_dir = "path/to/bird200k/dataset"  # Update this path
    model_name = "google/vit-base-patch16-224"
    output_dir = "app/model"
    num_labels = 200  # Number of bird species in Bird200K
    
    # Load feature extractor and model
    feature_extractor = ViTFeatureExtractor.from_pretrained(model_name)
    model = ViTForImageClassification.from_pretrained(
        model_name,
        num_labels=num_labels,
        ignore_mismatched_sizes=True
    )
    
    # Prepare dataset
    image_paths, labels, label_to_idx = prepare_dataset(data_dir)
    
    # Split dataset
    train_paths, val_paths, train_labels, val_labels = train_test_split(
        image_paths, labels, test_size=0.2, random_state=42
    )
    
    # Create datasets
    train_dataset = BirdDataset(train_paths, train_labels, feature_extractor)
    val_dataset = BirdDataset(val_paths, val_labels, feature_extractor)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        push_to_hub=False,
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )
    
    # Train the model
    trainer.train()
    
    # Save the model and label mapping
    model.save_pretrained(output_dir)
    feature_extractor.save_pretrained(output_dir)
    np.save(os.path.join(output_dir, "label_to_idx.npy"), label_to_idx)

if __name__ == "__main__":
    main() 