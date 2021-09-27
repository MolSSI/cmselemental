# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2021-07-19

- Initial release of cmselemental

## [0.2.0] - 2021-XX-XX

- ([`:pr:4`])(https://github.com/MolSSI/cmselemental/pull/4) Add serialization support for YAML
- ([`:pr:5`])(https://github.com/MolSSI/cmselemental/pull/5) Add support for writing, reading. and converting `ProtoModel` to/from HDF5 based on the [HDF5/JSON](https://hdf5-json.readthedocs.io) specification. Add `$schema` keyword to the generated `ProtoModel` schema.
- ([`:pr:6`])(https://github.com/MolSSI/cmselemental/pull/6) Add support for storing logging data to ProcOutput and transform `__repr__` and `__str__` to instant methods in ProtoModel.
- ([`:pr:7`])(https://github.com/MolSSI/cmselemental/pull/7) Add a new (classproperty) method to `ProtoModel`: `default_schema_name`.
- ([`:pr:8`])(https://github.com/MolSSI/cmselemental/pull/8) Create a decorators (util.decorators) submodule. Remove util.files submodules.
