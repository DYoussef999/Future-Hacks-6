import json
from difflib import get_close_matches
import tkinter as tk
from tkinter import scrolledtext

# Load knowledge base
def load_knowledge_base(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
        return data
    except FileNotFoundError:
        return {"questions": []}

# Save knowledge base
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Find best match for user input
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Get answer for question from knowledge base
def get_answer_for_question(question:str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

# Chat bot function
def chat_bot(user_input: str, knowledge_base: dict, chat_box: scrolledtext.ScrolledText):
    # find best match to user input
    best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    # if there exists a response appropriate to question, then use it... else ask user to teach
    if best_match:
        answer: str = get_answer_for_question(best_match, knowledge_base)
        chat_box.configure(state='normal')
        chat_box.tag_configure('bot', foreground='#2c3e50', font=('Arial', 10, 'bold'))
        chat_box.insert(tk.END, 'Bot: ', 'bot')
        chat_box.insert(tk.END, f'{answer}\n')
        chat_box.configure(state='disabled')
    else:
        chat_box.configure(state='normal')
        chat_box.tag_configure('bot', foreground='#2c3e50', font=('Arial', 10, 'bold'))
        chat_box.insert(tk.END, 'Bot: ', 'bot')
        chat_box.insert(tk.END, 'I cannot find an answer to this question in my database.\n')
        chat_box.configure(state='disabled')

# Reset chat function
def reset_chat(chat_box: scrolledtext.ScrolledText):
    chat_box.configure(state='normal')
    chat_box.delete('1.0', tk.END)
    chat_box.configure(state='disabled')

# GUI function
def create_gui():
    root = tk.Tk()
    root.title("Healthy Chatbot")
    root.configure(bg='#27ae60')

    frame = tk.Frame(root, bg='#27ae60')
    frame.pack(fill=tk.BOTH, expand=True)

    chat_box = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state='disabled', bg='#ffffff', fg='#2c3e50', font=('Arial', 10))
    chat_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    entry = tk.Entry(frame, bg='#ffffff', fg='#2c3e50', font=('Arial', 10))
    entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    entry.bind("<Return>", lambda event: send_message())

    reset_button = tk.Button(frame, text="Reset Chat", command=lambda: reset_chat(chat_box), bg='#ff6347', fg='#ffffff', font=('Arial', 10, 'bold'))
    reset_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    entry.focus()

    # Configure row to scale with window size
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=0)
    frame.grid_rowconfigure(2, weight=0)

    # Configure column to scale with window size
    frame.grid_columnconfigure(0, weight=1)

    knowledge_base = load_knowledge_base('knowledge_base.json')

    def send_message():
        user_input = entry.get()
        if user_input:
            chat_box.configure(state='normal')
            chat_box.tag_configure('you', foreground='#e67e22', font=('Arial', 10, 'bold'))
            chat_box.insert(tk.END, 'You: ', 'you')
            chat_box.insert(tk.END, f'{user_input}\n')
            chat_bot(user_input, knowledge_base, chat_box)
            chat_box.configure(state='disabled')
            entry.delete(0, tk.END)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
