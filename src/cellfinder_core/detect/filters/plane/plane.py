import numpy as np

from cellfinder_core.detect.filters.plane.classical_filter import enhance_peaks
from cellfinder_core.detect.filters.plane.tile_walker import TileWalker


def get_tile_mask(
    plane,
    clipping_value,
    threshold_value,
    soma_diameter,
    log_sigma_size,
    n_sds_above_mean_thresh,
):
    laplace_gaussian_sigma = log_sigma_size * soma_diameter
    plane = plane.T
    np.clip(plane, 0, clipping_value, out=plane)

    walker = TileWalker(plane, soma_diameter)

    walker.walk_out_of_brain_only()

    thresholded_img = enhance_peaks(
        walker.thresholded_img,
        clipping_value,
        gaussian_sigma=laplace_gaussian_sigma,
    )

    # threshold
    avg = thresholded_img.ravel().mean()
    sd = thresholded_img.ravel().std()

    plane[
        thresholded_img > avg + n_sds_above_mean_thresh * sd
    ] = threshold_value
    return walker.good_tiles_mask.astype(np.uint8)
