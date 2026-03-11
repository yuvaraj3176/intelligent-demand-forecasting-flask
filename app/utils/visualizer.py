"""
Visualization Module for Sales Analytics
Implemented by Member 2
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Flask
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import seaborn as sns

class Visualizer:
    def __init__(self):
        """Initialize Visualizer with styling"""
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B8F6B', '#8E44AD']
        
    def plot_sales_trend(self, sales_data, save_path):
        """
        Plot sales trend with moving average
        """
        if not sales_data:
            return False
        
        try:
            df = pd.DataFrame(sales_data)
            df['date'] = pd.to_datetime(df['date'])
            df['sales_quantity'] = pd.to_numeric(df['sales_quantity'])
            df = df.sort_values('date')
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            
            # Plot 1: Sales trend
            ax1.plot(df['date'], df['sales_quantity'], 
                    marker='o', linestyle='-', color=self.colors[0], 
                    markersize=4, linewidth=2, label='Daily Sales')
            
            # Add 7-day moving average if enough data
            if len(df) >= 7:
                df['ma_7'] = df['sales_quantity'].rolling(window=7, min_periods=1).mean()
                ax1.plot(df['date'], df['ma_7'], 
                        linestyle='--', color=self.colors[2], 
                        linewidth=2, label='7-Day Moving Average')
            
            ax1.set_title('Sales Trend Over Time', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Sales Quantity')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Plot 2: Distribution
            ax2.hist(df['sales_quantity'], bins=min(20, len(df)), 
                    color=self.colors[1], alpha=0.7, edgecolor='black')
            ax2.set_title('Sales Distribution', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Sales Quantity')
            ax2.set_ylabel('Frequency')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(save_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return True
            
        except Exception as e:
            print(f"Error plotting sales trend: {str(e)}")
            return False
    
    def plot_category_distribution(self, sales_data, save_path):
        """
        Plot sales distribution by category
        """
        if not sales_data:
            return False
        
        try:
            df = pd.DataFrame(sales_data)
            df['sales_quantity'] = pd.to_numeric(df['sales_quantity'])
            
            # Aggregate by category
            category_sales = df.groupby('category')['sales_quantity'].sum().sort_values(ascending=False)
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            # Pie chart
            if len(category_sales) > 6:
                # Group small categories
                top_categories = category_sales.head(5)
                others = category_sales.iloc[5:].sum()
                if others > 0:
                    top_categories['Others'] = others
                plot_data = top_categories
            else:
                plot_data = category_sales
            
            colors = self.colors[:len(plot_data)]
            wedges, texts, autotexts = ax1.pie(plot_data.values, 
                                               labels=plot_data.index,
                                               autopct='%1.1f%%',
                                               colors=colors,
                                               startangle=90)
            
            ax1.set_title('Sales by Category (Pie Chart)', fontsize=14, fontweight='bold')
            
            # Bar chart
            bars = ax2.bar(range(len(category_sales)), category_sales.values, 
                          color=self.colors * (len(category_sales) // len(self.colors) + 1))
            ax2.set_title('Sales by Category (Bar Chart)', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Category')
            ax2.set_ylabel('Total Sales')
            ax2.set_xticks(range(len(category_sales)))
            ax2.set_xticklabels(category_sales.index, rotation=45, ha='right')
            
            # Add value labels
            for bar, value in zip(bars, category_sales.values):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(value)}', ha='center', va='bottom', fontsize=9)
            
            ax2.grid(True, alpha=0.3, axis='y')
            
            plt.tight_layout()
            plt.savefig(save_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return True
            
        except Exception as e:
            print(f"Error plotting category distribution: {str(e)}")
            return False
    
    def plot_monthly_trend(self, sales_data, save_path):
        """
        Plot monthly sales trend
        """
        if not sales_data or len(sales_data) < 30:
            return False
        
        try:
            df = pd.DataFrame(sales_data)
            df['date'] = pd.to_datetime(df['date'])
            df['sales_quantity'] = pd.to_numeric(df['sales_quantity'])
            df['month'] = df['date'].dt.to_period('M')
            
            # Aggregate by month
            monthly = df.groupby('month')['sales_quantity'].sum()
            
            plt.figure(figsize=(12, 6))
            plt.plot(range(len(monthly)), monthly.values, 
                    marker='o', linestyle='-', color=self.colors[0], linewidth=2, markersize=8)
            
            plt.title('Monthly Sales Trend', fontsize=14, fontweight='bold')
            plt.xlabel('Month')
            plt.ylabel('Total Sales')
            plt.xticks(range(len(monthly)), [str(m) for m in monthly.index], rotation=45)
            plt.grid(True, alpha=0.3)
            
            # Add value labels
            for i, value in enumerate(monthly.values):
                plt.text(i, value, f'{int(value)}', ha='center', va='bottom', fontsize=9)
            
            plt.tight_layout()
            plt.savefig(save_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return True
            
        except Exception as e:
            print(f"Error plotting monthly trend: {str(e)}")
            return False
    
    def plot_top_products(self, sales_data, save_path, n=10):
        """
        Plot top products by sales quantity
        """
        if not sales_data:
            return False
        
        try:
            df = pd.DataFrame(sales_data)
            df['sales_quantity'] = pd.to_numeric(df['sales_quantity'])
            
            # Get top products
            top_products = df.groupby('product_name')['sales_quantity'].sum().nlargest(n)
            
            plt.figure(figsize=(12, 6))
            bars = plt.barh(range(len(top_products)), top_products.values, 
                           color=self.colors * (len(top_products) // len(self.colors) + 1))
            
            plt.title(f'Top {n} Products by Sales', fontsize=14, fontweight='bold')
            plt.xlabel('Total Sales Quantity')
            plt.ylabel('Product')
            plt.yticks(range(len(top_products)), top_products.index)
            
            # Add value labels
            for bar, value in zip(bars, top_products.values):
                width = bar.get_width()
                plt.text(width, bar.get_y() + bar.get_height()/2., 
                        f'{int(value)}', ha='left', va='center', fontsize=9)
            
            plt.grid(True, alpha=0.3, axis='x')
            plt.tight_layout()
            plt.savefig(save_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return True
            
        except Exception as e:
            print(f"Error plotting top products: {str(e)}")
            return False