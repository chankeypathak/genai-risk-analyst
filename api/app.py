# FastAPI/Streamlit entry point (placeholder)
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "GenAI Risk & Compliance Analyst API is running."}

# For Streamlit, you can add a separate entry point or reuse this file.
