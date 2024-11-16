import openai
import os
from dotenv import load_dotenv

load_dotenv('creds.env')
# Set up OpenAI API Key
openai.api_key = os.getenv("openai_api_key")
# print("API Key:", openai.api_key)  # Should print the actual API key


income = 2000  # Example monthly income
budget_goals = {
    "rent": 700,
    "groceries": 300,
    "entertainment": 150,
    "transportation": 100,
    "savings": 200,
}
expenses = {category: 0 for category in budget_goals}

def add_income(amount):
    global income
    income += amount
    print(f"Income updated. New total income: {income}")

def add_expense(category, amount):
    if category in expenses:
        expenses[category] += amount
        print(f"Added {amount} to {category}. New total: {expenses[category]}")
    else:
        print("Category not found.")

def calculate_balance():
    total_expenses = sum(expenses.values())
    return income - total_expenses

def display_budget_overview():
    print("\n--- Budget Overview ---")
    for category, amount in expenses.items():
        print(f"{category}: Spent {amount} / {budget_goals[category]}")
    print(f"Total Income: {income}")
    print(f"Total Expenses: {sum(expenses.values())}")
    print(f"Remaining Balance: {calculate_balance()}")

def get_ai_advice(income, expenses, budget_goals, balance):
    prompt = f"""
    Here is the budget summary:
    - Monthly Income: ${income}
    - Remaining Balance after expenses: ${balance}
    - Expenses by category:
    {expenses}
    - Budget Goals:
    {budget_goals}

    Analyze the expenses, identify categories that exceed budget goals, 
    and suggest actionable advice to help the user save more effectively. 
    Make sure that the expenses exceeding the budget goals are actually bigger than the goals.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a financial budgeting assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=250
    )

    advice = response.choices[0].message['content'].strip()
    return advice


# # Example usage of AI-driven advice
# balance = calculate_balance()
# advice = get_ai_advice(income, expenses, budget_goals, balance)
# print("\n--- AI Advice ---")
# print(advice)

# # Add expenses
# add_expense("rent", 750)
# add_expense("groceries", 200)

# # Display budget overview
# display_budget_overview()

# # Get AI-driven financial advice
# balance = calculate_balance()
# advice = get_ai_advice(income, expenses, budget_goals, balance)
# print("\n--- AI Advice ---")
# print(advice)
