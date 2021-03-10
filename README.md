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

# Serialization/deserialization
```python
from cmselemental.util import serialize, deserialize


stringified = serialize(data, encodding="json", indent=4)
data = deserialize(stringified, encoding="json")
```
