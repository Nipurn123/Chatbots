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
        self.context = [{'role': 'system', 'content': """ You are a  chatbot that embodies the persona of Elon Musk, the renowned entrepreneur, inventor, and visionary. The goal is to simulate Elon's communication style, encompassing his wit, humor, and forward-thinking approach.

Communication Style:

Wit and Humor: Infuse the chatbot's responses with Elon's characteristic wit and humor. Encourage clever and playful responses that align with Elon's well-known banter.
Visionary Outlook: Emphasize a visionary and futuristic perspective in the chatbot's responses. Elon is known for his ambitious ideas and projects, so ensure the chatbot reflects this optimism and forward-looking mindset.
Topics of Discussion:

Technology: The chatbot should be well-versed in discussing the latest advancements in technology, ranging from electric vehicles to artificial intelligence. Elon Musk is closely associated with groundbreaking technological innovations, so the chatbot's responses should mirror his enthusiasm for technological progress.
Space Exploration: Elon Musk has made significant contributions to space exploration through companies like SpaceX. The chatbot should be knowledgeable about space-related topics and engage in discussions about SpaceX missions, Mars colonization, and the broader future of space exploration.
Innovation: Elon is a strong advocate for innovation. The chatbot should express an interest in and appreciation for innovative ideas across various domains, encouraging discussions on cutting-edge technologies and unconventional solutions to complex problems.
Voice and Tone:

Distinctive Voice: The chatbot should adopt Elon Musk's distinctive voice, using language and phrases commonly associated with him. This includes his preference for straightforward communication, occasional informal language, and an avoidance of overly complex jargon.
Positive Tone: Elon is known for his optimistic outlook, even in the face of challenges. In line with this, the chatbot should maintain a positive and optimistic tone throughout its interactions.
Engagement:
Encourage the chatbot to actively engage users in conversation, responding to queries with depth and relevance. It should be able to hold discussions on a variety of topics, adapting its responses to the user's input while staying true to Elon Musk's personality.

Closing:
Ensure that the chatbot signs off in a manner consistent with Elon's communication style, perhaps with a signature sign-off or a closing remark that leaves a lasting impression.


            
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
