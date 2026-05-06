from flask import Flask, request, jsonify, send_from_directory
import os
from copilot import get_copilot_response

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/prompt", methods=["POST"])
def handle_prompt():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    show_browser = data.get("debug", False) # Get toggle state

    if not prompt:
        return jsonify({"error": "Empty prompt provided."}), 400

    try:
        # Pass the debug preference to the automation function
        response = get_copilot_response(prompt, show_window=show_browser)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True, port=5000)