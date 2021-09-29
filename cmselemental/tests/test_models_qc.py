import pytest
import cmselemental

qcel_found = cmselemental.util.importing.which_import("qcelemental")


@pytest.mark.skipif(not qcel_found, reason="qcelemental not installed")
def test_optim_qcel():
    from qcelemental.models.procedures import (
        OptimizationProtocols,
        QCInputSpecification,
    )
    from qcelemental.models import Molecule

    class OptimizationInput(cmselemental.models.InputProc):

        schema_name: str = "qcschema"
        schema_version: int = 2
        protocols: OptimizationProtocols = OptimizationProtocols()
        input_specification: QCInputSpecification = ...
        initial_molecule: Molecule = ...

        def __repr_args__(self) -> "ReprArgs":
            return [
                ("model", self.input_specification.model.dict()),
                ("molecule_hash", self.initial_molecule.get_hash()[:7]),
            ]

    opt = OptimizationInput(
        **{
            "input_specification": {"driver": "gradient", "model": {"method": "UFF"}},
            "initial_molecule": {"symbols": ["He"], "geometry": [0, 0, 0]},
        }
    )

    assert "molecule_hash" in str(opt)
    assert "molecule_hash" in repr(opt)
