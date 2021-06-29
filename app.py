from flask import Flask, request, jsonify, Response
from PIL import Image
import numpy as np
import base64
from io import BytesIO
import io
import os
import requests
#from pydantic import BaseModel
import json
import argparse
import six.moves.urllib as urllib
import tarfile
import urllib.request

from custom_np_encoder import NumpyArrayEncoder
from jsonya import id2name
from detection import load_model, detection
from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
#from keras.preprocessing.image import save_img


import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

########################################################################################
gpus = tf.config.experimental.list_physical_devices('GPU')

if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)

        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")

    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)
        print('shit!!')

########################################################################################

CWD_PATH = os.getcwd()
THRESHOLD = 0.5
NUM_CLASSES = 50

MODEL_NAME = 'model/faster_rcnn_inception_v2_coco_2018_01_28'
#MODEL_FILE = MODEL_NAME + '.tar.gz'
#DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
PATH_TO_LABELS = 'data/mscoco_label_map.pbtxt'
#PATH_TO_IMAGE = os.path.join(CWD_PATH,IMAGE_NAME)



# opener = urllib.request.URLopener()
# opener.retrieve(DOWNLOAD_BASE+MODEL_FILE, MODEL_FILE)
# tar_file = tarfile.open(MODEL_FILE)
# for file in tar_file.getmembers():
#     file_name = os.path.basename(file.name)
#     if 'frozen_inference_graph.pb' in file_name:
#         tar_file.extract(file, os.getcwd())


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

####################################################################################################

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    tf.config.experimental.set_memory_growth(physical_devices[1], True)
    tf.config.experimental.set_memory_growth(physical_devices[2], True)

sess, detection_graph = load_model()

DEFAULT_PORT = 5000
DEFAULT_HOST = '0.0.0.0'

#####################################################################################################

def parse_args():

  parser = argparse.ArgumentParser(description='Twistcode object detection API')

  parser.add_argument('--debug', dest='debug',
                        help='Run in debug mode.',
                        required=False, action='store_true', default=False)

  parser.add_argument('--port', dest='port',
                        help='Port to run on.', type=int,
                        required=False, default=DEFAULT_PORT)

  parser.add_argument('--host', dest='host',
                        help='Host to run on, set to 0.0.0.0 for remote access', type=str,
                        required=False, default=DEFAULT_HOST)

  args = parser.parse_args()
  return args

####################################################################################################
app = Flask(__name__)
#####################################################################################################
@app.route('/detections', methods=['POST'])
def get_detections():
    response = request.get_json()
    data_str = response['image']
    # point = data_str.find(',')
    # base64_str = data_str[point:]  # remove unused part like this: "data:image/jpeg;base64,"

    image = base64.b64decode(data_str)       
    img = Image.open(io.BytesIO(image))

    if(img.mode!='RGB'):
        img = img.convert("RGB")
    

    image_rgb = np.array(img)


    results = detection(sess, detection_graph, image_rgb, THRESHOLD)
    
    response_encoded = json.dumps(results, cls=NumpyArrayEncoder)

    print(results)
    
    response = response_encoded

    #return jsonify(results)
    return Response(response=response_encoded, status=200, mimetype="application/json")


#start flask app

def main():
  args = parse_args()
  app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()
