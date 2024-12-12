from fpdf import FPDF
import os
import win32print
import win32api
import tempfile
from datetime import datetime

class PrintManager:
    def __init__(self):
        self.pdf = FPDF()
        
    def create_invoice(self, order_data, customer_data, items):
        self.pdf.add_page()
        
        # Premium Header Design
        self.pdf.set_fill_color(26, 35, 126)  # Dark blue background
        self.pdf.rect(0, 0, 210, 40, 'F')
        
        # Restaurant Logo & Name
        self.pdf.set_font('Arial', 'B', 24)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.cell(0, 20, 'PakPak Restaurant', 0, 1, 'C')
        self.pdf.set_font('Arial', '', 12)
        self.pdf.cell(0, 10, 'Premium Bangladeshi Cuisine', 0, 1, 'C')
        
        # Reset text color
        self.pdf.set_text_color(0, 0, 0)
        
        # Customer & Order Info
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 10, f"Invoice #{order_data['order_id']}", 0, 1)
        self.pdf.cell(0, 10, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}", 0, 1)
        self.pdf.ln(5)
        
        # Customer Details
        self.pdf.set_fill_color(240, 240, 240)
        self.pdf.cell(0, 10, 'Customer Details', 1, 1, 'L', True)
        self.pdf.set_font('Arial', '', 11)
        self.pdf.cell(0, 8, f"Name: {customer_data['name']}", 0, 1)
        self.pdf.cell(0, 8, f"Phone: {customer_data['phone']}", 0, 1)
        self.pdf.cell(0, 8, f"Address: {customer_data['address']}", 0, 1)
        
        # Order Items Table
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 11)
        self.pdf.set_fill_color(26, 35, 126)
        self.pdf.set_text_color(255, 255, 255)
        
        # Table Header
        col_widths = [80, 30, 40, 40]
        self.pdf.cell(col_widths[0], 10, 'Item', 1, 0, 'C', True)
        self.pdf.cell(col_widths[1], 10, 'Qty', 1, 0, 'C', True)
        self.pdf.cell(col_widths[2], 10, 'Price', 1, 0, 'C', True)
        self.pdf.cell(col_widths[3], 10, 'Total', 1, 1, 'C', True)
        
        # Table Content
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_font('Arial', '', 11)
        
        total = 0
        for item in items:
            self.pdf.cell(col_widths[0], 8, item['name'], 1)
            self.pdf.cell(col_widths[1], 8, str(item['quantity']), 1, 0, 'C')
            self.pdf.cell(col_widths[2], 8, f"{item['price']} TK", 1, 0, 'R')
            self.pdf.cell(col_widths[3], 8, f"{item['subtotal']} TK", 1, 1, 'R')
            total += item['subtotal']
        
        # Summary
        self.pdf.ln(5)
        summary_x = 120
        self.pdf.set_font('Arial', 'B', 11)
        
        # Subtotal
        self.pdf.cell(summary_x)
        self.pdf.cell(40, 8, 'Subtotal:', 0, 0, 'R')
        self.pdf.cell(40, 8, f"{order_data['subtotal']}", 0, 1, 'R')
        
        # VAT
        self.pdf.cell(summary_x)
        self.pdf.cell(40, 8, 'VAT (15%):', 0, 0, 'R')
        self.pdf.cell(40, 8, f"{order_data['vat']}", 0, 1, 'R')
        
        # Total
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(summary_x)
        self.pdf.cell(40, 10, 'Total:', 0, 0, 'R')
        self.pdf.cell(40, 10, f"{order_data['total']}", 0, 1, 'R')
        
        # Footer
        self.pdf.ln(15)
        self.pdf.set_font('Arial', 'I', 10)
        self.pdf.cell(0, 10, 'Thank you for dining with us!', 0, 1, 'C')
        self.pdf.cell(0, 10, 'Please visit us again.', 0, 1, 'C')
        
        # Save to temporary file
        temp_file = tempfile.mktemp('.pdf')
        self.pdf.output(temp_file)
        return temp_file
        
    def print_invoice(self, order_data, customer_data, items):
        try:
            # Generate PDF
            pdf_file = self.create_invoice(order_data, customer_data, items)
            
            # Get default printer
            printer_name = win32print.GetDefaultPrinter()
            
            # Print PDF
            win32api.ShellExecute(
                0,
                "print",
                pdf_file,
                f'/d:"{printer_name}"',
                ".",
                0
            )
            
            # Clean up temporary file
            os.remove(pdf_file)
            return True
        except Exception as e:
            print(f"Printing error: {e}")
            return False