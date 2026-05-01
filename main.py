from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import boto3
import json
import uuid
from dotenv import load_dotenv

load_dotenv()

QUEUE_URL = os.getenv("QUEUE_URL")
if not QUEUE_URL:
    raise ValueError("QUEUE_URL no está definida en el .env")

sqs = boto3.client(
    'sqs',
    region_name='us-east-1',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN")
)

s3 = boto3.client(
    "s3",
    region_name="us-east-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN")
)

BUCKET = os.getenv("S3_BUCKET")

app = FastAPI()

UPLOAD_DIR = "images"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    # s3.upload_file(file_path, BUCKET, filename)   (Cambiar la línea de arriba por esto cuando este lo de S3)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    mensaje = {
        "file_name": filename
    }

    try:
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(mensaje)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Imagen enviada a procesamiento",
        "filename": filename
    }


@app.get("/")
def home():
    return {"status": "API funcionando"}