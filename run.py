import os

from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

# Load environment variables from .env if present
load_dotenv()

# Render will set PORT in the environment
PORT = int(os.getenv("PORT", 8000))

# Create the FastAPI app
app = FastAPI(title="Servination API")

@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Servination backend is running on Render."
    }

if __name__ == "__main__":
    # Bind to 0.0.0.0 so Render can route traffic into the container
    uvicorn.run(app, host="0.0.0.0", port=PORT)
