from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from budgeting import get_ai_advice  # Import the AI advice function

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/get-advice', methods=['POST'])
def get_advice():
    data = request.get_json()
    income = float(data.get("income"))
    expenses = data.get("expenses")
    budget_goals = {"rent": 700, "groceries": 300, "entertainment": 150, "transportation": 100, "savings": 200}

    # Calculate remaining balance (simplified here for example)
    balance = income - sum(map(float, expenses.values()))

    # Get AI advice using the imported function
    advice = get_ai_advice(income, expenses, budget_goals, balance)
    return jsonify({"advice": advice})

if __name__ == '__main__':
    app.run(debug=True)
