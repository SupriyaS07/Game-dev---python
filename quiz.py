import tkinter as tk
from tkinter import messagebox
import pygame

# Quiz Questions - 10 for each level
quiz_data = {
    "easy": [
        {"question": "What is the output of print(3 + 2)?", "options": ["32", "5", "23", "Error"], "answer": "5"},
        {"question": "Which keyword is used to define a function?", "options": ["func", "define", "def", "function"], "answer": "def"},
        {"question": "What is the output of print(len('hello'))?", "options": ["4", "5", "6", "None"], "answer": "5"},
        {"question": "What symbol is used for comments in Python?", "options": ["//", "#", "--", "/*"], "answer": "#"},
        {"question": "Which data type is used to store text?", "options": ["int", "str", "list", "bool"], "answer": "str"},
        {"question": "Which method converts string to uppercase?", "options": ["capitalize()", "upper()", "toupper()", "toUpperCase()"], "answer": "upper()"},
        {"question": "How do you insert comments in Python?", "options": ["<!-- -->", "#", "//", "/* */"], "answer": "#"},
        {"question": "What is 10 // 3 in Python?", "options": ["3.3", "3", "3.0", "Error"], "answer": "3"},
        {"question": "What will print(type(5)) display?", "options": ["<class 'int'>", "<int>", "int", "number"], "answer": "<class 'int'>"},
        {"question": "How do you start a while loop?", "options": ["loop while", "while (x > 5)", "while x > 5:", "whle x > 5"], "answer": "while x > 5:"}
    ],
    "intermediate": [
        {"question": "What does len() return?", "options": ["Memory size", "Length of object", "File size", "Number type"], "answer": "Length of object"},
        {"question": "Which data type is mutable?", "options": ["tuple", "str", "int", "list"], "answer": "list"},
        {"question": "What is the result of 2 ** 3?", "options": ["6", "8", "9", "4"], "answer": "8"},
        {"question": "What is the correct way to open a file?", "options": ["file = open('test.txt')", "file.open('test.txt')", "open file 'test.txt'", "file = open.file('test.txt')"], "answer": "file = open('test.txt')"},
        {"question": "Which operator checks equality?", "options": ["=", "==", "!=", "==="], "answer": "=="},
        {"question": "What is a dictionary in Python?", "options": ["A list", "Key-value pairs", "Tuple", "String"], "answer": "Key-value pairs"},
        {"question": "Which keyword is used to handle exceptions?", "options": ["try", "except", "error", "raise"], "answer": "except"},
        {"question": "How do you import a module?", "options": ["import.module()", "load module", "import math", "using math"], "answer": "import math"},
        {"question": "What will print(list('abc')) return?", "options": ["['abc']", "['a', 'b', 'c']", "abc", "('a','b','c')"], "answer": "['a', 'b', 'c']"},
        {"question": "What is the output of bool('False')?", "options": ["False", "Error", "True", "None"], "answer": "True"}
    ],
    "hard": [
        {"question": "What is the output of [i**2 for i in range(3)]?", "options": ["[1,2,3]", "[0,1,4]", "[0,2,4]", "[1,4,9]"], "answer": "[0,1,4]"},
        {"question": "How do you inherit a class?", "options": ["include", "inherit", "super", "class Sub(Base)"], "answer": "class Sub(Base)"},
        {"question": "What is a lambda in Python?", "options": ["A function", "A loop", "A string", "A list"], "answer": "A function"},
        {"question": "What does the zip() function do?", "options": ["Combines iterables", "Sorts items", "Compresses files", "Encrypts strings"], "answer": "Combines iterables"},
        {"question": "What will set([1,2,2,3]) return?", "options": ["[1,2,3]", "{1,2,2,3}", "{1,2,3}", "[1,2,2,3]"], "answer": "{1,2,3}"},
        {"question": "What is the result of {'a':1}['b']?", "options": ["1", "KeyError", "None", "b"], "answer": "KeyError"},
        {"question": "Which is correct syntax for list comprehension?", "options": ["[x for x in range(5)]", "{x for x in range(5)}", "(x for x in range(5))", "All of the above"], "answer": "All of the above"},
        {"question": "What does @staticmethod do?", "options": ["Creates class method", "Creates static method", "Nothing", "Starts a thread"], "answer": "Creates static method"},
        {"question": "What is the purpose of __init__?", "options": ["Create method", "Create object", "Constructor", "Import class"], "answer": "Constructor"},
        {"question": "What does 'with open('file.txt') as f:' do?", "options": ["Open file", "Automatically closes file", "Raises error if file missing", "All of the above"], "answer": "All of the above"}
    ]
}

# Quiz App Class
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Python Quiz Game")
        self.root.geometry("600x500")
        self.root.configure(bg="#f5f5f5")  # light background
        pygame.mixer.init()
        pygame.mixer.music.load("background music.mp3")  # Replace with your music file name
        pygame.mixer.music.play(-1)  # -1 means loop forever

        self.level = None
        self.question_index = 0
        self.score = 0
        self.timer_label = None
        self.time_left = 10
        self.timer_running = False

        self.intro_screen()

    def intro_screen(self):
        self.clear_screen()
        title = tk.Label(self.root, text="Python Quiz Game", font=("Helvetica", 24, "bold"), bg="#f5f5f5", fg="#333")
        title.pack(pady=40)

        for level, color in zip(["Easy", "Intermediate", "Hard"], ["#4CAF50", "#2196F3", "#FF5722"]):
            btn = tk.Button(self.root, text=level, font=("Arial", 16), bg=color, fg="white", width=20,
                            relief="flat", command=lambda lvl=level.lower(): self.start_quiz(lvl))
            btn.pack(pady=10)

    def start_quiz(self, level):
        self.level = level
        self.question_index = 0
        self.score = 0
        self.display_question()

    def display_question(self):
        self.clear_screen()
        self.time_left = 10
        self.timer_running = True

        if self.question_index >= len(quiz_data[self.level]):
            self.end_quiz()
            return

        question_data = quiz_data[self.level][self.question_index]

        question_label = tk.Label(self.root,
                                  text=f"Q{self.question_index + 1}: {question_data['question']}",
                                  wraplength=500, font=("Arial", 18, "bold"),
                                  bg="#f5f5f5", fg="#333")
        question_label.pack(pady=30)

        self.timer_label = tk.Label(self.root, text=f"⏳ Time Left: {self.time_left}s", font=("Arial", 14, "bold"),
                                    fg="#e91e63", bg="#f5f5f5")
        self.timer_label.pack(pady=5)

        for option in question_data['options']:
            btn = tk.Button(self.root, text=option, font=("Arial", 14), bg="#ffffff", fg="#333",
                            activebackground="#d3d3d3", relief="solid", borderwidth=1, width=40,
                            command=lambda opt=option: self.check_answer(opt))
            btn.pack(pady=8)

        self.update_timer()

    def update_timer(self):
        if self.time_left > 0 and self.timer_running:
            self.time_left -= 1
            self.timer_label.config(text=f"⏳ Time Left: {self.time_left}s")
            self.root.after(2000, self.update_timer)
        elif self.time_left == 0:
            self.timer_running = False
            messagebox.showinfo("Time's Up", "⏰ You ran out of time!")
            self.next_question()

    def check_answer(self, selected_option):
        correct_answer = quiz_data[self.level][self.question_index]['answer']
        self.timer_running = False

        if selected_option == correct_answer:
            self.score += 1

        self.next_question()

    def next_question(self):
        self.question_index += 1
        self.display_question()

    def end_quiz(self):
        self.clear_screen()
        result_msg = f"🎉 You scored {self.score} out of {len(quiz_data[self.level])}!"
        messagebox.showinfo("Quiz Complete", result_msg)
        self.intro_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
