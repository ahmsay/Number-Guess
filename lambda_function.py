import numpy as np
import json
from PIL import Image
import base64
from io import BytesIO
import boto3

runtime = boto3.Session().client('sagemaker-runtime')

def normalize(x, axis):
    eps = np.finfo(float).eps
    mean = np.mean(x, axis=axis, keepdims=True)
    std = np.std(x, axis=axis, keepdims=True) + eps
    return (x - mean) / std

def convert_image_for_prediction(base64_encoded_image):
    image_contents = base64_encoded_image.split(",")
    image_in_bytes = base64.b64decode(image_contents[1])
    image = Image.open(BytesIO(image_in_bytes)).convert("L")
    image = image.resize((28,28))
    image_array = np.array(image)
    normalized_image = normalize([image_array], axis=(1, 2))
    image_formatted_for_prediction = np.expand_dims(normalized_image, 3).tolist()
    return json.dumps({"instances": image_formatted_for_prediction})

def generate_result(result):
    prediction_list = result["predictions"][0]
    prediction_list_sorted = sorted(prediction_list, reverse=True)
    first_guess = prediction_list.index(prediction_list_sorted[0])
    second_guess = prediction_list.index(prediction_list_sorted[1])
    return {"first_guess": first_guess, "second_guess": second_guess}

def lambda_handler(event, context):
    base64_encoded_image = event["body"]
    data = convert_image_for_prediction(base64_encoded_image)
    response = runtime.invoke_endpoint(EndpointName="number-guess", ContentType='application/json', Body=data)
    predictions = json.loads(response['Body'].read().decode())
    result = generate_result(predictions)

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
