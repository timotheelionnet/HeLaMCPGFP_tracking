from cellpose import models,io
import skimage as sk
import numpy as np
import pandas as pd
import trackpy as tp

image = '/Users/lionnt01/Documents/data/NichTSTracking/cellpose/stitchSlidingAvg7.tif'
image = '/Users/lionnt01/Documents/data/NichTSTracking/cellpose/train/stitchSlidingAvg7_frame196.tif'
model = '/Users/lionnt01/Documents/GitHub/HeLaMCPGFP_tracking/cellpose/models/CP_20221111_093301'
mask_out = '/Users/lionnt01/Documents/data/NichTSTracking/cellpose/out/out1'
diameter = 100
#read tif image in
print("Loading image...")
im = sk.io.imread(image)
print("Loaded image...")

#load cellpose model
print("Loading model...")
model = models.CellposeModel(pretrained_model=model)
print("Model loaded...")

#run on image
print("Running model...")
masks, flows, styles = model.eval(im, diameter=diameter)
print("Done running model.")

#save output
print("Flows to seg...")
io.masks_flows_to_seg(im, masks, flows, 120, mask_out, [0])
print("Saving...")
io.save_to_png(im, masks, flows, mask_out)
#convert to numpy array
