"""
Google Cloud Function for Retail ETL Analytics API.
Reads aggregated data from GCS and returns KPI calculations.
"""

import json
import os
import logging
from google.cloud import storage
from google.cloud import functions_v1
import pandas as pd
import numpy as np
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize GCS client
storage_client = storage.Client()

# Configuration
BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 'retail-etl-data')
KPI_FILE_PATH = os.environ.get('KPI_FILE_PATH', 'output/kpis.json')


def load_kpis_from_gcs(bucket_name: str, file_path: str) -> Dict[str, Any]:
    """Load KPI data from Google Cloud Storage."""
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        
        if not blob.exists():
            logger.warning(f"KPI file not found: {file_path}")
            return None
        
        content = blob.download_as_text()
        kpis = json.loads(content)
        logger.info(f"Successfully loaded KPIs from gs://{bucket_name}/{file_path}")
        return kpis
    
    except Exception as e:
        logger.error(f"Error loading KPIs from GCS: {e}")
        raise


def calculate_kpi_summary(kpis: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate summary KPIs from loaded data."""
    if not kpis:
        return {"error": "No KPI data available"}
    
    overall_stats = kpis.get('overall_stats', {})
    platform_stats = kpis.get('platform_stats', {})
    
    summary = {
        "total_revenue_estimate": None,  # Would need sales data
        "total_products": overall_stats.get('total_products', 0),
        "total_skus": overall_stats.get('total_skus', 0),
        "price_range": {
            "min": overall_stats.get('price_statistics', {}).get('min_price', 0),
            "max": overall_stats.get('price_statistics', {}).get('max_price', 0),
            "avg": overall_stats.get('price_statistics', {}).get('avg_price', 0)
        },
        "platform_comparison": platform_stats,
        "top_category": None,
        "timestamp": kpis.get('timestamp', 'N/A')
    }
    
    # Find top category by product count
    category_kpi = kpis.get('category_kpi', [])
    if category_kpi:
        top_category = max(category_kpi, key=lambda x: x.get('product_count', 0))
        summary["top_category"] = {
            "name": top_category.get('Category', 'N/A'),
            "product_count": top_category.get('product_count', 0),
            "avg_price": top_category.get('avg_price', 0)
        }
    
    return summary


def get_region_analysis(kpis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze data by 'region' (simulated - using catalog as region proxy).
    In real scenario, this would use actual region data.
    """
    catalog_kpi = kpis.get('catalog_kpi', [])
    
    if not catalog_kpi:
        return {"error": "No catalog/region data available"}
    
    # Sort by product count (assuming higher product count = more sales)
    sorted_catalogs = sorted(
        catalog_kpi, 
        key=lambda x: x.get('product_count', 0), 
        reverse=True
    )
    
    return {
        "top_region": sorted_catalogs[0] if sorted_catalogs else None,
        "region_breakdown": sorted_catalogs[:5],  # Top 5
        "total_regions": len(catalog_kpi)
    }


def retail_etl_api(request):
    """
    HTTP Cloud Function entry point.
    
    Expected query parameters:
    - endpoint: 'summary', 'region', 'platform', 'category', or 'all'
    - category: (optional) filter by category
    - platform: (optional) filter by platform
    """
    # Set CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    
    try:
        # Get query parameters
        endpoint = request.args.get('endpoint', 'summary')
        category = request.args.get('category')
        platform = request.args.get('platform')
        
        # Load KPIs from GCS
        logger.info(f"Loading KPIs from bucket: {BUCKET_NAME}, path: {KPI_FILE_PATH}")
        kpis = load_kpis_from_gcs(BUCKET_NAME, KPI_FILE_PATH)
        
        if not kpis:
            return (json.dumps({"error": "KPI data not found"}), 404, headers)
        
        # Route to appropriate endpoint
        if endpoint == 'summary':
            result = calculate_kpi_summary(kpis)
        
        elif endpoint == 'region':
            result = get_region_analysis(kpis)
        
        elif endpoint == 'platform':
            platform_stats = kpis.get('platform_stats', {})
            if platform:
                result = platform_stats.get(platform.lower(), {"error": f"Platform '{platform}' not found"})
            else:
                result = platform_stats
        
        elif endpoint == 'category':
            category_kpi = kpis.get('category_kpi', [])
            if category:
                result = next(
                    (c for c in category_kpi if c.get('Category', '').lower() == category.lower()),
                    {"error": f"Category '{category}' not found"}
                )
            else:
                result = {"categories": category_kpi}
        
        elif endpoint == 'all':
            result = kpis
        
        else:
            result = {"error": f"Unknown endpoint: {endpoint}. Use: summary, region, platform, category, or all"}
        
        # Add metadata
        response = {
            "status": "success",
            "endpoint": endpoint,
            "data": result,
            "timestamp": kpis.get('timestamp', 'N/A')
        }
        
        return (json.dumps(response, indent=2), 200, headers)
    
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        error_response = {
            "status": "error",
            "message": str(e)
        }
        return (json.dumps(error_response), 500, headers)


# For local testing
if __name__ == "__main__":
    class MockRequest:
        def __init__(self):
            self.method = 'GET'
            self.args = {'endpoint': 'summary'}
    
    request = MockRequest()
    result = retail_etl_api(request)
    print(result[0])

