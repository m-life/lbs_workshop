from fastapi import FastAPI, UploadFile, File, Depends
from config import Settings, get_settings
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from lib.db import get_db
from service import (
    get_client,
    list_files,
    upload_file_to_s3,
    generate_presigned_url
)

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


@app.post("/upload_file")
def upload_file(file: UploadFile = File(...)):
    s3 = get_client(service='s3', settings=settings)
    return upload_file_to_s3(
        s3_client=s3,
        bucket_name=settings.bucket_name,
        object_name=f"uploaded_{file.filename}",
        file=file,
    )


@app.get("/retrieve-file-link")
def get_file_from_s3(my_file: str):
    s3 = get_client(service='s3', settings=settings)
    return generate_presigned_url(
        bucket_name=settings.bucket_name,
        s3_client=s3,
        object_name=my_file
    )


@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    query = text("select * from team0.documents")
    res = db.execute(query).all()
    return [row[1] for row in res]

