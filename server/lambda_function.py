import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing import image
import numpy as np
from PIL import Image
import base64
from io import BytesIO
from keras.models import model_from_json

json_file = open('classifier.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("classifier.h5")
loaded_model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])

def lambda_handler(event, context):
    data = event['data'].split(',')
    imgdata = base64.b64decode(data[1])
    im = Image.open(BytesIO(imgdata)).convert('L')
    im = im.resize((28,28), Image.ANTIALIAS)
    im = image.img_to_array(im)
    im = im / 255
    im = np.expand_dims(im, axis = 0)
    pred = loaded_model.predict(im)
    pred = pred.tolist()
    return {
      'statusCode': 200,
      'body': pred[0]
    }
