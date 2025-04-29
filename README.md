# Image Classification Web Application

A Flask-based web application that classifies images using the Vision Transformer (ViT) model from Hugging Face.

## Features

- Image upload and classification
- Real-time predictions
- Docker containerization
- CI/CD pipeline with Jenkins

## Prerequisites

- Python 3.9+
- Docker
- Hugging Face account and API token

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a `.env` file in the app directory with your Hugging Face token:
```
HF_TOKEN=your_huggingface_token_here
```

3. Build and run the Docker container:
```bash
docker build -t image-classification-app .
docker run -p 5000:5000 -e HF_TOKEN=your_huggingface_token_here image-classification-app
```

4. Access the application at `http://localhost:5000`

## CI/CD Pipeline

The project uses Jenkins for continuous integration and deployment. The pipeline:
1. Builds the Docker image
2. Runs tests
3. Deploys the application
4. Updates the running container

## Project Structure

```
.
├── app/
│   ├── static/
│   ├── templates/
│   ├── app.py
│   └── model_infer.py
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

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
