import SleepDataPipeline
import h5py
import argparse

def main():
    d = {
        'ABC': SleepDataPipeline.Abc,
        'CCSHS': SleepDataPipeline.Ccshs,
        'CFS': SleepDataPipeline.Cfs,
        'CHAT': SleepDataPipeline.Chat,
        'HPAP': SleepDataPipeline.Homepap,
        'MESA': SleepDataPipeline.Mesa,
        'MROS': SleepDataPipeline.Mros,
        'SHHS': SleepDataPipeline.Shhs,
        'SOF': SleepDataPipeline.Sof,
        'SEDF-SC': SleepDataPipeline.Sedf_SC_Physionet,
        'SEDF-ST': SleepDataPipeline.Sedf_ST_Physionet,
        'MASS-C1': SleepDataPipeline.Mass_C1,
        'MASS-C3': SleepDataPipeline.Mass_C3,
        'ISRUC-SG1': SleepDataPipeline.Isruc_SG1,
        'ISRUC-SG2': SleepDataPipeline.Isruc_SG2,
        'ISRUC-SG3': SleepDataPipeline.Isruc_SG3,
        'DOD-O': SleepDataPipeline.Dod_o,
        'DOD-H': SleepDataPipeline.Dod_h,
        'DCSM': SleepDataPipeline.Dcsm,
        'PHYS': SleepDataPipeline.Phys,
        'SVUH': SleepDataPipeline.Svuh
    }

    parser = argparse.ArgumentParser(add_help=False)
    
    parser.add_argument("--dataset_name", type=str)
    parser.add_argument("--num_sub", type=int)
    args = parser.parse_args()

    dataset_name = args.dataset_name
    num_sub = args.num_sub
    
    if (num_sub == 0):
        num_sub = None

    source = f"/users/strmjesp/mnt/{dataset_name}/"
    target = "/users/strmjesp/mnt/transformed"

    object = d[dataset_name](num_sub, source, target)
if __name__ == "__main__":
    main() 
