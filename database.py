import psycopg2
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            self.create_tables()
        except Exception as e:
            print(f"Database connection error: {e}")

    def create_tables(self):
        commands = (
            """
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER REFERENCES customers(id),
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_amount DECIMAL(10,2),
                payment_method VARCHAR(50),
                status VARCHAR(20)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS order_items (
                id SERIAL PRIMARY KEY,
                order_id INTEGER REFERENCES orders(id),
                item_name VARCHAR(100),
                quantity INTEGER,
                unit_price DECIMAL(10,2),
                subtotal DECIMAL(10,2)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS food_items (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(50),
                price DECIMAL(10,2) NOT NULL
            )
            """
        )

        for command in commands:
            self.cursor.execute(command)
        self.conn.commit()

    def save_order(self, customer_data, order_items, total_amount):
        try:
            # Insert customer
            self.cursor.execute(
                "INSERT INTO customers (name, phone, address) VALUES (%s, %s, %s) RETURNING id",
                (customer_data['name'], customer_data['phone'], customer_data.get('address', ''))
            )
            customer_id = self.cursor.fetchone()[0]

            # Insert order
            self.cursor.execute(
                "INSERT INTO orders (customer_id, total_amount, payment_method, status) VALUES (%s, %s, %s, %s) RETURNING id",
                (customer_id, total_amount, customer_data.get('payment_method', 'Cash'), 'Completed')
            )
            order_id = self.cursor.fetchone()[0]

            # Insert order items
            for item in order_items:
                self.cursor.execute(
                    "INSERT INTO order_items (order_id, item_name, quantity, unit_price, subtotal) VALUES (%s, %s, %s, %s, %s)",
                    (order_id, item['name'], item['quantity'], item['price'], item['subtotal'])
                )

            self.conn.commit()
            return order_id
        except Exception as e:
            self.conn.rollback()
            print(f"Error saving order: {e}")
            return None

    def add_food_item(self, name, category, price):
        try:
            self.cursor.execute(
                "INSERT INTO food_items (name, category, price) VALUES (%s, %s, %s)",
                (name, category, price)
            )
            self.conn.commit()
            print(f"Food item '{name}' added successfully.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error adding food item: {e}")

    def update_food_item(self, food_id, name=None, category=None, price=None):
        try:
            updates = []
            params = []

            if name:
                updates.append("name = %s")
                params.append(name)
            if category:
                updates.append("category = %s")
                params.append(category)
            if price:
                updates.append("price = %s")
                params.append(price)

            params.append(food_id)
            query = f"UPDATE food_items SET {', '.join(updates)} WHERE id = %s"
            self.cursor.execute(query, params)
            self.conn.commit()
            print(f"Food item with ID {food_id} updated successfully.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error updating food item: {e}")

    def delete_food_item(self, food_id):
        try:
            self.cursor.execute("DELETE FROM food_items WHERE id = %s", (food_id,))
            self.conn.commit()
            print(f"Food item with ID {food_id} deleted successfully.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error deleting food item: {e}")

    def get_all_food_items(self):
        try:
            self.cursor.execute("SELECT * FROM food_items")
            food_items = self.cursor.fetchall()
            return food_items
        except Exception as e:
            print(f"Error fetching food items: {e}")
            return []

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

# Example usage:
# db = Database()
# db.connect()
# db.add_food_item("Pizza", "Fast Food", 12.99)
# db.update_food_item(1, price=13.99)
# db.delete_food_item(1)
# food_items = db.get_all_food_items()
# print(food_items)
# db.close()
