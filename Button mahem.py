""" This is my first version of the button game Ive created in terms of sprints this would be sprint 1 and 2 combined this contains the basic essansials for the game like scoring, streaks and colours and in my future vesions I would add futher progression"""
import tkinter as tk
import random

class main:
    def __init__(self, root):
        self.root = root
        self.root.title("button mayhem")
        self.root.geometry("400x500")

        #Board
        self.total_buttons = 6
        self.max_level = 5
        
        # Progression
        self.current_level = 1
        self.losing_index = []
        self.safe_clicks_count = 0
        self.active_buttons = {}
        
        #Score
        self.current_score = 0
        self.current_streak = 0
        self.best_streak = 0
        
        # Make UI
        self.setup_ui()
        
        #Make first game
        self.start_new_game()

    def setup_ui(self):
        """Create base OOP UI layout structure"""
        #header for streak
        self.header_frame = tk.Frame(self.root, pady=10)
        self.header_frame.pack(fill="x")

        #Shows current level
        self.level_label = tk.Label(
            self.header_frame, 
            text="LEVEL 1 / 5", 
            font=("Arial", 14, "bold"),
            fg="#007bff"
        )
        self.level_label.pack()
        
        self.streak_label = tk.Label(
            self.header_frame, 
            text="Streak: 0  |  Best: 0", 
            font=("Arial", 12, "bold"),
            fg="#555555"
        )
        self.streak_label.pack()

        #scoreboard
        self.score_label = tk.Label(
            self.root, 
            text="Score: 0", 
            font=("Arial", 18, "bold"),
            fg="#111111"
        )
        self.score_label.pack(pady=5)

        self.status_label = tk.Label(
            self.root, 
            text="Pick a button! Avoid the bomb.", 
            font=("Arial", 14)
        )
        self.status_label.pack(pady=15)
        
        #make 6 buttons
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(expand=True)
        
        self.control_frame = tk.Frame(self.root, pady=15)
        self.control_frame.pack(fill="x")

        #restart button
        self.restart_button = tk.Button(
            self.control_frame, 
            text="Restart (Level 1)", 
            font=("Arial", 11, "bold"),
            command=self.reset_to_start,
            bg="#f8f9fa"
        )
        self.restart_button.pack(side="left", padx=20)

        self.action_button = tk.Button(
            self.control_frame, 
            text="Next Level", 
            font=("Arial", 11, "bold"),
            command=self.handle_action_button,
            state="disabled",
            bg="#007bff",
            fg="white"
        )
        self.action_button.pack(side="right", padx=20)

    """starts the game with the new progression"""
    def start_new_game(self):

        self.safe_clicks_count = 0
        num_bombs = self.current_level
        total_safe = self.total_buttons - num_bombs

        #Update the display
        self.level_label.config(text=f"LEVEL {self.current_level} / {self.max_level}")
        self.status_label.config(
            text=f"Find all {total_safe} safe buttons! ({num_bombs} bombs hidden)", 
            fg="black"
        )
        # Reset action button text and state for the active round
        self.action_button.config(text="Next Level", state="disabled")
        
        # Pick a 'n' amonut of losing buttons
        self.losing_index = random.sample(range(self.total_buttons), k=num_bombs)
        
        # reset 6 buttons
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
                # Click detection passing button index
                command=lambda idx=i: self.handle_click(idx)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.active_buttons[i] = btn

    """Click detection and win/lose """
    def handle_click(self, clicked_index):

        clicked_btn = self.active_buttons[clicked_index]
        
        #Check for losing button click
        if clicked_index in self.losing_index:
            clicked_btn.config(
                bg="#dc3545",
                fg="white",
                disabledforeground="white",
                font=("Arial", 17),
                text="💥",
                state="disabled",
            )
            #rest scores
            self.status_label.config(text="GAME OVER! You picked the bomb!", fg="#dc3545")
            self.current_score = 0
            self.current_streak = 0
            self.current_level = 1
            self.update_scoreboard()

            #show bomb
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
                state="disabled"
            )
            self.safe_clicks_count += 1
            
            total_safe_buttons = self.total_buttons - self.current_level
            points_earned = int(100 / total_safe_buttons)  
            self.current_score += points_earned
            self.update_scoreboard()
            
            # Check if all buttons pressed in the board
            if self.safe_clicks_count == total_safe_buttons:
                self.handle_board_cleared()           

    def handle_board_cleared(self):
        """Triggers when a level is cleared"""
        self.disable_all_buttons()
        
        # Check for win
        if self.current_level == self.max_level:
            self.current_streak += 1
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak
            self.update_scoreboard()
            
            self.status_label.config(
                text="You lowkey so tuff", 
                fg="#28a745"
            )
            # Reset progression for next attempt
            self.current_level = 1
            self.action_button.config(text="Play From Start", state="normal")
        else:
            self.status_label.config(
                text=f"LEVEL {self.current_level} CLEARED!", 
                fg="#28a745"
            )
            self.current_level += 1
            self.action_button.config(text=f"nxt Level", state="normal")

    def handle_action_button(self):
        """Action button callback for either retrying or advancing to the next board"""
        self.start_new_game()

    def reset_to_start(self):
        """Reset game state back to Level 1"""
        self.current_level = 1
        self.current_score = 0
        self.update_scoreboard()
        self.start_new_game()

    def reveal_all_bombs(self):
        """Reveals all hidden bombs when a player loses"""
        for idx in self.losing_index:
            btn = self.active_buttons[idx]
            btn.config(
                bg="#dc3545",
                fg="white",
                disabledforeground="white",
                text="💥\nBOMB"
            )

    def disable_all_buttons(self):
        """Locks remaining active buttons"""
        for btn in self.active_buttons.values():
            btn.config(state="disabled")
    
    def update_scoreboard(self):
        self.score_label.config(text=f"Score: {self.current_score}")
        self.streak_label.config(text=f"Streak: {self.current_streak} | Best: {self.best_streak}")


if __name__ == "__main__":
    root = tk.Tk()
    app = main(root)
    root.mainloop()