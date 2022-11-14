from cellpose import models,io
import skimage as sk
import numpy as np
import pandas as pd
import trackpy as tp
import sys
import tifffile as tf

image = '/Users/lionnt01/Documents/data/NichTSTracking/cellpose/stitchSlidingAvg7.tif'
model = '/Users/lionnt01/Documents/GitHub/HeLaMCPGFP_tracking/cellpose/models/CP_20221111_093301'
mask_out = '/Users/lionnt01/Documents/data/NichTSTracking/cellpose/out/out1'
diameter = 100

#figuring out which version is running
print("Python version")
print (sys.version)

#read tif image in
print("Loading image...")
im = tf.memmap(image)
print("Loaded image, shape is "+str(im.shape))

#load cellpose model
print("Loading model...")
model = models.CellposeModel(pretrained_model=model)
print("Model loaded...")

#run on image
print("Running model...")
ctr = 0
for frame in im:
    print("iteration {}...".format(ctr))
    ctr = ctr+1
    masks, flows, styles = model.eval(frame, diameter=diameter)
    print("Done running model.")
    print("Flows to seg...")
    io.masks_flows_to_seg(frame, masks, flows, 120, mask_out, [0])
    print("Saving...")
    io.save_to_png(frame, masks, flows, mask_out+"_"+str(ctr))
