import tkinter as tk
from tkinter import messagebox

# Quiz questions and answers
quiz_data = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"],
        "answer": "Paris"
    },
    {
        "question": "What is the largest planet in our solar system?",
        "options": ["Earth", "Jupiter", "Mars", "Saturn"],
        "answer": "Jupiter"
    },
    {
        "question": "Which element has the chemical symbol 'O'?",
        "options": ["Oxygen", "Gold", "Osmium", "Oganesson"],
        "answer": "Oxygen"
    },
    {
        "question": "Who wrote '1984'?",
        "options": ["George Orwell", "Aldous Huxley", "J.K. Rowling", "Mark Twain"],
        "answer": "George Orwell"
    }
]


class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("400x300")
        self.score = 0
        self.question_index = 0

        self.question_label = tk.Label(root, text="", wraplength=350)
        self.question_label.pack(pady=20)

        self.option_var = tk.StringVar()

        self.option_buttons = []
        for _ in range(4):
            button = tk.Radiobutton(root, text="", variable=self.option_var, value="")
            button.pack(anchor=tk.W)
            self.option_buttons.append(button)

        self.submit_button = tk.Button(root, text="Submit", command=self.check_answer)
        self.submit_button.pack(pady=20)

        self.load_question()

    def load_question(self):
        current_question = quiz_data[self.question_index]
        self.question_label.config(text=current_question["question"])
        self.option_var.set(None)

        for i, option in enumerate(current_question["options"]):
            self.option_buttons[i].config(text=option, value=option)

    def check_answer(self):
        selected_option = self.option_var.get()
        if selected_option == "":
            messagebox.showwarning("Warning", "Please select an option")
            return

        current_question = quiz_data[self.question_index]
        if selected_option == current_question["answer"]:
            self.score += 1

        self.question_index += 1

        if self.question_index < len(quiz_data):
            self.load_question()
        else:
            self.show_result()

    def show_result(self):
        messagebox.showinfo("Quiz Over", f"Your score is: {self.score}/{len(quiz_data)}")
        self.root.quit()


# Create the main window
root = tk.Tk()
quiz_game = QuizGame(root)
root.mainloop()
