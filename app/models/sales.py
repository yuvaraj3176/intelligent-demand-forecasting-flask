import csv
import os
from datetime import datetime
from config import Config

class SalesManager:
    def __init__(self):
        self.data_file = Config.SALES_CSV
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create sales_data.csv with headers if it doesn't exist"""
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['sale_id', 'product_id', 'product_name', 'date', 
                               'sales_quantity', 'category', 'price', 'created_by', 'created_at'])
    
    def _get_next_id(self):
        """Get next available sale ID"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                rows = list(reader)
                return max(int(row[0]) for row in rows) + 1 if rows else 1
        except:
            return 1
    
    def add_sale(self, product_id, product_name, date, quantity, category, price, user_id):
        """Add a new sales record"""
        sale_id = self._get_next_id()
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            with open(self.data_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([sale_id, product_id, product_name, date, quantity, 
                               category, price, user_id, created_at])
            return True, "Sale added successfully!", sale_id
        except Exception as e:
            return False, f"Failed to add sale: {str(e)}", None
    
    def get_all_sales(self):
        """Get all sales records"""
        sales = []
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    sales.append(row)
            return sales
        except:
            return []
    
    def get_sale_by_id(self, sale_id):
        """Get a specific sale by ID"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if int(row['sale_id']) == sale_id:
                        return row
            return None
        except:
            return None
    
    def update_sale(self, sale_id, **kwargs):
        """Update a sales record"""
        sales = self.get_all_sales()
        updated = False
        
        for sale in sales:
            if int(sale['sale_id']) == sale_id:
                for key, value in kwargs.items():
                    if key in sale and value:
                        sale[key] = value
                updated = True
                break
        
        if not updated:
            return False, f"Sale ID {sale_id} not found!"
        
        try:
            with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
                if sales:
                    writer = csv.DictWriter(file, fieldnames=sales[0].keys())
                    writer.writeheader()
                    writer.writerows(sales)
            return True, "Sale updated successfully!"
        except Exception as e:
            return False, f"Failed to update sale: {str(e)}"
    
    def delete_sale(self, sale_id):
        """Delete a sales record"""
        sales = self.get_all_sales()
        filtered_sales = [s for s in sales if int(s['sale_id']) != sale_id]
        
        if len(filtered_sales) == len(sales):
            return False, f"Sale ID {sale_id} not found!"
        
        try:
            with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
                if filtered_sales:
                    writer = csv.DictWriter(file, fieldnames=filtered_sales[0].keys())
                    writer.writeheader()
                    writer.writerows(filtered_sales)
                else:
                    # If no records, write only headers
                    writer = csv.writer(file)
                    writer.writerow(['sale_id', 'product_id', 'product_name', 'date', 
                                   'sales_quantity', 'category', 'price', 'created_by', 'created_at'])
            return True, "Sale deleted successfully!"
        except Exception as e:
            return False, f"Failed to delete sale: {str(e)}"