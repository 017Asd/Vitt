# ViT-Based CIFAR-10 Classifier with Flask, Docker & Jenkins Integration 🚀

## Overview

This project builds a full-stack ML pipeline where a **Vision Transformer (ViT)** model is fine-tuned on the **CIFAR-10 dataset** and deployed using a **Flask web server**. The application is containerized with Docker and integrated with Jenkins for CI/CD automation on an **AWS EC2 instance**.

---

## 🔍 Features

- ✅ Fine-tuned ViT model on CIFAR-10 dataset
- 🌐 Flask-based image upload & prediction web app
- 🐳 Docker containerization for seamless deployment
- 🛠️ Jenkins for automatic build & deployment on code updates
- ☁️ Hosted on AWS EC2 with port forwarding for public access

---

## 🧠 Model Training (Fine-tuning)

We used the HuggingFace `transformers` library to:
- Load a pretrained ViT model
- Modify its head for **10-class CIFAR-10 classification**
- Fine-tune it using custom training script with:
  - Augmented CIFAR-10 dataset
  - `Trainer` API from HuggingFace
  - Model saved in `model/` folder

> Note: Training was done offline to keep the Docker image light. Only the fine-tuned weights are used during inference.

---

## 📂 Project Structure

```bash
vit/
├── Dockerfile
├── requirements.txt
├── app/
│   ├── app.py                # Flask web server
│   ├── model_infer.py        # ViT image inference logic
│   ├── static/               # CSS/JS files
│   ├── templates/            # HTML pages
│   └── model/                # Fine-tuned ViT model weights
├── Jenkinsfile (optional)
└── README.md
