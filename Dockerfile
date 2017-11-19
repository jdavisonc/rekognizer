FROM valian/docker-python-opencv-ffmpeg

RUN pip install boto3 pillow && apt-get update && apt-get install -y python-tk

COPY rekognizer.py .

ENTRYPOINT ["python", "rekognizer.py"]