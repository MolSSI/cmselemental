CMSElemental
====================
[//]: # (Badges)
[![CI](https://github.com/MolSSI/cmselemental/actions/workflows/CI.yaml/badge.svg)](https://github.com/MolSSI/cmselemental/actions/workflows/CI.yaml)
[![codecov](https://codecov.io/gh/MolSSI/cmslemental/branch/main/graph/badge.svg)](https://codecov.io/gh/MolSSI/cmslemental/branch/main)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/MolSSI/cmselemental.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MolSSI/cmselemental/context:python)

A python package which provides data models & tools for the Computational Molecular Sciences (CMS).

# Base Models
The most fundamental model is `ProtoModel`, a subclass of the [pydantic](https://pydantic-docs.helpmanual.io) `BaseModel`, which provides commonly used methods in CMS.
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
Routines for serializing to popular formats like JSON and YAML are available, with support for encoding Numpy arrays. 
```python
from cmselemental.util import serialize, deserialize

stringified = serialize(data, encodding="json", indent=4)
data = deserialize(stringified, encoding="json")
```
