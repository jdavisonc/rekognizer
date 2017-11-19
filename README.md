# Rekognizer
Rekognizer is a python utility routine that search for Humans on a video (surveillance or similar). It recognize an object with confident greater than 80%, and if it is a Human, return 1 as success, then return 0.

Under the hood, it uses Rekognition AWS as deep learning image processing API.

# Dependencies
* OpenCV
* Python Imaging Library (PIL)
* Boto3 (AWS) SDK

# Arguments
1. Video
2. Extract Image Frame from Video every X seconds

# How to run
```
export AWS_ACCESS_KEY_ID=XXX AWS_SECRET_ACCESS_KEY=YYY
docker build -r rekognizer .
docker run --rm -it -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -v $PWD:/srv rekognizer /srv/my_video.mp4 15
```
