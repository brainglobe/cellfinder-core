from pathlib import Path

import numpy as np
from imlib.cells.cells import Cell

from cellfinder_core.classify.cube_generator import CubeGeneratorFromFile
from cellfinder_core.classify.tools import get_model

points = [Cell((50, 50, 50), 1)]
signal_array = np.random.rand(100, 100, 100)
background_array = signal_array
voxel_sizes = [5, 2, 2]
network_voxel_sizes = (5, 1, 1)

inference_generator = CubeGeneratorFromFile(
    points,
    signal_array,
    background_array,
    voxel_sizes,
    network_voxel_sizes,
)

model_weights = Path(
    "/Users/dstansby/.cellfinder/model_weights/resnet50_tv.h5"
)
model = get_model(
    model_weights=model_weights,
    network_depth="50-layer",
    inference=True,
)

predictions = model.predict(
    inference_generator,
)
