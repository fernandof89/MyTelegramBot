import openai

api_key = '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'  # replace YOUR_API_KEY with your actual API key

# Authenticate with the OpenAI API
openai.api_key = api_key

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response['choices'][0]['message']['content']


if __name__ == "__main__":
    # Code in this block will only be run when chatgpt.py is executed directly, not when it is imported as a module.
    prompt = input("Enter a prompt: ")
    print(generate_response(prompt))





