import h5py
from sklearn.model_selection import train_test_split
import argparse
import os

def split_dataset(dataset, 
                  train_ratio, 
                  val_ratio, 
                  test_ratio, 
                  shuffle=True
                 ):
    
    max_val_len = 50 # 50 according to U-Sleep
    max_test_len = 100 # 100 according to U-Sleep
    
    dataset_len = len(dataset)
    
    train_len = round(dataset_len*train_ratio)
    val_len = round(dataset_len*val_ratio)
    test_len = dataset_len - train_len - val_len # We do this to make sure round does not cause us to have values like 6/3/3 for an 11 rec dataset.
    
    if val_len > max_val_len:
        diff = val_len - max_val_len
        train_len += diff
        val_len = max_val_len
    
    if test_len > max_test_len:
        diff = test_len - max_test_len
        train_len += diff
        test_len = max_test_len

    print(f"Number of train subjects: {train_len}")
    print(f"Number of validation subjects: {val_len}")
    print(f"Number of test subjects_ {test_len}")
    
    assert train_len + val_len + test_len == len(dataset)
    
    train_subjects = dataset[:train_len]
    val_subjects = dataset[train_len:train_len+val_len]
    test_subjects = dataset[train_len+val_len:]
    
    return train_subjects, val_subjects, test_subjects


def rename_keys(file, groups, split_type):
    for key in groups:
        base_key = key.split("_")[-1]
        new_key = split_type + "_" + base_key
        
        file.move(key, new_key)
        
        
def train_val_test_split(basepath, filename, train_ratio, val_ratio, test_ratio):
    """
    Function to split a single tranformed hdf5 dataset into train, validation and test datasets by tagging them in subject group name:
    
    {split_type}_{subject_id}
    
    E.g. train_800002
    
    # TODO: Currently split by number of subjects, but subjects can have different number of records. In future we might want to count number of records for each subject and split based on that.
    """
    print(basepath)
    print(filename)
    
    assert os.path.exists(basepath+filename)

    with h5py.File(basepath + filename, 'a') as file:
        print("Opened: " + basepath+filename)
        subj_keys = list(file.keys())
        #print(subj_keys)
        
        train, val, test = split_dataset(subj_keys, train_ratio, val_ratio, test_ratio)
        
        rename_keys(file, train, "train")
        rename_keys(file, val, "val")
        rename_keys(file, test, "test")
        
    
if __name__ == '__main__':
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

    CLI.add_argument(
      "--train_ratio",
      type=float
    )

    CLI.add_argument(
      "--val_ratio",
      type=float
    )

    CLI.add_argument(
      "--test_ratio",
      type=float
    )
    
    args = CLI.parse_args()
    
    bpath = args.basepath
    filenames = args.files

    train_ratio = args.train_ratio
    val_ratio = args.val_ratio
    test_ratio = args.test_ratio

    assert train_ratio+val_ratio+test_ratio == 1

    for file in filenames:
        train_val_test_split(bpath, file, train_ratio, val_ratio, test_ratio)    

        # Testing if keys are changed
        with h5py.File(bpath + file, 'a') as f:
            print(f.keys())
    
