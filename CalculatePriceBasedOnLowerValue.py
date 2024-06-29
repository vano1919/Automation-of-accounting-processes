import sqlite3
import os
from CalculatePriceBasedOnHigherValue import CalculatePriceBasedOnHigherValue


class CalculatePriceBasedOnLowerValue:

    def __init__(self):
        self.db_path = "D:\PythonGeneral\pythonOop\dataFiles\products.sqlite3"
        self._ensure_directory_exists()
        self._connect()

        # Create table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                ID TEXT PRIMARY KEY,
                oldValue REAL
            )
        ''')

    def _ensure_directory_exists(self):
        directory = os.path.dirname(self.db_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def _connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_old_value(self, product_id):
        """Retrieve the oldValue for a given product_id."""
        self.cursor.execute('SELECT oldValue FROM Products WHERE ID=?', (product_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def add_product(self, product_id, product_new_value):
        """Add a product with its ID and newValue to the SQL file."""
        self.cursor.execute('INSERT OR IGNORE INTO Products (ID, oldValue) VALUES (?, ?)',
                            (product_id, product_new_value))
        self.conn.commit()

    def delete_product(self, product_id):
        """Delete a product from the SQL file based on its ID."""
        self.cursor.execute('DELETE FROM Products WHERE ID=?', (product_id,))
        self.conn.commit()

    def product_exists(self, product_id):
        """Check if a product with the given ID exists in the database."""
        self.cursor.execute('SELECT ID FROM Products WHERE ID=?', (product_id,))
        result = self.cursor.fetchone()
        return True if result else False

    def calculate_final_price(self, product_id, product_new_value):
        old_value = self.get_old_value(product_id)

        # If old_value exists for the product_id
        if old_value:
            final_price = (old_value + product_new_value) / 2
            self.delete_product(product_id)
            return CalculatePriceBasedOnHigherValue.calculate_final_price(final_price)
        else:
            self.add_product(product_id, product_new_value)
            return None



