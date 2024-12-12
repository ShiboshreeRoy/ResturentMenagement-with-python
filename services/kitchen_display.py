import tkinter as tk
from tkinter import ttk
from typing import Dict, List
from models.order import Order, OrderStatus
from datetime import datetime, timedelta

class KitchenDisplaySystem:
    def __init__(self, root):
        self.root = root
        self.orders: Dict[int, Order] = {}
        self.setup_ui()
        
    def setup_ui(self):
        # Create main frame
        self.main_frame = ttk.Frame(self.root, style='Premium.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Orders grid
        self.orders_frame = ttk.Frame(self.main_frame)
        self.orders_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Column headers
        headers = ['Order #', 'Table', 'Items', 'Time', 'Status', 'Actions']
        for i, header in enumerate(headers):
            ttk.Label(
                self.orders_frame,
                text=header,
                style='Premium.TLabel',
                font=('Helvetica', 12, 'bold')
            ).grid(row=0, column=i, padx=5, pady=5)
            
    def add_order(self, order: Order):
        if order.id not in self.orders:
            self.orders[order.id] = order
            self.display_order(order)
            
    def display_order(self, order: Order):
        row = len(self.orders)
        
        # Order number
        ttk.Label(
            self.orders_frame,
            text=f"#{order.id}",
            style='Premium.TLabel'
        ).grid(row=row, column=0, padx=5, pady=5)
        
        # Table number
        ttk.Label(
            self.orders_frame,
            text=f"Table {order.table_number}" if order.table_number else "Takeaway",
            style='Premium.TLabel'
        ).grid(row=row, column=1, padx=5, pady=5)
        
        # Items
        items_text = "\n".join(
            f"{item.quantity}x {item.item_name}" 
            for item in order.items
        )
        ttk.Label(
            self.orders_frame,
            text=items_text,
            style='Premium.TLabel',
            wraplength=200
        ).grid(row=row, column=2, padx=5, pady=5)
        
        # Time
        elapsed = datetime.now() - order.order_date
        time_text = f"{elapsed.seconds // 60}m ago"
        ttk.Label(
            self.orders_frame,
            text=time_text,
            style='Premium.TLabel'
        ).grid(row=row, column=3, padx=5, pady=5)
        
        # Status
        status_label = ttk.Label(
            self.orders_frame,
            text=order.status.value,
            style='Premium.TLabel'
        )
        status_label.grid(row=row, column=4, padx=5, pady=5)
        
        # Action buttons
        actions_frame = ttk.Frame(self.orders_frame)
        actions_frame.grid(row=row, column=5, padx=5, pady=5)
        
        ttk.Button(
            actions_frame,
            text="Start",
            command=lambda: self.update_order_status(order.id, OrderStatus.PREPARING)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            actions_frame,
            text="Ready",
            command=lambda: self.update_order_status(order.id, OrderStatus.READY)
        ).pack(side=tk.LEFT, padx=2)
        
    def update_order_status(self, order_id: int, status: OrderStatus):
        if order_id in self.orders:
            self.orders[order_id].status = status
            # Refresh display
            self.refresh_display()
            
    def refresh_display(self):
        # Clear current display
        for widget in self.orders_frame.winfo_children():
            widget.destroy()
            
        # Redisplay all orders
        for order in self.orders.values():
            self.display_order(order)
