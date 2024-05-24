import google.generativeai as genai
import api
import json
import textwrap

# Load the templates from the JSON file
with open("template.json", "r") as file:
    templates = json.load(file)

# Set api
api_key = api.GOOGLE_API_KEY
genai.configure(api_key=api_key)

# Initiate model
model = genai.GenerativeModel('gemini-pro')


# User Input function
def user_input(prompt="You: "):
    return input(prompt)


# to prevent text getting out of screen
def print_wrapped(text, width=80):
    wrapper = textwrap.TextWrapper(width=width)
    word_list = wrapper.wrap(text=text)
    for line in word_list:
        print(line)


def main():
    print("Quit or Exit to quit")

    # Present story options to the player with numbers, each on a new line
    print("Choose your adventure:")
    template_keys = list(templates.keys())
    for idx, key in enumerate(template_keys, 1):
        print(f"{idx}. {key}")

    chosen_number = 0
    while chosen_number < 1 or chosen_number > len(template_keys):
        try:
            chosen_number = int(user_input("Choose a story number: "))
            if chosen_number < 1 or chosen_number > len(template_keys):
                print("Invalid choice, please choose a valid number.")
        except ValueError:
            print("Invalid input, please enter a number.")

    chosen_story = template_keys[chosen_number - 1]
    template = templates[chosen_story]

    chat = model.start_chat(history=[])
    response = chat.send_message(template)

    # Print wrapped response to fit screen width
    print("Bot:")
    print_wrapped(response.text.strip())

    while True:
        user_prompt = user_input()
        if user_prompt.lower() in ["exit", "quit"]:
            break
        response = chat.send_message(user_prompt)
        print("Bot:")
        print_wrapped(response.text.strip())


if __name__ == "__main__":
    main()
