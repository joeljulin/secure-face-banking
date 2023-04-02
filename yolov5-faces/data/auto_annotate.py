import os
import glob
import imageio
import numpy as np
import cv2
import numpy.ma as ma
from tqdm import tqdm
import matplotlib.pyplot as plt
from tf_bodypix.api import load_model, download_model, BodyPixModelPaths

BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16
bp_model = load_model(download_model(BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16))


part = ['left_face','right_face']

test = '../secure-face2/test/images/'
train= '../secure-face2/train/images/'
valid = '../secure-face2/valid/images/'
vidcap = cv2.VideoCapture('IMG_8640.MOV')
vidcap.set(cv2.CAP_PROP_FPS, .5)

def find_face_center_and_size(mask):
    # Convert the mask to a numpy array
    mask_array = np.array(mask)
    
    # Find the coordinates of all the white pixels in the mask
    white_pixels = np.where(mask_array == 255)
    
    # Calculate the mean x and y coordinates of the white pixels
    center_x = int(np.mean(white_pixels[1]))
    center_y = int(np.mean(white_pixels[0]))
    
    # Calculate the size of the mask in x and y directions
    mask_size_x = np.max(white_pixels[1]) - np.min(white_pixels[1]) + 1
    mask_size_y = np.max(white_pixels[0]) - np.min(white_pixels[0]) + 1
    
    # Return the center coordinates and mask size
    return (center_x, center_y, mask_size_x, mask_size_y)

def getFrame(sec, count, i, name, class_num):
    hasFrames,image = vidcap.read()
    if hasFrames:
        prediction = bp_model.predict_single(image)
        new_mask = prediction.get_mask(threshold=.3).numpy().astype(np.uint8)
        part_mask = prediction.get_part_mask(new_mask, part_names=part)
        part_mask = part_mask * 255

    
        if count%2 == 0:
             cv2.imwrite(os.path.join(test, f'{name}{count:06d}.png'), image)     # save frame as JPG file
             with open(f'../secure-face2/test/labels/{name}{count:06d}.txt', 'w') as f:
                x, y, mask_x, mask_y = find_face_center_and_size(part_mask)
                
                f.write(f'{class_num} {x/image.shape[1]} {y/image.shape[0]} {mask_x/image.shape[1]} {mask_y/image.shape[0]}')
        if count%3 == 0:
            cv2.imwrite(os.path.join(train, f'{name}{count:06d}.png'), image)     # save frame as JPG file
            with open(f'../secure-face2/train/labels/{name}{count:06d}.txt', 'w') as f:
                x, y, mask_x, mask_y = find_face_center_and_size(part_mask)
                
                f.write(f'{class_num} {x/image.shape[1]} {y/image.shape[0]} {mask_x/image.shape[1]} {mask_y/image.shape[0]}')
            if count%9 == 0:
                cv2.imwrite(os.path.join(valid, f'{name}{count:06d}.png'), image)     # save frame as JPG file
                with open(f'../secure-face2/valid/labels/{name}{count:06d}.txt', 'w') as f:
                    x, y, mask_x, mask_y = find_face_center_and_size(part_mask)
                    f.write(f'{class_num} {x/image.shape[1]} {y/image.shape[0]} {mask_x/image.shape[1]} {mask_y/image.shape[0]}')
    return hasFrames
sec = 0
count = 0
i = 0
frameRate = 10
success = getFrame(sec, count, i, 'britton', 0)
while success:
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec, count, i, 'britton', 0)
    count = count + 1

# sec = 0
# i = 0
vidcap = cv2.VideoCapture('IMG_5950.mp4')
vidcap.set(cv2.CAP_PROP_FPS, .5)

success = getFrame(sec, count, i, 'jared', 1)
while success:
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec, count, i, 'jared', 1)
    count = count + 1

vidcap = cv2.VideoCapture('ross.mov')
vidcap.set(cv2.CAP_PROP_FPS, .5)

success = getFrame(sec, count, i, 'ross', 2)
while success:
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec, count, i, 'ross', 2)
    count = count + 1


vidcap = cv2.VideoCapture('IMG_5953.MOV')
vidcap.set(cv2.CAP_PROP_FPS, .5)

success = getFrame(sec, count, i, 'joel', 3)
while success:
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec, count, i, 'joel', 3)
    count = count + 1