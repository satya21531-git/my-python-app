import os
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route("/add")
def add():
    a = request.args.get('a')
    b = request.args.get('b')
    return jsonify({
        "result": a+b
    })

if __name__ == "__main__":
    # Default 5001 — macOS often binds 5000 to AirPlay Receiver
    port = int(os.environ.get("PORT", "5001"))
    app.run(host="0.0.0.0", port=port)