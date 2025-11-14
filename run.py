import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()
PORT = int(os.getenv("APP_PORT", 8000))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=PORT, reload=False)
