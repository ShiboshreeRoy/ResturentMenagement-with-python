from tkinter import ttk
import tkinter as tk

def apply_theme(root):
    # Custom style configuration
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure general colors
    style.configure('Premium.TFrame', background='#2e3b8d')  # Darker background for frames
    style.configure('Premium.TLabel', 
                   background='#2e3b8d',  # Dark background for labels
                   foreground='#ffffff',
                   font=('Helvetica', 12),
                   anchor='center')  # Center the text within labels
    
    # Button styles
    style.configure('Premium.TButton',
                   background='#3f51b5',  # Modern blue background
                   foreground='#ffffff',
                   padding=(15, 8),  # Wider padding for a more spacious button
                   font=('Helvetica', 11, 'bold'),
                   relief='flat')  # Flat buttons for modern look
    
    style.map('Premium.TButton',
              background=[('active', '#3949ab')],
              foreground=[('active', '#ffffff')])

    # Button hover effect (using active state for hover effect)
    style.map('Premium.TButton',
              background=[('pressed', '#303f9f')],
              foreground=[('pressed', '#ffffff')])
    
    # Entry widget styles (modern look with rounded edges)
    style.configure('Premium.TEntry',
                   fieldbackground='#ffffff',  # White background for entries
                   foreground='#333333',  # Dark text color
                   font=('Helvetica', 12),
                   padding=10,
                   relief='flat',
                   insertbackground='#1a237e')  # Custom cursor color
    style.map('Premium.TEntry',
              fieldbackground=[('focus', '#e8eaf6')])  # Light color on focus for Entry widget
    
    # Frame styles (raised frame with shadow for a 3D effect)
    style.configure('Card.TFrame',
                   background='#ffffff',
                   relief='raised',
                   borderwidth=2,
                   highlightthickness=2,
                   highlightcolor='#e0e0e0',  # Light border color
                   highlightbackground='#bdbdbd')  # Slight shadow effect
    
    # Adding rounded corners to frames and buttons (using padding and relief)
    style.configure('Premium.TFrame',
                    relief='flat',  # Flat frame for modern look
                    borderwidth=10)
    
    # Additional custom styling for the root window (transparent background)
    root.configure(bg='#2e3b8d')  # Set the root background color for consistency
    return style

