#!/usr/bin/env python3
import sys
import os
import cv2
import pickle
import argparse
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf
from unet import UNet

if __name__=="__main__":
    unet = UNet()
    CURR_PATH = unet.args.output_dir
    
    files = os.listdir(CURR_PATH)

    test_data = [i for i in files if ".png" in i and i.startswith("test_")]
	
    dim = 256
    actual_images = [i for i in test_data]
    # actual_images = actual_images[1:2]
    X_test = [cv2.imread(os.path.join(CURR_PATH,i), 1) for i in actual_images]  

    X_test = np.array(X_test).reshape((len(X_test),dim,dim,3)).astype(np.float32)
    model = load_model(os.path.join(CURR_PATH,"model_copy.h5"), compile=False)
    preds = model.predict(X_test)

    for i in range(len(preds)):
        im = preds[i]
        im[im>0.5] = 1
        im[im<0.5] = 0
        width,height=im.shape[1],im.shape[0]
        img=cv2.imread(os.path.join(CURR_PATH,actual_images[i]),0)
        img=cv2.resize(img,(256,256)).reshape(256,256, 1)
        masked_img=np.squeeze(img*im.reshape(256,256, 1))
        masked_img[masked_img>0.5] = 255
        masked_img[masked_img<0.5] = 0
        masked_img=cv2.resize(masked_img,(width,height)).astype(np.float32)
        # print('Writing to ','pred_'+ str(test_data[i].split('.png')[0][5:]+'_mask.png') )
        cv2.imwrite(os.path.join(CURR_PATH,'pred_'+ str(test_data[i].split('.png')[0][5:]+'_mask.png')), masked_img)   
        # cv2.imwrite(os.path.join(CURR_PATH,'test_mask.png'), masked_img)   