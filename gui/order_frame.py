import tkinter as tk
from tkinter import ttk

class OrderFrame(ttk.Frame):
    def __init__(self, parent, menu_items, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.menu_items = menu_items
        self.selected_items = {}
        self.setup_ui()
        
    def setup_ui(self):
        # Create scrollable frame
        canvas = tk.Canvas(self, borderwidth=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create menu items
        for category, items in self.menu_items.items():
            self.create_category_section(category, items)
            
    def create_category_section(self, category, items):
        # Category header
        category_frame = ttk.LabelFrame(self.scrollable_frame, text=category, padding=10)
        category_frame.pack(fill="x", padx=5, pady=5)
        
        # Create grid for items
        for i, (item, price) in enumerate(items.items()):
            # Item name and price
            ttk.Label(category_frame, text=f"{item}").grid(row=i, column=0, sticky="w", padx=5)
            ttk.Label(category_frame, text=f"{price} TK").grid(row=i, column=1, padx=5)
            
            # Quantity spinbox
            var = tk.StringVar(value='0')
            self.selected_items[item] = var
            spinbox = ttk.Spinbox(
                category_frame,
                from_=0,
                to=99,
                width=5,
                textvariable=var
            )
            spinbox.grid(row=i, column=2, padx=5)
            
            # Special instructions
            ttk.Entry(category_frame, width=30).grid(row=i, column=3, padx=5)
            
    def get_selected_items(self):
        items = []
        for item, var in self.selected_items.items():
            try:
                quantity = int(var.get())
                if quantity > 0:
                    category = self.get_item_category(item)
                    if category:
                        price = self.menu_items[category][item]
                        items.append({
                            'name': item,
                            'quantity': quantity,
                            'price': price,
                            'subtotal': quantity * price
                        })
            except ValueError:
                continue
        return items
        
    def get_item_category(self, item):
        for category, items in self.menu_items.items():
            if item in items:
                return category
        return None
        
    def clear_selections(self):
        for var in self.selected_items.values():
            var.set('0')


