
FROM nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04
FROM python:3.7

#set up environment
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y curl
RUN apt-get install unzip
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get install ffmpeg libsm6 libxext6  -y


RUN pip3 install --upgrade setuptools

# clone the repository 
RUN git clone --depth 1 https://github.com/tensorflow/models.git


RUN pip3 install --upgrade pip 

# Install object detection api dependencies
RUN apt-get install -y protobuf-compiler python-pil python-lxml python-tk && \
    pip install Cython && \
    pip install contextlib2 && \
    pip install jupyter && \
    pip install matplotlib && \
    pip install pycocotools && \
    pip install opencv-python && \
    pip install flask && \
    pip install tensorflow && \
    pip install Pillow && \
    pip install tf_slim && \
    pip install requests

# Get protoc 3.0.0, rather than the old version already in the container
RUN curl -OL "https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip" && \
    unzip protoc-3.0.0-linux-x86_64.zip -d proto3 && \
    mv proto3/bin/* /usr/local/bin && \
    mv proto3/include/* /usr/local/include && \
    rm -rf proto3 protoc-3.0.0-linux-x86_64.zip

# Run protoc on the object detection repo
RUN cd models/research && \
    protoc object_detection/protos/*.proto --python_out=.

# Set the PYTHONPATH to finish installing the API
ENV PYTHONPATH=$PYTHONPATH:/models/research/object_detection
ENV PYTHONPATH=$PYTHONPATH:/models/research/slim
ENV PYTHONPATH=$PYTHONPATH:/models/research

# # clone the flask application
RUN git clone https://github.com/twistcode/yakyakyey.git


WORKDIR /yakyakyey/matakehati/flask_without_db/object_detection_cpu
# set this as the working directory
# WORKDIR /app

# # Install object detection api dependencies
# COPY requirements.txt /app/requirements.txt
# RUN pip3 install -r requirements.txt

# COPY . /app

EXPOSE 5000


# download the pretrained model
# change here to download your pretrained model
RUN mkdir model && \
    cd model/ && \
    curl -O "http://download.tensorflow.org/models/object_detection/faster_rcnn_inception_v2_coco_2018_01_28.tar.gz" && \
    tar -xvzf faster_rcnn_inception_v2_coco_2018_01_28.tar.gz 
    #rm ssd_mobilenet_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03.tar.gz


CMD ["python3", "app.py"]
