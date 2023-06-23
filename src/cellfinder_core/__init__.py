from importlib.metadata import PackageNotFoundError, version
from warnings import warn

# Handle tensorflow optional dependency
_TENSORFLOW_INSTALLED = True
_TF_VERSION = "0.0.0"
try:
    _TF_VERSION = version("tensorflow")
except PackageNotFoundError as e:
    # Optional tensorflow dependency not installed
    warn(
        "cellfinder-core has been installed without tensorflow. Certain functions will be unavailable. See [FIXME] for full details"
    )
    _TENSORFLOW_INSTALLED = False

# Handle versioning
try:
    __version__ = version("cellfinder-core")
except PackageNotFoundError as e:
    raise PackageNotFoundError("cellfinder-core package not installed") from e

__author__ = "Adam Tyson, Christian Niedworok, Charly Rousseau"
__license__ = "BSD-3-Clause"

import logging

logger = logging.getLogger("cellfinder_core")
