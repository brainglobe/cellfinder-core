# %%
import os
from pathlib import Path
import imlib.IO.cells as cell_io

from cellfinder_core.main import main as cellfinder_run
from cellfinder_core.tools.IO import read_with_dask



# Input data
data_dir = Path(os.getcwd()) / "tests" / "data" / "integration" / "detection"
signal_data_dir = data_dir / "crop_planes" / "ch0"
background_data_dir = data_dir / "crop_planes" / "ch1"
voxel_sizes = [5, 2, 2]  # microns



if __name__ == "__main__":
    
    # Read data
    # - dask for ~ TB of data, you pass the directory and it will load all the images as a 3D array
    # - tiff can also be a 3D array but no examples in the test data
    signal_array = read_with_dask(str(signal_data_dir))  # (30, 510, 667) ---> planes , image size (h, w?)
    background_array = read_with_dask(str(background_data_dir))

    # D+C pipeline
    # Detection and classification pipeline
    # the output is a list of imlib Cell objects w/ centroid coordinate and type
    detected_cells = cellfinder_run(
        signal_array,
        background_array,
        voxel_sizes,
    )

    # Inspect results
    print(f'Sample cell type: {type(detected_cells[0])}') 
    print('Sample cell attributes: '
          f'x={detected_cells[0].x}, '
          f'y={detected_cells[0].y}, '
          f'z={detected_cells[0].z}, '
          f'type={detected_cells[0].type}')  # Cell: x: 132, y: 308, z: 10, type: 2
    
    num_cells = sum([cell.type == 2 for cell in detected_cells])  # Cell type 2 is a true positive (classified as cell), 
    num_non_cells = sum([cell.type == 1 for cell in detected_cells])  # Cell type 1 is a false positive (classified as non-cell)
    print(f'{num_cells}/{len(detected_cells)} cells classified as cells')
    print(f'{num_non_cells}/{len(detected_cells)} cells classified as non-cells')


    # Save results in the cellfinder XML standard
    # it only saves type 1
    cell_io.save_cells(detected_cells, 'output.xml')

    # # to read them
    # cell_io.get_cells('output.xml')