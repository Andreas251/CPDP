
import h5py
import os
import sys
import argparse

def count_records(base, files):
    
    #sets = os.listdir(base)
    
    for s in files:
        with h5py.File(f"{base}/{s}.hdf5", "r") as f:
            subjects = f.keys()
            
            tot_records = 0
            for sub in subjects:
                records = f[sub]
                tot_records += len(records)
            
            print(f"Number of sujbects for {s}: {len(subjects)}")    
            print(f"Number of records for {s}: {tot_records}")

def main():
    # Argument = Base path to HDF5 files
    
    CLI=argparse.ArgumentParser()
    
    CLI.add_argument(
      "--basepath",
      type=str
    )
    
    CLI.add_argument(
      "--files",
      nargs="*",
      type=str,  # any type/callable can be used here
      default=[],
    )
    
    args = CLI.parse_args()

    base = args.basepath
    files = args.files
    count_records(base, files)


if __name__ == "__main__":
    main()
