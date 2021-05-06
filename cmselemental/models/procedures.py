from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydantic import Field, constr, validator

from ..extras import provenance_stamp
from .base import ProtoModel
from .common import (
    ComputeError,
    Provenance,
)

cmsschema_proc_input_default = "cmsschema_proc_input"
cmsschema_proc_output_default = "cmsschema_proc_output"

__all__ = ["ProcInput", "ProcOutput"]


class ProcInput(ProtoModel):
    id: Optional[str] = None
    hash_index: Optional[str] = None
    schema_name: Optional[
        constr(strip_whitespace=True, regex=cmsschema_proc_input_default)
    ] = Field(  # type: ignore
        cmsschema_proc_input_default,
        description=(
            f"The CMSSchema specification to which this model conforms. Explicitly fixed as {cmsschema_proc_input_default}."
        ),
    )
    schema_version: Optional[int] = Field(  # type: ignore
        0,
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


class ProcOutput(ProtoModel):
    proc_input: Optional[ProcInput] = None
    schema_name: Optional[
        constr(strip_whitespace=True, regex=cmsschema_proc_output_default)
    ] = Field(  # type: ignore
        cmsschema_proc_output_default,
        description=(
            f"The CMSSchema specification to which this model conforms. Explicitly fixed as {cmsschema_proc_output_default}."
        ),
    )
    schema_version: Optional[int] = Field(  # type: ignore
        0,
        description="The version number of ``schema_name`` to which this model conforms.",
    )
    stdout: Optional[str] = Field(
        None, description="The standard output of the program."
    )
    stderr: Optional[str] = Field(
        None, description="The standard error of the program."
    )
    warnings: Optional[str] = Field(
        None, description="Warning messages."
    )
    success: bool = Field(
        ...,
        description="The success of a given programs execution. If False, other fields may be blank.",
    )
    error: Optional[ComputeError] = Field(None, description=str(ComputeError.__doc__))
    provenance: Optional[Provenance] = Field(..., description=str(Provenance.__doc__)
    )
    extras: Optional[Dict[str, Any]] = Field(
        {}, description="Extra fields that are not part of the schema."
    )