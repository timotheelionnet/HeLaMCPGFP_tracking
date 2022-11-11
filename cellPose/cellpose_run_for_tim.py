from cellpose import models,io
import skimage as sk
import numpy as np
import pandas as pd
import trackpy as tp

image = 'path to the image to be segmented'
model = 'path to your model here'
mask_out = 'path to save cellpose output (this will be automatically named with .npy and .png extensions in io commands)'
diameter = 'int for the avg diameter of your object'
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
mask = np.where(masks>0, 1, 0)
#label objects
labeled_array, number_ojects = sk.measure.label(mask)

#trackpy commands, here... you will need to compile all of the individual labeled arrays from before
features = pd.DataFrame()
segmented_movie = 'numpy array of each frame segmented and labeled (labels do not need to match I dont think)' 

for n in range(segmented_movie.shape[0]):
    for region in sk.measure.regionprops(segmented_movie[n,:,:]):
        features = features.append([{'y': region.centroid[0],
                                     'x': region.centroid[1],
                                     'frame': n,
                                     },])
#define a search range, also can alter blinking
search_range = 11
#perform the linking on the features dataframe, will get another dataframe back
t = tp.link_df(features, search_range, memory=5)
t.to_csv('outfilename')