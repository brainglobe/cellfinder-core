
# ------------------------------------
# Runtime benchmarks 
# ------------------------------------
def timeraw_import_main():
    return"""
    from cellfinder_core.main import main
    """

def timeraw_import_io_dask():
    return"""
    from cellfinder_core.tools.IO import read_with_dask
    """   