from flask import Flask, request, jsonify
from flask_cors import CORS
from budgeting import get_ai_advice

app = Flask(__name__)
CORS(app)

@app.route('/get-advice', methods=['POST'])
def get_advice():
    data = request.get_json()
    income = float(data.get("income"))
    expenses = data.get("expenses")
    budget_goals = data.get("budgetGoals")  # Use budget goals from the request

    # Calculate remaining balance
    balance = income - sum(map(float, expenses.values()))

    # Get AI advice using the imported function
    advice = get_ai_advice(income, expenses, budget_goals, balance)
    return jsonify({"advice": advice})

if __name__ == '__main__':
    app.run(debug=True)
