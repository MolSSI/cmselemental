CMSElemental
====================
[//]: # (Badges)
[![CI](https://github.com/MolSSI/cmselemental/actions/workflows/CI.yaml/badge.svg)](https://github.com/MolSSI/cmselemental/actions/workflows/CI.yaml)
[![codecov](https://codecov.io/gh/MolSSI/cmslemental/branch/main/graph/badge.svg)](https://codecov.io/gh/MolSSI/cmslemental/branch/main)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/MolSSI/cmselemental.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MolSSI/cmselemental/context:python)

A python package which provides data models & tools for the Computational Molecular Sciences (CMS).
CMSElemental provides:

- Pydantic models:
  - Base models: primarily `ProtoModel`, a subclass of the [pydantic](https://pydantic-docs.helpmanual.io) `BaseModel`, which provides commonly used methods in CMS for data parsing, validation, and serialization.
  - Procedure models: for storing generic intput/output data associated with CMS procedures.
  - Common models: a miscellaneous collection of frequently used models in CMS.

- File I/O methods:
  - JSON: support for JSON schema ([draft-07](https://json-schema.org/specification-links.html#draft-7)).
  - YAML: support for YAML [1.1](https://yaml.org/spec/1.1) (PyYAML) and [1.2](https://yaml.org/spec/1.2) (ruamel.yaml).
  - MessagePack: support for the msgpack data format.
  - HDF5: support for [HDF5](https://support.hdfgroup.org/HDF5/doc1.6/UG/03_Model.html) file schema and the [HDF5-JSON](https://github.com/HDFGroup/hdf5-json) specification.
