import h5py
from sklearn.model_selection import train_test_split
import argparse

def split_dataset(dataset, 
                  train_ratio, 
                  val_ratio, 
                  test_ratio, 
                  shuffle=True
                 ):
    val_size = val_ratio / (val_ratio + train_ratio)
    
    X_train, X_test = train_test_split(dataset, test_size=test_ratio, shuffle=shuffle)
    X_train, X_val = train_test_split(X_train, test_size=val_size, shuffle=shuffle)

    return X_train, X_val, X_test


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
    
    with h5py.File(basepath + filename, 'a') as file:
        subj_keys = list(file.keys())
        print(subj_keys)
        
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
    
    args = CLI.parse_args()
    
    bpath = args.basepath
    filenames = args.files

    for file in filenames:
        train_ratio = 0.7
        val_ratio = 0.15
        test_ratio = 0.15

        train_val_test_split(bpath, file, train_ratio, val_ratio, test_ratio)    

        # Testing if keys are changed
        with h5py.File(bpath + file, 'a') as f:
            print(f.keys())
    
