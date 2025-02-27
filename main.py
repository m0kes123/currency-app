from fastapi import FastAPI, Query
from entity.models import Information
from datetime import date, datetime
import service.cbrf as cbrf
from settings import settings
import uvicorn
from routes import setup_routes


app = FastAPI()

setup_routes(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(settings.PORT))