from cellpose import models
import tifffile
from .utils import Timer

from skimage.measure import regionprops
import numpy as np

def get_nuclei_labels(nuclei_image):
    timer = Timer("segmentation")
    model = models.Cellpose(gpu=True, model_type="nuclei")
    labels, flows, styles, diams = model.eval(nuclei_image, do_3D=True)
    timer.print_duration()
    return labels

def segment_on_mask(label_image, mask):
    timer = Timer("masking")
    masked_labels = np.zeros(label_image.shape, dtype=label_image.dtype)
    label_props = regionprops(label_image)
    for label in label_props:
        print(label.label)
        centroid = tuple(int(coord) for coord in label.centroid)
        if (mask[centroid] == 255):
            masked_labels[label_image == label.label] = label.label
    timer.print_duration()
    unmasked_labels = label_image - masked_labels
    return masked_labels, unmasked_labels

def get() -> int:
    print("HELLO WORLD!")
    return 5