from magicgui import magic_factory
from .utils import Timer, Widgets
import tifffile
import numpy as np
from cellpose.models import Cellpose
from os import path
from napari import current_viewer


@magic_factory(
    image_path=Widgets.FileWidget("nuclear image", "path to the image to be segmented"),
    diameter=Widgets.TextWidget("cell diameter", "approximate diameter of cells to be segmented (leave blank to calculate automatically)"),
    prob_threshold=Widgets.FloatWidget("prob threshold", "cell probability threshold (set lower for more and larger cells)", -8.0, 8.0, 0.2, 0),
    mask_path=Widgets.FileWidget("cropping mask", "path to the amira mask to use for cropping of the cardiac regoin"),
)
def segment_nuclei(image_path, diameter, prob_threshold, mask_path):
    # Opening images.
    timer = Timer("Opening images")
    nuclei_image = tifffile.imread(image_path)
    amira_mask = tifffile.imread(mask_path)

    # Clearning extraneous data from image.
    timer.restart("Cropping nuclear image")
    mask = amira_mask != amira_mask[0, 0, 0]
    nuclei_image = nuclei_image * mask

    # Cropping nuclear image.
    mask_indices = np.where(mask)
    lower_bound = tuple(np.min(mask_indices, axis=1))
    upper_bound = tuple(np.max(mask_indices, axis=1) + 1)
    nuclei_image = nuclei_image[
        lower_bound[0]:upper_bound[0],
        lower_bound[1]:upper_bound[1],
        lower_bound[2]:upper_bound[2]]
    tifffile.imwrite(path.join(path.dirname(image_path), "nuclei_cropped.tif"), nuclei_image)
    del amira_mask, mask, mask_indices
    timer.print_duration()

    # Creating label image.
    timer.restart("Segmenting nuclear image")
    model = Cellpose(gpu=True, model_type="nuclei")
    label_image, flows, styles, diams = model.eval(
        nuclei_image,
        do_3D=True,
        diameter=float(diameter) if diameter else 0,
        cellprob_threshold=prob_threshold
    )
    timer.print_duration()

    # Saving and adding to viewer.
    timer.restart("Saving label image")
    tifffile.imwrite(path.join(path.dirname(image_path), "label_nuclei.tif"), label_image)
    viewer = current_viewer()
    viewer.dims.ndisplay = 2
    viewer.add_image(nuclei_image)
    viewer.add_labels(label_image, opacity=0.75)
    timer.end()
