import os
import mne
import sys

from .base import SleepdataPipeline


class Chat(SleepdataPipeline):
    """
    ABOUT THIS DATASET 
    
    Channels included in dataset: ['Airflow', 'CannulaFlow', 'SUM', 'Chest', 'ABD', 'Snore', 'M1', 'M2', 'C3', 'C4', 'O1', 'O2', 'F3', 'F4', 'T3', 'T4', 'E1', 'E2', 'ECG1', 'ECG2', 'Lchin', 'Rchin', 'Cchin', 'ECG3', 'Lleg1', 'Lleg2', 'Rleg1', 'Rleg2', 'SAO2Nellcor', 'PulseNellcor', 'PlethNellcor', 'EtCO2', 'Cap', 'RR', 'SaO2', 'Pulse', 'Position', 'DHR']
.
    
    EEG and EOG signals were each sampled at 200Hz.
    """
    def sleep_stage_dict(self):
        return {
            "W": 0
        }
  
    def sample_rate(self):
        return 200
        
        
    def dataset_name(self):
        return "chat"
    
    
    def read_psg(self, record_path):
        print(record_path)
        record_dir = os.listdir(record_path)
        print(record_dir)
        
        path_to_psg = record_path + "edfs/baseline/chat-baseline-300001.edf"
        
        
        data = mne.io.read_raw_edf(path_to_psg)
        print(data.ch_names)
        
        
        
        sys.exit()
        