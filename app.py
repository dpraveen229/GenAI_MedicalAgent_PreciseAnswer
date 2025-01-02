import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Home route to display the UI
@app.route("/")
def home():
    return render_template("index.html")

# API endpoint to handle user input
@app.route("/process_input", methods=["POST"])
def process_input():
    data = request.json
    name = data.get("name")
    age = data.get("age")
    state = data.get("state")
    country = data.get("country")
    medical_problem = data.get("medical_problem")

    # Generate the dynamic prompt
    prompt = (f"A {age}-year-old patient from {state}, {country} is experiencing {medical_problem}. "
              "Provide advice in simple terms suitable for the patient."
              "Answer must be very precise and easy to understand and answer must be within 100 words.")
    
    print(f"Prompt: {prompt}")

    try:
        # Send the prompt to OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Use a valid OpenAI model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7, 
        )
        
        # Return the generated response from OpenAI
        return jsonify({"response": response['choices'][0]['message']['content']})

    except Exception as e:
        # Log the error message and return a 500 response
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)