import os
import napari
import tifffile
from magicgui import magic_factory

import numpy as np
import pandas as pd
from skimage.measure import regionprops_table

@magic_factory(
    labels_image={"widget_type": "FileEdit", "tooltip": "path to the nuclei label image"},
    intensity_image={"widget_type": "FileEdit", "tooltip": "path to the intensity (marker) image"},
    masks_image={"widget_type": "FileEdit", "tooltip": "path to the Amira masks file"},
    threshold={"widget_type": "FloatSlider", "value": 0.3, "max": 1, "tooltip": "threshold for determining marker activity"},
    target_tissues={"widget_type": "LineEdit", "value": "", "tooltip": "tissues to include in the created activity label image"},
    call_button="Run Segmentation"
)
def run_analysis(labels_image, intensity_image, masks_image, threshold, target_tissues):
    # Opening images.
    labels = tifffile.imread(labels_image)
    marker = tifffile.imread(intensity_image)
    amira_masks = tifffile.imread(masks_image)

    # Getting label props dataframe.
    df = pd.DataFrame(regionprops_table(labels, intensity_image=marker, properties=["label", "intensity_mean", "centroid", "area"]))
    df["tissue"] = amira_masks[df["centroid-0"].astype(int), df["centroid-1"].astype(int), df["centroid-2"].astype(int)]
    df.to_csv(os.path.join(os.path.dirname(labels_image), "data_full.csv"))

    # Collecting summary and average information.
    tissue_indexes = []
    positives = []
    totals = []
    for tissue in df["tissue"].unique():
        tissue_df = df[df["tissue"] == tissue]
        tissue_indexes.append(tissue)
        positives.append((tissue_df["intensity_mean"] >= 255 * threshold).sum())
        totals.append(len(tissue_df))
    result = pd.DataFrame({
        "tissue": tissue_indexes,
        "total_objects": totals,
        "positives": positives
    })
    result.to_csv(os.path.join(os.path.dirname(labels_image), "data_summary.csv"))

    # Adding to viewer.
    viewer = napari.current_viewer()
    viewer.dims.ndisplay = 2
    viewer.add_image(marker)
    viewer.add_labels(amira_masks)
    viewer.add_labels(labels)

    # Creating marker image.
    if len(target_tissues) > 0:
        selected_indexes = [int(i) for i in target_tissues.split(",")]
        marker_image = np.zeros(labels.shape + (3,), dtype=np.uint8)
        for label in df.itertuples(index=True):
            print(str(round(100 * label.Index / len(df), 1)) + " %")
            if (label.tissue in selected_indexes):
                if (label.intensity_mean >= 255 * threshold):
                    marker_image[labels == label.label] = [200, 0, 0]
                else:
                    marker_image[labels == label.label] = [0, 0, 200]
        tifffile.imwrite(os.path.join(os.path.dirname(labels_image), "label_marker.tif"), marker_image)
        viewer.add_image(marker_image)
