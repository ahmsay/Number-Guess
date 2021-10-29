import tensorflow as tf
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
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

app = Flask(__name__)
api = Api(app)
CORS(app)

class Test(Resource):
    def get(self):
        return {'message': 'Connection successfull'}
    
    def post(self):
        try:
            data = request.get_json()
            data = data['data'].split(',')
            imgdata = base64.b64decode(data[1])
            im = Image.open(BytesIO(imgdata)).convert('L')
            im = im.resize((28,28), Image.ANTIALIAS)
            im = image.img_to_array(im)
            im = im / 255
            im = np.expand_dims(im, axis = 0)
            pred = loaded_model.predict(im)
            pred = pred.tolist()
            return {'pred': pred[0]}
        except Exception as e:
            return {'error': str(e)}
    
api.add_resource(Test, '/')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)