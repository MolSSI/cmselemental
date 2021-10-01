from typing import Dict, Any
import numpy
import json

try:
    import h5py
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "Hdf5 functionality requires h5py. Solve by: pip install h5py."
    )

import collections
from contextlib import redirect_stdout

encoding = "utf-8"
str_encode = h5py.string_dtype(encoding=encoding)

numpy_h5py_dtypes = {
    "U": str_encode,
    "i": "int64",
    "f": "float64",
}


def h5tojson(h5filename: str, jsonfilename: str, mode: str = "w"):
    from h5json import Hdf5db
    from h5json import hdf5dtype
    from h5json.h5tojson.h5tojson import getTempFileName, DumpJson

    options = collections.namedtuple("options", ["D", "d", "filename"])(
        D=None, d=None, filename=h5filename
    )

    with Hdf5db(
        options.filename, dbFilePath=getTempFileName(), readonly=True, app_logger=None
    ) as db:
        dumper = DumpJson(db, app_logger=None, options=options)
        with open(jsonfilename, mode) as fileobj:
            with redirect_stdout(fileobj):
                dumper.dumpFile()


def jsontoh5(jsonfilename: str, h5filename: str):
    from h5json import Hdf5db
    from h5json.jsontoh5.jsontoh5 import Writeh5

    with open(jsonfilename, "r") as fileobj:
        stringified = json.load(fileobj)

    if "root" not in stringified:
        raise Exception("no root key in input file")
    root_uuid = stringified["root"]

    # create the file, will raise IOError if there's a problem
    Hdf5db.createHDF5File(h5filename)

    with Hdf5db(
        h5filename, root_uuid=root_uuid, update_timestamps=False, app_logger=None
    ) as db:
        h5writer = Writeh5(db, stringified)
        h5writer.writeFile()

    # open with h5py and remove the _db_ group
    # Note: this will delete any anonymous (un-linked) objects
    with h5py.File(h5filename, "a") as fileobj:
        if "__db__" in fileobj:
            del fileobj["__db__"]


def write_file(filename: str, data: Dict[str, Any], mode: str = "w", **kwargs):
    with h5py.File(filename, mode) as hdfobj:
        write_dict(hdfobj, data)


def read_file(filename: str, **kwargs) -> Dict[str, Any]:
    with h5py.File(filename, "r") as hdfobj:
        return read_dict(hdfobj, **kwargs)


def _get_dtype(data):
    """Returns data type for hdf5 datasets."""
    if isinstance(data, str):
        return str_encode
    elif isinstance(data, float):
        return "float64"
    elif isinstance(data, int):
        return "int64"
    elif isinstance(data, numpy.ndarray):
        dtype = numpy_h5py_dtypes.get(data.dtype.kind, None)
        if dtype is None and data.dtype.kind == "V":
            dtype = [
                (f"f{i}", numpy_h5py_dtypes.get(data.dtype[i].kind))
                for i in range(len(data.dtype))
            ]
            if None in dtype:
                raise NotImplementedError(f"Data type {data.dtype} not supported.")
        return dtype
    elif isinstance(data, (list, tuple)):
        if isinstance(data[0], tuple):
            return ",".join([_get_dtype(item) for item in data[0]])
        elif isinstance(data[0], list):
            raise NotImplementedError("List of lists not supported.")
        else:
            assert all(
                isinstance(item, int) for item in data
            ), "Only homogenous arrays supported."  # keep this? Can degrade performance
            return _get_dtype(data[0])  # assume homogenous list/tuple
    else:
        raise NotImplementedError(f"Data type {type(data)} not supported.")


def _wrap_homogenous_array(data):
    dtype = _get_dtype(data)
    return numpy.array(data, dtype=dtype)


def write_dict(
    hdfobj: "h5py._hl.files.File",
    data: Dict[str, Any],
    units_metadata: bool = True,
    **kwargs,
) -> None:
    """
    Writes a python dictionary to an HDF5 file. By default, any attribute that ends in '_units' is stored
    as metadata in the hdf5 file. Can be turned off by setting units_metadata=False.

    Parameters
    ----------
    hdfobj: h5py._hl.files.File
        The hdf file object to write data to.
    data: Dict[str, Any]
        The dictionary of data to write.
    units_metadata: bool
        Treat any key ending in '_units' as metadata.
    **kwargs: Optional[Dict[str, Any]], optional
        Any additional keywords to pass to the constructor.

    """
    for key, val in data.items():
        if isinstance(val, dict):
            grp = hdfobj.create_group(key)
            write_dict(grp, val)
        elif units_metadata:
            if not key.endswith("_units"):  # Deal with units later
                val = _wrap_homogenous_array(val)
                hdfobj.create_dataset(name=key, data=val)

    # Save units as metadata
    if units_metadata:
        for key, val in data.items():
            if key.endswith("_units"):
                array_name, _ = key.split("_units")
                hdfobj[array_name].attrs[key] = val


def read_dict(hdfobj: "h5py._hl.files.File", **kwargs) -> Dict[str, Any]:
    """
    Converts an hdf file object to a python dictionary.

    Parameters
    ----------
    hdfobj: h5py._hl.files.File
        The hdf file object to read data from.
    **kwargs: Optional[Dict[str, Any]], optional
        Any additional keywords to pass to the constructor.
    Returns
    -------
    Dict[str, Any]
        A python dictionary that stores HDF5 data.

    """

    data = {}
    for key in hdfobj.keys():
        if isinstance(hdfobj[key], h5py.Group):
            data[key] = read_dict(hdfobj[key])
        elif isinstance(hdfobj[key], h5py.Dataset):
            data[key] = hdfobj[key][()]

            # For MMEl, store key_units as metadata
            if key + "_units" in hdfobj[key].attrs.keys():
                data[key + "_units"] = hdfobj[key].attrs[key + "_units"]

            if isinstance(data[key], bytes):
                data[key] = data[key].decode()
            elif isinstance(data[key], numpy.ndarray):
                if data[key].dtype.char == "O":
                    if len(data[key].dtype) < 2:  # homogenous array
                        data[key] = data[key].astype("U")  # unicode default in py3
                    else:
                        pass  # do nothing with homogenous array
        else:
            raise ValueError(f"Data type not understood: {hdfobj[key]}")
    return data
