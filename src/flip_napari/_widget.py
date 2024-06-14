import napari
from magicgui import magic_factory
# from napari_dmlab import segmentation
from skimage.measure import regionprops_table
import pandas as pd
import tifffile
import numpy as np

# Amira masks:
# 0 - myo?
# 1 - background
# 2 - epi?

# the magic_factory decorator lets us customize aspects of our widget
# we specify a widget type for the threshold parameter
# and use auto_call=True so the function is called whenever
# the value of a parameter changes
@magic_factory(
    save_path={"widget_type": "FileEdit", "mode": "d", "tooltip": "location to save output images and data"},
    threshold={"widget_type": "FloatSlider", "max": 1, "tooltip": "threshold for determining marker activity"},
    marker_tissues={"widget_type": "LineEdit", "value": "", "tooltip": "tissue indexes to include in the created marker image (e.g. 2,6,7)"},
    call_button="Run Segmentation"
)
def widget_3d(
    label_image: "napari.layers.Labels",
    amira_masks: "napari.layers.Labels",
    intensity_image: "napari.layers.Image",
    save_path: "str",
    threshold: "float",
    marker_tissues: "str"
):
    print("Hello World!")
    # # Getting label props dataframe.
    # df = pd.DataFrame(regionprops_table(label_image.data, intensity_image=intensity_image.data, properties=["label", "intensity_mean", "centroid", "area"]))
    # df["tissue"] = amira_masks.data[df["centroid-0"].astype(int), df["centroid-1"].astype(int), df["centroid-2"].astype(int)]
    # df.to_csv(str(save_path) + "/data_full.csv")

    # # Collecting summary and average information.
    # tissue_indexes = []
    # positives = []
    # totals = []
    # for tissue in df["tissue"].unique():
    #     tissue_df = df[df["tissue"] == tissue]
    #     tissue_indexes.append(tissue)
    #     positives.append((tissue_df["intensity_mean"] >= 255 * threshold).sum())
    #     totals.append(len(tissue_df))
    # result = pd.DataFrame({
    #     "tissue": tissue_indexes,
    #     "total_objects": totals,
    #     "positives": positives
    # })
    # result.to_csv(str(save_path) + "/data_summary.csv")

    # # Creating marker image.
    # selected_indexes = [int(i) for i in marker_tissues.split(",")]
    # marker_image = np.zeros(label_image.data.shape + (3,), dtype=np.uint8)
    # for label in df.itertuples(index=True):
    #     print(str(round(100 * label.Index / len(df), 1)) + " %")
    #     if (label.tissue in selected_indexes):
    #         if (label.intensity_mean >= 255 * threshold):
    #             marker_image[label_image.data == label.label] = [200, 0, 0]
    #         else:
    #             marker_image[label_image.data == label.label] = [0, 0, 200]
    # tifffile.imwrite(str(save_path) + "/label_marker.tif", marker_image)

    # # Running segmentation on mask.
    # masked_labels, unmasked_labels = segmentation.segment_on_mask(label_image.data, amira_masks.data, int(target_mask))
    # tifffile.imwrite(str(save_path) + "/label_masked.tif", masked_labels)
    # tifffile.imwrite(str(save_path) + "/label_unmasked.tif", unmasked_labels)

    # # Getting intensities table and saving.
    # data = regionprops_table(masked_labels, intensity_image=intensity_image.data, properties=["label", "intensity_mean", "centroid", "area"])
    # df = pd.DataFrame(data)
    # df.to_csv(str(save_path) + "/label_data.csv")

    # # Creating marker image.
    # positives = df[df["intensity_mean"] >= 255 * threshold]["label"].values
    # negatives = df[df["intensity_mean"] < 255 * threshold]["label"].values
    # marker_image = np.zeros(masked_labels.shape + (3,), dtype=np.uint8)
    # marker_image[np.isin(masked_labels, positives)] = [200, 0, 0]
    # marker_image[np.isin(masked_labels, negatives)] = [0, 0, 200]
    # tifffile.imwrite(str(save_path) + "/label_marker.tif", marker_image)

    # # Getting quantifications.
    # quantifications = pd.DataFrame({"positive": [len(positives)], "negative": [len(negatives)]})
    # quantifications.to_csv(str(save_path) + "/summary.csv")
    # print("Complete!")
