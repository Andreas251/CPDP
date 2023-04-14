
import h5py
import os
import sys

def count_records(base):
    
    sets = os.listdir(base)
    
    for s in sets:
        with h5py.File(f"{base}/{s}", "r") as f:
            subjects = f.keys()

            tot_records = 0
            for sub in subjects:
                records = f[sub]
                tot_records += len(records)
                
            print(f"Number of records for {s}: {tot_records}")

def main():
    # Argument = Base path to HDF5 files
    base = sys.argv[1]
    
    count_records(base)


if __name__ == "__main__":
    main()
