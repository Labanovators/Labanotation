from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            file_path = f"uploads/{uploaded_file.filename}"
            uploaded_file.save(file_path)
            return f"File '{uploaded_file.filename}' has been uploaded and saved to the server."

    return '''
    <html>
        <head>
            <title>Labanotation</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                    text-align: center;
                }
                h1 {
                    color: #333;
                }
                p {
                    font-size: 18px;
                }
                form {
                    margin-top: 20px;
                }
                input[type="file"] {
                    display: block;
                    margin: 0 auto;
                }
                input[type="submit"] {
                    margin: 10px auto;
                    background-color: #3498db;
                    color: #fff;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <h1>Labanotation Generator</h1>
            <p>Please provide a photo or video to start Labanotation generation</p>

            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
