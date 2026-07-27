import tkinter as tk

class main:
    def __init__(self, root):
        self.root = root
        self.root.title("buttonmayhem")
        self.root.geometry("400x400")
        


        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(expand=True)
        

        self.create_buttons()

    def create_buttons(self):

        for i in range(6):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                self.grid_frame, 
                text=f"Button {i + 1}", 
                font=("Arial", 12, "bold"),
                width=10, 
                height=3,
            )
            btn.grid(row=row, column=col, padx=8, pady=8)

if __name__ == "__main__":
    root = tk.Tk()
    app = main(root)
    root.mainloop()