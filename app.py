from text_classification import get_classification_ollama

from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/org/category/ollama/v0", methods=["POST"])
def get_gpt_result():
    title = request.get_json().get("title")
    description = request.get_json().get("description")

    category = get_classification_ollama(description=description, title=title)
    return jsonify({'result': 'success', 'category': category})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)