# SleepDataPipeline

This repository can be used to transform most PSG datasets to a standardized HDF5 file.

Configuration is specified in conf.yaml - the below example transforms EESM:

parameters:
 scale_and_clip: True
 output_sample_rate: 128
target_path:
 "/my/target/output/path"
datasets:
 - name: Eesm
   path: "/path/to/eesm/data/"

Datasets is a list, so multiple datasets can be transformed in the same execution.


# Available datasets
Available datasets and their correct datapath:

ABC
