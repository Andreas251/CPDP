# SleepDataPipeline

This repository can be used to transform raw PSG data to a standardized HDF5 file.

For example, ABC can be transformed by executing:

d = SleepDataPipeline.Abc(None, raw data directory, target directory)

"None" can be changed to a number, indicating how many number of subjects is needed, if one needs a proof-of-concept or test dataset.