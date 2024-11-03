from flask import Flask, request, jsonify
from budgeting import get_ai_advice  # Import the function from budgeting.py

app = Flask(__name__)

@app.route('/get-advice', methods=['POST'])
def get_advice():
    data = request.get_json()
    income = data.get("income")
    expenses = data.get("expenses")
    budget_goals = data.get("budget_goals")
    balance = data.get("balance")

    # Use the imported function from budgeting.py
    advice = get_ai_advice(income, expenses, budget_goals, balance)
    return jsonify({"advice": advice})

if __name__ == '__main__':
    app.run(debug=True)
