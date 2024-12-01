from flask import Flask, request, jsonify
from chatbot import LLM

# Initialize Flask app
app = Flask(__name__)

# Initialize the LLM model
# Ensure you provide the appropriate directory for your Chroma DB and prompt
model = LLM(save_directory="db", system_prompt="""
Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Only return the helpful answer below and nothing else. Always provide a discliamer that the user should see a doctor before taking any medicine
Answer in a short and consice way
Context: {context}
{question}

Helpful answer:
""")

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        # Extract the JSON request
        data = request.get_json()
        
        # Ensure 'question' is provided in the request
        if 'question' not in data:
            return jsonify({"error": "Missing 'question' field in the request."}), 400

        question = data['question']
        
        # Get the response from the model
        response = model.respond(question)
        print(response["result"])

        # Return the result in JSON format
        return jsonify({"response": response["result"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
