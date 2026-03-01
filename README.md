# E-Commerce Data Analysis Dashboard

## Overview

This final project for the Dicoding Data Analysis course provides an end-to-end data analysis on the **E-Commerce Public Dataset**. The project showcases data wrangling, exploratory data analysis, visualizations, advanced analysis (RFM & Geospatial), and an interactive Streamlit dashboard.

## Folder Structure

```
submission/
├── dashboard/
│   ├── dashboard.py         # Streamlit application script
│   └── main_data.csv        # Cleaned and processed dataset used in the dashboard
├── data/
│   ├── customers_dataset.csv
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   ├── products_dataset.csv
│   └── product_category_name_translation.csv
├── notebook.ipynb           # Jupyter Notebook with the end-to-end data analysis
├── README.md                # Project guidelines and instructions
├── requirements.txt         # Dependencies
└── url.txt                  # Dashboard URL on Streamlit Cloud
```

## Setup and Installation

To run this project on your local machine, please follow the steps below:

### 1. Clone or Download Repository

Ensure you have downloaded the entire submission folder.

### 2. Install Requirements

Open your terminal/command prompt and navigate into the `submission` directory. Using Python 3.9+, run:

```bash
pip install -r requirements.txt
```

### 3. Run the Dashboard

Navigate to the `dashboard/` directory or run Streamlit directly from the root using:

```bash
streamlit run dashboard/dashboard.py
```

This will open the application in your default web browser (typically at http://localhost:8501).

## Key Features

- **Visualizations**: Displays top & worst product categories and monthly order volumes.
- **RFM Analysis**: Automatically segments customers based on Recency, Frequency, and Monetary parameters.
- **Geospatial Analysis**: Unveils the distribution of customers across multiple states.
