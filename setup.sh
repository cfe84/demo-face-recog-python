#!/bin/bash
apt-get install python3 python3-pip libssl-dev cmake

git clone https://github.com/davisking/dlib.git
cd dlib/
mkdir build; cd build; cmake .. -DDLIB_USE_CUDA=0 -DUSE_AVX_INSTRUCTIONS=1; cmake --build .
cd ..
python3 setup.py install --yes USE_AVX_INSTRUCTIONS --no DLIB_USE_CUDA
pip3 install face_recognition

