import tkinter as tk
from tkinter import messagebox
import random

# Colors and styles
BG_COLOR = "#1e1e2f"
BTN_COLOR = "#4e4e7a"
BTN_HOVER = "#6e6eb5"
TEXT_COLOR = "#ffffff"
FONT = ("Helvetica", 14, "bold")

choices = ["Rock", "Paper", "Scissors"]

class RPSGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("600x500")
        self.root.configure(bg=BG_COLOR)
        self.user_score = 0
        self.computer_score = 0
        self.target_score = 3

        self.setup_widgets()

    def setup_widgets(self):
        # Title
        title = tk.Label(self.root, text="🎮 Rock Paper Scissors", font=("Helvetica", 20, "bold"), bg=BG_COLOR, fg="#ffcc00")
        title.pack(pady=10)

        # Target score entry
        target_frame = tk.Frame(self.root, bg=BG_COLOR)
        target_frame.pack(pady=10)
        tk.Label(target_frame, text="Set Target Score:", font=FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(side="left")
        self.target_entry = tk.Entry(target_frame, font=FONT, width=5)
        self.target_entry.insert(0, "3")
        self.target_entry.pack(side="left", padx=5)
        set_btn = self.create_button(target_frame, "Set", self.set_target)
        set_btn.pack(side="left", padx=10)

        # Choices Frame
        self.choices_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.choices_frame.pack(pady=20)

        self.rock_btn = self.create_button(self.choices_frame, "🪨 Rock", lambda: self.play("Rock"))
        self.paper_btn = self.create_button(self.choices_frame, "📄 Paper", lambda: self.play("Paper"))
        self.scissors_btn = self.create_button(self.choices_frame, "✂️ Scissors", lambda: self.play("Scissors"))

        self.rock_btn.grid(row=0, column=0, padx=10)
        self.paper_btn.grid(row=0, column=1, padx=10)
        self.scissors_btn.grid(row=0, column=2, padx=10)

        # Result Display
        self.result_text = tk.Label(self.root, text="", font=("Helvetica", 16), bg=BG_COLOR, fg="#00ffaa")
        self.result_text.pack(pady=20)

        # Score display
        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=FONT, bg=BG_COLOR, fg="#ffffff")
        self.score_label.pack(pady=5)

    def create_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, font=FONT, bg=BTN_COLOR, fg=TEXT_COLOR,
                        activebackground=BTN_HOVER, activeforeground="#fff", bd=0,
                        relief="raised", padx=20, pady=10, command=command)
        btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=BTN_COLOR))
        btn.config(cursor="hand2")
        return btn

    def set_target(self):
        try:
            value = int(self.target_entry.get())
            if value > 0:
                self.target_score = value
                messagebox.showinfo("Target Set", f"Target score set to {value}")
            else:
                raise ValueError
        except:
            messagebox.showerror("Invalid", "Enter a valid positive number")

    def play(self, user_choice):
        comp_choice = random.choice(choices)
        result = ""

        if user_choice == comp_choice:
            result = f"Tie! Both chose {user_choice}"
        elif (user_choice == "Rock" and comp_choice == "Scissors") or \
             (user_choice == "Paper" and comp_choice == "Rock") or \
             (user_choice == "Scissors" and comp_choice == "Paper"):
            self.user_score += 1
            result = f"You Win! {user_choice} beats {comp_choice}"
        else:
            self.computer_score += 1
            result = f"You Lose! {comp_choice} beats {user_choice}"

        self.result_text.config(text=result)
        self.score_label.config(text=self.get_score_text())

        if self.user_score == self.target_score or self.computer_score == self.target_score:
            winner = "You" if self.user_score == self.target_score else "Computer"
            messagebox.showinfo("🎉 Final Winner", f"{winner} wins the game!")
            self.user_score = 0
            self.computer_score = 0
            self.score_label.config(text=self.get_score_text())
            self.result_text.config(text="")

    def get_score_text(self):
        return f"👤 You: {self.user_score}   🤖 Computer: {self.computer_score}   🎯 Target: {self.target_score}"

# Run the Game
if __name__ == "__main__":
    root = tk.Tk()
    game = RPSGame(root)
    root.mainloop()
