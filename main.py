import tkinter as tk
from tkinter import ttk, messagebox
from utils.database_manager import DatabaseManager
from utils.print_manager import PrintManager
from gui.order_frame import OrderFrame
from styles.theme import apply_theme
from config import DB_CONFIG, FOOD_ITEMS, DRINKS, DESSERTS
import datetime


class PakPakRestaurantSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("PakPak Restaurant Management System")
        self.root.geometry("1350x750+0+0")
        
        # Apply custom theme
        self.style = apply_theme(self.root)
        
        # Initialize services
        self.db = DatabaseManager(DB_CONFIG)
        self.print_manager = PrintManager()
        
        self.db.connect()  # Connect to the database
        
        # Initialize UI components and variables
        self.setup_variables()
        self.create_gui()

    def setup_variables(self):
        """Initialize variables for customer details and order summary."""
        self.customer_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.customer_address = tk.StringVar()
        self.table_number = tk.StringVar()
        self.waiter_name = tk.StringVar()
        self.payment_method = tk.StringVar(value="Cash")
        
        self.total_amount = tk.StringVar(value="0.00 TK")
        self.vat_amount = tk.StringVar(value="0.00 TK")
        self.grand_total = tk.StringVar(value="0.00 TK")

    def create_gui(self):
        """Create the main GUI layout."""
        main_container = ttk.Frame(self.root, style="Premium.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header
        self.create_header(main_container)

        # Content Area
        content = ttk.Frame(main_container, style="Premium.TFrame")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left Panel: Menu and Order Section
        left_panel = ttk.Frame(content, style="Card.TFrame")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        menu_items = {"Food Items": FOOD_ITEMS, "Drinks": DRINKS, "Desserts": DESSERTS}
        self.order_frame = OrderFrame(left_panel, menu_items)
        self.order_frame.pack(fill=tk.BOTH, expand=True)

        # Right Panel: Customer Info, Order Summary, and Actions
        right_panel = ttk.Frame(content, style="Card.TFrame")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)

        self.create_customer_section(right_panel)
        self.create_order_summary(right_panel)
        self.create_action_buttons(right_panel)

    def create_header(self, parent):
        """Create the header section."""
        header = ttk.Frame(parent, style="Premium.TFrame")
        header.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(
            header, text="PakPak Restaurant", font=("Helvetica", 24, "bold"), style="Premium.TLabel"
        ).pack()

        ttk.Label(
            header, text="Experience Quality & Taste", font=("Helvetica", 14), style="Premium.TLabel"
        ).pack()

    def create_customer_section(self, parent):
        """Create the customer information section."""
        customer_frame = ttk.LabelFrame(parent, text="Customer Information", style="Card.TFrame", padding=10)
        customer_frame.pack(fill=tk.X, pady=10)

        fields = [
            ("Name:", self.customer_name),
            ("Phone:", self.customer_phone),
            ("Address:", self.customer_address),
            ("Table No:", self.table_number),
            ("Waiter:", self.waiter_name),
        ]
        for row, (label, var) in enumerate(fields):
            ttk.Label(customer_frame, text=label).grid(row=row, column=0, padx=5, pady=5, sticky="w")
            ttk.Entry(customer_frame, textvariable=var, style="Premium.TEntry").grid(row=row, column=1, padx=5, pady=5, sticky="ew")

        # Payment Method
        ttk.Label(customer_frame, text="Payment:").grid(row=len(fields), column=0, padx=5, pady=5, sticky="w")
        payment_methods = ["Cash", "Card", "bKash", "Nagad"]
        ttk.Combobox(
            customer_frame,
            textvariable=self.payment_method,
            values=payment_methods,
            state="readonly",
            style="Premium.TCombobox",
        ).grid(row=len(fields), column=1, padx=5, pady=5, sticky="ew")

    def create_order_summary(self, parent):
        """Create the order summary section."""
        summary_frame = ttk.LabelFrame(parent, text="Order Summary", style="Card.TFrame", padding=10)
        summary_frame.pack(fill=tk.X, pady=10)

        fields = [
            ("Subtotal:", self.total_amount),
            ("VAT (15%):", self.vat_amount),
            ("Total:", self.grand_total),
        ]
        for row, (label, var) in enumerate(fields):
            ttk.Label(summary_frame, text=label).grid(row=row, column=0, padx=5, pady=5, sticky="w")
            ttk.Label(summary_frame, textvariable=var, font=("Helvetica", 12 if row == 2 else 10)).grid(row=row, column=1, padx=5, pady=5, sticky="e")

    def create_action_buttons(self, parent):
        """Create horizontal buttons for actions like calculate, place order, print, and clear."""
        button_frame = ttk.Frame(parent, style="Premium.TFrame")
        button_frame.pack(fill=tk.X, pady=10)

        # Define button details
        buttons = [
            ("Calculate Total", self.calculate_total),
            ("Place Order", self.place_order),
            ("Print Receipt", self.print_receipt),
            ("Clear", self.clear_form),
        ]

        for index, (text, command) in enumerate(buttons):
            ttk.Button(
                button_frame,
                text=text,
                style="Premium.TButton",
                command=command
            ).grid(row=0, column=index, padx=10, pady=5, sticky="ew")

        # Make the buttons expand evenly
        for column_index in range(len(buttons)):
            button_frame.columnconfigure(column_index, weight=1)

    def calculate_total(self):
        """Calculate the total amount including VAT."""
        items = self.order_frame.get_selected_items()
        if not items:
            messagebox.showwarning("Warning", "Please select at least one item")
            return

        subtotal = sum(item["subtotal"] for item in items)
        vat = subtotal * 0.15
        total = subtotal + vat

        self.total_amount.set(f"{subtotal:.2f} TK")
        self.vat_amount.set(f"{vat:.2f} TK")
        self.grand_total.set(f"{total:.2f} TK")

    def place_order(self):
        """Place the order and save it to the database."""
        if not self.validate_order():
            return

        customer_data = {
            "name": self.customer_name.get(),
            "phone": self.customer_phone.get(),
            "address": self.customer_address.get(),
            "payment_method": self.payment_method.get(),
        }

        items = self.order_frame.get_selected_items()
        total = float(self.grand_total.get().split()[0])

        order_id = self.db.save_order(
            customer_data,
            items,
            total,
            self.table_number.get(),
            self.waiter_name.get(),
        )

        if order_id:
            messagebox.showinfo("Success", "Order placed successfully!")
            self.print_receipt()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to place order")

    def print_receipt(self):
        """Print the receipt using the PrintManager."""
        if not self.validate_order():
            return

        order_data = {
            "order_id": datetime.datetime.now().strftime("%Y%m%d%H%M"),
            "subtotal": self.total_amount.get(),
            "vat": self.vat_amount.get(),
            "total": self.grand_total.get(),
        }
        customer_data = {
            "name": self.customer_name.get(),
            "phone": self.customer_phone.get(),
            "address": self.customer_address.get(),
        }
        items = self.order_frame.get_selected_items()

        if self.print_manager.print_invoice(order_data, customer_data, items):
            messagebox.showinfo("Success", "Receipt printed successfully!")
        else:
            messagebox.showerror("Error", "Failed to print receipt")

    def validate_order(self):
        """Validate the order before proceeding."""
        if not self.customer_name.get() or not self.customer_phone.get():
            messagebox.showwarning("Warning", "Please enter customer name and phone number")
            return False

        if not self.order_frame.get_selected_items():
            messagebox.showwarning("Warning", "Please select at least one item")
            return False

        return True

    def clear_form(self):
        """Clear all inputs and reset the form."""
        self.customer_name.set("")
        self.customer_phone.set("")
        self.customer_address.set("")
        self.table_number.set("")
        self.waiter_name.set("")
        self.payment_method.set("Cash")

        self.total_amount.set("0.00 TK")
        self.vat_amount.set("0.00 TK")
        self.grand_total.set("0.00 TK")

        self.order_frame.clear_selections()

    def __del__(self):
        """Ensure database connection is closed."""
        self.db.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = PakPakRestaurantSystem(root)
    root.mainloop()

