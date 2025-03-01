from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import routes

# Create FastAPI instance
app = FastAPI()

# allow frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware, # add Cross-Origin Resource Sharing (CORS) middleware
    allow_origins=["*"], # allow all origins
    allow_credentials=True, # allow credentials
    allow_methods=["*"], # allow all methods
    allow_headers=["*"], # allow all headers
)

app.include_router(routes.router) # include the routes from routes.py
