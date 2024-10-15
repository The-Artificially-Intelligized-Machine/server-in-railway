from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize models
GROQ_API_KEY = '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'
chat = ChatGroq(
    temperature=0,
    model_name="llama3-8b-8192",
    groq_api_key=GROQ_API_KEY)

# Initialize variables
user_name = "dron"
curr_time = datetime.datetime.now()

# Define the LLM function
def llm(role, put):
    prompt = ChatPromptTemplate.from_messages([
        ("system", role),
        ("human", put)
    ])
    variables = {
        "TASK": [],
        "REMINDER": [],
        "NOTE": []
    }  # Initialize variables with empty lists
    chain = prompt | chat
    result = chain.invoke(variables).content.strip()
    return result

# Extract task prompt
Ext_todo = f"""
        You are Azmth. A very intelligent, context-aware personal AI assistant to the human named: {user_name}.
        Here are the instructions you need to follow:
        1. The provided text is a natural language transcription at time {curr_time}. This is for your context awareness.
        2. Extract To-Do tasks, reminders, and notes from the input.
        3. Format the result as JSON, with separate categories for TASK, REMINDER, and NOTE.
        Example Output: JSON only.
        If no input is provided, or if there's a problem, return 'None' for all categories.
        You are permitted to only return JSON or 'None'. Do not add anything else at any cost.
        If tasks are found, return JSON or in every other case, return None.
"""

# Route to handle requests from the frontend
@app.route('/endpoint', methods=['POST'])
def handle_request():
    try:
        data = request.json
        print(data['message'])
        input_text = data['message']
        if not input_text:
            return jsonify({"error": "Please provide input_text in the request body."}), 400

        # Call the LLM function with the provided input
        response = llm(Ext_todo, input_text)
        # Log the response to the terminal
        print(f"Response sent to frontend: {response}")

        # Return the LLM response as JSON
        return jsonify({"response": response})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)