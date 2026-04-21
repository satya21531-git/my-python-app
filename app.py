"""
Why "same behavior everywhere" is hard without Docker:

Each machine has its own Python build, paths, timezone, and installed packages.
This app exposes that drift on purpose — compare GET /runtime from your laptop
versus your deployed URL after `pip install -r requirements.txt` on the server.
With Docker, you ship one image: same interpreter, same OS libs, same TZ (if set).
"""
import os
import platform
import socket
import sys
from datetime import datetime, timezone

import flask
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return (
        "Hello, World! Try "
        "<a href=/runtime>/runtime</a> and "
        "<a href=/time_comparison>/time_comparison</a> — compare local vs deployed."
    )


@app.route("/runtime")
def runtime():
    """Fingerprints the process environment (will differ across hosts without a shared image)."""
    return jsonify(
        {
            "python_version": sys.version.split()[0],
            "python_full": sys.version,
            "python_executable": sys.executable,
            "flask_version": flask.__version__,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "hostname": socket.gethostname(),
            "cwd": os.getcwd(),
            "tz_env": os.environ.get("TZ", "(unset)"),
        }
    )


@app.route("/time_comparison")
def time_comparison():
    """Naive local clock vs UTC: wall-clock strings often differ by region unless TZ is fixed."""
    return jsonify(
        {
            "local_naive_iso": datetime.now().isoformat(timespec="seconds"),
            "utc_iso": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "note": "local_naive_iso follows the host timezone; servers and laptops often disagree.",
        }
    )


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