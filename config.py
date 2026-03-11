import os

class Config:
    SECRET_KEY = 'dev-secret-key-change-in-production'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    USERS_CSV = os.path.join(DATA_DIR, 'users.csv')
    SALES_CSV = os.path.join(DATA_DIR, 'sales_data.csv')