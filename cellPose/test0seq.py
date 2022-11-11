from cellpose import models,io
import skimage as sk
import numpy as np
import pandas as pd
import trackpy as tp

image = '/Users/lionnt01/Documents/data/NichTSTracking/CPmasks/MAX_HS_Long_lowPower-196int_100s_10ms_1_MMStack_Pos1_6.ome-1_frame1.tif'
model = '/Users/lionnt01/Documents/data/NichTSTracking/CPmasks/models/CP_20221110_150112'
mask_out = '/Users/lionnt01/Documents/data/NichTSTracking/CPmasks/cellposeOut/out1'
diameter = 100
#read tif image in
im = sk.io.imread(image)
#load cellpose model
model = models.CellposeModel(pretrained_model=model)
#run on image
masks, flows, styles = model.eval(im, diameter=diameter)
#save output
io.masks_flows_to_seg(im, masks, flows, 120, mask_out, [0])
io.save_to_png(im, masks, flows, mask_out)
#convert to numpy array
