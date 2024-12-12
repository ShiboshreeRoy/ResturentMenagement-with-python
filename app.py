import tkinter as tk
from tkinter import messagebox, ttk

# Assuming a Database class with the required methods is available
from database import Database


class Application:
    def __init__(self, root):
        self.db = Database()
        self.db.connect()
        self.root = root
        self.root.title("Restaurant Management System")
        
        self.create_widgets()

    def create_widgets(self):
        """Create all widgets and tabs for the UI."""
        # Tabs
        self.tab_control = ttk.Notebook(self.root)
        self.tab_food = ttk.Frame(self.tab_control)
        self.tab_order = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_food, text="Food Menu")
        self.tab_control.add(self.tab_order, text="Place Order")
        self.tab_control.pack(expand=1, fill="both")

        # Food Menu Tab
        self.food_menu_widgets()
        
        # Order Tab
        self.order_widgets()

    def food_menu_widgets(self):
        """Create widgets for managing food items."""
        frame = tk.Frame(self.tab_food)
        frame.pack(pady=10, padx=10, fill="x")

        tk.Label(frame, text="Food Name:").grid(row=0, column=0, padx=5, pady=5)
        self.food_name_entry = tk.Entry(frame)
        self.food_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        self.food_category_entry = tk.Entry(frame)
        self.food_category_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Price:").grid(row=2, column=0, padx=5, pady=5)
        self.food_price_entry = tk.Entry(frame)
        self.food_price_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame, text="Add Food", command=self.add_food).grid(row=3, column=0, columnspan=2, pady=10)

        # Food Items Display
        self.food_tree = ttk.Treeview(self.tab_food, columns=("ID", "Name", "Category", "Price"), show="headings")
        self.food_tree.heading("ID", text="ID")
        self.food_tree.heading("Name", text="Name")
        self.food_tree.heading("Category", text="Category")
        self.food_tree.heading("Price", text="Price")
        self.food_tree.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(self.tab_food, text="Delete Selected", command=self.delete_food).pack(pady=10)

        self.load_food_items()

    def order_widgets(self):
        """Placeholder for order management tab."""
        tk.Label(self.tab_order, text="Order functionality coming soon...").pack(pady=20)

    def add_food(self):
        """Add new food item to the database."""
        name = self.food_name_entry.get().strip()
        category = self.food_category_entry.get().strip()
        price = self.food_price_entry.get().strip()

        if not name or not category or not price:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            price = float(price)
            self.db.add_food_item(name, category, price)
            self.load_food_items()
            # Clear entries after successful addition
            self.food_name_entry.delete(0, tk.END)
            self.food_category_entry.delete(0, tk.END)
            self.food_price_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number")

    def delete_food(self):
        """Delete selected food item from the database."""
        selected_item = self.food_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        food_id = self.food_tree.item(selected_item, "values")[0]
        self.db.delete_food_item(food_id)
        self.load_food_items()

    def load_food_items(self):
        """Load food items from the database and display them."""
        for item in self.food_tree.get_children():
            self.food_tree.delete(item)

        food_items = self.db.get_all_food_items()
        for food in food_items:
            self.food_tree.insert("", "end", values=food)

    def on_close(self):
        """Ensure the database connection is closed properly when exiting."""
        self.db.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
