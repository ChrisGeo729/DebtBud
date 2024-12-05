from flask import Flask, request, jsonify
from flask_cors import CORS
from budgeting import get_ai_advice
import openai
import os
from openai.embeddings_utils import cosine_similarity

app = Flask(__name__)
CORS(app)

# Set OpenAI API key
openai.api_key = os.getenv("openai_api_key")

# Predefined topics for semantic validation
PREDEFINED_TOPICS = [
    "loan repayment", "interest rates", "loan term", "monthly payments",
    "budgeting", "debt management", "financial planning", "student loans",
    "budgeting tool", "loan repayment calculator", "community forum"
]

def get_embedding(text):
    """
    Get an embedding for the given text using OpenAI's API.
    """
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

def is_query_valid_semantic(user_message):
    """
    Validate the user's message using semantic similarity to predefined topics.
    """
    try:
        user_embedding = get_embedding(user_message)
        topic_embeddings = [get_embedding(topic) for topic in PREDEFINED_TOPICS]
        similarities = [cosine_similarity(user_embedding, topic_embedding) for topic_embedding in topic_embeddings]
        threshold = 0.75  # Adjust for sensitivity
        return any(similarity > threshold for similarity in similarities)
    except Exception as e:
        print(f"Error in semantic validation: {e}")
        return False


@app.route('/get-advice', methods=['POST'])
def get_advice():
    data = request.get_json()

    # Debugging print statements to inspect incoming data
    print("Received Payload:", data)

    income = float(data.get("income", 0))
    expenses = data.get("expenses", {})
    budget_goals = data.get("budget_goals", {})  # Use correct key

    # Debugging print statements to inspect parsed data
    print("Income:", income)
    print("Expenses:", expenses)
    print("Budget Goals:", budget_goals)

    # Calculate remaining balance
    balance = income - sum(map(float, expenses.values()))
    print("Calculated Balance:", balance)

    # Get AI advice using the imported function
    advice = get_ai_advice(income, expenses, budget_goals, balance)
    return jsonify({"advice": advice})



@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Use semantic validation to check query relevance
    if not is_query_valid_semantic(user_message):
        return jsonify({
            "message": "Hi there! 😊 I'm here to assist with loan repayment planning, budgeting, and financial advice. "
                       "If you have questions about these topics or need help navigating the DebtBud website, feel free to ask!"
        })

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful, friendly, and professional financial assistant. Your role is to guide users through the resources "
                        "and tools available on the DebtBud website. Specifically, you can assist with:\n"
                        "1. Loan repayment planning.\n"
                        "2. Budgeting and financial advice.\n"
                        "3. Debt management strategies.\n"
                        "4. Understanding features like the budgeting tool, loan repayment calculator, and community forum.\n\n"
                        "When asked, provide clear and concise instructions for navigating these features on the website. "
                        "Always stay within the scope of the website's content and avoid speculation or irrelevant topics. "
                        "Be friendly and approachable, using a conversational tone."
                    )
                },
                {"role": "user", "content": user_message}
            ],
            temperature=0.5,
        )
        ai_message = response['choices'][0]['message']['content']
        if "REDIRECT_TO:" in ai_message:
            redirect_url = ai_message.split("REDIRECT_TO:")[-1].strip()
            return jsonify({"message": ai_message, "redirect_url": redirect_url})
        else:
            return jsonify({"message": ai_message})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Something went wrong on my end. Please try again later!"}), 500


if __name__ == '__main__':
    app.run(debug=True)
