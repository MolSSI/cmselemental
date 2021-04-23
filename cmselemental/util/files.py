import uuid
from pathlib import Path


def random_file(suffix="", *, path=".", unique=True):
    """Returns a random file name generated from a universally
    unique identifier (UUID).

    Parameters
    ----------
    suffix: str
        Filename suffix
    path: str
        Path to filename
    unique: bool
        Ensures filename does not exist on disk
    Return
    ------
    filename: str
        Absolute filename path
    """
    fname = str(uuid.uuid4()) + suffix
    fpath = Path(fname)

    if path:
        fpath = Path(path) / fpath

    if unique:
        if fpath.is_file():
            return random_file(suffix, path=path, unique=unique)

    return str(fpath.absolute())
