""" This is my first version of the button game Ive created in terms of sprints this would be sprint 1 and 2 combined this contains the basic essansials for the game like scoring, streaks and colours and in my future vesions I would add futher progression"""
import tkinter as tk
import random

class main:
    def __init__(self, root):
        self.root = root
        self.root.title("Sprint 1 - Core Game Loop")
        self.root.geometry("400x450")
        
        # Variables
        self.total_buttons = 6
        self.losing_index = 0
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
        self.status_label = tk.Label(
            self.root, 
            text="Pick a button! Avoid the bomb.", 
            font=("Arial", 14)
        )
        self.header_frame = tk.Frame(self.root, pady=10)
        self.header_frame.pack(fill="x")
        
        self.streak_label = tk.Label(
            self.header_frame, 
            text="Streak: 0  |  Best: 0", 
            font=("Arial", 12, "bold"),
            fg="#555555"
        )
        self.streak_label.pack()
        
        self.score_label = tk.Label(
            self.root, 
            text="Score: 0", 
            font=("Arial", 18, "bold"),
            fg="#111111"
        )
        self.score_label.pack(pady=5)
        self.status_label.pack(pady=15)
        
        #make 6 buttons
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(expand=True)
        
        #restart button
        self.restart_button = tk.Button(
            self.root, 
            text="Play Again", 
            font=("Arial", 12, "bold"),
            command=self.start_new_game,
            state="disabled"

        )
        self.restart_button.pack(pady=20)


    """Reset board state & re-randomize losing button"""
    def start_new_game(self):

        self.safe_clicks_count = 0
        self.status_label.config(text="Pick a button! Avoid the bomb.")
        self.restart_button.config(state="disabled")
        
        # Make losing button
        self.losing_index = random.randint(0, self.total_buttons - 1)
        
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
        if clicked_index == self.losing_index:
            clicked_btn.config(
                bg="#dc3545",
                fg="white",
                disabledforeground="white",
                font =("arial",17),
                text="💥",
                state="disabled" 
            )
            self.status_label.config(text="GAME OVER! You picked the bomb!")
            self.end_game()
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
            total_safe_buttons = self.total_buttons - 1
            points_earned = int(100 / total_safe_buttons)  
            self.current_score += points_earned
            self.update_scoreboard()
            if self.safe_clicks_count == total_safe_buttons:
                #adds streak when board cleared
                self.current_streak += 1
                if self.current_streak > self.best_streak:
                    self.best_streak = self.current_streak
                
                self.update_scoreboard()
                self.status_label.config(text="YOU WIN! Full board cleared!", fg="#28a745")
                self.end_game()
            
            
            # Check for win
            if self.safe_clicks_count == self.total_buttons - 1:
                self.status_label.config(text="YOU WIN! All safe buttons cleared!")
                self.end_game()
    """lock the board and enable restart when round finishes"""
    def end_game(self):

        for btn in self.active_buttons.values():
            btn.config(state="disabled")
        self.restart_button.config(state="normal")
    
    def update_scoreboard(self):
        self.score_label.config(text=f"Score: {self.current_score}")
        self.streak_label.config(text=f"Streak: {self.current_streak} | Best: {self.best_streak}")


if __name__ == "__main__":
    root = tk.Tk()
    app = main(root)
    root.mainloop()