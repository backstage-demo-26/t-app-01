from flask import Flask, jsonify, request
from functools import wraps
from hmac import compare_digest
import time
import socket 

app = Flask(__name__)

# -----------------------------
# Security Decorator
# -----------------------------
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        provided_key = request.headers.get("x-api-key")

        if not provided_key:
            return jsonify({"error": "API key missing"}), 401
			
        api_key=os.environ.get("API_KEY", "my_default_local_secret"),

        if not compare_digest(provided_key, api_key):
            return jsonify({"error": "Invalid API key"}), 403

        return f(*args, **kwargs)

    return decorated


# -----------------------------
# Routes
# -----------------------------
@app.route('/api/t-app-01/v1/healthz')
def health():
    return jsonify({
        "status": "up",
        "timestamp": int(time.time())
    }), 200


@app.route('/api/t-app-01/v1/info')
def info():
    return jsonify({
        "app_name": "t-app-01",
        "version": "1.0.0",
        "hostname": socket.gethostname(),
        "timestamp": int(time.time())
    })



# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    
	
