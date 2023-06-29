import os
from pathlib import Path

from cellfinder_core.tools.IO import get_tiff_meta, read_with_dask

p = Path(os.path.dirname(__file__)).absolute()
CELLFINDER_CORE_PATH = p.parents[2]
# Q for review: is there a nice way to get cellfinder-core path?
TESTS_DATA_INTEGRATION_PATH = (
    Path(CELLFINDER_CORE_PATH) / "tests" / "data" / "integration"
)


# ---------------------------------------------
# Benchmarks for reading 3d arrays with dask
# --------------------------------------------
class Dask:
    param_names = [
        "tests_data_integration_subdir",
        "voxel_sizes",  # in microns
    ]

    params = (
        [
            TESTS_DATA_INTEGRATION_PATH
            / Path("detection", "crop_planes", "ch0"),
            TESTS_DATA_INTEGRATION_PATH
            / Path("detection", "crop_planes", "ch1"),
        ],
        [[3, 2, 2], [5, 2, 2]],
    )

    def setup(self, subdir, voxel_sizes):
        self.data_dir = str(subdir)

    def teardown(self, subdir, voxel_sizes):
        del self.data_dir
        # Q for review: do I need this? only if it is the parameter we sweep
        # across?
        # from https://github.com/astropy/astropy-benchmarks/blob/
        # 8758dabf84001903ea00c31a001809708969a3e4/benchmarks/cosmology.py#L24
        # (they only use teardown in that case)

    def time_read_with_dask(self, subdir, voxel_sizes):
        read_with_dask(self.data_dir)


# -----------------------------------------------
# Benchmarks for reading metadata from tif files
# -------------------------------------------------
class Tif:
    param_names = [
        "tests_data_integration_tiffile",
    ]

    params = (
        [
            *[
                x
                for x in Path(
                    TESTS_DATA_INTEGRATION_PATH, "training", "cells"
                ).glob("*.tif")
            ],
            *[
                x
                for x in Path(
                    TESTS_DATA_INTEGRATION_PATH, "training", "non_cells"
                ).glob("*.tif")
            ],
        ],
    )

    def setup(self, subdir):
        self.data_dir = str(subdir)

    def teardown(self, subdir):
        del self.data_dir

    def time_get_tiff_meta(
        self,
        subdir,
    ):
        get_tiff_meta(self.data_dir)
