from flask import Flask, render_template, request
import face_recognition
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
KNOWN_PEOPLE_FOLDER = "known_people"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            unknown_image = face_recognition.load_image_file(filepath)
            unknown_encoding = face_recognition.face_encodings(unknown_image)
            if not unknown_encoding:
                result = "لم يتم التعرف على وجه في الصورة."
            else:
                unknown_encoding = unknown_encoding[0]
                result = "لم يتم العثور على تطابق."

                for person_image in os.listdir(KNOWN_PEOPLE_FOLDER):
                    person_path = os.path.join(KNOWN_PEOPLE_FOLDER, person_image)
                    known_image = face_recognition.load_image_file(person_path)
                    known_encoding = face_recognition.face_encodings(known_image)
                    if not known_encoding:
                        continue
                    known_encoding = known_encoding[0]
                    match = face_recognition.compare_faces([known_encoding], unknown_encoding)
                    if match[0]:
                        result = f"تطابق مع: {os.path.splitext(person_image)[0]}"
                        break
    return render_template("index.html", result=result)

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(KNOWN_PEOPLE_FOLDER, exist_ok=True)
    app.run(debug=True)