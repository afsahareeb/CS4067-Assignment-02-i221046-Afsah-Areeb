from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routes
from database import init_db

# Initialize Database on Startup
init_db()

app = FastAPI()

#  Allow frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)