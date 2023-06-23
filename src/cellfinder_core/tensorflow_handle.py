from functools import wraps
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Callable
from warnings import warn

# Handle tensorflow optional dependency
_TENSORFLOW_INSTALLED = True
_TF_VERSION = "0.0.0"
try:
    _TF_VERSION = version("tensorflow")
    import tensorflow as tf
except PackageNotFoundError:
    # Optional tensorflow dependency not installed
    warn(
        "cellfinder-core has been installed without tensorflow."
        "Certain functions will be unavailable."
        "See [FIXME] for full details"
    )
    _TENSORFLOW_INSTALLED = False
    # This will define the name tf even if tensorflow is not present.
    # This allows us to apply the decorator to our code,
    # avoiding large if-blocks within each function.
    tf = None


def tensorflow_required_function(fn_to_wrap: Callable) -> Any:
    """Decorator that marks functions as requiring the optional tensorflow
    dependency to run.

    Functions with this decorator applied will throw an error when they are
    executed and the tensorflow package is not available.
    Otherwise, the function will execute normally.
    """

    @wraps(fn_to_wrap)
    def wrapped_fn():
        if _TENSORFLOW_INSTALLED:
            fn_to_wrap()
        else:
            raise RuntimeError(
                f"[cellfinder-core].{fn_to_wrap.__name__}"
                "requires tensorflow, which is not installed"
            )

    return wrapped_fn
