# ViT-Based Bird Species Classifier with Flask, Docker & Jenkins Integration 🦜

## Overview

This project builds a full-stack ML pipeline where a **Vision Transformer (ViT)** model is fine-tuned on the **Bird200K dataset** and deployed using a **Flask web server**. The application is containerized with Docker and integrated with Jenkins for CI/CD automation on an **AWS EC2 instance**.

---

## 🔍 Features

- ✅ Fine-tuned ViT model on Bird200K dataset (200 bird species)
- 🌐 Flask-based bird image upload & species prediction web app
- 🐳 Docker containerization for seamless deployment
- 🛠️ Jenkins for automatic build & deployment on code updates
- ☁️ Hosted on AWS EC2 with port forwarding for public access
- 📊 Confidence scores for predictions

---

## 🧠 Model Training (Fine-tuning)

We used the HuggingFace `transformers` library to:
- Load a pretrained ViT model
- Modify its head for **200-class bird species classification**
- Fine-tune it using custom training script with:
  - Bird200K dataset
  - `Trainer` API from HuggingFace
  - Model saved in `app/model/` folder

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
│   ├── train.py             # Model training script
│   ├── static/              # CSS/JS files
│   ├── templates/           # HTML pages
│   └── model/               # Fine-tuned ViT model weights
├── Jenkinsfile
└── README.md
```

---

## 🚀 Getting Started

1. **Setup Environment**
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare Dataset**
   - Download Bird200K dataset
   - Organize images in species-specific folders
   - Update `data_dir` path in `train.py`

3. **Train Model**
   ```bash
   python app/train.py
   ```

4. **Run Web App**
   ```bash
   python app/app.py
   ```

5. **Docker Deployment**
   ```bash
   docker build -t bird-classifier .
   docker run -p 5000:5000 bird-classifier
   ```

---

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **ML Framework**: PyTorch, HuggingFace Transformers
- **Model**: Vision Transformer (ViT)
- **Dataset**: Bird200K
- **Containerization**: Docker
- **CI/CD**: Jenkins
- **Cloud**: AWS EC2

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/bird-classifier/issues).
