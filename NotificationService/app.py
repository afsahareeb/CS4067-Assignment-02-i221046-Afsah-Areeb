from fastapi import FastAPI
from routes import notification_bp
from model import init_db

app = FastAPI()

# Initialize MongoDB
init_db()

# Include the notification routes
app.include_router(notification_bp)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5002)
