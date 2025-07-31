# Dockerfile for GenAI Risk & Compliance Analyst
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for MLflow and Airflow
RUN pip install --no-cache-dir mlflow apache-airflow

# Copy project files
COPY . .

# Expose Streamlit and MLflow ports
EXPOSE 8501 5000

# Default command: run Streamlit app
CMD ["streamlit", "run", "api/app.py"]
