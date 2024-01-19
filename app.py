from text_classification import get_classification_ollama

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/api/org/category/ollama/v0", methods=["GET"])
def get_gpt_result():
    title = request.get_json().get("title")
    description = request.get_json().get("description")

    category = get_classification_ollama(description=description, title=title)
    return category

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)