# Base Models
```python
from cmselemental.models import ProtoModel


class Model(ProtoModel):
    ...

obj = Model(...)
is_same = obj.compare(other_obj)
stringified = obj.json()
data = obj.dict()
```
```python
from cmselemental.models import ProgramHarness


class GenericComponent(ProgramHarness):

    @classmethod
    def input(cls):
        return Model

    @classmethod
    def output(cls):
        return Model
    
    ...
```

# Serialization/deserialization
```python
from cmselemental.util import serialize, deserialize


stringified = serialize(data, encodding="json", indent=4)
data = deserialize(stringified, encoding="json")
```

# Program execution
```python
from cmselemental.util.common import execute, temporary_directory
from cmselemental.util.importing import which


with temporary_directory(parent=parent, suffix="_psi_scratch") as tmpdir:
 
    success, output = execute(
        [which("psi4"), "--scratch", tmpdir, "--json", "data.json"],
        {"data.json": json.dumps(input_data)},
        ["data.json"],
        scratch_directory=tmpdir,
    )
```
