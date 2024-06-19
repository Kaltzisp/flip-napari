import os
import tifffile
from .modules import segmentation
from magicgui import magic_factory

@magic_factory(
    image_path={"widget_type": "FileEdit", "tooltip": "path to the nuclear image for segmentation"},
)
def segment_nuclei(image_path):
    image = tifffile.imread(image_path)
    labels = segmentation.get_nuclei_labels(image)
    tifffile.imwrite(os.path.join(os.path.dirname(image_path), "label.tif"), labels)
