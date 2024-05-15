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

from lib.text_utils import (
    start_job,
    get_job_response,
    get_job_results,
    get_text_with_info,
    get_text_with_line_spacing_info,
    # extract_paragraphs_only,
    get_paragraphs_based_on_period
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


@app.get("/upload-data-to-db")
def extract_data_and_load_to_db(
        my_file: str,
        db: Session = Depends(get_db)
):

    # Insert one row into documents
    query = "insert into team0.documents (s3_path) values (:my_file) returning id"
    document_id = db.execute(text(query), {'my_file': my_file}).scalar()
    textract = get_client('textract', settings)

    jid = start_job(textract, settings.bucket_name, 'interpretation_light.pdf')
    get_job_response(textract, jid)
    result = get_job_results(textract, jid)
    result_info = get_text_with_info(result)
    result_info_completed = get_text_with_line_spacing_info(result_info)
    # test_paragraph = extract_paragraphs_only(result_info_completed)
    paragraphs = get_paragraphs_based_on_period(result_info_completed)

    for i in paragraphs:
        print(i)

    # Insert all the paragraphs into chunks
    query = "insert into team0.chunks (document_id, content) values (:document_id, :content)"
    for i in paragraphs:
        db.execute(text(query), {'document_id': document_id, 'content': i})
        db.commit()
    db.commit()
    return 'done!'
