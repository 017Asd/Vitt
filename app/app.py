import logging
from flask import Flask, request, render_template
from model_infer import predict
import os

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
logging.info(f"Upload folder is set to: {UPLOAD_FOLDER}")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    image_url = None

    if request.method == "POST":
        file = request.files.get("file")
        if file:
            filename = file.filename
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
            prediction = predict(save_path)
            image_url = f"/static/uploads/{filename}"
            logging.info(f"Image uploaded and accessible at: {image_url}")
        else:
            logging.warning("No file found in POST request.")

    return render_template("index.html", prediction=prediction, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
