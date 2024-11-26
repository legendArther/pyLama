import tkinter as tk
from tkinter import scrolledtext
import os
from dotenv import load_dotenv
import replicate

# Load environment variables
load_dotenv()

# Get API token from .env
API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

if not API_TOKEN:
    raise ValueError("REPLICATE_API_TOKEN not found in .env file")

# Authenticate with Replicate
replicate.Client(api_token=API_TOKEN)

# Function to handle chat interactions
def send_message():
    user_input = input_box.get("1.0", "end").strip()
    if not user_input:
        return
    
    input_box.delete("1.0", "end")
    
    # Display user input
    chat_box.config(state="normal")
    chat_box.insert(tk.END, f"You: {user_input}\n")
    
    # Prepare input for the model
    input_data = {
        "prompt": user_input,
        "max_new_tokens": 512,
        "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
                           "{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
                           "{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
    }
    
    try:
        # Run the model on Replicate
        output = replicate.run("meta/meta-llama-3-8b-instruct", input=input_data)
        bot_reply = "".join(output)
    except Exception as e:
        bot_reply = f"Error: {str(e)}"
    
    # Display bot reply
    chat_box.insert(tk.END, f"Bot: {bot_reply}\n")
    chat_box.config(state="disabled")
    chat_box.see(tk.END)

# Create the main application window
root = tk.Tk()
root.title("Chatbot App")

# Chat display
chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="normal", width=50, height=20)
chat_box.pack(pady=10)
chat_box.insert(tk.END, "Bot: Hi! How can I assist you today?\n")
chat_box.config(state="disabled")

# User input box
input_box = tk.Text(root, height=3, width=50)
input_box.pack(pady=5)

# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

# Start the GUI loop
root.mainloop()
