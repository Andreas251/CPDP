import os
import mne

from .base import SleepdataPipeline


class Abc(SleepdataPipeline):
    """
    ABOUT THIS DATASET 
    
    Channels included in dataset: [''].
    
    EEG and EOG signals were each sampled at 256Hz.
    """
    def sleep_stage_dict(self):
        return {
            "W": 0
        }
  
    def sample_rate(self):
        return 256
        
        
    def dataset_name(self):
        return "abc"
    
    
    def read_psg(self, record_path):
        print(record_path)
        record_dir = os.listdir(record_path)
        print(record_dir)
        
        path_to_psg = record_path + "edfs/baseline/abc-baseline-900001.edf"
        
        
        data = mne.io.read_raw_edf(path_to_psg)
        print(data.ch_names)
        
        
        
        sys.exit()
        