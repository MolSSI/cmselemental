from typing import Callable
import functools


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


def require(pkg_name: str) -> Callable:
    """Returns a decorator function, ensures pkg_name is available and can be imported.
    Parameters
    ----------
    pkg_name: str
        Name of the package required.
    Returns
    -------
    deco_require: Callable
        Decorator function
    Raises
    ------
    ModuleNotFoundError
        When pkg_name is not found.
    Example:
    --------
    @require("some_pkg")
    def foo(...):
        ...
    """

    def deco_require(func):
        @functools.wraps(func)
        def inner_func(*args, **kwargs):
            if not which_import(pkg_name, return_bool=True):
                raise ModuleNotFoundError(f"Could not find or import {pkg_name}.")
            return func(*args, **kwargs)

        return inner_func

    return deco_require
