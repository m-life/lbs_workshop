from fastapi import FastAPI
from config import Settings, get_settings

# -- START FAST-API INITIAL CONFIG -- #
settings: Settings = get_settings()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": f"World! My app is {settings.app_title}"}
