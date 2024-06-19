from magicgui import magic_factory
from .utils import Timer, Widgets
import tifffile
from cellpose.models import Cellpose
from os import path
from napari import current_viewer


@magic_factory(
    image_path=Widgets.FileWidget("nuclear image", "path to the image to be segmented"),
    diameter=Widgets.TextWidget("cell diameter", "approximate diameter of cells to be segmented (leave blank to calculate automatically)"),
    prob_threshold=Widgets.FloatWidget("prob threshold", "cell probability threshold (set lower for more and larger cells)", -8.0, 8.0, 0.2, 0)
)
def segment_nuclei(image_path, diameter, prob_threshold):
    timer = Timer("nuclear segmentation")

    # Creating label image.
    nuclei_image = tifffile.imread(image_path)
    model = Cellpose(gpu=True, model_type="nuclei")
    label_image, flows, styles, diams = model.eval(
        nuclei_image,
        do_3D=True,
        diameter=float(diameter) if diameter else 0,
        cellprob_threshold=prob_threshold
    )

    # Saving and adding to viewer.
    tifffile.imwrite(path.join(path.dirname(image_path), "label_nuclei.tif"), label_image)
    viewer = current_viewer()
    viewer.dims.ndisplay = 2
    viewer.add_image(nuclei_image)
    viewer.add_labels(label_image, opacity=0.75)

    timer.print_duration()
