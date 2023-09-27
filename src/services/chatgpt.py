import openai

api_key = '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'  # replace YOUR_API_KEY with your actual API key

# Authenticate with the OpenAI API
openai.api_key = api_key

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1024,
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    # Code in this block will only be run when chatgpt.py is executed directly, not when it is imported as a module.
    prompt = input("Enter a prompt: ")
    print(generate_response(prompt))
