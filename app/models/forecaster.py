"""
Demand Forecasting Module using Statsmodels
Implemented by Member 2
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Flask
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class Forecaster:
    def __init__(self):
        """Initialize Forecaster"""
        self.forecast = None
        self.model = None
        self.training_data = None
        self.performance_metrics = {}
    
    def prepare_data(self, sales_data):
        """
        Prepare and validate data for forecasting
        sales_data: list of dictionaries with 'ds' and 'y' keys
        """
        if not sales_data:
            return None
        
        try:
            df = pd.DataFrame(sales_data)
            df['ds'] = pd.to_datetime(df['ds'])
            df['y'] = pd.to_numeric(df['y'])
            
            # Clean data
            df = df.dropna()
            df = df.sort_values('ds')
            df = df.drop_duplicates(subset=['ds'], keep='last')
            
            # Check if we have enough data
            if len(df) < 7:
                return None
            
            self.training_data = df
            return df
            
        except Exception as e:
            print(f"Error preparing data: {str(e)}")
            return None
    
    def train_model(self, sales_data, periods=30):
        """
        Train Holt-Winters model and generate forecast
        """
        df = self.prepare_data(sales_data)
        if df is None:
            return None, "Insufficient data (need at least 7 days)"
        
        try:
            # Prepare time series
            ts_data = df.set_index('ds')['y']
            
            # Determine seasonality based on data length
            if len(df) >= 14:
                seasonal_periods = 7  # Weekly seasonality
                seasonal = 'add'
            else:
                seasonal_periods = None
                seasonal = None
            
            # Fit model
            self.model = ExponentialSmoothing(
                ts_data,
                seasonal_periods=seasonal_periods,
                trend='add',
                seasonal=seasonal,
                initialization_method='estimated'
            )
            
            fitted_model = self.model.fit()
            
            # Generate forecast
            forecast_values = fitted_model.forecast(periods)
            
            # Calculate confidence intervals (simplified)
            residuals = fitted_model.resid
            std_resid = np.std(residuals) if len(residuals) > 0 else 1
            
            # Create forecast dataframe
            last_date = df['ds'].iloc[-1]
            forecast_dates = pd.date_range(
                start=last_date + timedelta(days=1), 
                periods=periods
            )
            
            self.forecast = pd.DataFrame({
                'ds': forecast_dates,
                'yhat': forecast_values.values,
                'yhat_lower': forecast_values.values - 1.96 * std_resid,
                'yhat_upper': forecast_values.values + 1.96 * std_resid
            })
            
            # Calculate performance metrics
            self._calculate_metrics(df, fitted_model.fittedvalues)
            
            return self.forecast, f"Forecast generated for {periods} days"
            
        except Exception as e:
            return None, f"Forecasting failed: {str(e)}"
    
    def _calculate_metrics(self, actual, fitted):
        """Calculate performance metrics"""
        try:
            # Align data
            common_idx = actual.set_index('ds')['y'].index.intersection(fitted.index)
            y_true = actual.set_index('ds')['y'][common_idx]
            y_pred = fitted[common_idx]
            
            if len(y_true) > 0:
                mae = np.mean(np.abs(y_true - y_pred))
                mse = np.mean((y_true - y_pred)**2)
                rmse = np.sqrt(mse)
                mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
                
                self.performance_metrics = {
                    'MAE': round(mae, 2),
                    'RMSE': round(rmse, 2),
                    'MAPE': f"{round(mape, 2)}%",
                    'Data Points': len(y_true)
                }
        except:
            self.performance_metrics = {}
    
    def plot_forecast(self, save_path):
        """
        Plot forecast and save to file
        """
        if self.forecast is None or self.training_data is None:
            return False
        
        try:
            plt.figure(figsize=(12, 6))
            
            # Plot historical data
            plt.plot(self.training_data['ds'], self.training_data['y'], 
                    'b-', label='Historical', linewidth=2, marker='o', markersize=4)
            
            # Plot forecast
            plt.plot(self.forecast['ds'], self.forecast['yhat'], 
                    'r--', label='Forecast', linewidth=2, marker='s', markersize=4)
            
            # Plot confidence interval
            plt.fill_between(self.forecast['ds'], 
                            self.forecast['yhat_lower'], 
                            self.forecast['yhat_upper'], 
                            color='r', alpha=0.2, label='95% Confidence Interval')
            
            # Add vertical line to separate historical and forecast
            plt.axvline(x=self.training_data['ds'].iloc[-1], 
                       color='gray', linestyle=':', alpha=0.7)
            
            plt.title('Demand Forecast', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Sales Quantity', fontsize=12)
            plt.legend(loc='best')
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save plot
            plt.savefig(save_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return True
            
        except Exception as e:
            print(f"Error plotting forecast: {str(e)}")
            return False
    
    def plot_components(self, save_path):
        """
        Plot trend and seasonality components
        """
        if self.training_data is None or len(self.training_data) < 14:
            return False
        
        try:
            # Perform decomposition
            ts_data = self.training_data.set_index('ds')['y']
            decomposition = seasonal_decompose(ts_data, model='additive', period=7)
            
            fig, axes = plt.subplots(4, 1, figsize=(12, 10))
            
            # Original
            axes[0].plot(decomposition.observed)
            axes[0].set_title('Original Time Series', fontweight='bold')
            axes[0].set_ylabel('Sales')
            axes[0].grid(True, alpha=0.3)
            
            # Trend
            axes[1].plot(decomposition.trend)
            axes[1].set_title('Trend Component', fontweight='bold')
            axes[1].set_ylabel('Trend')
            axes[1].grid(True, alpha=0.3)
            
            # Seasonal
            axes[2].plot(decomposition.seasonal)
            axes[2].set_title('Seasonal Component (Weekly)', fontweight='bold')
            axes[2].set_ylabel('Seasonal')
            axes[2].grid(True, alpha=0.3)
            
            # Residual
            axes[3].plot(decomposition.resid)
            axes[3].set_title('Residual Component', fontweight='bold')
            axes[3].set_xlabel('Date')
            axes[3].set_ylabel('Residual')
            axes[3].grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(save_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return True
            
        except Exception as e:
            print(f"Error plotting components: {str(e)}")
            return False
    
    def get_forecast_summary(self):
        """Get forecast summary statistics"""
        if self.forecast is None:
            return {}
        
        summary = {
            'forecast_period': f"{self.forecast['ds'].min().strftime('%Y-%m-%d')} to {self.forecast['ds'].max().strftime('%Y-%m-%d')}",
            'total_days': len(self.forecast),
            'avg_forecast': round(self.forecast['yhat'].mean(), 2),
            'min_forecast': round(self.forecast['yhat'].min(), 2),
            'max_forecast': round(self.forecast['yhat'].max(), 2),
            'total_forecast': round(self.forecast['yhat'].sum(), 2)
        }
        
        # Add performance metrics
        if self.performance_metrics:
            summary['performance'] = self.performance_metrics
        
        return summary