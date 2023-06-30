import shutil
from pathlib import Path

from brainglobe_utils.general.system import get_num_processes

from cellfinder_core.tools.prep import (
    prep_classification,
    prep_models,
    prep_tensorflow,
    prep_training,
)


class PrepModels:
    param_names = ["model_name"]
    params = ["resnet50_tv", "resnet50_all"]

    # increase default timeout to allow for download
    timeout = 480

    # Q for review:
    # - should I run only one sample ('number'=1)?
    #   'number' as defined here:
    #    https://asv.readthedocs.io/en/stable/writing_benchmarks.html#timing
    # - how are prep_classification and prep_training different?

    def setup(self, model_name):
        self.n_free_cpus = 2  # TODO: should this be parametrised??
        self.n_processes = get_num_processes(
            min_free_cpu_cores=self.n_free_cpus
        )
        self.trained_model = None
        self.model_weights = None
        self.install_path = Path.home() / ".cellfinder"
        self.model_name = model_name

        # remove .cellfinder dir if it exists already
        shutil.rmtree(self.install_path, ignore_errors=True)
        # Q for review:
        # - is this safe?
        # - should I check if install_path is the expected path?

    def teardown(self, model_name):
        # remove .cellfinder dir after benchmarks
        shutil.rmtree(self.install_path)

    def time_prep_models(self, model_name):
        prep_models(
            self.trained_model,
            self.model_weights,
            self.install_path,
            model_name,
        )

    def time_prep_classification(self, model_name):
        prep_classification(
            self.trained_model,
            self.model_weights,
            self.install_path,
            model_name,
            self.n_free_cpus,
        )

    def time_prep_training(self, model_name):
        prep_training(
            self.n_free_cpus,
            self.trained_model,
            self.model_weights,
            self.install_path,
            model_name,
        )


class PrepTF:
    def setup(self):
        n_free_cpus = 2  # TODO: should we parametrise this?
        self.n_processes = get_num_processes(min_free_cpu_cores=n_free_cpus)

    def time_prep_tensorflow(self):
        prep_tensorflow(self.n_processes)
