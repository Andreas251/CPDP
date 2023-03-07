import os
from h5py import File

from .base import SleepdataPipeline


class Dcsm(SleepdataPipeline):
    """
    ABOUT THIS DATASET 
    
    Channels included in dataset: ['ABDOMEN', 'C3-M2', 'C4-M1', 'CHIN', 'E1-M2', 'E2-M2', 'ECG-II', 'F3-M2', 'F4-M1', 'LAT', 'NASAL', 'O1-M2', 'O2-M1', 'RAT', 'SNORE', 'SPO2', 'THORAX'].
    
    EEG and EOG signals were each sampled at 256Hz.
    """
    def label_mapping(self):
        return {
            "W": self.Labels.Wake,
            "N1": self.Labels.N1,
            "N2": self.Labels.N2,
            "N3": self.Labels.N3,
            "REM": self.Labels.REM
        }
  

    def sample_rate(self):
        return 256
        
        
    def dataset_name(self):
        return "dcsm"
    
    
    def channel_mapping(self):
        return {
            "E1-M2": {'ref1': self.TTRef.EL, 'ref2': self.TTRef.RPA},
            "E2-M2": {'ref1': self.TTRef.ER, 'ref2': self.TTRef.RPA},
            "C3-M2": {'ref1': self.TTRef.C3, 'ref2': self.TTRef.RPA},
            "C4-M1": {'ref1': self.TTRef.C4, 'ref2': self.TTRef.LPA},
            "F3-M2": {'ref1': self.TTRef.F3, 'ref2': self.TTRef.RPA},
            "F4-M1": {'ref1': self.TTRef.F4, 'ref2': self.TTRef.LPA},
            "O1-M2": {'ref1': self.TTRef.O1, 'ref2': self.TTRef.RPA},
            "O2-M1": {'ref1': self.TTRef.O2, 'ref2': self.TTRef.LPA}
        }
    
    
    def list_records(self, basepath):
        paths_dict = {}
        
        record_paths = os.listdir(basepath)
        
        for path in record_paths:
            record_path = f"{basepath}{path}"
            psg_path = f"{record_path}/psg.h5"
            hyp_path = f"{record_path}/hypnogram.ids"
            paths_dict[path] = [(psg_path, hyp_path)]
        
        return paths_dict
    
    
    def read_psg(self, record):
        psg_path, hyp_path = record
        
        x = dict()
        y = []
        
        with File(psg_path, "r") as h5:
            h5channels = h5.get("channels")
            
            for channel in self.channel_mapping().keys():
                channel_data = h5channels[channel][:]
                
                x[channel] = channel_data
        
        with open(hyp_path) as f:
            hypnogram = f.readlines()

            for element in hypnogram:
                prev_stages_time, stage_time, label = element.rstrip().split(",")
                stage_time = int(stage_time)

                n_epochs_in_stage = int(stage_time/30)

                for label_entry in range(n_epochs_in_stage):
                    stg = label
                    assert stg != None
                    
                    y.append(stg)
                    
        return x, y
