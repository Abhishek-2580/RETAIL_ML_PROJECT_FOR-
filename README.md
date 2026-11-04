# RetailPulse: Retail Analytics & Machine Learning Project

End-to-end analysis of a retail business: sales EDA, demand forecasting, inventory risk, customer segmentation and churn prediction.

## Project Goals
- Understand sales, profit and performance by category, store, city and channel
- Forecast product demand for the next 4 weeks
- Identify stockout risk and overstock in inventory
- Segment customers using RFM analysis
- Predict which customers are likely to churn

## Datasets
| File | Description |
|------|-------------|
| `bm_customers.csv` | Customer details (age, gender, loyalty segment, registration date) |
| `bm_sales.csv` | Transaction-level sales |
| `bm_skus.csv` | Product details (category, subcategory, cost and list price) |
| `bm_stores.csv` | Store details (city, opening date) |
| `bm_inventory.csv` | Stock on hand, reorder points, restock dates |

## Approach

### 1. Data Cleaning & EDA
- Renamed columns, fixed date types, removed duplicates, validated keys across tables
- Merged sales, product, customer, store and inventory data
- Analysed monthly trends, category/subcategory profit, store, city and channel performance

### 2. Demand Forecasting
- Time-based train/test split (last 30 days held out)
- Baselines: last-week repeat, 28-day average, same weeks last year
- Model: Prophet (weekly level, 4-week horizon)
- Evaluation: MAE, RMSE, WAPE and a 13-window rolling backtest
- Covers the top 5 products by volume

### 3. Inventory Analysis
- Items below reorder point, weeks of cover, dead stock
- Excess stock value beyond 26 weeks of demand
- Stockout risk status per product (OK / WATCH / STOCKOUT RISK)

### 4. Customer Segmentation
- RFM features (log-transformed and standardised)
- K-Means with k = 3, chosen using silhouette score
- Segments compared with loyalty tier, age and gender

### 5. Churn Prediction
- Churn = no purchase in the following 60 days
- Features built only from data before the cutoff (no leakage)
- Models: Logistic Regression and Random Forest
- Metrics: ROC-AUC, PR-AUC, 5-fold cross-validation

## Results
> Fill these in from your notebook outputs.

| Task | Best Model | Key Metric |
|------|-----------|------------|
| Demand forecast | _e.g. Prophet / blend_ | WAPE: _xx%_ |
| Segmentation | K-Means (k=3) | Silhouette: _x.xx_ |
| Churn prediction | _e.g. Random Forest_ | AUC: _x.xx_ |

**Key findings**
- _Top category / city / channel by revenue_
- _Products at stockout risk_
- _Share of stock value that is excess_
- _Main differences between customer segments_

## Project Structure
```
├── RETAIL_ML_PROJECT.ipynb   # Main notebook
├── data/                     # Exported outputs (forecasts, segments, inventory)
├── forecast_next_4_weeks.csv
├── README.md
└── requirements.txt
```

## How to Run
```bash
pip install -r requirements.txt
jupyter notebook RETAIL_ML_PROJECT.ipynb
```
Place the five `bm_*.csv` files in the same folder as the notebook before running.

## Tech Stack
Python, pandas, NumPy, Matplotlib, Seaborn, scikit-learn, Prophet, MLflow

## Author
_Your name_ · _LinkedIn / GitHub link_
