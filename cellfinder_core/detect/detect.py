import multiprocessing
from datetime import datetime
from multiprocessing import Lock
from multiprocessing import Queue as MultiprocessingQueue

import numpy as np
from imlib.general.system import get_num_processes

from cellfinder_core.detect.filters.plane.multiprocessing import (
    MpTileProcessor,
)
from cellfinder_core.detect.filters.setup_filters import setup_tile_filtering
from cellfinder_core.detect.filters.volume.multiprocessing import Mp3DFilter


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


class DetectRunner:
    def __init__(self):
        """
        A class for running detection.

        The API of this class mimics that of `multiprocessing.Proces
        `, providing ``.start()`` to start the detection processes and
        ``.join()`` to block execution until detection is complete and return
        the results.

        While the processes are running progress can be queried by getting
        items from ``self.planes_done_queue``, which stores the plane ids that
        have been processed.

        Attributes
        ----------
        planes_done_queue : multiprocessing.Queue
            Stores the plane IDs that have been processed. Can be used to
            externally query the progress of the MP3D filter.
        """
        self.planes_done_queue = MultiprocessingQueue()

    def __call__(self, *args, **kwargs):
        """
        Run detection.
        """
        self.start(*args, **kwargs)
        return self.join()

    def start(
        self,
        signal_array,
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
        log_sigma_size,
        n_sds_above_mean_thresh,
        outlier_keep=False,
        artifact_keep=False,
        save_planes=False,
        plane_directory=None,
    ):
        """
        Start running the detection algorithm.

        This will spawn processes that carry out the detection algorithm,
        allowing code to continue executing elsewhere whilst work is being
        done. To block until finished and get the results call ``.finish()``.
        """
        n_processes = get_num_processes(min_free_cpu_cores=n_free_cpus)
        self.start_time = datetime.now()
        self.signal_array = signal_array

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

        if end_plane == -1:
            end_plane = len(signal_array)
        signal_array = signal_array[start_plane:end_plane]

        workers_queue = MultiprocessingQueue(maxsize=n_processes)
        # WARNING: needs to be AT LEAST ball_z_size
        self.mp_3d_filter_queue = MultiprocessingQueue(maxsize=ball_z_size)
        for _ in range(n_processes):
            # place holder for the queue to have the right size on first run
            workers_queue.put(None)

        if signal_array.ndim != 3:
            raise IOError("Input data must be 3D")

        setup_params = [
            signal_array[0, :, :],
            soma_diameter,
            ball_xy_size,
            ball_z_size,
            ball_overlap_fraction,
            start_plane,
        ]

        # Create 3D analysis filter
        self.mp3d_filter_output_queue = MultiprocessingQueue()
        self.mp_3d_filter = Mp3DFilter(
            self.mp_3d_filter_queue,
            self.mp3d_filter_output_queue,
            self.planes_done_queue,
            soma_diameter,
            setup_params=setup_params,
            soma_size_spread_factor=soma_spread_factor,
            planes_paths_range=signal_array,
            save_planes=save_planes,
            plane_directory=plane_directory,
            start_plane=start_plane,
            max_cluster_size=max_cluster_size,
            outlier_keep=outlier_keep,
            artifact_keep=artifact_keep,
        )

        # start 3D analysis (waits for planes in queue)
        self.bf_process = multiprocessing.Process(
            target=self.mp_3d_filter.process, args=()
        )
        # needs to be started before the loop
        self.bf_process.start()
        clipping_val, threshold_value = setup_tile_filtering(
            signal_array[0, :, :]
        )

        # Create 2D analysis filter
        mp_tile_processor = MpTileProcessor(
            workers_queue, self.mp_3d_filter_queue
        )
        prev_lock = Lock()

        # start 2D tile filter (output goes into queue for 3D analysis)
        # Creates a list of (running) processes for each 2D plane
        self.processes = []
        for plane_id, plane in enumerate(signal_array):
            workers_queue.get()
            # Create a new lock for this specific plane
            lock = Lock()
            lock.acquire()
            p = multiprocessing.Process(
                target=mp_tile_processor.process,
                args=(
                    plane_id,
                    np.array(plane),
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
            self.processes.append(p)
            p.start()

    @property
    def nplanes(self):
        """Number of planes being processed."""
        return len(self.signal_array)

    def join(self):
        """
        Get detection results.

        This will block execution until the results are ready.
        """
        # Wait for the final 2D filter process to finish
        self.processes[-1].join()
        # Tell 3D filter that there are no more planes left
        self.mp_3d_filter_queue.put((None, None, None))
        cells = self.mp3d_filter_output_queue.get()
        # Wait for 3D filter to finish
        self.bf_process.join()

        print(
            "Detection complete - all planes done in : {}".format(
                datetime.now() - self.start_time
            )
        )
        return cells


main = DetectRunner()
