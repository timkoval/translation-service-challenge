from fastapi_pagination import add_pagination
from fastapi import FastAPI
import uvicorn
from app.db import close_db_connect, connect_and_init_db
from app.routers import translation

app = FastAPI()

app.add_event_handler("startup", connect_and_init_db)
app.add_event_handler("shutdown", close_db_connect)
add_pagination(app)

app.include_router(translation.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8085)
