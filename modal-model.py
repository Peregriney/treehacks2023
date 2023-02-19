import os
import modal
import io
import json
from PIL import Image
from fastapi import File, FastAPI
import torch
import pathlib
OUTPUT_DIR = "/tmp/"
from torchvision import models

RANDOM_SPLIT = False
SAMPLE_ONLY = True
FLIP = False
CLASSES = [87, 29]
#model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
#img = 'https://ultralytics.com/images/zidane.jpg'
#img = '../Desktop/CS_Stanford_Courses/duck-ex.jpg'
#results = model(img)
#print(results.pandas().xyxy[0].to_json(orient="records"))

RESIZE_SIZE = 256

BASE_DIR = "CUB_200_2011/"
IMAGES_DIR = BASE_DIR + "images/"

CLASSES_FILE = BASE_DIR + "classes.txt"
BBOX_FILE = BASE_DIR + "bounding_boxes.txt"
IMAGE_FILE = BASE_DIR + "images.txt"
LABEL_FILE = BASE_DIR + "image_class_labels.txt"
SIZE_FILE = BASE_DIR + "sizes.txt"
SPLIT_FILE = BASE_DIR + "train_test_split.txt"

TRAIN_LST_FILE = "birds_ssd_train.lst"
VAL_LST_FILE = "birds_ssd_val.lst"

if SAMPLE_ONLY:
    TRAIN_LST_FILE = "birds_ssd_sample_train.lst"
    VAL_LST_FILE = "birds_ssd_sample_val.lst"

TRAIN_RATIO = 0.8
CLASS_COLS = ["class_number", "class_id"]
IM2REC_SSD_COLS = [
    "header_cols",
    "label_width",
    "zero_based_id",
    "xmin",
    "ymin",
    "xmax",
    "ymax",
    "image_file_name",
]

image = (
    modal.Image.debian_slim()
    .run_commands(
        "apt-get install -y libgl1-mesa-glx libglib2.0-0 wget"
        #f"wget  -P /root",
    )
    .pip_install_from_requirements(requirements_txt='requirements.txt')
#("opencv-python", "torch", "torchvision", "pandas")
)

stub = modal.Stub("yolo-detection", image=image)

if stub.is_inside():
	import cv2
	import torch
	from torchvision import models
	import pandas as pd
	#model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
	
stub.sv = modal.SharedVolume().persist("fluviator-vol")

#@stub.webhook()
#def web():
#    return {
#        "image": b'182309843'
#    }

#images_to_send = []

@stub.function(shared_volumes = {"/boxpreds": stub.sv},timeout=600)
def predict_droneimg(fn):
	#import base64
	#print('entered predict_droneimg function')	
	model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
	model.eval()
	#print('we have entered the predict_droneimg function')
	#print('before trying to evaluate FILE using model')
	results = model(fn)

	#print("before trying to interpret pandas form of results")	
	#print(pd.DataFrame(results.pandas().xyxy[0]))
	for box in pd.DataFrame(results.pandas().xyxy[0]).iterrows():
		#print(box)
		#print(type(box))
		#print(box.shape)
		#print("one bounding box")
		#if box[4] != 'bird': #or is it box 4???
		if 'bird' not in str(box[1]):
			print('remove this file because bird not found')
			os.remove(os.path.join('/boxpreds',fn))
			
			break
			#with open(fn, 'rb') as f:
				#out_bytes = base64.b64encode(f.read())
				#web(out_bytes)
	print("all bounding boxes are fine")
	#results.save(save_dir='/boxpreds')
	return   # fn, results

@stub.function(shared_volumes = {"/boxpreds": stub.sv})
def process_new_imgs(images_bytes):
	#print(f"checking new images from folder")
	
	#model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
	#model.eval()
	#print('model has been loaded DING')
	positive_flags = []
	output_tags = []
	ctr = 1
	for img_bytes in images_bytes: 
		fnstr = 'pic'+str(ctr)+'.jpeg'
		f = open(os.path.join('/boxpreds',fnstr), 'wb')
		f.write(img_bytes)
		f.close()
		#file, results = predict_droneimg.call(, model) #if you turn it modal again, use .call()
		print('right BEFORE calling predict_droneimg')
		predict_droneimg.call(os.path.join('/boxpreds', fnstr))
		ctr += 1
#if needed can write these bytes to a file
		#f.close()
		#positive_flags.append(file)
		#output_tags.append(results)
	#f = open('clfinput.jpeg', 'w')
	
	#print()
	#os.remove(f) ####DO I NEED TO USE PATH INSTEAD HERE??
	#return positive_flags, output_tags
	return
	###
	##INCLUDE THE REST/PATH/ WEBHOOK HERE TO CONNECT
    
@stub.local_entrypoint
def main(folderpath: str = "imgstills"):
	#from torchvision import models
	#import models
	print('modal started')
	seen: set[str] = set()
	#files = list(pathlib.Path(folderpath).iterdir())
	files = [os.path.join(folderpath,filename) for filename in os.listdir(folderpath)]
	print([str(f) for f in files])
	files = [f for f in files if f not in seen]
    
	#print(type(files))
	#print(type(files[0])
	#print(len(files))
	#print('name of files')
	filelist = []	
	for file in files:
		#file = os.path.join(folderpath, file)
		print(file)
		print(type(file))
		if '.jpeg' in file:
			with open(file, "rb") as f: #file.read_bytes()
				data = f.read()
				filelist.append(data)
	print('info about filelist, which should store a list of bytes objects')
	
	print(len(filelist))
	print(type(filelist[0]))
	
	#positive_flags, output_tags = process_new_imgs.call(filelist)###(folderpath)
	process_new_imgs.call(filelist)
	#THIS CALL TO FUNCTION DOES NOT RETURN ANYTHING! :) 
	#for idx in range(len(positive_flags)):
	#	fn = positive_flags[idx]
	#	results = output_tags[idx]
		#print(results.pandas().xyxy[0].to_json(orient="records"))
	#	results.save()
	#INCLUDE REST/PATH / WEBHOOK HERE

@stub.webhook(shared_volumes = {"/boxpreds": stub.sv})
def web():
	import base64
	folderpath = '/boxpreds'
	#for filename in shared_volumes:
	files = [os.path.join(folderpath,filename) for filename in os.listdir(folderpath)]
	output_obj = {}
	for file in files: 
		with open(file, "rb") as f: 
			dat = base64.b64encode(f.read())
			output_obj[file] = dat

	return output_obj



