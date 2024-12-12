from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from models.order import Order

class AnalyticsService:
    def __init__(self, db_config):
        self.db_config = db_config
        
    def get_sales_report(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        conn = psycopg2.connect(**self.db_config)
        query = """
            SELECT 
                DATE(order_date) as date,
                COUNT(*) as order_count,
                SUM(total_amount) as revenue,
                AVG(total_amount) as avg_order_value
            FROM orders
            WHERE order_date BETWEEN %s AND %s
            GROUP BY DATE(order_date)
            ORDER BY date
        """
        
        df = pd.read_sql_query(
            query, 
            conn, 
            params=(start_date, end_date)
        )
        conn.close()
        return df
        
    def get_popular_items(self, days: int = 30) -> List[Tuple[str, int]]:
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        start_date = datetime.now() - timedelta(days=days)
        
        cursor.execute("""
            SELECT 
                item_name,
                SUM(quantity) as total_quantity
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            WHERE o.order_date >= %s
            GROUP BY item_name
            ORDER BY total_quantity DESC
            LIMIT 10
        """, (start_date,))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return results
        
    def generate_sales_chart(self, days: int = 30) -> str:
        # Get sales data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        df = self.get_sales_report(start_date, end_date)
        
        # Create chart
        plt.figure(figsize=(12, 6))
        plt.plot(df['date'], df['revenue'], marker='o')
        plt.title('Daily Sales Revenue')
        plt.xlabel('Date')
        plt.ylabel('Revenue (TK)')
        plt.xticks(rotation=45)
        plt.grid(True)
        
        # Save chart
        chart_path = 'sales_chart.png'
        plt.savefig(chart_path, bbox_inches='tight')
        plt.close()
        
        return chart_path
        
    def get_customer_insights(self) -> Dict:
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        # Average order value
        cursor.execute("""
            SELECT AVG(total_amount)
            FROM orders
            WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
        """)
        avg_order_value = cursor.fetchone()[0]
        
        # Repeat customers
        cursor.execute("""
            SELECT COUNT(DISTINCT customer_id)
            FROM orders
            GROUP BY customer_id
            HAVING COUNT(*) > 1
        """)
        repeat_customers = len(cursor.fetchall())
        
        # Peak hours
        cursor.execute("""
            SELECT 
                EXTRACT(HOUR FROM order_date) as hour,
                COUNT(*) as order_count
            FROM orders
            WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY hour
            ORDER BY order_count DESC
            LIMIT 1
        """)
        peak_hour = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            'avg_order_value': avg_order_value,
            'repeat_customers': repeat_customers,
            'peak_hour': peak_hour[0] if peak_hour else None
        }
