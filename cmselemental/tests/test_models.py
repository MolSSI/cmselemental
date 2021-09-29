import pytest

from cmselemental.models import (
    ComputeError,
    FailedOperation,
    InputProc,
    OutputProc,
    ProtoModel,
    Provenance,
)


@pytest.mark.skip(reason="no way of currently testing this")
def test_repr_provenance(request):

    prov = Provenance(creator="cmsel", version="v0.3.2")
    drop_qcsk(prov, request.node.name)

    assert "cmsel" in str(prov)
    assert "cmsel" in repr(prov)


def test_repr_compute_error():
    ce = ComputeError(error_type="random_error", error_message="this is bad")

    assert "random_error" in str(ce)
    assert "random_error" in repr(ce)


def test_repr_failed_op():
    fail_op = FailedOperation(
        error=ComputeError(error_type="random_error", error_message="this is bad")
    )
    assert (
        str(fail_op)
        == """FailedOperation(error=ComputeError(error_type='random_error', error_message='this is bad'))"""
    )


def test_repr_proc_input():

    opt = InputProc(
        **{
            "schema_name": "some_schema",
            "schema_version": 2,
            "id": "some_id",
            "engine": "some_engine",
            "engine_version": "1.0.0",
        }
    )

    assert "provenance" in str(opt)
    assert "schema_name" in str(opt)
    assert "schema_version" in str(opt)


def test_repr_proc_output():

    opt = OutputProc(
        **{
            "schema_name": "my_schema",
            "schema_version": 1,
            "stdout": "stdout",
            "stderr": "stderr",
            "success": False,
        }
    )

    assert "provenance" in str(opt)
    assert "schema_name" in str(opt)
    assert "schema_version" in str(opt)


def test_model_custom_repr():
    class Model(ProtoModel):
        a: int

        def __repr__(self) -> str:
            return "Hello world!"

    m = Model(a=5)
    assert repr(m) == "Hello world!"
    assert "Model(" in str(m)

    class Model2(ProtoModel):
        a: int

        def __str__(self) -> str:
            return "Hello world!"

    m = Model2(a=5)
    assert "Model2(" in repr(m)
    assert str(m) == "Hello world!"
