# Hotel Reservation Cancellation Prediction - End-to-End MLOps

## 1. Project Overview

This project implements an end-to-end MLOps system to predict hotel reservation cancellations. Using a LightGBM classifier, the system predicts if a reservation is likely to be canceled based on various booking and customer features. The pipeline handles everything from data ingestion (from Google Cloud Storage), preprocessing, feature engineering, model training with MLflow tracking, to deployment via Jenkins and Google Cloud Run. The tech stack comprises Python, scikit-learn, LightGBM, Flask, MLflow, Google Cloud Platform, Jenkins, and Docker. Test cases may include validation of data ingestion, data transformation, model performance, and REST API prediction endpoints.

## 2. Project Structure

```
MLOps_Hotel_Reservation_Prediction/
├── application.py              # Flask application for model serving
├── artifacts/                  # Stores outputs of pipeline execution
│   ├── models/                 # Trained models
│   ├── processed/              # Cleaned and transformed data
│   └── raw/                    # Raw ingested data from GCS
├── config/                     # Configuration directory
│   ├── config.yaml             # Main config for ingestion and processing
│   ├── model_params.py         # LightGBM and other model parameters
│   └── path_config.py          # File paths and artifact locations
├── custom_jenkins/             # Jenkins pipeline config
├── logs/                       # Runtime and training logs
├── mlruns/                     # MLflow tracking data and metadata
├── pipeline/                   # Pipeline orchestration script
│   └── training_pipeline.py    # Entry-point for executing full ML pipeline
├── src/                        # Core logic of the pipeline
│   ├── data_ingestion.py       # Fetches and splits data
│   ├── data_preprocessing.py   # Cleans, encodes, and balances data
│   ├── model_training.py       # Trains and evaluates the ML model
│   ├── custom_exception.py     # Custom error class
│   └── logger.py               # Logger configuration
├── static/                     # Web assets (e.g., images)
├── templates/                  # HTML templates for UI
├── Dockerfile                  # Docker container instructions
├── Jenkinsfile                 # CI/CD automation with Jenkins
├── requirements.txt            # Python dependencies
└── setup.py                    # Python package metadata
```

## 3. Detailed Workflow

### A. Data Ingestion & Storage

**Technology:** Google Cloud Storage, Pandas

* Connects securely to a GCS bucket using a service account key
* Downloads the dataset and performs a train-test split based on the config
* Logs all actions using a custom logger

### B. Data Preprocessing & Feature Engineering

**Technology:** scikit-learn, pandas, imbalanced-learn

* Encodes categorical variables using `LabelEncoder`
* Handles skewed numerical distributions using log transformations
* Balances the dataset using SMOTE (Synthetic Minority Over-sampling Technique)
* Selects relevant features based on feature importance from a RandomForest
* Outputs processed data into `artifacts/processed/`

### C. Model Training and Evaluation

**Technology:** LightGBM, MLflow, scikit-learn

* Uses LightGBM classifier trained on balanced, clean data
* Hyperparameter optimization through `RandomizedSearchCV`
* Evaluation metrics: Accuracy, Precision, Recall, F1-Score
* Each training run is logged and tracked using MLflow

### D. Deployment (CI/CD)

**Technology:** Flask, Docker, Jenkins, Google Cloud Run

* Flask REST API (`application.py`) serves model predictions via `/predict`
* Dockerfile containerizes the Flask app
* Jenkinsfile automates build, test, and deploy stages
* Deploys container to Google Cloud Run for scalable access

## 4. Local Environment Setup

### Step 1: Google Cloud Configuration

```bash
# Download and install GCP SDK
# Create and download a service account key from GCP Console
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your-service-account-key.json"
```

### Step 2: Create Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Unix
# or
.\venv\Scripts\activate  # Windows
```

### Step 3: Install Requirements

```bash
pip install -e .
```

### Step 4: Configure Pipeline

Update `config/config.yaml`:

```yaml
data_ingestion:
  bucket_name: "your-bucket"
  bucket_filename: "hotel_bookings.csv"
  train_ratio: 0.8

data_processing:
  categorical_columns:
    - "market_segment_type"
    - "room_type_reserved"
    - "type_of_meal_plan"
  numerical_columns:
    - "lead_time"
    - "avg_price_per_room"
    - "no_of_special_requests"
  skewness_threshold: 0.5
```

### Step 5: Run MLflow for Tracking

```bash
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 \
  --port 5000
```

### Step 6: Run Training Pipeline

```bash
python pipeline/training_pipeline.py
```

### Step 7: Run Flask App

```bash
python application.py
```

Access the app at `http://localhost:5000`

## 5. Testing & Monitoring

* Use `pytest` to test data functions and API endpoints.
* Monitor experiments via MLflow UI.
* Logs are available in `logs/`.

## License

This project is licensed under the MIT License.
