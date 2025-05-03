# Hotel Reservation Prediction System

## Project Overview
A machine learning-based web application that predicts hotel reservation cancellations using  ML techniques. The system processes booking details through a web interface to predict cancellation probability, helping hotels optimize their reservation management. I have also maintained a custom pipeline for ML Model and used technologies to track various artifacts as we go down the pipeline

## Technologies Stack
- **Data Processing**: pandas (2.0.0+), numpy (1.24.0+)
- **Machine Learning**: scikit-learn, LightGBM
- **Web Framework**: Flask
- **MLOps**: MLflow
- **Cloud Storage**: Google Cloud Storage
- **Other Tools**: PyYAML, imbalanced-learn

## Directory Structure
```
├── artifacts/          # Generated artifacts during pipeline execution
│   ├── raw/           # Raw data files
│   ├── processed/     # Processed datasets
│   └── models/        # Trained model files
├── config/            # Configuration files
│   └── config.yaml    # Main configuration
├── logs/              # Application and training logs
├── pipeline/          # ML pipeline components
│   ├── ingestion.py
│   ├── preprocessing.py
│   └── training.py
├── static/           # CSS and JavaScript files
├── templates/        # HTML templates
├── utils/           # Helper functions
└── src/            # Core application code
```

## Pipeline Architecture

### 1. Data Ingestion
- Fetches data from Google Cloud Storage
- Performs train-test split
- Generates data ingestion artifacts

```python
artifacts/
    ├── raw/
    │   └── hotel_bookings.csv
    └── processed/
        ├── train.csv
        └── test.csv
```

### 2. Data Preprocessing
- Feature engineering
- Label encoding
- SMOTE for imbalanced data
- Feature selection using Random Forest

### 3. Model Training
- LightGBM classifier implementation
- Hyperparameter tuning
- MLflow experiment tracking
- Model evaluation and serialization

## Setup Instructions

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # For Mac/Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create `.env` file:
```
FLASK_APP=app.py
FLASK_ENV=development
GOOGLE_CLOUD_CREDENTIALS=path/to/credentials.json
MLFLOW_TRACKING_URI=http://localhost:5000
```

### 4. Create Required Directories
```bash
mkdir -p artifacts/raw artifacts/processed artifacts/models logs config
```

### 5. Configure Google Cloud Storage
- Place your Google Cloud credentials in `config/credentials.json`
- Update bucket name in `config/config.yaml`

### 6. Start MLflow Server
```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000
```

### 7. Run Application
```bash
flask run
```

## Usage

### Training Pipeline
```bash
python pipeline/main.py --config config/config.yaml
```

### Making Predictions
1. Access web interface at `http://localhost:5000`
2. Input reservation details
3. Click "Predict" to get cancellation probability

## Model Performance
- Accuracy: 85%
- F1 Score: 0.83
- ROC-AUC: 0.87

## Project Structure Best Practices
- Modular code architecture
- Configuration management
- Experiment tracking
- Logging implementation
- Error handling
- Type hints
- Documentation

## Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## Required Files
```
.
├── .gitignore
├── requirements.txt
├── config.yaml
├── .env
└── credentials.json
```

## License
MIT License

## Contact
For questions or feedback, please open an issue in the repository.