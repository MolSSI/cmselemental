import pytest
import cmselemental
import numpy

using_msgpack = pytest.mark.skipif(
    cmselemental.util.which_import("msgpack", return_bool=True) is False,
    reason="Not detecting module msgpack. Install package if necessary and add to envvar PYTHONPATH",
)

using_pyyaml = pytest.mark.skipif(
    cmselemental.util.which_import("yaml", return_bool=True) is False,
    reason="Not detecting module pyyaml. Install package if necessary and add to envvar PYTHONPATH",
)


serialize_extensions = [
    "json",
    "json-ext",
    pytest.param("msgpack-ext", marks=using_msgpack),
    pytest.param("yaml", marks=using_pyyaml),
]


@pytest.mark.parametrize(
    "obj",
    [
        5,
        1.11111,
        "hello",
        "\u0394",
        numpy.random.rand(4),
        {"a": 5},
        {"a": 1.111111111111},
        {"a": "hello"},
        {
            "a": numpy.random.rand(4),
            "b": numpy.array(5.1111111),
            "c": numpy.array("hello"),
        },
        ["12345"],
        ["hello", "world"],
        [5, 123.234, "abcdé", "\u0394", "\U00000394"],
        [5, "B63", numpy.random.rand(4)],
        ["abcdé", {"a": numpy.random.rand(2), "b": numpy.random.rand(5)}],
        [
            numpy.array(3),
            numpy.arange(3, dtype=numpy.uint16),
            {"b": numpy.array(["a", "b"])},
        ],
    ],
)
@pytest.mark.parametrize("encoding", serialize_extensions)
def test_serialization(obj, encoding):
    new_obj = cmselemental.util.deserialize(
        cmselemental.util.serialize(obj, encoding=encoding), encoding=encoding
    )
    assert cmselemental.testing.compare_recursive(obj, new_obj)
