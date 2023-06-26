import os
from pathlib import Path

from cellfinder_core.tools.IO import read_with_dask



p = Path(os.path.dirname(__file__)).absolute()
CELLFINDER_CORE_PATH = p.parents[1]
TESTS_DATA_INTEGRATION_PATH = (
    Path(CELLFINDER_CORE_PATH) 
    / "tests" / "data" / "integration"
)


class IO:
    """
    Benchmarks for IO tools

    # TODO: parametrise these?
    # TODO: use cache?
    """

    # -----------------------------
    # Benchmark parameters
    # -----------------------------
    params = (
        [
            Path(*("detection", "crop_planes", "ch0")),
            Path(*("detection", "crop_planes", "ch1")),
        ],
        [
            [5, 2, 2]  # microns
        ]
    )
    param_names = [
        'tests_data_integration_subdir',
        'voxel_sizes'
    ]

    # -----------------------------
    # Setup fn: 
    # prepare paths for reading data
    # -----------------------------
    def setup(
            self, 
            subdir, 
            voxel_sizes
    ):
        self.data_dir = TESTS_DATA_INTEGRATION_PATH / subdir
        
    # -----------------------------
    # Runtime benchmarks
    # -----------------------------
    def time_read_with_dask(
            self, 
            subdir, 
            voxel_sizes
    ):
        read_with_dask(
            str(self.data_dir)
        )


    # def time_read_with_numpy()?


    # -----------------------------
    # Peak memory benchmarks?
    # -----------------------------

# class Tiff:


# class Prep:

