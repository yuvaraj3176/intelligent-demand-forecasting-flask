import hashlib
import csv
import os
from datetime import datetime
from config import Config

class UserManager:
    def __init__(self):
        self.data_file = Config.USERS_CSV
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create users.csv with headers if it doesn't exist"""
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['user_id', 'username', 'password_hash', 'name', 'email', 'created_date'])
    
    def _hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _get_next_id(self):
        """Get next available user ID"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                rows = list(reader)
                return max(int(row[0]) for row in rows) + 1 if rows else 1
        except:
            return 1
    
    def register(self, username, password, name, email):
        """Register a new user"""
        # Check if username exists
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == username:
                        return False, "Username already exists!"
        except:
            pass
        
        # Create new user
        user_id = self._get_next_id()
        password_hash = self._hash_password(password)
        created_date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            with open(self.data_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([user_id, username, password_hash, name, email, created_date])
            return True, "Registration successful! Please login."
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def login(self, username, password):
        """Login user"""
        password_hash = self._hash_password(password)
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == username and row['password_hash'] == password_hash:
                        user = {
                            'user_id': row['user_id'],
                            'username': row['username'],
                            'name': row['name'],
                            'email': row['email']
                        }
                        return True, f"Welcome back, {row['name']}!", user
                return False, "Invalid username or password!", None
        except Exception as e:
            return False, f"Login failed: {str(e)}", None