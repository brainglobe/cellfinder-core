import os
from pathlib import Path

from cellfinder_core.tools.IO import get_tiff_meta, read_with_dask

p = Path(os.path.dirname(__file__)).absolute()
CELLFINDER_CORE_PATH = p.parents[2]
TESTS_DATA_INTEGRATION_PATH = (
    Path(CELLFINDER_CORE_PATH) / "tests" / "data" / "integration"
)
# Q for review: is there a nice way to get cellfinder-core path?


class Read:
    # ---------------------------------------------
    # Setup & teardown functions
    # --------------------------------------------
    def setup(self, subdir):
        self.data_dir = str(subdir)

    def teardown(self, subdir):
        del self.data_dir
        # Q for review: do I need this?
        # maybe only relevant if it is the parameter we sweep across?
        # from https://github.com/astropy/astropy-benchmarks/blob/
        # 8758dabf84001903ea00c31a001809708969a3e4/benchmarks/cosmology.py#L24
        # (they only use teardown function in that case)

    # ---------------------------------------------
    # Benchmarks for reading 3d arrays with dask
    # --------------------------------------------
    def time_read_with_dask(self, subdir):
        read_with_dask(self.data_dir)

    time_read_with_dask.param_names = [
        "tests_data_integration_subdir",
    ]
    time_read_with_dask.params = (
        [
            TESTS_DATA_INTEGRATION_PATH
            / Path("detection", "crop_planes", "ch0"),
            TESTS_DATA_INTEGRATION_PATH
            / Path("detection", "crop_planes", "ch1"),
        ],
    )

    # -----------------------------------------------
    # Benchmarks for reading metadata from tif files
    # -------------------------------------------------
    def time_get_tiff_meta(
        self,
        subdir,
    ):
        get_tiff_meta(self.data_dir)

    time_get_tiff_meta.param_names = [
        "tests_data_integration_tiffile",
    ]

    cells_tif_files = list(
        Path(TESTS_DATA_INTEGRATION_PATH, "training", "cells").glob("*.tif")
    )
    non_cells_tif_files = list(
        Path(TESTS_DATA_INTEGRATION_PATH, "training", "non_cells").glob(
            "*.tif"
        )
    )
    time_get_tiff_meta.params = cells_tif_files + non_cells_tif_files
