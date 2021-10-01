import pytest
import numpy
import cmselemental
from pathlib import Path


using_h5py = pytest.mark.skipif(
    cmselemental.util.which_import("h5py", return_bool=True) is False,
    reason="Not detecting module h5py. Install package if necessary and add to envvar PYTHONPATH",
)


@using_h5py
@pytest.mark.parametrize(
    "obj",
    [
        {
            "a": numpy.random.rand(4),
            "b": numpy.array(5.1111111),
            "c": numpy.array("hello"),
            "abcdé": {"a": numpy.random.rand(2), "b": numpy.random.rand(5)},
            "nested": [(1, 0), (0, 1), (2, 2)],
        },
        {
            "a": numpy.array([(0, 1, 2), (2, 3, 4)], dtype="i8,i8,i8"),
            "b": numpy.array([("ALA", 1.0, 2.0), ("FF", 3.0, 4.0)], dtype="U3,f8,f8"),
        },
    ],
)
def test_write(obj):
    from cmselemental.util.hdf import write_file

    path_to_file = Path("filename.h5")
    write_file(path_to_file.name, data=obj)
    assert path_to_file.is_file()
    path_to_file.unlink()
