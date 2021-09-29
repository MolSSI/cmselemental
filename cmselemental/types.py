from typing import Any, Dict
import numpy

__all__ = ["Array"]


class TypedArray(numpy.ndarray):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            v = numpy.asarray(v, dtype=cls._dtype)
        except ValueError:
            raise ValueError("Could not cast {} to NumPy Array!".format(v))

        return v

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        dt = cls._dtype
        if dt is int or numpy.issubdtype(dt, numpy.integer):
            items = {"type": "number", "multipleOf": 1.0}
        elif dt is float or numpy.issubdtype(dt, numpy.floating):
            items = {"type": "number"}
        elif dt is str or numpy.issubdtype(dt, numpy.string_):
            items = {"type": "string"}
        elif dt is bool or numpy.issubdtype(dt, numpy.bool_):
            items = {"type": "boolean"}
        else:
            items = {"type": "array"}
        field_schema.update(type="array", items=items)


class ArrayMeta(type):
    def __getitem__(self, dtype):
        return type("Array", (TypedArray,), {"_dtype": dtype})


class Array(numpy.ndarray, metaclass=ArrayMeta):
    pass
