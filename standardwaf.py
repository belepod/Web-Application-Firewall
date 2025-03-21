from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Define rules to detect malicious patterns
SQL_INJECTION_PATTERNS = [r"(?i)\b(select|union|drop|insert|update|delete|alter|create|exec)\b"]
XSS_PATTERNS = [r"(?i)<script.*?>.*?</script.*?>", r"(?i)javascript:"]
IP_BLOCKLIST = set()

# Function to check for malicious patterns
def is_malicious(payload):
    for pattern in SQL_INJECTION_PATTERNS + XSS_PATTERNS:
        if re.search(pattern, payload):
            return True
    return False

@app.before_request
def waf():
    ip = request.remote_addr
    if ip in IP_BLOCKLIST:
        return jsonify({"message": "Blocked by WAF"}), 403

    # Check for malicious patterns in query params, headers, and body
    if any(is_malicious(str(value)) for value in request.args.values()):
        IP_BLOCKLIST.add(ip)  # Add to blocklist
        return jsonify({"message": "Malicious request detected"}), 403

    if request.data:
        if is_malicious(request.data.decode("utf-8")):
            IP_BLOCKLIST.add(ip)
            return jsonify({"message": "Malicious request detected"}), 403

@app.route('/')
def index():
    return "Welcome to the secure web app!"

if __name__ == "__main__":
    app.run(debug=True)
