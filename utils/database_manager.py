import psycopg2
from datetime import datetime

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.conn = None
        self.cursor = None
        
    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.config)
            self.cursor = self.conn.cursor()
            self.create_tables()
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
            
    def create_tables(self):
        commands = (
            """
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                loyalty_points INTEGER DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER REFERENCES customers(id),
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_amount DECIMAL(10,2),
                payment_method VARCHAR(50),
                status VARCHAR(20),
                table_number INTEGER,
                waiter_name VARCHAR(100)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS order_items (
                id SERIAL PRIMARY KEY,
                order_id INTEGER REFERENCES orders(id),
                item_name VARCHAR(100),
                quantity INTEGER,
                unit_price DECIMAL(10,2),
                subtotal DECIMAL(10,2),
                special_instructions TEXT
            )
            """
        )
        
        for command in commands:
            self.cursor.execute(command)
        self.conn.commit()
        
    def save_order(self, customer_data, order_items, total_amount, table_number=None, waiter_name=None):
        try:
            # Check if customer exists
            self.cursor.execute(
                "SELECT id FROM customers WHERE phone = %s",
                (customer_data['phone'],)
            )
            result = self.cursor.fetchone()
            
            if result:
                customer_id = result[0]
                # Update loyalty points
                self.cursor.execute(
                    "UPDATE customers SET loyalty_points = loyalty_points + %s WHERE id = %s",
                    (int(total_amount / 100), customer_id)
                )
            else:
                # Insert new customer
                self.cursor.execute(
                    "INSERT INTO customers (name, phone, address) VALUES (%s, %s, %s) RETURNING id",
                    (customer_data['name'], customer_data['phone'], customer_data.get('address', ''))
                )
                customer_id = self.cursor.fetchone()[0]
            
            # Insert order
            self.cursor.execute(
                """
                INSERT INTO orders (customer_id, total_amount, payment_method, status, table_number, waiter_name) 
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                """,
                (customer_id, total_amount, customer_data.get('payment_method', 'Cash'), 
                 'Completed', table_number, waiter_name)
            )
            order_id = self.cursor.fetchone()[0]
            
            # Insert order items
            for item in order_items:
                self.cursor.execute(
                    """
                    INSERT INTO order_items (order_id, item_name, quantity, unit_price, subtotal, special_instructions) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (order_id, item['name'], item['quantity'], item['price'], 
                     item['subtotal'], item.get('special_instructions', ''))
                )
                
            self.conn.commit()
            return order_id
        except Exception as e:
            self.conn.rollback()
            print(f"Error saving order: {e}")
            return None
            
    def get_customer_orders(self, phone):
        try:
            self.cursor.execute(
                """
                SELECT o.id, o.order_date, o.total_amount, o.status
                FROM orders o
                JOIN customers c ON o.customer_id = c.id
                WHERE c.phone = %s
                ORDER BY o.order_date DESC
                """,
                (phone,)
            )
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching customer orders: {e}")
            return []
            
    def get_daily_sales(self, date=None):
        try:
            if not date:
                date = datetime.now().date()
            self.cursor.execute(
                """
                SELECT SUM(total_amount) as total_sales, COUNT(*) as order_count
                FROM orders
                WHERE DATE(order_date) = %s
                """,
                (date,)
            )
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching daily sales: {e}")
            return None
            
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()