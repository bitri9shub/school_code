import tkinter as tk

class MultiInterfaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Interface Application")
        self.root.geometry("500x400")
        
        # Create main container
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)
        
        # Show home interface initially
        self.show_home()
    
    def clear_interface(self):
        """Remove all widgets from container"""
        for widget in self.container.winfo_children():
            widget.destroy()
    
    def show_home(self):
        """Show the home interface with two buttons"""
        self.clear_interface()
        
        # Title
        title = tk.Label(self.container, text="Main Menu", 
                        font=("Arial", 24, "bold"))
        title.pack(pady=50)
        
        # Button A
        btn_a = tk.Button(self.container, text="Button A - Interface 1",
                         command=self.show_interface_a,
                         width=25, height=2,
                         font=("Arial", 12),
                         bg="#4CAF50", fg="white")
        btn_a.pack(pady=20)
        
        # Button B
        btn_b = tk.Button(self.container, text="Button B - Interface 2",
                         command=self.show_interface_b,
                         width=25, height=2,
                         font=("Arial", 12),
                         bg="#2196F3", fg="white")
        btn_b.pack(pady=20)
    
    def show_interface_a(self):
        """Show Interface A"""
        self.clear_interface()
        
        # Title
        title = tk.Label(self.container, text="Interface A", 
                        font=("Arial", 20, "bold"),
                        fg="#4CAF50")
        title.pack(pady=30)
        
        # Some content for Interface A
        content = tk.Label(self.container, 
                          text="This is Interface A\nYou can add your custom widgets here",
                          font=("Arial", 12))
        content.pack(pady=20)
        
        # Example entry field
        tk.Label(self.container, text="Enter something:").pack(pady=5)
        entry = tk.Entry(self.container, width=30)
        entry.pack(pady=5)
        
        # Back button
        back_btn = tk.Button(self.container, text="← Back to Main Menu",
                            command=self.show_home,
                            font=("Arial", 10))
        back_btn.pack(pady=30)
    
    def show_interface_b(self):
        """Show Interface B"""
        self.clear_interface()
        
        # Title
        title = tk.Label(self.container, text="Interface B", 
                        font=("Arial", 20, "bold"),
                        fg="#2196F3")
        title.pack(pady=30)
        
        # Some content for Interface B
        content = tk.Label(self.container, 
                          text="This is Interface B\nCompletely different from Interface A",
                          font=("Arial", 12))
        content.pack(pady=20)
        
        # Example listbox
        tk.Label(self.container, text="Select an option:").pack(pady=5)
        listbox = tk.Listbox(self.container, height=5)
        for i in range(1, 6):
            listbox.insert(tk.END, f"Option {i}")
        listbox.pack(pady=5)
        
        # Back button
        back_btn = tk.Button(self.container, text="← Back to Main Menu",
                            command=self.show_home,
                            font=("Arial", 10))
        back_btn.pack(pady=30)

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MultiInterfaceApp(root)
    root.mainloop()

