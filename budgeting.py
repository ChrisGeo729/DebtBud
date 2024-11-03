import openai
import os

# Set up OpenAI API Key
api_key = os.getenv("api_key")
print(api_key)

# def get_ai_advice(expenses, budget_goals, balance):
#     # Prepare the prompt
#     prompt = f"""
#     Here is the budget summary:
#     - Monthly Income: {income}
#     - Total Remaining Balance: {balance}
#     - Expenses:
#     {expenses}
#     - Budget Goals:
#     {budget_goals}

#     Based on this data, provide advice on how to manage the budget better, 
#     identify areas to save more, and suggest financial strategies or insights for the user.
#     """

#     # Call OpenAI's API to get the response
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=150
#     )

#     return response.choices[0].text.strip()
