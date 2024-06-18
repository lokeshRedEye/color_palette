import os
import numpy as np
from flask import Flask, request, render_template, url_for
from PIL import Image
import random

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_random_colors(image_file, num_colors=30):
    # Open the image file
    image = Image.open(image_file)
    # Convert image to RGB mode
    image = image.convert("RGB")
    # Resize image to reduce the number of pixels (optional)
    image = image.resize((100, 100))
    # Convert image to numpy array
    np_image = np.array(image)
    # Reshape the array to be a list of pixels
    pixels = np_image.reshape((-1, 3))
    # Ensure num_colors is not greater than the number of unique pixels
    num_colors = min(num_colors, len(pixels))
    # Randomly sample colors
    random_colors = random.sample(list(map(tuple, pixels)), num_colors)
    # Convert numpy.uint8 values to regular integers
    random_colors = [(int(r), int(g), int(b)) for r, g, b in random_colors]
    return random_colors

@app.route("/", methods=["GET", "POST"])
def home():
    array_colors = []
    uploaded_image = None
    if request.method == "POST":
        # Check if the post request has the file part
        if 'image' not in request.files:
            return "No file part"

        file = request.files['image']
        if file:
            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            # Extract random colors
            array_colors = extract_random_colors(file_path)
            # Generate the image URL
            uploaded_image = url_for('static', filename=f'uploads/{file.filename}')

    return render_template("index.html", colors=array_colors, uploaded_image=uploaded_image)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
