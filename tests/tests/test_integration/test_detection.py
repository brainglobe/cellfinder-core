import os
import pathlib
from math import isclose

import imlib.IO.cells as cell_io
import pytest

from cellfinder_core.main import main
from cellfinder_core.tools.IO import read_with_dask

data_dir = (
    pathlib.Path(__file__)
    / ".."
    / ".."
    / ".."
    / "data"
    / "integration"
    / "detection"
).resolve()
signal_data_path = os.path.join(data_dir, "crop_planes", "ch0")
background_data_path = os.path.join(data_dir, "crop_planes", "ch1")
cells_validation_xml = os.path.join(data_dir, "cell_classification.xml")

voxel_sizes = [5, 2, 2]
DETECTION_TOLERANCE = 2


# FIXME: This isn't a very good example


@pytest.fixture
def signal_array():
    return read_with_dask(signal_data_path)


@pytest.fixture
def background_array():
    return read_with_dask(background_data_path)


@pytest.mark.slow
def test_detection_full(signal_array, background_array):

    cells_test = main(
        signal_array,
        background_array,
        voxel_sizes,
    )
    cells_validation = cell_io.get_cells(cells_validation_xml)

    num_non_cells_validation = sum(
        [cell.type == 1 for cell in cells_validation]
    )
    num_cells_validation = sum([cell.type == 2 for cell in cells_validation])

    num_non_cells_test = sum([cell.type == 1 for cell in cells_test])
    num_cells_test = sum([cell.type == 2 for cell in cells_test])

    assert isclose(
        num_non_cells_validation,
        num_non_cells_test,
        abs_tol=DETECTION_TOLERANCE,
    )
    assert isclose(
        num_cells_validation, num_cells_test, abs_tol=DETECTION_TOLERANCE
    )


def test_detection_verbose(signal_array, background_array, capsys):
    # capsys captures stdout/stderr
    signal_array = signal_array[0:1, ...]
    background_array = background_array[0:1, ...]

    # verbose=False shouldn't emit anything to stdout
    cells_test = main(
        signal_array, background_array, voxel_sizes, verbose=False
    )
    captured = capsys.readouterr()
    assert captured.out == ""

    # verbose=True (the default) should emit feedback to stdout
    cells_test = main(signal_array, background_array, voxel_sizes)
    captured = capsys.readouterr()
    assert len(captured.out) > 0
