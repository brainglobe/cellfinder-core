import shutil
from pathlib import Path

# NOTE: imlib to be replaced by brainglobe_utils
from imlib.general.system import get_num_processes

from cellfinder_core.tools.prep import (
    prep_classification,
    prep_models,
    prep_tensorflow,
    prep_training,
)


class Prep:
    # common params?
    # rounds = 2  # default
    # repeat = 1  # default if rounds!= 1
    # ---> (min_repeat, max_repeat, max_time) = (1, 5, 10.0)
    # number = 1  # run only once per repeat?

    # common setup
    def setup(self):
        # print('setup')

        # TODO: how is n_free_cpus and n_process diff?
        # n_processes: n of CPUs to use?
        # n_free_cpus: n of CPUs to leave free in the machine?
        # Determine how many CPU cores to use, based on a minimum number
        # of cpu cores
        # to leave free, and an optional max number of processes.
        self.n_free_cpus = 2  # should this be parametrised??
        self.n_processes = get_num_processes(
            min_free_cpu_cores=self.n_free_cpus
        )
        self.trained_model = None
        self.model_weights = None
        self.install_path = Path.home() / ".cellfinder"  # default
        self.model_name = "resnet50_tv"  # resnet50_all

    def teardown(self):
        # pass

        # ------------------
        # TODO: not sure why the benchmark is timing out with this teardown?
        # remove everything in temp dir?
        # Q for review: is this safe?
        shutil.rmtree(self.install_path)
        # print('teardown')
        # ------------------

        # print([f for f in Path(self.install_path).glob("*")])

        # for f in Path(self.install_path).glob("*"):
        #     if f.is_dir():
        #         shutil.rmtree(f,)
        # return
        # #     print(f)
        #     f.unlink(missing_ok=True)
        # Path(self.install_path).rmdir()

    def time_prep_tensorfow(self):
        prep_tensorflow(self.n_processes)

    def time_prep_models(self):
        # downloads model weights to .cellfinder dir
        # -should I remove the files after each rep so that it is comparable?
        # (overwriting may not be the same as writing from scratch?)
        prep_models(
            self.trained_model,
            self.model_weights,
            self.install_path,
            self.model_name,
        )

    def time_prep_classification(self):
        prep_classification(
            self.trained_model,
            self.model_weights,
            self.install_path,
            self.model_name,
            self.n_free_cpus,
        )

    def time_prep_training(self):
        prep_training(
            self.n_free_cpus,
            self.trained_model,
            self.model_weights,
            self.install_path,
            self.model_name,
        )
