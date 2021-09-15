import dask.array as d_array

from cellfinder_core.tools import IO


def test_read_with_dask_txt():
    stack = IO.read_with_dask("tests/data/tools/brain_paths.txt")
    assert type(stack) == d_array.Array


def test_read_with_dask_glob_txt_equal():
    txt_stack = IO.read_with_dask("tests/data/tools/brain_paths.txt")
    glob_stack = IO.read_with_dask("tests/data/brain/")

    assert d_array.equal(txt_stack, glob_stack).all()
