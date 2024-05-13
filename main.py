from fastapi import FastAPI
from config import Settings, get_settings
from service import get_client, list_files

# -- START FAST-API INITIAL CONFIG -- #
settings: Settings = get_settings()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": f"World My app is {settings.app_title}"}


@app.get("/list-files")
def retrieve_all_files_in_my_bucket():
    s3 = get_client(service='s3', settings=settings)
    file_list = list_files(s3_client=s3, bucket_name=settings.bucket_name)
    return file_list


# @app.post("/upload_file")
# # TODO
#
# @app.get("/retrieve-file-link")
# # TODO
