from fastapi import File, UploadFile
from pydantic import BaseModel


class InputRequest(BaseModel):
    request_id: str
    file_url: str


class OutputRequest(BaseModel):
    prediction: str
