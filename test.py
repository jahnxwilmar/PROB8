import customtkinter as ctk

# Initialize the main window
root = ctk.CTk()
root.geometry("400x400")  # Adjust the size as needed

# Create a 3x3 grid of frames
for row in range(3):
    for col in range(3):
        # Create a frame for each cell
        cell_frame = ctk.CTkFrame(root, width=100, height=100, corner_radius=10)
        cell_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Make each cell expandable (optional)
        root.grid_rowconfigure(row, weight=1)
        root.grid_columnconfigure(col, weight=1)

        # You can add additional widgets within each cell if needed
        label = ctk.CTkLabel(cell_frame, text=f"Cell {row+1},{col+1}")
        label.pack(expand=True)

# Run the application
root.mainloop()
