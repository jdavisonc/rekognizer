
import boto3
import json
import pickle
import io
import os
import cv2
import os
import sys
from PIL import Image

from multiprocessing.dummy import Pool as ThreadPool
from threading import Lock

# Rekognition client
rekognition = boto3.client('rekognition', region_name='us-west-2')

# Globals 
d_index = {}
labels_dict = {}
labels_alert = ['person', 'people', 'human']
lock = Lock()

def get_frame_rate(video):
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
     
    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    else:
        fps = video.get(cv2.CAP_PROP_FPS)
    print "Frames per second: {0}".format(fps)
    return fps

def get_frames_every_x_sec(video, secs=1, fmt='opencv'):
    vidcap = cv2.VideoCapture(video)
    fps = get_frame_rate(vidcap)
    inc = int(fps * secs)
    count = 0
    while vidcap.isOpened():
        success, image = vidcap.read()
        if success:
            if count % inc == 0:
                cv2_im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                if fmt == 'PIL':
                    im = Image.fromarray(cv2_im)
                elif fmt == 'DISK':
                    cv2.imwrite(os.path.join(path_output_dir, '%d.png') % count, image)
                else:
                    im = cv2_im
                yield count, im 
        else:
            break
        count += 1
    print "Total Frames: {0}".format(count)
    cv2.destroyAllWindows()
    vidcap.release()

# Extract features helper
def get_labels(params):
    f, image = params

    try:
        resp = rekognition.detect_labels(Image={'Bytes': image.getvalue()})
        labels = resp['Labels']
        
        dt = {}
        for v in labels:
            l = v['Name'].lower() 
            c = v['Confidence']

            if c < 80:
                continue
            
            dt[l] = c

        lock.acquire()
        d_index[f] = dt
        labels_dict.update(dt)
        lock.release()
    except Exception, e:
        print e


if __name__ == '__main__' :

    argv_len = len(sys.argv)

    video_file = sys.argv[1]
    capture_rate = int(sys.argv[2])

    frames = []
    for f_no, img in get_frames_every_x_sec(video_file, capture_rate, "PIL"):
        b_img = io.BytesIO()
        img.save(b_img, format='PNG')
        frames.append([f_no, b_img]) 

    N_THREADS = 25 
    pool = ThreadPool(N_THREADS)
    results = pool.map(get_labels, frames)
    pool.close()
    pool.join()

    print labels_dict
    if any(x in labels_dict for x in labels_alert):
        print "HUMAN FOUND!!"
        sys.exit(1)
    else:
        sys.exit(0)