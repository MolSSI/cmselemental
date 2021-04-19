import re

from . import _version

__all__ = ["get_information", "provenance_stamp"]

versions = _version.get_versions()

__info = {"version": versions["version"], "git_revision": versions["full-revisionid"]}


def get_information(key):
    """
    Obtains a variety of runtime information about QCEngine.
    """
    key = key.lower()
    if key not in __info:
        raise KeyError("Information key '{}' not understood.".format(key))

    return __info[key]


def provenance_stamp(creator, routine):
    """Return dictionary satisfying QCSchema,
    https://github.com/MolSSI/QCSchema/blob/master/qcschema/dev/definitions.py#L23-L41
    with QCEngine's credentials for creator and version. The
    generating routine's name is passed in through `routine`.
    """
    return {
        "creator": creator,
        "version": get_information("version"),
        "routine": routine,
    }
