'''from datetime import datetime
import os
from fpdf import FPDF

class ReceiptGenerator:
    def __init__(self):
        self.pdf = FPDF()

    def generate_receipt(self, order_data, customer_data, items):
        # Create folder based on date-time and customer name
        folder_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + f"_{customer_data['name']}"
        folder_path = os.path.join("receipts", folder_name)
        os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists

        # Add a new page
        self.pdf.add_page()

        # Header
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 10, 'Pak Pak Restaurant', 0, 1, 'C')
        self.pdf.set_font('Arial', '', 12)
        self.pdf.cell(0, 10, 'Address: Your Restaurant Address', 0, 1, 'C')
        self.pdf.cell(0, 10, 'Phone: Your Phone Number', 0, 1, 'C')

        # Customer Info
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 10, f"Customer: {customer_data['name']}", 0, 1)
        self.pdf.cell(0, 10, f"Phone: {customer_data['phone']}", 0, 1)
        self.pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
        self.pdf.cell(0, 10, f"Order #: {order_data['order_id']}", 0, 1)

        # Items
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(80, 10, 'Item', 1)
        self.pdf.cell(30, 10, 'Qty', 1)
        self.pdf.cell(40, 10, 'Price', 1)
        self.pdf.cell(40, 10, 'Total', 1)
        self.pdf.ln()

        self.pdf.set_font('Arial', '', 12)
        for item in items:
            self.pdf.cell(80, 10, item['name'], 1)
            self.pdf.cell(30, 10, str(item['quantity']), 1)
            self.pdf.cell(40, 10, f"{item['price']} TK", 1)
            self.pdf.cell(40, 10, f"{item['subtotal']} TK", 1)
            self.pdf.ln()

        # Total
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(150, 10, 'Subtotal:', 0, 0, 'R')
        self.pdf.cell(40, 10, f"{order_data['subtotal']} TK", 0, 1)
        self.pdf.cell(150, 10, 'VAT (15%):', 0, 0, 'R')
        self.pdf.cell(40, 10, f"{order_data['vat']} TK", 0, 1)
        self.pdf.cell(150, 10, 'Total:', 0, 0, 'R')
        self.pdf.cell(40, 10, f"{order_data['total']} TK", 0, 1)

        # Footer
        self.pdf.ln(20)
        self.pdf.set_font('Arial', '', 10)
        self.pdf.cell(0, 10, 'Thank you for dining with us!', 0, 1, 'C')
        self.pdf.cell(0, 10, 'We hope to see you again soon.', 0, 1, 'C')

        # Save the receipt in the created folder
        receipt_filename = f"receipt_{order_data['order_id']}.pdf"
        receipt_path = os.path.join(folder_path, receipt_filename)
        self.pdf.output(receipt_path)

        # Display the receipt path in the console
        print(f"Receipt saved at: {receipt_path}")
        return receipt_path

# Example Usage
order_data = {
    'order_id': 'ORD123456',
    'subtotal': '500.00',
    'vat': '75.00',
    'total': '575.00'
}

customer_data = {
    'name': 'John Doe',
    'phone': '123-456-7890'
}

items = [
    {'name': 'Burger', 'quantity': 2, 'price': '150', 'subtotal': '300'},
    {'name': 'Coke', 'quantity': 1, 'price': '50', 'subtotal': '50'},
    {'name': 'Fries', 'quantity': 1, 'price': '100', 'subtotal': '100'},
]

# Create an instance of the ReceiptGenerator class
receipt_generator = ReceiptGenerator() 
receipt_path = ReceiptGenerator.generate_receipt(order_data, customer_data, items)
'''
from datetime import datetime
from fpdf import FPDF

class ReceiptGenerator:
    def __init__(self):
        self.pdf = FPDF()
        
    def generate_receipt(self, order_data, customer_data, items):
        self.pdf.add_page()
        
        # Header
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 10, 'Pak Pak Restaurant', 0, 1, 'C')
        self.pdf.set_font('Arial', '', 12)
        self.pdf.cell(0, 10, 'Address: Your Restaurant Address', 0, 1, 'C')
        self.pdf.cell(0, 10, 'Phone: Your Phone Number', 0, 1, 'C')
        
        # Customer Info
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 10, f"Customer: {customer_data['name']}", 0, 1)
        self.pdf.cell(0, 10, f"Phone: {customer_data['phone']}", 0, 1)
        self.pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
       # self.pdf.cell(0, 10, f"Order #: {order_data['order_id']}", 0, 1)
        
        # Items
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(80, 10, 'Item', 1)
        self.pdf.cell(30, 10, 'Qty', 1)
        self.pdf.cell(40, 10, 'Price', 1)
        self.pdf.cell(40, 10, 'Total', 1)
        self.pdf.ln()
        
        self.pdf.set_font('Arial', '', 12)
        for item in items:
            self.pdf.cell(80, 10, item['name'], 1)
            self.pdf.cell(30, 10, str(item['quantity']), 1)
            self.pdf.cell(40, 10, f"{item['price']} TK", 1)
            self.pdf.cell(40, 10, f"{item['subtotal']} TK", 1)
            self.pdf.ln()
            
        # Total
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(150, 10, 'Subtotal:', 0, 0, 'R')
        self.pdf.cell(40, 10, f"{order_data['subtotal']} TK", 0, 1)
        #self.pdf.cell(150, 10, 'VAT (15%):', 0, 0, 'R')
        self.pdf.cell(40, 10, f"{order_data['vat']} TK", 0, 1)
        self.pdf.cell(150, 10, 'Total:', 0, 0, 'R')
        self.pdf.cell(40, 10, f"{order_data['total']} TK", 0, 1)
        
        # Footer
        self.pdf.ln(20)
        self.pdf.set_font('Arial', '', 10)
        self.pdf.cell(0, 10, 'Thank you for dining with us!', 0, 1, 'C')
        
        # Save
        filename = f"receipt_{order_data['order_id']}.pdf"
        self.pdf.output(filename)
        return filename