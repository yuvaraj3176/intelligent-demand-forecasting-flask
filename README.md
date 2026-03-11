# 📊 Intelligent Demand Forecasting System

A Flask-based web application for demand forecasting with user authentication, CRUD operations, and time series analysis using statsmodels.

---

## 🚀 Features

### 🔐 User Authentication
- Register new account
- Login/Logout functionality
- Session management
- Password hashing for security

### 📦 Sales Management (CRUD)
- **Create**: Add new sales records
- **Read**: View all sales in table format
- **Update**: Edit existing sales
- **Delete**: Remove sales records

### 🔮 Demand Forecasting
- Holt-Winters Exponential Smoothing model
- Forecast periods: 7, 15, 30, 60, 90 days
- 95% confidence intervals
- Performance metrics (MAE, RMSE, MAPE)

### 📈 Data Visualization
- Sales trend with moving average
- Category distribution (pie & bar charts)
- Monthly sales trend
- Top products analysis
- Forecast charts with confidence bands

### 🎨 User Interface
- Responsive Bootstrap 5 design
- Clean dashboard layout
- Mobile-friendly
- Flash messages for feedback

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.11, Flask 2.3.3 |
| Data Processing | Pandas, NumPy |
| Forecasting | Statsmodels 0.14.0 |
| Visualization | Matplotlib, Seaborn |
| Frontend | HTML5, CSS3, Bootstrap 5 |
| Storage | CSV files |
| Version Control | Git, GitHub |

---

## 📁 Project Structure
intelligent-demand-forecasting-flask/
├── app/
│ ├── init.py
│ ├── routes.py
│ ├── models/
│ │ ├── user.py
│ │ ├── sales.py
│ │ └── forecaster.py
│ ├── utils/
│ │ └── visualizer.py
│ ├── templates/
│ │ ├── base.html
│ │ ├── index.html
│ │ ├── register.html
│ │ ├── login.html
│ │ ├── dashboard.html
│ │ ├── sales.html
│ │ ├── add_sale.html
│ │ ├── update_sale.html
│ │ ├── forecast.html
│ │ └── charts.html
│ └── static/
│ ├── css/
│ │ └── style.css
│ └── images/
├── data/
│ ├── users.csv
│ └── sales_data.csv
├── config.py
├── run.py
├── requirements.txt
└── README.md

text

---

## 🚦 Installation

### Prerequisites
- Python 3.11 or higher
- Git
- pip package manager

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/intelligent-demand-forecasting-flask.git
   cd intelligent-demand-forecasting-flask
Create virtual environment

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Run the application

bash
python run.py
Open in browser

text
http://localhost:5000
📖 Usage Guide
First Time Users
Register - Click "Register" and create account

Login - Use your credentials

Add Sales Data - Go to Sales → Add New Sale (add 7-10 records)

Generate Forecast - Go to Forecast page, select period

View Charts - Go to Charts page for analytics

Sample Test Data
Product ID	Product Name	Date	Quantity	Category	Price
P001	Laptop	2024-01-01	50	Electronics	999.99
P002	T-Shirt	2024-01-02	100	Clothing	19.99
P003	Coffee Mug	2024-01-03	200	Other	9.99
P004	Smartphone	2024-01-04	75	Electronics	699.99
P005	Jeans	2024-01-05	60	Clothing	49.99
P006	Notebook	2024-01-06	150	Books	4.99
P007	Desk Chair	2024-01-07	25	Furniture	149.99
P008	Headphones	2024-01-08	90	Electronics	79.99
P009	Sweater	2024-01-09	80	Clothing	39.99
P010	Water Bottle	2024-01-10	120	Other	14.99
📊 Features Demo
Dashboard
Total sales count

Total revenue

Unique products

Quick action buttons

Sales Management
Sortable table

Edit/Delete buttons

Total calculation

Category badges

Forecasting
Period selection

Forecast chart

Data table

Confidence intervals

Performance metrics

Charts
Sales trend

Category distribution

Monthly trend

Top products

🤝 Team Members
Member	Responsibilities
Member 1	Project setup, Authentication, CRUD operations, Base templates
Member 2	Forecasting module, Visualization, Charts integration
🔧 Troubleshooting
Problem	Solution
Module not found	Run pip install -r requirements.txt
Port 5000 in use	Use python run.py --port=5001
No forecast	Add at least 7 days of sales data
Charts not showing	Check app/static/images/ folder exists
Login fails	Check data/users.csv has headers
📝 Requirements.txt
txt
Flask==2.3.3
Flask-Login==0.6.2
Werkzeug==2.3.7
pandas==2.0.3
numpy==1.24.3
statsmodels==0.14.0
matplotlib==3.7.2
seaborn==0.12.2
email-validator==2.0.0
🎯 Future Scope
Database integration (SQLite/PostgreSQL)

REST API development

ARIMA/LSTM models

Export to PDF/Excel

Email notifications

Dark mode

Bulk import from Excel

Docker deployment

📄 License
MIT License - Free to use and modify

⭐ Support
If you like this project, please give it a star on GitHub!

Made with ❤️ by Team Members
© 2024 Intelligent Demand Forecasting System

text

---

## ✅ **How to Add This File**

1. **In VS Code**, create new file: `README.md`
2. **Copy all the content above**
3. **Paste** into the file
4. **Save** (Ctrl+S)
5. **Replace** `YOUR_USERNAME` with your actual GitHub username
6. **Commit and push**:


-> Screenshorts   
<img width="1920" height="1080" alt="Screenshot 2026-03-12 021821" src="https://github.com/user-attachments/assets/a6e915d9-9497-4220-9045-8a78db016f73" />
<img width="1920" height="1080" alt="Screenshot 2026-03-12 021821" src="https://github.com/user-attachments/assets/a6e915d9-9497-4220-9045-8a78db016f73" />
<img width="766" height="842" alt="Screenshot 2026-03-12 021905" src="https://github.com/user-attachments/assets/16471ded-ebb1-436b-94fe-e8f8ec513b11" />
<img width="766" height="842" alt="Screenshot 2026-03-12 021905" src="https://github.com/user-attachments/assets/16471ded-ebb1-436b-94fe-e8f8ec513b11" />
<img width="704" height="833" alt="Screenshot 2026-03-12 021930" src="https://github.com/user-attachments/assets/a33332a9-a1b8-42fd-a289-2794ede96883" />
<img width="704" height="833" alt="Screenshot 2026-03-12 021930" src="https://github.com/user-attachments/assets/a33332a9-a1b8-42fd-a289-2794ede96883" />
<img width="1096" height="841" alt="Screenshot 2026-03-12 022100" src="https://github.com/user-attachments/assets/9103890b-ec93-463c-ac6d-3076d1f94e1d" />
<img width="1096" height="841" alt="Screenshot 2026-03-12 022100" src="https://github.com/user-attachments/assets/9103890b-ec93-463c-ac6d-3076d1f94e1d" />
<img width="1920" height="1080" alt="Screenshot 2026-03-12 020117" src="https://github.com/user-attachments/assets/a00aaf89-952a-431c-a77c-4117a56322c4" />
<img width="1920" height="1080" alt="Screenshot 2026-03-12 020117" src="https://github.com/user-attachments/assets/a00aaf89-952a-431c-a77c-4117a56322c4" />
<img width="1920" height="1080" alt="Screenshot 2026-03-12 021523" src="https://github.com/user-attachments/assets/4a98f0e5-4ea3-478a-931c-6778160b4195" />
<img width="1920" height="1080" alt="Screenshot 2026-03-12 021523" src="https://github.com/user-attachments/assets/4a98f0e5-4ea3-478a-931c-6778160b4195" />
<img width="1920" height="1080" alt="Screenshot 2026-03-12 021547" src="https://github.com/user-attachments/assets/01d1f4dd-ddfc-4487-bbf5-e32fdb2c9b86" />
<img width="1920" height="1080" alt="Screenshot 2026-03-12 021547" src="https://github.com/user-attachments/assets/01d1f4dd-ddfc-4487-bbf5-e32fdb2c9b86" />
bash
   git add README.md
   git commit -m "Add README documentation"
   git push origin main
