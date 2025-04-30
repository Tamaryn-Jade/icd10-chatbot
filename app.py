from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample ICD-10 data (replace with Excel loading later)
ICD_CODES = {
    "A00.0": "Cholera due to Vibrio cholerae 01, biovar cholerae",
    "A00.1": "Cholera due to Vibrio cholerae 01, biovar eltor",
    "A00.9": "Cholera, unspecified",
    "A01.0": "Typhoid fever"
}

# Sample coding rules data (from PDF)
CODING_RULES = {
    "primary diagnosis": (
        "The primary diagnosis or main condition is defined as:\n"
        "1. The condition, diagnosed at the end of the episode of healthcare, primarily responsible for the patient’s need for treatment or investigation.\n"
        "2. If there is more than one such condition, select the most clinically severe or life-threatening."
    )
}

def search_icd(code):
    return ICD_CODES.get(code.upper(), None)

def search_rule(query):
    for keyword in CODING_RULES:
        if keyword in query.lower():
            return CODING_RULES[keyword]
    return "Sorry, I couldn't find a matching coding rule."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"response": "Please enter a valid question."})

    if len(user_input) <= 6 and user_input[:1].isalpha():
        response = search_icd(user_input)
        if response:
            return jsonify({"response": f"ICD-10 code {user_input.upper()}: {response}"})
        else:
            return jsonify({"response": "ICD-10 code not found."})
    else:
        response = search_rule(user_input)
        return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
