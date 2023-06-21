from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("cellfinder-core")
except PackageNotFoundError:
    # Implying that the package we've just imported doesn't exist.
    # Worrying, but throw an error here in this case
    raise PackageNotFoundError(
        "cellfinder-core name package is not present, but you appear to be importing it?"
    )

__author__ = "Adam Tyson, Christian Niedworok, Charly Rousseau"
__license__ = "BSD-3-Clause"

import logging

logger = logging.getLogger("cellfinder_core")
