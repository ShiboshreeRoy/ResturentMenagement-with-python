from typing import Dict, Optional
from decimal import Decimal
from datetime import datetime
import psycopg2
from models.menu_item import MenuItem

class InventoryManager:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None
        self.cursor = None
        
    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            self.create_tables()
            return True
        except Exception as e:
            print(f"Inventory database error: {e}")
            return False
            
    def create_tables(self):
        commands = (
            """
            CREATE TABLE IF NOT EXISTS inventory (
                id SERIAL PRIMARY KEY,
                item_name VARCHAR(100) NOT NULL,
                quantity DECIMAL(10,2) NOT NULL,
                unit VARCHAR(20) NOT NULL,
                reorder_level DECIMAL(10,2),
                cost_per_unit DECIMAL(10,2),
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS inventory_transactions (
                id SERIAL PRIMARY KEY,
                inventory_id INTEGER REFERENCES inventory(id),
                transaction_type VARCHAR(20) NOT NULL,
                quantity DECIMAL(10,2) NOT NULL,
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reference_id VARCHAR(100),
                notes TEXT
            )
            """
        )
        
        for command in commands:
            self.cursor.execute(command)
        self.conn.commit()
        
    def update_inventory(self, item_name: str, quantity: Decimal, 
                        transaction_type: str, reference_id: Optional[str] = None):
        try:
            # Get current inventory
            self.cursor.execute(
                "SELECT id, quantity FROM inventory WHERE item_name = %s",
                (item_name,)
            )
            result = self.cursor.fetchone()
            
            if result:
                inventory_id, current_quantity = result
                new_quantity = (current_quantity + quantity 
                              if transaction_type == 'IN' else current_quantity - quantity)
                
                # Update inventory
                self.cursor.execute(
                    """
                    UPDATE inventory 
                    SET quantity = %s, last_updated = CURRENT_TIMESTAMP 
                    WHERE id = %s
                    """,
                    (new_quantity, inventory_id)
                )
                
                # Record transaction
                self.cursor.execute(
                    """
                    INSERT INTO inventory_transactions 
                    (inventory_id, transaction_type, quantity, reference_id) 
                    VALUES (%s, %s, %s, %s)
                    """,
                    (inventory_id, transaction_type, quantity, reference_id)
                )
                
                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error updating inventory: {e}")
            return False
            
    def check_low_stock(self) -> Dict[str, Decimal]:
        try:
            self.cursor.execute(
                """
                SELECT item_name, quantity, reorder_level 
                FROM inventory 
                WHERE quantity <= reorder_level
                """
            )
            results = self.cursor.fetchall()
            return {row[0]: row[1] for row in results}
        except Exception as e:
            print(f"Error checking stock levels: {e}")
            return {}
            
    def get_inventory_value(self) -> Decimal:
        try:
            self.cursor.execute(
                """
                SELECT SUM(quantity * cost_per_unit) 
                FROM inventory
                """
            )
            result = self.cursor.fetchone()
            return result[0] if result[0] else Decimal('0')
        except Exception as e:
            print(f"Error calculating inventory value: {e}")
            return Decimal('0')
