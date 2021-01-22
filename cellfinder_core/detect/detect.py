from datetime import datetime
import logging
import multiprocessing
from multiprocessing import Queue as MultiprocessingQueue
from multiprocessing import Lock

from imlib.general.system import (
    get_sorted_file_paths,
    get_num_processes,
)

from cellfinder_core.detect.filters.plane.multiprocessing import (
    MpTileProcessor,
)
from cellfinder_core.detect.filters.setup_filters import setup_tile_filtering
from cellfinder_core.detect.filters.volume.multiprocessing import (
    Mp3DFilter,
)


def calculate_parameters_in_pixels(
    voxel_sizes,
    soma_diameter_um,
    max_cluster_size_um3,
    ball_xy_size_um,
    ball_z_size_um,
):
    """
    Convert the command-line arguments from real (um) units to pixels
    """

    mean_in_plane_pixel_size = 0.5 * (
        float(voxel_sizes[2]) + float(voxel_sizes[1])
    )
    voxel_volume = (
        float(voxel_sizes[2]) * float(voxel_sizes[1]) * float(voxel_sizes[0])
    )
    soma_diameter = int(round(soma_diameter_um / mean_in_plane_pixel_size))
    max_cluster_size = int(round(max_cluster_size_um3 / voxel_volume))
    ball_xy_size = int(round(ball_xy_size_um / mean_in_plane_pixel_size))
    ball_z_size = int(round(ball_z_size_um / float(voxel_sizes[0])))

    return soma_diameter, max_cluster_size, ball_xy_size, ball_z_size


def main(
    signal_planes_paths,
    start_plane,
    end_plane,
    voxel_sizes,
    soma_diameter,
    max_cluster_size,
    ball_xy_size,
    ball_z_size,
    ball_overlap_fraction,
    soma_spread_factor,
    n_free_cpus,
    points_file,
    log_sigma_size,
    n_sds_above_mean_thresh,
    outlier_keep=False,
    artifact_keep=False,
    save_planes=False,
    plane_directory=None,
    save_csv=False,
):
    n_processes = get_num_processes(min_free_cpu_cores=n_free_cpus)
    start_time = datetime.now()

    (
        soma_diameter,
        max_cluster_size,
        ball_xy_size,
        ball_z_size,
    ) = calculate_parameters_in_pixels(
        voxel_sizes,
        soma_diameter,
        max_cluster_size,
        ball_xy_size,
        ball_z_size,
    )

    # file extension only used if a directory is passed
    img_paths = get_sorted_file_paths(
        signal_planes_paths, file_extension="tif"
    )

    if end_plane == -1:
        end_plane = len(img_paths)
    planes_paths_range = img_paths[start_plane:end_plane]

    workers_queue = MultiprocessingQueue(maxsize=n_processes)
    # WARNING: needs to be AT LEAST ball_z_size
    mp_3d_filter_queue = MultiprocessingQueue(maxsize=ball_z_size)
    for plane_id in range(n_processes):
        # place holder for the queue to have the right size on first run
        workers_queue.put(None)

    setup_params = [
        img_paths[0],
        soma_diameter,
        ball_xy_size,
        ball_z_size,
        ball_overlap_fraction,
        start_plane,
    ]

    mp_3d_filter = Mp3DFilter(
        mp_3d_filter_queue,
        soma_diameter,
        points_file,
        setup_params=setup_params,
        soma_size_spread_factor=soma_spread_factor,
        planes_paths_range=planes_paths_range,
        save_planes=save_planes,
        plane_directory=plane_directory,
        start_plane=start_plane,
        max_cluster_size=max_cluster_size,
        outlier_keep=outlier_keep,
        artifact_keep=artifact_keep,
        save_csv=save_csv,
    )

    # start 3D analysis (waits for planes in queue)
    bf_process = multiprocessing.Process(target=mp_3d_filter.process, args=())
    bf_process.start()  # needs to be started before the loop
    clipping_val, threshold_value = setup_tile_filtering(img_paths[0])
    mp_tile_processor = MpTileProcessor(workers_queue, mp_3d_filter_queue)
    prev_lock = Lock()
    processes = []

    # start 2D tile filter (output goes into queue for 3D analysis)
    for plane_id, path in enumerate(planes_paths_range):
        workers_queue.get()
        lock = Lock()
        lock.acquire()
        p = multiprocessing.Process(
            target=mp_tile_processor.process,
            args=(
                plane_id,
                path,
                prev_lock,
                lock,
                clipping_val,
                threshold_value,
                soma_diameter,
                log_sigma_size,
                n_sds_above_mean_thresh,
            ),
        )
        prev_lock = lock
        processes.append(p)
        p.start()

    processes[-1].join()
    mp_3d_filter_queue.put((None, None, None))  # Signal the end
    bf_process.join()

    logging.info(
        "Detection complete - all planes done in : {}".format(
            datetime.now() - start_time
        )
    )
