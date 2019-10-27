#curl https://pjreddie.com/media/files/yolov3.weights -o yolov3.weights

import cv2 as cv
from src.sub_processes import *
import matplotlib
from matplotlib import pyplot as plt
import time
import src.database_management as db_class
import pandas as pd


# read config
config = readConfig()

#Write down conf, nms thresholds,inp width/height
confThreshold = config['model_config']['confThreshold'] #0.25
nmsThreshold = config['model_config']['nmsThreshold'] #0.40
inpWidth = config['model_config']['inpWidth'] #416
inpHeight = config['model_config']['inpHeight'] #416
tolerance = config['model_config']['tolerance'] #0.35

#Load names of classes and turn that into a list
classesFile = config['model_config']['classesFile'] #"coco.names"
classes = None

with open(classesFile,'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

#Model configuration
modelConf = config['model_config']['modelConf'] #'yolov3.cfg'
modelWeights = config['model_config']['modelWeights'] #'yolov3.weights'

#Set up the net

net = cv.dnn.readNetFromDarknet(modelConf, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


#Process inputs
winName = 'DL OD with OpenCV'
cv.namedWindow(winName, cv.WINDOW_NORMAL)
cv.resizeWindow(winName, 1000,1000)


cap = cv.VideoCapture(0)
time.sleep(1)

#get frame from video
hasFrame, frame = cap.read()

#Create a 4D blob from a frame
blob = cv.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 10, crop = False)

#Set the input the the net
net.setInput(blob)
outs = net.forward(getOutputsNames(net))

classIDs, confidences = postprocess (frame, outs, classes, confThreshold, nmsThreshold)

cap.release()


# filtering object according to the goal
print(str(len(classIDs)) + ' objects identified')
car_cont = 0
person_cont = 0
for idx1,idx2 in enumerate(classIDs):
    if classes[classIDs[idx1]]=='car' or classes[classIDs[idx1]]=='truck' or classes[classIDs[idx1]]=='motorbike' or classes[classIDs[idx1]]=='bus':
        if confidences[idx1] >= tolerance:
            print(classes[classIDs[idx1]]+', '+str(confidences[idx1]))
            car_cont += 1
    if classes[classIDs[idx1]] == 'person':
        if confidences[idx1] >= tolerance:
            print(classes[classIDs[idx1]]+', '+str(confidences[idx1]))
            person_cont += 1


print(str(car_cont) + ' vehicles correctly identified')
print(str(person_cont) + ' persons correctly identified')


ts = int(time.time())

# saving on the database
db = db_class.database_management()
db.get_connection()
data = {'timestamp':[ts], 'count':[car_cont], 'type': [1]}
df = pd.DataFrame(data)
headers = ['timestamp','count', 'type']
db.insert('identified_objects',headers,df)


# saving on the database
db = db_class.database_management()
db.get_connection()
data = {'timestamp':[ts], 'count':[person_cont], 'type': [0]}
df = pd.DataFrame(data)
headers = ['timestamp','count','type']
db.insert('identified_objects'
          '',headers,df)

# closing db conn
db.close()