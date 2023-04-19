import os
from h5py import File

from .base import SleepdataPipeline
import pandas as pd
import mne
import numpy as np

class Eesm(SleepdataPipeline):
    """
    ABOUT THIS DATASET 
    """
    
    def label_mapping(self):
        return {
            1: self.Labels.Wake,
            2: self.Labels.REM,
            3: self.Labels.N1,
            4: self.Labels.N2,
            5: self.Labels.N3,
            6: self.Labels.UNKNOWN,
            7: self.Labels.UNKNOWN,
            8: self.Labels.UNKNOWN
        }
        
    def dataset_name(self):
        return "eesm"
    
    def channel_mapping(self):
        return {
            #"ELA": self.Mapping(self.TTRef.EL, self.TTRef.LPA),
            #"ELB": self.Mapping(self.TTRef.EL, self.TTRef.LPA),
            #"ELC": self.Mapping(self.TTRef.EL, self.TTRef.LPA),
            #"ELT": self.Mapping(self.TTRef.EL, self.TTRef.LPA),
            #"ELE": self.Mapping(self.TTRef.EL, self.TTRef.LPA),
            #"ELI": self.Mapping(self.TTRef.EL, self.TTRef.LPA),
            #"ERA": self.Mapping(self.TTRef.ER, self.TTRef.LPA),
            #"ERB": self.Mapping(self.TTRef.ER, self.TTRef.LPA),
            #"ERC": self.Mapping(self.TTRef.ER, self.TTRef.LPA),
            #"ERT": self.Mapping(self.TTRef.ER, self.TTRef.LPA),
            #"ERE": self.Mapping(self.TTRef.ER, self.TTRef.LPA),
            #"ERI": self.Mapping(self.TTRef.ER, self.TTRef.LPA),
            "EOGr": self.Mapping(self.TTRef.ER, self.TTRef.LPA),
            "EOGl": self.Mapping(self.TTRef.EL, self.TTRef.LPA),
            #"M1": self.Mapping(self.TTRef.M1, self.TTRef.LPA),
            "F3": self.Mapping(self.TTRef.F3, self.TTRef.LPA),
            "C3": self.Mapping(self.TTRef.C3, self.TTRef.LPA),
            "O1": self.Mapping(self.TTRef.O1, self.TTRef.LPA),
            #"M2": self.Mapping(self.TTRef.M2, self.TTRef.LPA),
            "F4": self.Mapping(self.TTRef.F4, self.TTRef.LPA),
            "C4": self.Mapping(self.TTRef.C4, self.TTRef.LPA),
            "O2": self.Mapping(self.TTRef.O2, self.TTRef.LPA)
        }
    
    
    def list_records(self, basepath):
        paths_dict = {}
        
        subject_paths = [x for x in os.listdir(basepath) if x.startswith("sub")]

        for s_path in subject_paths:
            subject_id = s_path
            record_paths = [x for x in os.listdir(basepath+s_path) if x.startswith("ses")]
            
            records = []
            
            for r_path in record_paths:
                base_data_path = f"{basepath}{s_path}/{r_path}/eeg"
                
                data_path = f"{base_data_path}/{s_path}_{r_path}_task-sleep_eeg.set"
                label_path = f"{base_data_path}/{s_path}_{r_path}_task-sleep_acq-scoring_events.tsv"
                
                if os.path.exists(data_path) and os.path.exists(label_path):
                    records.append((data_path, label_path))
                
            paths_dict[subject_id] = records
            
        return paths_dict
    
    
    def read_psg(self, record):
        psg_path, hyp_path = record
        
        try:
            label_pd = pd.read_csv(hyp_path, sep = '\t')
        except:
            self.log_warning("Could not read CSV file", subject="", record=psg_path)
            return None
                
        y = label_pd["Staging1"].values.tolist()
        x = dict()
        
        data = mne.io.read_raw_eeglab(psg_path, verbose=False)
        sample_rate = int(data.info['sfreq'])
        
        df = data.to_data_frame()
        
        df = df.fillna(df.mean(), inplace=False)
        
        for channel in self.channel_mapping().keys():
            try:
                channel_data = df[channel]
            except ValueError:
                self.log_warning(f"Channel {channel} non-existing", subject="", record=psg_path)
                continue
                
            nans = np.isnan(channel_data)
            nans = [x for x in nans if x == True]
            num_nans = len(nans)
            
            if num_nans > 0:
                self.log_warning(f"Num nans are {num_nans}", subject="", record=psg_path)
                return None
            
            channel_data = channel_data.values.tolist()
            
            x[channel] = (channel_data, sample_rate)

        return x, y
