# main.py
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a route for the root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
