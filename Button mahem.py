""" This version adds file handling I decided to use messafebox from tikinter as it is way more simpler and had less issues when using it for data entry"""

import random
import tkinter as tk
from tkinter import messagebox, simpledialog


# -------------------------------------------------- #
#                       MAIN                         #
# -------------------------------------------------- #
class main:

    def __init__(self, root):
        self.root = root
        self.root.title("button mayhem")
        self.root.geometry("400x560")

        # ---------------- Variables ---------------- #
        # Board
        self.total_buttons = 6
        self.max_level = 5

        # File handling & User
        self.username = ""
        self.score_file = "score.txt"

        # Progression
        self.current_level = 1
        self.losing_index = []
        self.safe_clicks_count = 0
        self.active_buttons = {}

        # Score & Streaks
        self.current_score = 0
        self.current_streak = 0
        self.best_streak = 0

        # Timer and timeout
        self.timeout_seconds = 3
        self.seconds_remaining = 3
        self.timer_job = None
        self.timer_active = False

        # Get user details & saved high score
        self.get_valid_username()
        self.load_high_score()

        # Save data on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Make UI
        self.setup_ui()

        # Make first game
        self.start_new_game()

    # -------------------------------------------------- #
    #               File Handling                        #
    # -------------------------------------------------- #
    def get_valid_username(self):
        #asks for username 
        while True:
            name = simpledialog.askstring(
                "Arigato!!! tuff civilian", "We want to know ur name inorder to sell it to the goverment for dabloons:"
            )

            if name is None:
                name = ""

            cleaned_name = name.strip()

            if cleaned_name:
                self.username = cleaned_name
                break
            else:
                messagebox.showwarning(
                    "Invalid Input",
                    "Username cannot be blank! Please try again.",
                )

    def load_high_score(self):
        """Loads saved best streak from score.txt for the current user."""
        try:
            with open(self.score_file, "r") as file:
                for line in file:
                    line = line.strip()
                    if ":" in line:
                        user, score = line.split(":", 1)
                        if user.strip() == self.username:
                            self.best_streak = int(score.strip())
        except (FileNotFoundError, ValueError):
            self.best_streak = 0

    def save_high_score(self):
        """Saves current player's best streak into score.txt without losing other users."""
        scores = {}

        # Read existing records
        try:
            with open(self.score_file, "r") as file:
                for line in file:
                    line = line.strip()
                    if ":" in line:
                        user, score = line.split(":", 1)
                        scores[user.strip()] = int(score.strip())
        except FileNotFoundError:
            pass

        # Update high score for current user
        prev_best = scores.get(self.username, 0)
        scores[self.username] = max(prev_best, self.best_streak)

        # Write all scores back to text file
        try:
            with open(self.score_file, "w") as file:
                for user, score in scores.items():
                    file.write(f"{user}:{score}\n")
        except OSError as e:
            print(f"Error saving score: {e}")

    def on_close(self):
        """Saves data and destroys window when user clicks X."""
        self.save_high_score()
        self.root.destroy()

    # -------------------------------------------------- #
    #                   UI                               #
    # -------------------------------------------------- #
    def setup_ui(self):
        """Create base OOP UI layout structure"""
        # header frame
        self.header_frame = tk.Frame(self.root, pady=10)
        self.header_frame.pack(fill="x")

        # Shows player name
        self.user_label = tk.Label(
            self.header_frame,
            text=f"Player: {self.username}",
            font=("Arial", 11, "italic"),
            fg="#333333",
        )
        self.user_label.pack()

        # Shows current level
        self.level_label = tk.Label(
            self.header_frame,
            text="LEVEL 1 / 5",
            font=("Arial", 14, "bold"),
            fg="#007bff",
        )
        self.level_label.pack()

        # Timeout
        self.timer_label = tk.Label(
            self.header_frame,
            text="Time Left: 3s",
            font=("Arial", 17, "bold"),
            fg="#dc3545",
        )
        self.timer_label.pack(pady=2)

        # streak tracker
        self.streak_label = tk.Label(
            self.header_frame,
            text=f"Streak: 0  |  Best: {self.best_streak}",
            font=("Arial", 12, "bold"),
            fg="#555555",
        )
        self.streak_label.pack()

        # scoreboard
        self.score_label = tk.Label(
            self.root, text="Score: 0", font=("Arial", 18, "bold"), fg="#111111"
        )
        self.score_label.pack(pady=5)

        self.status_label = tk.Label(
            self.root, text="Pick a button! Avoid the bomb.", font=("Arial", 14)
        )
        self.status_label.pack(pady=15)

        # make grid for btn
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(expand=True)

        self.control_frame = tk.Frame(self.root, pady=15)
        self.control_frame.pack(fill="x")

        # restart button
        self.restart_button = tk.Button(
            self.control_frame,
            text="Restart (Level 1)",
            font=("Arial", 11, "bold"),
            command=self.reset_to_start,
            bg="#f8f9fa",
        )
        self.restart_button.pack(side="left", padx=20)

        self.action_button = tk.Button(
            self.control_frame,
            text="Next Level",
            font=("Arial", 11, "bold"),
            command=self.handle_action_button,
            state="disabled",
            bg="#007bff",
            fg="white",
        )
        self.action_button.pack(side="right", padx=20)

    # -------------------------------------------------- #
    #                   Start Game                       #
    # -------------------------------------------------- #
    def start_new_game(self):
        self.safe_clicks_count = 0
        num_bombs = self.current_level
        total_safe = self.total_buttons - num_bombs

        # reset timer for each new board
        self.reset_timer()
        self.start_timer()

        # Update labels
        self.level_label.config(
            text=f"LEVEL {self.current_level} / {self.max_level}"
        )
        self.status_label.config(
            text=f"Find all {total_safe} safe buttons! ({num_bombs} bombs hidden)",
            fg="black",
        )
        self.action_button.config(text="Nxt lvl", state="disabled")

        # Pick losing buttons
        self.losing_index = random.sample(
            range(self.total_buttons), k=num_bombs
        )

        # Reset buttons grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.active_buttons.clear()

        for i in range(self.total_buttons):
            row = i // 3
            col = i % 3

            btn = tk.Button(
                self.grid_frame,
                text=f"Button {i + 1}",
                width=10,
                height=3,
                command=lambda idx=i: self.handle_click(idx),
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.active_buttons[i] = btn
                #For debuggin makes the losing button redish
        for idx in self.losing_index:
            self.active_buttons[idx].config(bg="#ffcccc")

    # -------------------------------------------------- #
    #                   Timer                            #
    # -------------------------------------------------- #
    def start_timer(self):
        if not self.timer_active:
            self.timer_active = True
            self.update_timer()

    def update_timer(self):
        """Count down from 3 => 0 seconds then pick a random button"""
        if self.timer_active:
            self.timer_label.config(
                text=f"Time Left: {self.seconds_remaining}s"
            )

            if self.seconds_remaining <= 0:
                self.auto_pick_random_button()
            else:
                self.seconds_remaining -= 1
                self.timer_job = self.root.after(1000, self.update_timer)

    def stop_timer(self):
        self.timer_active = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def reset_timer(self):
        self.stop_timer()
        self.seconds_remaining = self.timeout_seconds
        self.timer_label.config(text=f"Time Left: {self.timeout_seconds}s")

    def auto_pick_random_button(self):
        """Selects a random available (active) button on timeout"""
        available_indices = [
            idx
            for idx, btn in self.active_buttons.items()
            if btn["state"] != "disabled"
        ]

        if available_indices:
            random_pick = random.choice(available_indices)
            self.handle_click(random_pick)

    # -------------------------------------------------- #
    #                   Progression                      #
    # -------------------------------------------------- #
    def handle_click(self, clicked_index):
        clicked_btn = self.active_buttons[clicked_index]

        # Check for losing button click
        if clicked_index in self.losing_index:
            self.stop_timer()
            clicked_btn.config(
                bg="#dc3545",
                fg="white",
                disabledforeground="white",
                font=("Arial", 17),
                text="💥",
                state="disabled",
            )
            
            # Reset current streak and score on loss
            self.status_label.config(
                text="GAME OVER! You picked the bomb!", fg="#dc3545"
            )
            self.current_score = 0
            self.current_streak = 0
            self.current_level = 1
            self.update_scoreboard()

            # Reveal all bombs & lock board
            self.reveal_all_bombs()
            self.disable_all_buttons()

            self.action_button.config(text="Try Again", state="normal")

        else:
            # Safe pick
            clicked_btn.config(
                bg="#28a745",
                fg="white",
                disabledforeground="white",
                text="✓",
                state="disabled",
            )
            self.safe_clicks_count += 1

            total_safe_buttons = self.total_buttons - self.current_level
            points_earned = int(100 / total_safe_buttons)
            self.current_score += points_earned
            self.update_scoreboard()

            # Check if all safe buttons pressed on current board
            if self.safe_clicks_count == total_safe_buttons:
                self.handle_board_cleared()
            else:
                # Reset countdown timer for the next pick
                self.reset_timer()
                self.start_timer()

    def handle_board_cleared(self):
        """Triggers when a board level is cleared"""
        self.disable_all_buttons()
        self.stop_timer()

        # Increase current streak for clearing a board
        self.current_streak += 1
        if self.current_streak > self.best_streak:
            self.best_streak = self.current_streak
            self.save_high_score()  # Save instantly whenever high score increases

        self.update_scoreboard()

        # Check for max level win
        if self.current_level == self.max_level:
            self.status_label.config(
                text="You cleared all 5 levels! Legend!", fg="#28a745"
            )
            self.current_level = 1
            self.action_button.config(text="Play From Start", state="normal")
        else:
            self.status_label.config(
                text=f"LEVEL {self.current_level} CLEARED!", fg="#28a745"
            )
            self.current_level += 1
            self.action_button.config(text="Nxt lvl", state="normal")

    def handle_action_button(self):
        """Action button callback for either retrying or moving to the next board"""
        self.start_new_game()

    def reset_to_start(self):
        """Reset game back to Level 1"""
        self.current_level = 1
        self.current_score = 0
        self.current_streak = 0
        self.update_scoreboard()
        self.start_new_game()

    # -------------------------------------------------- #
    #                   Other Stuff                      #
    # -------------------------------------------------- #
    def reveal_all_bombs(self):
        """Reveals all hidden bombs when a player loses"""
        for idx in self.losing_index:
            btn = self.active_buttons[idx]
            btn.config(
                bg="#dc3545",
                fg="white",
                disabledforeground="white",
                text="💥\nBOMB",
            )

    def disable_all_buttons(self):
        """Locks remaining active buttons"""
        for btn in self.active_buttons.values():
            btn.config(state="disabled")

    def update_scoreboard(self):
        """Updates UI labels for current score and streak statistics"""
        self.score_label.config(text=f"Score: {self.current_score}")
        self.streak_label.config(
            text=f"Streak: {self.current_streak}  |  Best: {self.best_streak}"
        )


# -------------------------------------------------- #
#                    MAIN ENTRY                      #
# -------------------------------------------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = main(root)
    root.mainloop()