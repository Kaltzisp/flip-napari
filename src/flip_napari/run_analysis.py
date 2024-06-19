from magicgui import magic_factory
from .utils import Timer, Widgets
import tifffile
from pandas import DataFrame
from skimage.measure import regionprops_table
from os import path
from math import pi
import numpy as np
from napari import current_viewer
from vispy.color import Colormap


@magic_factory(
    label_image_path=Widgets.FileWidget("label image", "path to the nuclear label image"),
    intensity_image_path=Widgets.FileWidget("intensity image", "path to the intensity image"),
    masks_image_path=Widgets.FileWidget("masks image", "path to the masks image created in Amira"),
    threshold=Widgets.FloatWidget("threshold", "pixel intensity threshold for determining marker activity", 0, 1, 0.05, 0.4),
    min_diameter=Widgets.TextWidget("min diameter", "minimum permitted diameter for a cell to be included in summary results"),
    target_tissues=Widgets.TextWidget("target tissues", "indexes of tissues to include in the generated red/blue activity label")
)
def run_analysis(label_image_path, intensity_image_path, masks_image_path, threshold, min_diameter, target_tissues):
    timer = Timer("marker analysis")

    # Opening images and getting path.
    label_image = tifffile.imread(label_image_path)
    intensity_image = tifffile.imread(intensity_image_path)
    masks_image = tifffile.imread(masks_image_path)
    save_dir = path.dirname(label_image_path)

    # Getting label data.
    df = DataFrame(regionprops_table(label_image, intensity_image=intensity_image, properties=["label", "intensity_mean", "centroid", "area"]))
    df["tissue"] = masks_image[df["centroid-0"].astype(int), df["centroid-1"].astype(int), df["centroid-2"].astype(int)]
    df.to_csv(path.join(save_dir, "data_full.csv"))

    # Thresholding df by minimum volume.
    min_volume = (4/3) * pi * ((float(min_diameter) / 2) ** 3) if min_diameter else 0
    df = df[df["area"] >= min_volume]

    # Collecting summary information.
    tissue_indexes = []
    total_objects = []
    positive_objects = []
    for tissue in df["tissue"].unique():
        tissue_df = df[df["tissue"] == tissue]
        tissue_indexes.append(tissue)
        total_objects.append(len(tissue_df))
        positive_objects.append((tissue_df["intensity_mean"] >= 255 * threshold).sum())
    result = DataFrame({
        "tissue": tissue_indexes,
        "positive": positive_objects,
        "total": total_objects
    })
    result.to_csv(path.join(save_dir, "data_summary.csv"))

    # Adding to viewer.
    viewer = current_viewer()
    viewer.dims.ndisplay = 2
    viewer.add_image(intensity_image)
    viewer.add_labels(masks_image, opacity=0.5)

    # Creating activity label.
    if len(target_tissues) > 0:
        selected_indexes = [int(i) for i in target_tissues.split(",")]
        activity_label = np.zeros_like(label_image)
        for label in df.itertuples(index=True):
            print(f"Computing label {label.Index} of {len(df)}.")
            if (label.tissue in selected_indexes):
                if (label.intensity_mean >= 255 * threshold):
                    activity_label[label_image == label.label] = 2
                else:
                    activity_label[label_image == label.label] = 1
        tifffile.imwrite(path.join(save_dir, "label_activity.tif"), activity_label)

        # Creating color map and adding to viewer.
        viewer.add_image(activity_label, opacity=0.75, colormap=Colormap(["transparent", "blue", "red"]))

    timer.print_duration()
