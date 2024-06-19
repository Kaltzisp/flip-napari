from cellpose import models
from .utils import Timer


def get_nuclei_labels(nuclei_image):
    timer = Timer("segmentation")
    model = models.Cellpose(gpu=True, model_type="nuclei")
    labels, flows, styles, diams = model.eval(nuclei_image, do_3D=True)
    timer.print_duration()
    return labels
