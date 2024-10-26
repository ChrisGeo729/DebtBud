import openai

# Set up OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

def get_ai_advice(expenses, budget_goals, balance):
    # Prepare the prompt
    prompt = f"""
    Here is the budget summary:
    - Monthly Income: {income}
    - Total Remaining Balance: {balance}
    - Expenses:
    {expenses}
    - Budget Goals:
    {budget_goals}

    Based on this data, provide advice on how to manage the budget better, 
    identify areas to save more, and suggest financial strategies or insights for the user.
    """

    # Call OpenAI's API to get the response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    return response.choices[0].text.strip()
