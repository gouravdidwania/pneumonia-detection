import os

import numpy as np
import streamlit as st

import tensorflow as tf
import uvicorn
from tensorflow import keras
from tensorflow.keras.applications.vgg16 import preprocess_input

from fastapi import FastAPI, Request
from fastapi import Security
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile

from config import SECURITY_KEY
from data_type import OutputRequest
from security import get_api_key

import warnings

warnings.filterwarnings('ignore')

app = FastAPI(debug=True, title="Pneumonia Detection API", version="1.0")


class MyCustomException(Exception):
    def __init__(self, message: str):
        self.message = message


@app.exception_handler(MyCustomException)
async def MyCustomExceptionHandler(request: Request, exception: MyCustomException):
    return JSONResponse(status_code=500, content={"Message": exception.message})


@app.on_event('startup')
def initial():
    if SECURITY_KEY is None:
        raise Exception("Security Key Missing! Please create an .env file with the same.")


@app.get("/")
async def root():
    return "Server Online!"


@app.get("/health_check")
async def health_check():
    return {'status': "alive"}


@app.post("/predict", response_model=OutputRequest, dependencies=[Security(get_api_key)])
async def call_model(file: UploadFile = File(...)):
    if not file:
        print("No upload file sent")
        raise Exception("No File Uploaded")
    else:
        print(file.filename, "is Uploaded Successfully!")

    contents = file.file.read()

    with open('test/image.jpeg', 'wb') as f:
        f.write(contents)
        f.close()

    image = tf.keras.preprocessing.image.load_img('test/image.jpeg', color_mode='rgb', target_size=(150, 150))
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)

    d = {1: 'Pneumonia', 0: 'Normal'}
    model_path = 'model/model_export.h5'
    model1 = keras.models.load_model(model_path)
    predict = model1.predict(image)
    var = d[int(predict[0][0])]

    return {'prediction': var}


@app.get("/predict_image", response_model=OutputRequest)
def model():
    os.system('streamlit run app.py')
    st.title('Pneumonia Detection API')
    st.subheader('Upload Image')
    file = st.file_uploader("Upload JPEG/JPG", type=['jpeg', 'jpg'])
    if st.button('Upload'):
        if file is not None:
            file_details = {"Filename": file.name,
                            "FileType": file.type,
                            "FileSize": file.size}
            st.write(file_details)
            st.image(file)
            with open('test/image.jpeg', 'wb') as f:
                f.write(file.getbuffer())
            st.write(file_details['Filename'], "is Uploaded Successfully!")
        else:
            print("No upload file sent")
            raise Exception("No File Uploaded")

    image = tf.keras.preprocessing.image.load_img('test/image.jpeg', color_mode='rgb', target_size=(150, 150))
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)

    d = {1: 'Pneumonia', 0: 'Normal'}
    model_path = './model/model_export.h5'
    model1 = keras.models.load_model(model_path)
    predict = model1.predict(image)
    var = d[int(predict[0][0])]
    st.subheader("Detected: " + var)


if __name__ == '__main__':
    model()

