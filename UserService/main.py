from fastapi import FastAPI
import routes

app = FastAPI()

# register route from routes.py
app.include_router(routes.router)
