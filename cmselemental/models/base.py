import json
from pathlib import Path
from typing import Any, Dict, Optional, Set, Union

import numpy
from pydantic import BaseModel, BaseSettings

from ..testing import compare_recursive
from ..util import deserialize, serialize, yaml_import
from ..util.autodocs import AutoPydanticDocGenerator
from ..util.decorators import classproperty

cmsschema_draft = "http://json-schema.org/draft-07/schema#"

__all__ = ["ProtoModel", "AutodocBaseSettings"]


class ProtoModel(BaseModel):
    class Config:
        allow_mutation: bool = False
        extra: str = "forbid"
        json_encoders: Dict[str, Any] = {numpy.ndarray: lambda v: v.flatten().tolist()}
        serialize_default_excludes: Set = set()
        serialize_skip_defaults: bool = False
        force_skip_defaults: bool = False

        def schema_extra(schema, model):
            # below addresses the draft issue until https://github.com/samuelcolvin/pydantic/issues/1478 .
            schema["$schema"] = cmsschema_draft

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.__doc__ = AutoPydanticDocGenerator(cls, always_apply=True)

    def __repr__(self):
        return f'{self.__repr_name__()}({self.__repr_str__(", ")})'

    def __str__(self):
        return f'{self.__repr_name__()}({self.__repr_str__(", ")})'

    @classproperty
    def default_schema_name(cls) -> Union[str, None]:
        """Returns default schema name if found."""
        try:
            return cls.schema()["properties"]["schema_name"]["default"]
        except Exception:
            return None

    @classmethod
    def parse_raw(cls, data: Union[bytes, str], *, encoding: str = None) -> "ProtoModel":  # type: ignore
        """
        Parses raw string or bytes into a Model object.
        Parameters
        ----------
        data : Union[bytes, str]
            A serialized data blob to be deserialized into a Model.
        encoding : str, optional
            The type of the serialized array, available types are: {'json', 'json-ext', 'msgpack-ext', 'pickle'}
        Returns
        -------
        Model
            The requested model from a serialized format.
        """

        if encoding is None:
            if isinstance(data, str):
                encoding = "json"  # Choose JSON over YAML by default
            elif isinstance(data, bytes):
                encoding = "msgpack-ext"
            else:
                raise TypeError(
                    "Input is neither str nor bytes, please specify an encoding."
                )

        if encoding.endswith(("json", "javascript", "pickle")):
            return super().parse_raw(data, content_type=encoding)
        elif encoding in ["msgpack-ext", "json-ext", "yaml"]:
            obj = deserialize(data, encoding)
        else:
            raise TypeError(f"Content type '{encoding}' not understood.")

        return cls.parse_obj(obj)

    @classmethod
    def parse_file(cls, path: Union[str, Path], *, encoding: str = None) -> "ProtoModel":  # type: ignore
        """Parses a file into a Model object.
        Parameters
        ----------
        path : Union[str, Path]
            The path to the file.
        encoding : str, optional
            The type of the files, available types are: {'json', 'msgpack', 'pickle', 'hdf5'}. Attempts to
            automatically infer the file type from the file extension if None.
        Returns
        -------
        Model
            The requested model from a file format.
        """
        path = Path(path)

        if encoding is None:
            if path.suffix in [".json", ".js"]:
                encoding = "json"
            elif path.suffix in [".yaml", ".yml"]:
                encoding = "yaml"
            elif path.suffix in [".msgpack"]:
                encoding = "msgpack-ext"
            elif path.suffix in [".pickle"]:
                encoding = "pickle"
            elif path.suffix in [".yaml", ".yml"]:
                encoding = "yaml"
            elif path.suffix in [".hdf5", ".h5"]:
                encoding = "hdf5"
            else:
                raise TypeError(
                    "Could not infer `encoding`, please provide a `encoding` for this file."
                )
        if encoding == "yaml":
            return cls.parse_raw(path.read_text(), encoding=encoding)
        elif encoding in ("hdf5", "h5"):
            from ..util import hdf

            return cls.parse_obj(hdf.read_file(path))
        return cls.parse_raw(path.read_bytes(), encoding=encoding)

    def write_file(
        self,
        path: Union[str, Path],
        *,
        encoding: str = None,
        mode: str = "w",
        **kwargs: Optional[Dict[str, Any]],
    ):
        """Write a Model to an output file.
        Parameters
        ----------
        path : Union[str, Path]
            The path to the file.
        encoding : str, optional
            The type of the files, available types are: {'json', 'msgpack', 'pickle', 'hdf5'}. Attempts to
            automatically infer the file type from the file extension if None.
        mode : str, optional
            An optional string that specifies the mode in which the file is written. Overwrites existing
            file by default (mode='w'). For appending to existing file, set mode='a'.
        **kwargs: Dict[str, Any], optional
            Additional keyword arguments passed to self.dict(), allows which fields to include, exclude, etc.
        """
        encoding = encoding or Path(path).suffix[1:]

        if encoding in ["json", "js", "yaml", "yml"]:
            stringified = self.serialize(encoding=encoding, **kwargs)
            with open(path, mode) as fp:
                fp.write(stringified)
        elif encoding in ["hdf5", "h5"]:
            from ..util import hdf

            hdf.write_file(path, data=self.dict(**kwargs), mode=mode)

    def dict(
        self, *, ser_kwargs: Dict[str, Any] = {}, **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Returns object fields as a dictionary.
        Parameters
        ----------
        ser_kwargs: Optional[Dict[str, Any]]
            Additional keyword arguments to pass to serialize.
        **kwargs: Optional[Dict[str, Any]]
            Additional keyword arguments, allow which fields to include, exclude, etc.
        Returns
        -------
        Dict[str, Any]
            Fields as a dictionary.
        """
        encoding = kwargs.pop("encoding", None)

        kwargs["exclude"] = (
            kwargs.get("exclude", None) or set()
        ) | self.__config__.serialize_default_excludes  # type: ignore
        kwargs.setdefault("exclude_unset", self.__config__.serialize_skip_defaults)  # type: ignore
        if self.__config__.force_skip_defaults:  # type: ignore
            kwargs["exclude_unset"] = True

        data = super().dict(**kwargs)

        if encoding is None:
            return data
        elif encoding == "json":
            return json.loads(serialize(data, encoding=encoding, **ser_kwargs))
        elif encoding == "yaml":
            yaml = yaml_import(raise_error=True)
            return yaml.safe_load(serialize(data, encoding=encoding, **ser_kwargs))
        else:
            raise KeyError(
                f"Unknown encoding type '{encoding}', valid encoding types: 'json', 'yaml'."
            )

    def serialize(
        self,
        encoding: str,
        *,
        include: Optional[Set[str]] = None,
        exclude: Optional[Set[str]] = None,
        exclude_unset: Optional[bool] = None,
        exclude_defaults: Optional[bool] = None,
        exclude_none: Optional[bool] = None,
        **kwargs: Optional[Dict[str, Any]],
    ) -> Union[bytes, str]:
        """Generates a serialized representation of the model
        Parameters
        ----------
        encoding : str
            The serialization type, available types are: {'json', 'json-ext', 'msgpack-ext'}
        include : Optional[Set[str]], optional
            Fields to be included in the serialization.
        exclude : Optional[Set[str]], optional
            Fields to be excluded in the serialization.
        exclude_unset : Optional[bool], optional
            If True, skips fields that have default values provided.
        exclude_defaults: Optional[bool], optional
            If True, skips fields that have set or defaulted values equal to the default.
        exclude_none: Optional[bool], optional
            If True, skips fields that have value ``None``.
         **kwargs: Optional[Dict[str, Any]]
            Additional keyword arguments to pass to serialize.
        Returns
        -------
        Union[bytes, str]
            The serialized model.
        """

        fdargs = {}
        if include:
            fdargs["include"] = include
        if exclude:
            fdargs["exclude"] = exclude
        if exclude_unset:
            fdargs["exclude_unset"] = exclude_unset
        if exclude_defaults:
            fdargs["exclude_defaults"] = exclude_defaults
        if exclude_none:
            fdargs["exclude_none"] = exclude_none

        data = self.dict(**fdargs)

        if encoding == "js":
            encoding = "json"
        elif encoding == "yml":
            encoding = "yaml"

        return serialize(data, encoding=encoding, **kwargs)

    def json(self, **kwargs):
        # Alias JSON here from BaseModel to reflect dict changes
        return self.serialize("json", **kwargs)

    def yaml(self, **kwargs):
        return self.serialize("yaml", **kwargs)

    def compare(self, other: Union["ProtoModel", BaseModel], **kwargs) -> bool:
        """Compares the current object to the provided object recursively.
        Parameters
        ----------
        other : Model
            The model to compare to.
        **kwargs
            Additional kwargs to pass.
        Returns
        -------
        bool
            True if the objects match.
        """
        return compare_recursive(self, other, **kwargs)


class AutodocBaseSettings(BaseSettings):
    def __init_subclass__(cls) -> None:
        cls.__doc__ = AutoPydanticDocGenerator(cls, always_apply=True)
