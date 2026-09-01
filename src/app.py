"""
app.py
Minimal Flask wrapper exposing the multi-tool agent as an HTTP endpoint.
This is a deployment DEFINITION for Level 3 - it is not deployed to a
public host in this submission (see docs/level3-production-readiness.md
for why, and the reproducible deployment commands to actually do so).
"""

from flask import Flask, request, jsonify

from agent import run_agent

app = Flask(__name__)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "")

    if not question.strip():
        return jsonify({"status": "error", "reason": "Missing 'question' field."}), 400

    try:
        answer = run_agent(question)
        return jsonify({"status": "ok", "answer": answer})
    except Exception as exc:
        return jsonify({"status": "error", "reason": str(exc)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)