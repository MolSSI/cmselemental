from typing import TYPE_CHECKING, Any, Dict, Optional

from pydantic import Field

from .base import ProtoModel, cmsschema_draft

if TYPE_CHECKING:
    from pydantic.typing import ReprArgs

__all__ = ["Provenance", "ComputeError", "FailedOperation"]


class Provenance(ProtoModel):
    """Provenance information."""

    creator: str = Field(
        ...,
        description="The name of the program, library, or person who created the object.",
    )
    version: str = Field(
        "",
        description="The version of the creator, blank otherwise. This should be sortable by the very broad [PEP 440](https://www.python.org/dev/peps/pep-0440/).",
    )
    routine: str = Field(
        "",
        description="The name of the routine or function within the creator, blank otherwise.",
    )

    class Config(ProtoModel.Config):
        canonical_repr = True
        extra: str = "allow"

        def schema_extra(schema, model):
            schema["$schema"] = cmsschema_draft


class ComputeError(ProtoModel):
    """Complete description of the error from an unsuccessful program execution."""

    error_type: str = Field(  # type: ignore
        ...,  # Error enumeration not yet strict
        description="The type of error which was thrown. Restrict this field to short classifiers e.g. 'input_error'. Suggested classifiers: https://github.com/MolSSI/QCEngine/blob/master/qcengine/exceptions.py",
    )
    error_message: str = Field(  # type: ignore
        ...,
        description="Text associated with the thrown error. This is often the backtrace, but it can contain additional "
        "information as well.",
    )
    extras: Optional[Dict[str, Any]] = Field(  # type: ignore
        None,
        description="Additional information to bundle with the error.",
    )

    class Config:
        repr_style = ["error_type", "error_message"]

    def __repr_args__(self) -> "ReprArgs":
        return [("error_type", self.error_type), ("error_message", self.error_message)]


class FailedOperation(ProtoModel):
    """Record indicating that a given operation (program, procedure, etc.) has failed and containing the reason and input data which generated the failure."""

    id: str = Field(  # type: ignore
        None,
        description="A unique identifier which links this FailedOperation, often of the same Id of the operation "
        "should it have been successful. This will often be set programmatically by a database such as "
        "Fractal.",
    )
    input_data: Any = Field(  # type: ignore
        None,
        description="The input data which was passed in that generated this failure. This should be the complete "
        "input which when attempted to be run, caused the operation to fail.",
    )
    success: bool = Field(  # type: ignore
        False,
        description="A boolean indicator that the operation failed consistent with the model of successful operations. "
        "Should always be False. Allows programmatic assessment of all operations regardless of if they failed or "
        "succeeded",
    )
    error: ComputeError = Field(  # type: ignore
        ...,
        description="A container which has details of the error that failed this operation. See the "
        ":class:`ComputeError` for more details.",
    )
    extras: Optional[Dict[str, Any]] = Field(  # type: ignore
        None,
        description="Additional information to bundle with the failed operation. Details which pertain specifically "
        "to a thrown error should be contained in the `error` field. See :class:`ComputeError` for details.",
    )

    def __repr_args__(self) -> "ReprArgs":
        return [("error", self.error)]
