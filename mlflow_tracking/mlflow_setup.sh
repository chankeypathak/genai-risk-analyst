#!/bin/bash
# Start MLflow tracking server for local development
mlflow server --backend-store-uri sqlite:///mlflow_tracking/mlflow.db --default-artifact-root ./mlflow_tracking --host 0.0.0.0 --port 5000
