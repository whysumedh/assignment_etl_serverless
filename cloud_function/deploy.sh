
set -e

# Configuration
FUNCTION_NAME="retail-etl-api"
REGION="us-central1"
RUNTIME="python311"
ENTRY_POINT="retail_etl_api"
MEMORY="512MB"
TIMEOUT="60s"
MAX_INSTANCES="10"

# Get project ID
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "Error: No GCP project set. Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "Deploying Cloud Function: $FUNCTION_NAME"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo ""

# Set environment variables
export GCS_BUCKET_NAME="retail-etl-data-${PROJECT_ID}"
export KPI_FILE_PATH="output/kpis.json"

# Create GCS bucket if it doesn't exist
echo "Checking GCS bucket..."
if ! gsutil ls -b "gs://${GCS_BUCKET_NAME}" &>/dev/null; then
    echo "Creating GCS bucket: ${GCS_BUCKET_NAME}"
    gsutil mb -l ${REGION} "gs://${GCS_BUCKET_NAME}"
else
    echo "Bucket already exists: ${GCS_BUCKET_NAME}"
fi

# Deploy the function
echo ""
echo "Deploying Cloud Function..."
gcloud functions deploy ${FUNCTION_NAME} \
    --gen2 \
    --runtime=${RUNTIME} \
    --region=${REGION} \
    --source=. \
    --entry-point=${ENTRY_POINT} \
    --trigger-http \
    --allow-unauthenticated \
    --memory=${MEMORY} \
    --timeout=${TIMEOUT} \
    --max-instances=${MAX_INSTANCES} \
    --set-env-vars GCS_BUCKET_NAME=${GCS_BUCKET_NAME},KPI_FILE_PATH=${KPI_FILE_PATH} \
    --service-account=${PROJECT_ID}@appspot.gserviceaccount.com

# Get the function URL
FUNCTION_URL=$(gcloud functions describe ${FUNCTION_NAME} --gen2 --region=${REGION} --format="value(serviceConfig.uri)")

echo ""
echo "=========================================="
echo "Deployment successful!"
echo "=========================================="
echo "Function URL: ${FUNCTION_URL}"
echo ""
echo "Test the function:"
echo "curl '${FUNCTION_URL}?endpoint=summary'"
echo ""

