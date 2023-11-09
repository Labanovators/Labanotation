from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            file_path = f"uploads/{uploaded_file.filename}"
            uploaded_file.save(file_path)
            generate_labanotation(file_path)
            return f"File '{uploaded_file.filename}' has been uploaded, saved, and Labanotation has been generated."

    return render_template('index.html')


def generate_labanotation(file_path):
    subprocess.run(['sleep', '1'])
    subprocess.run(['python3', 'parse_image.py', "--input", file_path])


if __name__ == '__main__':
    app.run(debug=True)
