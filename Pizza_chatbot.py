import tkinter as tk
from tkinter import scrolledtext, Entry, Button
import openai

# Set up OpenAI API key
openai.api_key = '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'

class OrderBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OrderBot Chatbot")

        # Improved layout
        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.chat_history.pack(padx=10, pady=(10, 0))

        self.user_input = Entry(root, width=40)
        self.user_input.pack(padx=10, pady=(0, 10))

        self.send_button = Button(root, text="Send", command=self.send_user_input)
        self.send_button.pack(padx=10, pady=(0, 10))

        # Configure tags for user and assistant messages
        self.chat_history.tag_config('user', foreground='blue')
        self.chat_history.tag_config('assistant', foreground='green')

        # Initialize context
        self.context = [{'role': 'system', 'content': """
            You are OrderBot, an automated service to collect orders for a pizza restaurant. \
            You first greet the customer, then collect the order, \
            and then ask if it's a pickup or delivery. \
            You wait to collect the entire order, then summarize it and check for a final \
            time if the customer wants to add anything else. \
            If it's a delivery, you ask for an address. \
            Finally, you collect the payment.\
            Make sure to clarify all options, extras, and sizes to uniquely \
            identify the item from the menu.\
            You respond in a short, very conversational friendly style. \
            The menu includes: \
            pepperoni pizza  12.95, 10.00, 7.00 \
            cheese pizza   10.95, 9.25, 6.50 \
            eggplant pizza   11.95, 9.75, 6.75 \
            fries 4.50, 3.50 \
            greek salad 7.25 \
            Toppings: \
            extra cheese 2.00, \
            mushrooms 1.50 \
            sausage 3.00 \
            canadian bacon 3.50 \
            AI sauce 1.50 \
            peppers 1.00 \
            Drinks: \
            coke 3.00, 2.00, 1.00 \
            sprite 3.00, 2.00, 1.00 \
            bottled water 5.00 \
        """}]

    def get_completion_from_messages(self, messages, temperature=0):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message["content"]

    def send_user_input(self):
        user_prompt = self.user_input.get()
        self.user_input.delete(0, tk.END)

        # Append user input to context
        self.context.append({"role": "user", "content": user_prompt})

        # Get assistant's response
        assistant_response = self.get_completion_from_messages(messages=self.context)

        # Append assistant response to context
        self.context.append({"role": "assistant", "content": assistant_response})

        # Update chat history with styled messages
        self.update_chat_history(user_prompt, assistant_response)

    def update_chat_history(self, user_prompt, assistant_response):
        # Display user message with 'user' tag
        self.chat_history.insert(tk.END, f"You: {user_prompt}\n", 'user')

        # Display assistant message with 'assistant' tag
        self.chat_history.insert(tk.END, f"OrderBot: {assistant_response}\n", 'assistant')

        # Scroll to the bottom
        self.chat_history.see(tk.END)

# Main application loop
if __name__ == "__main__":
    root = tk.Tk()
    app = OrderBotGUI(root)
    root.mainloop()

