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
                state="disabled")
            self.safe_clicks_count += 1
            
            # Check for win
            if self.safe_clicks_count == self.total_buttons - 1:
                self.status_label.config(text="YOU WIN! All safe buttons cleared!")
                self.end_game()
    """lock the board and enable restart when round finishes"""
    def end_game(self):

        for btn in self.active_buttons.values():
            btn.config(state="disabled")
        self.restart_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = main(root)
    root.mainloop()