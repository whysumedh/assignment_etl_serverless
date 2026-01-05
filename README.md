# Retail ETL Serverless API

A serverless REST API deployed on Google Cloud Functions) providing retail pricing insights and KPIs from ETL-processed data stored in Google Cloud Storage.

---

## Deployment Details

**Function Name:** `retail-etl-api`  
**Function URL:** `https://retail-etl-api-yljjgc5pva-uc.a.run.app`  
Used Google Cloud for Deployment
Used Dataset : [Dataset](https://wgcp-my.sharepoint.com/:x:/r/personal/ritish_jogi_blend360_com/_layouts/15/Doc.aspx?sourcedoc=%7BBCD48020-E3F6-4FA8-9722-1A904E731DB1%7D&file=May-2022.csv&action=default&mobileredirect=true)

### GCS Configuration

- **Bucket:** `retail-etl-data-alpha-455913`
- **KPI File Path:** `output/kpis.json`
- **Service Account:** `alpha-455913@appspot.gserviceaccount.com`

### Deployment Output

```
Function URL: https://retail-etl-api-yljjgc5pva-uc.a.run.app
Console: https://console.cloud.google.com/functions/details/us-central1/retail-etl-api?project=alpha-455913
State: ACTIVE
Revision: retail-etl-api-00001-qub
```

---

## API Endpoints

All endpoints use the base URL: `https://retail-etl-api-yljjgc5pva-uc.a.run.app`

### 1. Summary Endpoint

**URL:** `?endpoint=summary`

Returns overall statistics, price ranges, platform comparisons, and top category information.

**Response:**
```json
{
  "status": "success",
  "endpoint": "summary",
  "data": {
    "total_revenue_estimate": null,
    "total_products": 1293,
    "total_skus": 1293,
    "price_range": {
      "min": 199.0,
      "max": 5997.0,
      "avg": 2241.3247873163186
    },
    "platform_comparison": {
      "ajio": {
        "products_available": 1293,
        "min_price": 199.0,
        "max_price": 5997.0,
        "avg_price": 2241.26407579273,
        "median_price": 2095.0,
        "coverage_pct": 100.0
      },
      "amazon": {
        "products_available": 1293,
        "min_price": 199.0,
        "max_price": 5997.0,
        "avg_price": 2247.789211136891,
        "median_price": 2097.0,
        "coverage_pct": 100.0
      },
      "amazon_fba": {
        "products_available": 1293,
        "min_price": 199.0,
        "max_price": 5997.0,
        "avg_price": 2247.789211136891,
        "median_price": 2097.0,
        "coverage_pct": 100.0
      },
      "flipkart": {
        "products_available": 1293,
        "min_price": 199.0,
        "max_price": 5997.0,
        "avg_price": 2243.12022428461,
        "median_price": 2097.0,
        "coverage_pct": 100.0
      },
      "limeroad": {
        "products_available": 1293,
        "min_price": 199.0,
        "max_price": 5997.0,
        "avg_price": 2242.974825986079,
        "median_price": 2095.0,
        "coverage_pct": 100.0
      },
      "myntra": {
        "products_available": 1293,
        "min_price": 199.0,
        "max_price": 5997.0,
        "avg_price": 2229.4450502706886,
        "median_price": 2095.0,
        "coverage_pct": 100.0
      },
      "paytm": {
        "products_available": 1293,
        "min_price": 199.0,
        "max_price": 5997.0,
        "avg_price": 2238.4891337973704,
        "median_price": 2095.0,
        "coverage_pct": 100.0
      },
      "snapdeal": {
        "products_available": 1293,
        "min_price": 199.0,
        "max_price": 5997.0,
        "avg_price": 2239.72656612529,
        "median_price": 2095.0,
        "coverage_pct": 100.0
      }
    },
    "top_category": {
      "name": "Kurta",
      "product_count": 802,
      "avg_price": 1982.39
    },
    "timestamp": "2026-01-05T00:10:07.396938"
  },
  "timestamp": "2026-01-05T00:10:07.396938"
}
```

### 2. Region Endpoint

**URL:** `?endpoint=region`

Returns catalog/region breakdown with pricing statistics.

**Response:**
```json
{
  "status": "success",
  "endpoint": "region",
  "data": {
    "top_region": {
      "Catalog": "Mix",
      "min_price": 1195.0,
      "max_price": 5997.0,
      "avg_price": 2149.41,
      "product_count": 794,
      "unique_skus": 794,
      "unique_categories": 4
    },
    "region_breakdown": [
      {
        "Catalog": "Mix",
        "min_price": 1195.0,
        "max_price": 5997.0,
        "avg_price": 2149.41,
        "product_count": 794,
        "unique_skus": 794,
        "unique_categories": 4
      },
      {
        "Catalog": "Surmaya",
        "min_price": 1250.0,
        "max_price": 5395.0,
        "avg_price": 2539.69,
        "product_count": 192,
        "unique_skus": 192,
        "unique_categories": 3
      },
      {
        "Catalog": "Nill",
        "min_price": 199.0,
        "max_price": 4899.0,
        "avg_price": 2420.6,
        "product_count": 72,
        "unique_skus": 72,
        "unique_categories": 1
      },
      {
        "Catalog": "Colors-8",
        "min_price": 1895.0,
        "max_price": 1895.0,
        "avg_price": 1895.0,
        "product_count": 48,
        "unique_skus": 48,
        "unique_categories": 1
      },
      {
        "Catalog": "Rozana",
        "min_price": 2495.0,
        "max_price": 2495.0,
        "avg_price": 2495.0,
        "product_count": 48,
        "unique_skus": 48,
        "unique_categories": 1
      }
    ],
    "total_regions": 9
  },
  "timestamp": "2026-01-05T00:10:07.396938"
}
```

### 3. Platform Endpoint

**URL:** `?endpoint=platform`

Returns detailed statistics for all e-commerce platforms.

**Response:**
```json
{
  "status": "success",
  "endpoint": "platform",
  "data": {
    "ajio": {
      "products_available": 1293,
      "min_price": 199.0,
      "max_price": 5997.0,
      "avg_price": 2241.26407579273,
      "median_price": 2095.0,
      "coverage_pct": 100.0
    },
    "amazon": {
      "products_available": 1293,
      "min_price": 199.0,
      "max_price": 5997.0,
      "avg_price": 2247.789211136891,
      "median_price": 2097.0,
      "coverage_pct": 100.0
    },
    "amazon_fba": {
      "products_available": 1293,
      "min_price": 199.0,
      "max_price": 5997.0,
      "avg_price": 2247.789211136891,
      "median_price": 2097.0,
      "coverage_pct": 100.0
    },
    "flipkart": {
      "products_available": 1293,
      "min_price": 199.0,
      "max_price": 5997.0,
      "avg_price": 2243.12022428461,
      "median_price": 2097.0,
      "coverage_pct": 100.0
    },
    "limeroad": {
      "products_available": 1293,
      "min_price": 199.0,
      "max_price": 5997.0,
      "avg_price": 2242.974825986079,
      "median_price": 2095.0,
      "coverage_pct": 100.0
    },
    "myntra": {
      "products_available": 1293,
      "min_price": 199.0,
      "max_price": 5997.0,
      "avg_price": 2229.4450502706886,
      "median_price": 2095.0,
      "coverage_pct": 100.0
    },
    "paytm": {
      "products_available": 1293,
      "min_price": 199.0,
      "max_price": 5997.0,
      "avg_price": 2238.4891337973704,
      "median_price": 2095.0,
      "coverage_pct": 100.0
    },
    "snapdeal": {
      "products_available": 1293,
      "min_price": 199.0,
      "max_price": 5997.0,
      "avg_price": 2239.72656612529,
      "median_price": 2095.0,
      "coverage_pct": 100.0
    }
  },
  "timestamp": "2026-01-05T00:10:07.396938"
}
```

### 4. Category Endpoint

**URL:** `?endpoint=category`

Returns category breakdown with pricing statistics.

**Response:**
```json
{
  "status": "success",
  "endpoint": "category",
  "data": {
    "categories": [
      {
        "Category": "Gown",
        "min_price": 2795.0,
        "max_price": 4295.0,
        "avg_price": 3151.25,
        "product_count": 32,
        "unique_skus": 32,
        "unique_styles": 6
      },
      {
        "Category": "Kurta",
        "min_price": 1195.0,
        "max_price": 3995.0,
        "avg_price": 1982.39,
        "product_count": 802,
        "unique_skus": 802,
        "unique_styles": 133
      },
      {
        "Category": "Kurta Set",
        "min_price": 1795.0,
        "max_price": 5997.0,
        "avg_price": 2730.36,
        "product_count": 342,
        "unique_skus": 342,
        "unique_styles": 58
      },
      {
        "Category": "Nill",
        "min_price": 199.0,
        "max_price": 4899.0,
        "avg_price": 2420.6,
        "product_count": 72,
        "unique_skus": 72,
        "unique_styles": 41
      },
      {
        "Category": "Tops",
        "min_price": 1595.0,
        "max_price": 1895.0,
        "avg_price": 1728.33,
        "product_count": 45,
        "unique_skus": 45,
        "unique_styles": 9
      }
    ]
  },
  "timestamp": "2026-01-05T00:10:07.396938"
}
```

### 5. All KPIs Endpoint

**URL:** `?endpoint=all`

Returns comprehensive KPIs including overall statistics, category KPIs, and catalog KPIs.

**Response:**
```json
{
  "status": "success",
  "endpoint": "all",
  "data": {
    "overall_stats": {
      "total_products": 1293,
      "total_skus": 1293,
      "total_styles": 247,
      "total_catalogs": 9,
      "total_categories": 5,
      "price_statistics": {
        "min_price": 199.0,
        "max_price": 5997.0,
        "avg_price": 2241.3247873163186,
        "median_price": 2095.0,
        "std_price": 701.4450521119986
      }
    },
    "category_kpi": [
      {
        "Category": "Gown",
        "min_price": 2795.0,
        "max_price": 4295.0,
        "avg_price": 3151.25,
        "product_count": 32,
        "unique_skus": 32,
        "unique_styles": 6
      },
      {
        "Category": "Kurta",
        "min_price": 1195.0,
        "max_price": 3995.0,
        "avg_price": 1982.39,
        "product_count": 802,
        "unique_skus": 802,
        "unique_styles": 133
      },
      {
        "Category": "Kurta Set",
        "min_price": 1795.0,
        "max_price": 5997.0,
        "avg_price": 2730.36,
        "product_count": 342,
        "unique_skus": 342,
        "unique_styles": 58
      },
      {
        "Category": "Nill",
        "min_price": 199.0,
        "max_price": 4899.0,
        "avg_price": 2420.6,
        "product_count": 72,
        "unique_skus": 72,
        "unique_styles": 41
      },
      {
        "Category": "Tops",
        "min_price": 1595.0,
        "max_price": 1895.0,
        "avg_price": 1728.33,
        "product_count": 45,
        "unique_skus": 45,
        "unique_styles": 9
      }
    ],
    "catalog_kpi": [
      {
        "Catalog": "Breeze-4",
        "min_price": 2195.0,
        "max_price": 2195.0,
        "avg_price": 2195.0,
        "product_count": 36,
        "unique_skus": 36,
        "unique_categories": 1
      },
      {
        "Catalog": "Colors-7",
        "min_price": 1595.0,
        "max_price": 1595.0,
        "avg_price": 1595.0,
        "product_count": 43,
        "unique_skus": 43,
        "unique_categories": 1
      },
      {
        "Catalog": "Colors-8",
        "min_price": 1895.0,
        "max_price": 1895.0,
        "avg_price": 1895.0,
        "product_count": 48,
        "unique_skus": 48,
        "unique_categories": 1
      },
      {
        "Catalog": "Four Gems 2",
        "min_price": 2795.0,
        "max_price": 2795.0,
        "avg_price": 2795.0,
        "product_count": 24,
        "unique_skus": 24,
        "unique_categories": 1
      }
    ]
  },
  "timestamp": "2026-01-05T00:10:07.396938"
}
```

---

## Quick Deployment Guide

### Prerequisites

1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
2. Authenticate: `gcloud auth login && gcloud auth application-default login`
3. Set project: `gcloud config set project YOUR_PROJECT_ID`
4. Enable APIs:
   ```bash
   gcloud services enable cloudfunctions.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable storage-component.googleapis.com
   gcloud services enable run.googleapis.com
   ```

### Deployment Steps

1. **Run ETL Pipeline:**
   ```bash
   cd assignment2_etl_serverless
   python etl_pipeline.py
   ```

2. **Create GCS Bucket and Upload Data:**
   ```bash
   gsutil mb -l us-central1 gs://retail-etl-data-YOUR_PROJECT_ID
   gsutil -m cp -r output/* gs://retail-etl-data-YOUR_PROJECT_ID/output/
   ```

3. **Deploy Cloud Function (Command Prompt):**
   ```cmd
   cd cloud_function
   for /f "tokens=*" %i in ('gcloud config get-value project') do set PROJECT_ID=%i
   set GCS_BUCKET_NAME=retail-etl-data-%PROJECT_ID%
   
   gcloud functions deploy retail-etl-api ^
       --gen2 ^
       --runtime=python311 ^
       --region=us-central1 ^
       --source=. ^
       --entry-point=retail_etl_api ^
       --trigger-http ^
       --allow-unauthenticated ^
       --memory=512MB ^
       --timeout=60s ^
       --max-instances=10 ^
       --set-env-vars GCS_BUCKET_NAME=%GCS_BUCKET_NAME%,KPI_FILE_PATH=output/kpis.json ^
       --service-account=%PROJECT_ID%@appspot.gserviceaccount.com
   ```

4. **Get Function URL:**
   ```bash
   gcloud functions describe retail-etl-api --gen2 --region=us-central1 --format="value(serviceConfig.uri)"
   ```

---

## Testing

Test endpoints using curl:

```bash
curl "https://retail-etl-api-yljjgc5pva-uc.a.run.app?endpoint=summary"
curl "https://retail-etl-api-yljjgc5pva-uc.a.run.app?endpoint=region"
curl "https://retail-etl-api-yljjgc5pva-uc.a.run.app?endpoint=platform"
curl "https://retail-etl-api-yljjgc5pva-uc.a.run.app?endpoint=category"
curl "https://retail-etl-api-yljjgc5pva-uc.a.run.app?endpoint=all"
```

---

## Key Statistics

- **Total Products:** 1,293
- **Total SKUs:** 1,293
- **Total Styles:** 247
- **Total Catalogs:** 9
- **Total Categories:** 5
- **Price Range:** ₹199 - ₹5,997
- **Average Price:** ₹2,241.32
- **Top Category:** Kurta (802 products, avg ₹1,982.39)

---

## Architecture

- **Source:** Google Cloud Storage (GCS) bucket
- **Compute:** Cloud Functions 2nd Gen (Python 3.11)
- **Data Format:** JSON (kpis.json)
- **Trigger:** HTTP requests
- **Authentication:** Public (unauthenticated for demo)
