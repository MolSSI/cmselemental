from typing import Any, Dict, Optional
from pydantic import Field

from ..extras import provenance_stamp
from .base import ProtoModel
from .common import (
    ComputeError,
    Provenance,
)

__all__ = ["InputProc", "OutputProc"]


class InputProc(ProtoModel):
    id: Optional[str] = None
    hash_index: Optional[str] = None
    schema_name: str = Field(  # type: ignore
        ...,
        description=("The schema specification to which this model conforms."),
    )
    schema_version: int = Field(  # type: ignore
        ...,
        description="The version number of ``schema_name`` to which this model conforms.",
    )
    keywords: Optional[Dict[str, Any]] = Field(
        {}, description="Procedure specific keywords to be used."
    )
    provenance: Optional[Provenance] = Field(
        Provenance(**provenance_stamp(__name__)), description=str(Provenance.__doc__)
    )
    engine: Optional[str] = Field(
        None,
        description="Engine name to use in the procedure e.g. OpenMM.",
    )
    engine_version: Optional[str] = Field(
        None, description="Supported engine version. e.g. '>=3.4.0'."
    )
    extras: Optional[Dict[str, Any]] = Field(
        {}, description="Extra fields that are not part of the schema."
    )


class OutputProc(ProtoModel):
    proc_input: Optional[InputProc] = None
    schema_name: str = Field(  # type: ignore
        ...,
        description=("The schema specification to which this model conforms."),
    )
    schema_version: int = Field(  # type: ignore
        ...,
        description="The version number of ``schema_name`` to which this model conforms.",
    )
    stdout: Optional[str] = Field(
        None, description="The standard output of the program."
    )
    stderr: Optional[str] = Field(
        None, description="The standard error of the program."
    )
    warnings: Optional[str] = Field(None, description="Warning messages.")
    log: Optional[str] = Field(None, description="Logging info.")
    success: bool = Field(
        ...,
        description="The success of a given programs execution. If False, other fields may be blank.",
    )
    error: Optional[ComputeError] = Field(None, description=str(ComputeError.__doc__))
    provenance: Optional[Provenance] = Field(
        Provenance(**provenance_stamp(__name__)), description=str(Provenance.__doc__)
    )
    extras: Optional[Dict[str, Any]] = Field(
        {}, description="Extra fields that are not part of the schema."
    )
