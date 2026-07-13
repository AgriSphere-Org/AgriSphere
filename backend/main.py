from fastapi import FastAPI

app = FastAPI(title="AgriSphere")

@app.get("/")
def home():
    return {
        "message": "Welcome to AgriSphere"
    }