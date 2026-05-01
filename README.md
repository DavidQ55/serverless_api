# Serverless Image Processing API

API desarrollada con FastAPI que permite subir imágenes y enviarlas a una cola SQS para su procesamiento en AWS Lambda.

## Tecnologías
- FastAPI
- AWS SQS
- AWS Lambda
- Python

## Ejecución

```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload
