""" This version launches directly to a main menu first, then asks for username upon selecting a mode """

import math
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
        self.root.geometry("450x600")

        # ---------------- Variables ---------------- #
        #Board
        self.total_buttons = 6
        self.max_level = 5
        self.custom_mode = False
        self.custom_bombs = 1

        # Colours
        self.COLOUR_BG = "#1e1e2e"
        self.COLOUR_PANEL = "#2a2a3c"
        self.COLOUR_PRIMARY = "#00f5d4"
        self.COLOUR_TEXT = "#f8f9fa"
        self.COLOUR_MUTED = "#a6adc8"
        self.COLOUR_DANGER = "#ff0055"
        self.COLOUR_SAFE = "#38b000"
        self.COLOUR_BTN_DEFAULT = "#313244"

        self.root.configure(bg=self.COLOUR_BG)
        #File handling
        self.username = ""
        self.score_file = "score.txt"

        # Progression
        self.current_level = 1
        self.losing_index = []
        self.safe_clicks_count = 0
        self.active_buttons = {}

        # Score and Streaks
        self.current_score = 0
        self.current_streak = 0
        self.best_streak = 0

        # Timer and timeout
        self.timeout_seconds = 3
        self.seconds_remaining = 3
        self.timer_job = None
        self.timer_active = False

        # Save data on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Show Main Menu first when program starts
        self.show_main_menu()

    # -------------------------------------------------- #
    #               File Handling                        #
    # -------------------------------------------------- #
    def get_valid_username(self):
        # asks for username
        while True:
            name = simpledialog.askstring(
                "Arigatho", "Enter your username to start:"
            )

            if name is None:
                return False  # User cancelled

            cleaned_name = name.strip()

            if cleaned_name:
                self.username = cleaned_name
                return True
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
        # saves current highscore
        if not self.username:
            return

        scores = {}

        #Read existing records
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

        # Write all scores back to txt file
        try:
            with open(self.score_file, "w") as file:
                for user, score in scores.items():
                    file.write(f"{user}:{score}\n")
        except OSError as e:
            print(f"Error saving score: {e}")

    def on_close(self):
        """Saves data and closes window when user clicks X."""
        self.save_high_score()
        self.root.destroy()

    # -------------------------------------------------- #
    #                   MAIN MENU                        #
    # -------------------------------------------------- #
    def clear_screen(self):
        """Clears all existing widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        """Display the Main Menu screen to pick game modes"""
        self.stop_timer()
        self.clear_screen()

        menu_frame = tk.Frame(self.root, bg=self.COLOUR_BG)
        menu_frame.pack(expand=True, fill="both")

        # Title Block
        title_label = tk.Label(
            menu_frame,
            text="BUTTON MAYHEM",
            font=("Arial", 22, "bold"),
            fg=self.COLOUR_PRIMARY,
            bg=self.COLOUR_BG,
        )
        title_label.pack(pady=(70, 10))

        sub_label = tk.Label(
            menu_frame,
            text="Select Game Mode",
            font=("Arial", 14),
            fg=self.COLOUR_TEXT,
            bg=self.COLOUR_BG,
        )
        sub_label.pack(pady=(0, 40))

        # Buttons to choose gamemodes
        normal_btn = tk.Button(
            menu_frame,
            text="Normal Mode (5 Levels)",
            font=("Arial", 12, "bold"),
            bg=self.COLOUR_PRIMARY,
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.start_normal_mode,
        )
        normal_btn.pack(pady=10, fill="x", padx=60)

        custom_btn = tk.Button(
            menu_frame,
            text="Custom Mode",
            font=("Arial", 12, "bold"),
            bg=self.COLOUR_SAFE,
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.start_custom_mode_from_menu,
        )
        custom_btn.pack(pady=10, fill="x", padx=60)

    def ensure_user_ready(self):
        """Prompts for username if not entered yet and loads saved score."""
        if not self.username:
            if not self.get_valid_username():
                return False  # User cancelled dialog
            self.load_high_score()
        return True

    def start_normal_mode(self):
        """Launches the standard progression mode after asking for username"""
        if not self.ensure_user_ready():
            return

        self.custom_mode = False
        self.total_buttons = 6
        self.current_level = 1
        self.current_score = 0
        self.current_streak = 0
        self.clear_screen()
        self.setup_ui()
        self.start_new_game()

    def start_custom_mode_from_menu(self):
        """Asks for username, prompts settings, then launches custom game"""
        if not self.ensure_user_ready():
            return

        if self.setup_custom_mode_prompts():
            self.clear_screen()
            self.setup_ui()
            self.start_new_game()

    # -------------------------------------------------- #
    #                   UI                               #
    # -------------------------------------------------- #
    def setup_ui(self):
        """Create base OOP UI layout structure"""
        # header 
        self.header_frame = tk.Frame(self.root, bg=self.COLOUR_PANEL, pady=10)
        self.header_frame.pack(fill="x")

        # Shows player name
        self.user_label = tk.Label(
            self.header_frame,
            text=f"Player: {self.username}",
            font=("Arial", 11, "italic"),
            fg=self.COLOUR_MUTED,
            bg=self.COLOUR_PANEL,
        )
        self.user_label.pack()

        # Shows current level
        self.level_label = tk.Label(
            self.header_frame,
            text="LEVEL 1 / 5",
            font=("Arial", 14, "bold"),
            fg=self.COLOUR_PRIMARY,
            bg=self.COLOUR_PANEL,
        )
        self.level_label.pack()

        # Timeout
        self.timer_label = tk.Label(
            self.header_frame,
            text="Time Left: 3s",
            font=("Arial", 17, "bold"),
            fg=self.COLOUR_DANGER,
            bg=self.COLOUR_PANEL,
        )
        self.timer_label.pack(pady=2)

        # streak tracker
        self.streak_label = tk.Label(
            self.header_frame,
            text=f"Streak: 0  |  Best: {self.best_streak}",
            font=("Arial", 12, "bold"),
            fg=self.COLOUR_TEXT,
            bg=self.COLOUR_PANEL,
        )
        self.streak_label.pack()

        # scoreboard
        self.score_label = tk.Label(
            self.root, text="Score: 0", font=("Arial", 18, "bold"), fg=self.COLOUR_TEXT, bg=self.COLOUR_BG
        )
        self.score_label.pack(pady=5)

        self.status_label = tk.Label(
            self.root, text="Pick a button! Avoid the bomb.", font=("Arial", 14), fg=self.COLOUR_TEXT, bg=self.COLOUR_BG
        )
        self.status_label.pack(pady=10)

        # make grid for btn
        self.grid_frame = tk.Frame(self.root, bg=self.COLOUR_BG)
        self.grid_frame.pack(expand=True)

        self.control_frame = tk.Frame(self.root, bg=self.COLOUR_PANEL, pady=10)
        self.control_frame.pack(fill="x")

        # restart button
        self.restart_button = tk.Button(
            self.control_frame,
            text="Menu",
            font=("Arial", 10, "bold"),
            command=self.show_main_menu,
            bg=self.COLOUR_BTN_DEFAULT,
            fg=self.COLOUR_TEXT,
            relief="flat",
        )
        self.restart_button.pack(side="left", padx=10)

        # custom mode 
        self.custom_button = tk.Button(
            self.control_frame,
            text="Custom Mode",
            font=("Arial", 10, "bold"),
            command=self.setup_custom_mode,
            bg=self.COLOUR_MUTED,
            fg="white",
            relief="flat",
        )
        self.custom_button.pack(side="left", padx=5)

        self.action_button = tk.Button(
            self.control_frame,
            text="Next Level",
            font=("Arial", 10, "bold"),
            command=self.handle_action_button,
            state="disabled",
            bg=self.COLOUR_PRIMARY,
            fg="white",
            relief="flat",
        )
        self.action_button.pack(side="right", padx=10)

    # -------------------------------------------------- #
    #                CUSTOM GAME MODE                    #
    # -------------------------------------------------- #
    def setup_custom_mode_prompts(self):
        """Prompts inputs for custom game mode settings."""
        # Ask for Total Buttons
        while True:
            total_input = simpledialog.askinteger(
                "Custom Mode", "Enter TOTAL number of buttons (min 2, max 25):"
            )
            if total_input is None:  # User cancelled
                return False
            if 2 <= total_input <= 25:
                break
            messagebox.showwarning(
                "Dont make me angry now 😈😈😈😈", "Total buttons must be between 2 and 25!"
            )

        #Ask for Losing Buttons 
        while True:
            bombs_input = simpledialog.askinteger(
                "Custom Mode",
                f"Enter NUMBER OF BOMBS (Must be less than {total_input}):",
            )
            if bombs_input is None:  # User cancelled
                return False
            if 1 <= bombs_input < total_input:
                break
            messagebox.showwarning(
                "Dont make me angry now 😈😈😈😈",
                f"Losing buttons must be at least 1 and LESS THAN total buttons ({total_input})!",
            )

        #custom settings
        self.custom_mode = True
        self.total_buttons = total_input
        self.custom_bombs = bombs_input
        self.current_score = 0
        return True

    def setup_custom_mode(self):
        """ask user for the number of buttons from 2-25."""
        if self.setup_custom_mode_prompts():
            self.update_scoreboard()
            self.start_new_game()

    # -------------------------------------------------- #
    #                   Start Game                       #
    # -------------------------------------------------- #
    def start_new_game(self):
        self.safe_clicks_count = 0

        if self.custom_mode:
            num_bombs = self.custom_bombs
            self.level_label.config(text="CUSTOM MODE", fg=self.COLOUR_MUTED)
        else:
            num_bombs = self.current_level
            self.level_label.config(
                text=f"LEVEL {self.current_level} / {self.max_level}",
                fg=self.COLOUR_PRIMARY,
            )

        total_safe = self.total_buttons - num_bombs

        # reset timer for each new board
        self.reset_timer()
        self.start_timer()

        # Update labels
        self.status_label.config(
            text=f"Find all {total_safe} safe buttons! ({num_bombs} bombs hidden)",
            fg=self.COLOUR_TEXT,
        )
        self.action_button.config(text="Nxt lvl", state="disabled", bg=self.COLOUR_MUTED)

        # Pick losing buttons
        self.losing_index = random.sample(
            range(self.total_buttons), k=num_bombs
        )

        # Reset buttons grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.active_buttons.clear()

        #Tuff equation to calc the no cols and rows in a grid
        cols = math.ceil(math.sqrt(self.total_buttons))

        for i in range(self.total_buttons):
            row = i // cols
            col = i % cols

            btn = tk.Button(
                self.grid_frame,
                text=f"Button {i + 1}",
                width=8 if cols > 3 else 10,
                height=2 if self.total_buttons > 9 else 3,
                bg=self.COLOUR_BTN_DEFAULT,
                fg=self.COLOUR_TEXT,
                relief="flat",
                command=lambda idx=i: self.handle_click(idx),
            )
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.active_buttons[i] = btn


        #for idx in self.losing_index:
            #self.active_buttons[idx].config(bg="#ffcccc")

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
                bg=self.COLOUR_DANGER,
                fg="white",
                disabledforeground="white",
                font=("Arial", 14 if self.total_buttons > 9 else 17),
                text="💥",
                state="disabled",
            )

            # Reset current streak and score on loss
            self.status_label.config(
                text="GAME OVER! You picked the bomb!", fg=self.COLOUR_DANGER
            )
            self.current_score = 0
            self.current_streak = 0
            self.update_scoreboard()

            # Reveal all bombs & lock board
            self.reveal_all_bombs()
            self.disable_all_buttons()

            self.action_button.config(text="Try Again", state="normal", bg=self.COLOUR_DANGER, fg="white")

        else:
            # Safe pick
            clicked_btn.config(
                bg=self.COLOUR_SAFE,
                fg="white",
                disabledforeground="white",
                text="✓",
                state="disabled",
            )
            self.safe_clicks_count += 1

            num_bombs = (
                self.custom_bombs if self.custom_mode else self.current_level
            )
            total_safe_buttons = self.total_buttons - num_bombs
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
            self.save_high_score()

        self.update_scoreboard()

        if self.custom_mode:
            self.status_label.config(text="CUSTOM BOARD CLEARED!", fg=self.COLOUR_SAFE)
            self.action_button.config(text="Play Again", state="normal", bg=self.COLOUR_SAFE, fg="white")
        else:
            # Check for win
            if self.current_level == self.max_level:
                self.status_label.config(
                    text="U lowk so tuff!!!!!!!!!!!!", fg=self.COLOUR_SAFE
                )
                self.current_level = 1
                self.action_button.config(text="play again", state="normal", bg=self.COLOUR_SAFE, fg="white")
            else:
                self.status_label.config(
                    text=f"LEVEL {self.current_level} CLEARED!", fg=self.COLOUR_SAFE
                )
                self.current_level += 1
                self.action_button.config(text="Nxt lvl", state="normal", bg=self.COLOUR_PRIMARY, fg="white")

    def handle_action_button(self):
        #Retry button
        self.start_new_game()

    def reset_to_start(self):
        """Reset game back to lvl 1"""
        self.custom_mode = False
        self.total_buttons = 6
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
                bg=self.COLOUR_DANGER,
                fg="white",
                disabledforeground="white",
                text="💥\nBOMB",
            )

    def disable_all_buttons(self):
        """Locks remaining active buttons"""
        for btn in self.active_buttons.values():
            btn.config(state="disabled")

    def update_scoreboard(self):
        """Updates UI labels for current score and streak"""
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