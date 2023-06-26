import os
from pathlib import Path

from cellfinder_core.tools.IO import read_with_dask


p = Path(os.path.dirname(__file__)).absolute()
CELLFINDER_CORE_PATH = p.parents[1]


class IO:
    """
    Benchmarks for IO tools
    """
    def setup(self):
        # prepare paths for reading data

        # TODO: parametrise these?
        self.data_dir = (
            Path(CELLFINDER_CORE_PATH) / "tests" / "data" / 
            "integration" / "detection" / "crop_planes" 
            / "ch0"
        )
        self.voxel_sizes = [5, 2, 2]  # microns
        
    def time_read_with_dask(self):
        self.signal_array = read_with_dask(
            str(self.data_dir)
        )


    # def time_read_with_numpy()?

# class Tiff:


# class Prep: