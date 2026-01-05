"""
ETL Pipeline for Retail Pricing Data (May-2022.csv)
Adapted from app.py structure but using pandas instead of PySpark for Cloud Function compatibility.
"""

import pandas as pd
import numpy as np
import json
import os
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


def load_data(file_path: str) -> pd.DataFrame:
    """Load CSV data into pandas DataFrame."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} records from {file_path}")
    return df


def extract_size_from_sku(sku: str) -> str:
    """Extract size from SKU pattern."""
    import re
    if pd.isna(sku) or not isinstance(sku, str):
        return None
    size_pattern = r'_([SMXL\d]+XL?)$'
    match = re.search(size_pattern, sku)
    if match:
        return match.group(1)
    return None


def clean_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and transform the data.
    - Handle missing values
    - Extract size from SKU
    - Calculate price metrics
    """
    print("Starting data cleaning and transformation...")
    initial_count = len(df)
    
    df_clean = df.copy()
    
    # Extract size from SKU
    df_clean['Size'] = df_clean['Sku'].apply(extract_size_from_sku)
    
    # Handle missing values
    df_clean['Weight'] = pd.to_numeric(df_clean['Weight'], errors='coerce').fillna(0)
    
    # Ensure numeric columns are actually numeric
    platform_cols = [col for col in df_clean.columns if 'MRP' in col and col not in ['MRP Old', 'Final MRP Old']]
    for col in ['TP'] + platform_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    # Filter out rows where all platform prices are missing
    df_clean = df_clean[df_clean[platform_cols].notna().any(axis=1)]
    
    # Remove invalid TP
    df_clean = df_clean[df_clean['TP'] > 0]
    
    # Standardize text fields
    if 'Catalog' in df_clean.columns:
        df_clean['Catalog'] = df_clean['Catalog'].str.strip()
    if 'Category' in df_clean.columns:
        df_clean['Category'] = df_clean['Category'].str.strip()
    
    # Calculate price metrics
    platform_prices = np.array([df_clean[col].values for col in platform_cols]).T
    
    df_clean['min_price'] = np.nanmin(platform_prices, axis=1)
    df_clean['max_price'] = np.nanmax(platform_prices, axis=1)
    df_clean['avg_price'] = np.nanmean(platform_prices, axis=1)
    df_clean['price_range'] = df_clean['max_price'] - df_clean['min_price']
    
    # Find cheapest platform
    cheapest_platforms = []
    for i, row in df_clean.iterrows():
        prices = {col: row[col] for col in platform_cols if pd.notna(row[col])}
        if prices:
            cheapest = min(prices.items(), key=lambda x: x[1])
            platform_name = cheapest[0].replace(' MRP', '').lower().replace(' ', '_')
            cheapest_platforms.append(platform_name)
        else:
            cheapest_platforms.append(None)
    
    df_clean['cheapest_platform'] = cheapest_platforms
    df_clean['cheapest_price'] = df_clean['min_price']
    
    # Remove duplicates
    df_clean = df_clean.drop_duplicates(subset=['Sku'], keep='first')
    
    final_count = len(df_clean)
    print(f"Cleaning completed: {initial_count} -> {final_count} records")
    
    return df_clean


def compute_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute comprehensive KPIs for pricing analysis.
    Returns dictionary of KPI DataFrames and statistics.
    """
    print("Computing KPIs...")
    
    platform_cols = [col for col in df.columns if 'MRP' in col and col not in ['MRP Old', 'Final MRP Old']]
    
    # 1. Overall Statistics
    overall_stats = {
        'total_products': int(len(df)),
        'total_skus': int(df['Sku'].nunique()),
        'total_styles': int(df['Style Id'].nunique()),
        'total_catalogs': int(df['Catalog'].nunique()),
        'total_categories': int(df['Category'].nunique()),
        'price_statistics': {
            'min_price': float(df['min_price'].min()),
            'max_price': float(df['max_price'].max()),
            'avg_price': float(df['avg_price'].mean()),
            'median_price': float(df['avg_price'].median()),
            'std_price': float(df['avg_price'].std())
        }
    }
    
    # 2. Category-wise KPIs
    category_kpi = df.groupby('Category').agg({
        'min_price': ['min', 'max', 'mean', 'count'],
        'Sku': 'nunique',
        'Style Id': 'nunique'
    }).round(2)
    category_kpi.columns = ['min_price', 'max_price', 'avg_price', 'product_count', 'unique_skus', 'unique_styles']
    category_kpi = category_kpi.reset_index()
    
    # 3. Catalog-wise KPIs
    catalog_kpi = df.groupby('Catalog').agg({
        'min_price': ['min', 'max', 'mean', 'count'],
        'Sku': 'nunique',
        'Category': 'nunique'
    }).round(2)
    catalog_kpi.columns = ['min_price', 'max_price', 'avg_price', 'product_count', 'unique_skus', 'unique_categories']
    catalog_kpi = catalog_kpi.reset_index()
    
    # 4. Platform Comparison KPIs
    platform_stats = {}
    for col in platform_cols:
        platform_name = col.replace(' MRP', '').lower().replace(' ', '_')
        platform_data = df[col].dropna()
        if len(platform_data) > 0:
            platform_stats[platform_name] = {
                'products_available': int(len(platform_data)),
                'min_price': float(platform_data.min()),
                'max_price': float(platform_data.max()),
                'avg_price': float(platform_data.mean()),
                'median_price': float(platform_data.median()),
                'coverage_pct': float(len(platform_data) / len(df) * 100)
            }
    
    # 5. Cheapest Platform Analysis
    cheapest_platform_kpi = df['cheapest_platform'].value_counts().to_dict()
    
    # 6. Price Variation Analysis
    price_variation_kpi = {
        'products_with_variation': int((df['price_range'] > 0).sum()),
        'products_uniform_price': int((df['price_range'] == 0).sum()),
        'avg_price_range': float(df['price_range'].mean()),
        'max_price_range': float(df['price_range'].max())
    }
    
    # 7. Top Products by Price Range (most variation)
    top_variation_products = df.nlargest(20, 'price_range')[
        ['Sku', 'Style Id', 'Catalog', 'Category', 'min_price', 'max_price', 'price_range', 'cheapest_platform']
    ].to_dict('records')
    
    # 8. Size Distribution
    size_kpi = df.groupby('Size').agg({
        'Sku': 'count',
        'min_price': 'mean',
        'max_price': 'mean'
    }).round(2)
    size_kpi.columns = ['product_count', 'avg_min_price', 'avg_max_price']
    size_kpi = size_kpi.reset_index()
    
    return {
        'overall_stats': overall_stats,
        'category_kpi': category_kpi.to_dict('records'),
        'catalog_kpi': catalog_kpi.to_dict('records'),
        'platform_stats': platform_stats,
        'cheapest_platform_kpi': cheapest_platform_kpi,
        'price_variation_kpi': price_variation_kpi,
        'top_variation_products': top_variation_products,
        'size_kpi': size_kpi.to_dict('records'),
        'timestamp': datetime.now().isoformat()
    }


def save_outputs(kpis: Dict[str, Any], output_dir: str):
    """Save KPI results to JSON and Parquet files."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save as JSON
    json_path = os.path.join(output_dir, 'kpis.json')
    with open(json_path, 'w') as f:
        json.dump(kpis, f, indent=2, default=str)
    print(f"KPIs saved to {json_path}")
    
    # Save individual DataFrames as CSV for easy access
    if 'category_kpi' in kpis:
        pd.DataFrame(kpis['category_kpi']).to_csv(
            os.path.join(output_dir, 'category_kpi.csv'), index=False
        )
    if 'catalog_kpi' in kpis:
        pd.DataFrame(kpis['catalog_kpi']).to_csv(
            os.path.join(output_dir, 'catalog_kpi.csv'), index=False
        )
    if 'size_kpi' in kpis:
        pd.DataFrame(kpis['size_kpi']).to_csv(
            os.path.join(output_dir, 'size_kpi.csv'), index=False
        )
    
    return json_path


def main(input_path: str, output_dir: str):
    """Main ETL pipeline function."""
    print("=" * 50)
    print("ETL Pipeline - Retail Pricing Data")
    print("=" * 50)
    
    # Extract
    print("\n[EXTRACT] Loading data...")
    df = load_data(input_path)
    
    # Transform
    print("\n[TRANSFORM] Cleaning and transforming data...")
    df_clean = clean_transform(df)
    
    # Load (Compute KPIs)
    print("\n[LOAD] Computing KPIs...")
    kpis = compute_kpis(df_clean)
    
    # Save outputs
    print("\n[SAVE] Saving outputs...")
    save_outputs(kpis, output_dir)
    
    print("\n" + "=" * 50)
    print("ETL Pipeline completed successfully!")
    print("=" * 50)
    
    return kpis


if __name__ == "__main__":
    # Default paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    input_file = project_root / 'data' / 'May-2022.csv'
    output_dir = script_dir / 'output'
    
    kpis = main(str(input_file), str(output_dir))
    print("\nSample KPI Results:")
    print(f"Total Products: {kpis['overall_stats']['total_products']}")
    print(f"Total SKUs: {kpis['overall_stats']['total_skus']}")
    print(f"Price Range: ₹{kpis['overall_stats']['price_statistics']['min_price']} - ₹{kpis['overall_stats']['price_statistics']['max_price']}")

