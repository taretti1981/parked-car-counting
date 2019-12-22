# curl https://pjreddie.com/media/files/yolov3.weights -o yolov3.weights
# log start
import os
import time
currentPath = os.path.dirname(os.path.abspath(__file__))
doit = True

if os.path.exists(currentPath + os.sep + "logfiles")==False:
    try:
        os.mkdir(currentPath + os.sep + "logfiles")
    except:
        print("Not possible to create the logfile folder")
        doit = False

if doit:
    logfile = open(currentPath + os.sep + "logfiles" + os.sep + "logfile_" + str(int(time.time())) + ".txt", "w")
    logfile.write("Main started\n")

if doit:
    try:
        logfile.write("Importing Packages\n")
        from src.sub_processes import *
        import matplotlib
        from matplotlib import pyplot as plt
        import src.database_management as db_class
        import pandas as pd
        import cv2 as cv
    except:
        doit = False
else:
    logfile.write("Error at importing packages\n")

# read config
if doit:
    try:
        logfile.write("Reading config\n")
        config = readConfig()
        print(config)
    except:
        doit = False
else:
    logfile.write("Error at reading config\n")

# Write down conf, nms thresholds,inp width/height
if doit:
    try:
        logfile.write("Getting Parameters from config\n")
        confThreshold = config['model_config']['confThreshold']  # 0.25
        nmsThreshold = config['model_config']['nmsThreshold']  # 0.40
        inpWidth = config['model_config']['inpWidth']  # 416
        inpHeight = config['model_config']['inpHeight']  # 416
        tolerance = config['model_config']['tolerance']  # 0.35
        # Load names of classes and turn that into a list
        classesFile = config['model_config']['classesFile']  # "coco.names"
        classes = None

    except:
        doit = False
else:
    logfile.write("Error at getting parameters\n")

if doit:
    try:
        logfile.write("Setting Model configuration\n")
        with open(classesFile, 'rt') as f:
            classes = f.read().rstrip('\n').split('\n')

        # Model configuration
        modelConf = config['model_config']['modelConf']  # 'yolov3.cfg'
        modelWeights = config['model_config']['modelWeights']  # 'yolov3.weights'

        # Set up the net
        net = cv.dnn.readNetFromDarknet(modelConf, modelWeights)
        net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
    except:
        doit = False
else:
    logfile.write("Error at setting model configuration\n")

# Process inputs
# winName = 'DL OD with OpenCV'
# cv.namedWindow(winName, cv.WINDOW_NORMAL)
# cv.resizeWindow(winName, 1000,1000)


if doit:
    try:
        logfile.write("Opening camera and taking a look\n")
        cap = cv.VideoCapture(0)
        time.sleep(1)

        # get frame from video
        hasFrame, frame = cap.read()

        # Create a 4D blob from a frame
        blob = cv.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 10, crop=False)

        # Set the input the the net
        net.setInput(blob)
        outs = net.forward(getOutputsNames(net))

        classIDs, confidences = postprocess(frame, outs, classes, confThreshold, nmsThreshold)

        cap.release()
    except:
        doit = False
else:
    logfile.write("Error at taking a look with the camera\n")

# filtering object according to the goal
if doit:
    try:
        logfile.write("Processing image\n")

        print(str(len(classIDs)) + ' objects identified')
        car_cont = 0
        person_cont = 0
        for idx1, idx2 in enumerate(classIDs):
            if classes[classIDs[idx1]] == 'car' or classes[classIDs[idx1]] == 'truck' or classes[
                classIDs[idx1]] == 'motorbike' or classes[classIDs[idx1]] == 'bus':
                if confidences[idx1] >= tolerance:
                    print(classes[classIDs[idx1]] + ', ' + str(confidences[idx1]))
                    car_cont += 1
            if classes[classIDs[idx1]] == 'person':
                if confidences[idx1] >= tolerance:
                    print(classes[classIDs[idx1]] + ', ' + str(confidences[idx1]))
                    person_cont += 1

        print(str(car_cont) + ' vehicles correctly identified')
        print(str(person_cont) + ' persons correctly identified')
        logfile.write(str(car_cont) + " vehicles correctly identified\n")
        logfile.write(str(person_cont) + " persons correctly identified\n")
    except:
        doit = False
else:
    logfile.write("Error at processing image\n")

ts = int(time.time())

# saving on the database
if doit:
    try:
        logfile.write("Opening connection to the database\n")
        db = db_class.database_management()
        db.get_connection()
    except:
        doit = False
else:
    logfile.write("Database connection failed\n")

if doit:
    try:
        logfile.write("Inserting data into the db\n")
        data = {'timestamp': [ts], 'count': [car_cont], 'type': [1]}
        df = pd.DataFrame(data)
        headers = ['timestamp', 'count', 'type']
        #db.insert('identified_objects', headers, df)

        # saving on the database
        data = {'timestamp': [ts], 'count': [person_cont], 'type': [0]}
        df = pd.DataFrame(data)
        headers = ['timestamp', 'count', 'type']
        #db.insert('identified_objects'
        #          '', headers, df)
    except:
        doit = False
else:
    logfile.write("Inserting into the Database failed\n")

try:
    # log insert
    if doit:
        logfile.write("Process sucessfully finished\n")
    else:
        logfile.write("Process failed\n")
    logfile.close()
except:
    print("Failed saving logfile")

try:
    # closing db conn
    db.close()
except:
    print('Failed closing db-conn')
