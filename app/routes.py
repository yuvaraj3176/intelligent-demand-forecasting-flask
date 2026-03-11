from flask import render_template, request, redirect, url_for, flash, session
from app.models.user import UserManager
from app.models.sales import SalesManager
from functools import wraps
from datetime import datetime
from app.models.forecaster import Forecaster
from app.utils.visualizer import Visualizer
import os

# Initialize managers
user_manager = UserManager()
sales_manager = SalesManager()
forecaster = Forecaster()
visualizer = Visualizer()


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

        total_sales = len(sales)
        total_revenue = sum(
            float(s.get('price', 0)) * float(s.get('sales_quantity', 0)) for s in sales
        )
        unique_products = len(set(s.get('product_id') for s in sales))

        return render_template(
            'dashboard.html',
            name=session.get('name'),
            total_sales=total_sales,
            total_revenue=round(total_revenue, 2),
            unique_products=unique_products
        )


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
                product_id,
                product_name,
                date,
                quantity,
                category,
                price,
                session['user_id']
            )

            flash(message, 'success' if success else 'danger')
            return redirect(url_for('sales'))

        today = datetime.now().strftime('%Y-%m-%d')
        return render_template('add_sale.html', today=today)


    @app.route('/sales/update/<int:sale_id>', methods=['GET', 'POST'])
    @login_required
    def update_sale(sale_id):

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

        success, message = sales_manager.delete_sale(sale_id)

        flash(message, 'success' if success else 'danger')

        return redirect(url_for('sales'))


    # ===============================
    # MEMBER 2 MODULE IMPLEMENTATION
    # ===============================

    @app.route('/forecast', methods=['GET', 'POST'])
    @login_required
    def forecast():
        """Generate demand forecast"""

        forecast_data = None
        summary = None

        if request.method == 'POST':

            periods = int(request.form.get('periods', 30))

            sales = sales_manager.get_all_sales()

            sales_data = []

            for s in sales:
                try:
                    sales_data.append({
                        'ds': s['date'],
                        'y': float(s['sales_quantity'])
                    })
                except:
                    continue

            if len(sales_data) < 7:

                flash('Need at least 7 days of sales data for forecasting', 'danger')

            else:

                forecast_result, message = forecaster.train_model(
                    sales_data,
                    periods
                )

                if forecast_result is not None:

                    forecast_data = forecast_result.to_dict('records')
                    summary = forecaster.get_forecast_summary()

                    chart_path = os.path.join(
                        'app', 'static', 'images', 'forecast.png'
                    )

                    os.makedirs(os.path.dirname(chart_path), exist_ok=True)

                    forecaster.plot_forecast(chart_path)

                    if len(sales_data) >= 14:

                        comp_path = os.path.join(
                            'app', 'static', 'images', 'components.png'
                        )

                        forecaster.plot_components(comp_path)

                    flash(message, 'success')

                else:
                    flash(message, 'danger')

        return render_template(
            'forecast.html',
            forecast=forecast_data,
            summary=summary
        )


    @app.route('/charts')
    @login_required
    def charts():
        """Display analytics charts"""

        sales = sales_manager.get_all_sales()

        if not sales:

            flash('No sales data available to generate charts', 'warning')

        else:

            img_dir = os.path.join('app', 'static', 'images')

            os.makedirs(img_dir, exist_ok=True)

            trend_path = os.path.join(img_dir, 'trend.png')
            category_path = os.path.join(img_dir, 'category.png')
            monthly_path = os.path.join(img_dir, 'monthly.png')
            top_products_path = os.path.join(img_dir, 'top_products.png')

            visualizer.plot_sales_trend(sales, trend_path)
            visualizer.plot_category_distribution(sales, category_path)
            visualizer.plot_monthly_trend(sales, monthly_path)
            visualizer.plot_top_products(sales, top_products_path, n=5)

        return render_template('charts.html')