from flask import render_template, request, redirect, url_for, flash, session
from app.models.user import UserManager
from app.models.sales import SalesManager
from functools import wraps
from datetime import datetime

user_manager = UserManager()
sales_manager = SalesManager()

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def init_app(app):
    """Initialize all routes"""
    
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """User registration page"""
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            name = request.form['name']
            email = request.form['email']
            
            success, message = user_manager.register(username, password, name, email)
            flash(message, 'success' if success else 'danger')
            if success:
                return redirect(url_for('login'))
        return render_template('register.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login page"""
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            success, message, user = user_manager.login(username, password)
            if success:
                session['user_id'] = user['user_id']
                session['username'] = user['username']
                session['name'] = user['name']
                flash(message, 'success')
                return redirect(url_for('dashboard'))
            else:
                flash(message, 'danger')
        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        """Logout user"""
        session.clear()
        flash('Logged out successfully', 'success')
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """User dashboard"""
        sales = sales_manager.get_all_sales()
        
        # Calculate statistics
        total_sales = len(sales)
        total_revenue = sum(float(s.get('price', 0)) * float(s.get('sales_quantity', 0)) for s in sales)
        unique_products = len(set(s.get('product_id') for s in sales))
        
        return render_template('dashboard.html',
                             name=session.get('name'),
                             total_sales=total_sales,
                             total_revenue=round(total_revenue, 2),
                             unique_products=unique_products)
    
    @app.route('/sales')
    @login_required
    def sales():
        """View all sales records"""
        sales = sales_manager.get_all_sales()
        return render_template('sales.html', sales=sales)
    
    @app.route('/sales/add', methods=['GET', 'POST'])
    @login_required
    def add_sale():
        """Add new sale record"""
        if request.method == 'POST':
            product_id = request.form['product_id']
            product_name = request.form['product_name']
            date = request.form['date']
            quantity = request.form['quantity']
            category = request.form['category']
            price = request.form['price']
            
            success, message, sale_id = sales_manager.add_sale(
                product_id, product_name, date, quantity, 
                category, price, session['user_id']
            )
            flash(message, 'success' if success else 'danger')
            return redirect(url_for('sales'))
        
        # Pass today's date to template
        today = datetime.now().strftime('%Y-%m-%d')
        return render_template('add_sale.html', today=today)
    
    @app.route('/sales/update/<int:sale_id>', methods=['GET', 'POST'])
    @login_required
    def update_sale(sale_id):
        """Update existing sale record"""
        sale = sales_manager.get_sale_by_id(sale_id)
        if not sale:
            flash('Sale not found', 'danger')
            return redirect(url_for('sales'))
        
        if request.method == 'POST':
            update_data = {}
            if request.form['product_name']:
                update_data['product_name'] = request.form['product_name']
            if request.form['date']:
                update_data['date'] = request.form['date']
            if request.form['quantity']:
                update_data['sales_quantity'] = request.form['quantity']
            if request.form['category']:
                update_data['category'] = request.form['category']
            if request.form['price']:
                update_data['price'] = request.form['price']
            
            if update_data:
                success, message = sales_manager.update_sale(sale_id, **update_data)
                flash(message, 'success' if success else 'danger')
            return redirect(url_for('sales'))
        
        return render_template('update_sale.html', sale=sale)
    
    @app.route('/sales/delete/<int:sale_id>')
    @login_required
    def delete_sale(sale_id):
        """Delete sale record"""
        success, message = sales_manager.delete_sale(sale_id)
        flash(message, 'success' if success else 'danger')
        return redirect(url_for('sales'))
        # ===== Member 2 will implement these routes =====
    @app.route('/forecast')
    @login_required
    def forecast():
        """Forecast page - To be implemented by Member 2"""
        flash('Forecasting module is being developed by Member 2', 'info')
        return render_template('forecast.html', forecast=None)
    
    @app.route('/charts')
    @login_required
    def charts():
        """Charts page - To be implemented by Member 2"""
        flash('Charts module is being developed by Member 2', 'info')
        return render_template('charts.html')