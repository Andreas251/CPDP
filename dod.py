import os
from h5py import File

from .base import SleepdataPipeline


class Dod(SleepdataPipeline):
    """
    ABOUT THIS DATASET 
    
    """
    def label_mapping(self):
        return {
            -1: self.Labels.UNKNOWN,
            0: self.Labels.Wake,
            1: self.Labels.N1,
            2: self.Labels.N2,
            3: self.Labels.N3,
            4: self.Labels.REM
        }
  

    def sample_rate(self):
        return 256
        
        
    def dataset_name(self):
        return "dod"
    
    
    def channel_mapping(self):
        return {
            "C3_M2": {'ref1': self.TTRef.C3, 'ref2': self.TTRef.RPA},
            "C4_M1": {'ref1': self.TTRef.C4, 'ref2': self.TTRef.LPA},
            "F4_F4": {'ref1': self.TTRef.F3, 'ref2': self.TTRef.F4},
            "F3_M2": {'ref1': self.TTRef.F3, 'ref2': self.TTRef.RPA},
            "F3_O1": {'ref1': self.TTRef.F3, 'ref2': self.TTRef.O1},
            "F4_O2": {'ref1': self.TTRef.F4, 'ref2': self.TTRef.O2},
            "O1_M2": {'ref1': self.TTRef.O1, 'ref2': self.TTRef.RPA},
            "O2_M1": {'ref1': self.TTRef.O2, 'ref2': self.TTRef.LPA},
            "EOG1": {'ref1': self.TTRef.EL, 'ref2': self.TTRef.RPA}, # TODO: Find out refs
            "EOG2": {'ref1': self.TTRef.ER, 'ref2': self.TTRef.RPA}, # TODO: Find out refs
        }
    
    
    def list_records(self, basepath):
        paths_dict = dict()
        
        for dir, subdir, filenames in os.walk(basepath):
            for file in filenames:
                record_no = file.split(".")[0]
                record_path = f"{dir}/{file}"
                
                paths_dict[record_no] = [record_path]
    
        return paths_dict
    
    
    def read_psg(self, record):
        
        x = dict()
        
        with File(record, "r") as h5:
            signals = h5.get("signals")
            eeg_channels = signals.get("eeg")
            eog_channels = signals.get("eog")
            
            # Number of epochs in signals are not an integer. Removing elements in the end to have an integer of epochs.
            channel_len = len(eeg_channels.get(list(eeg_channels.keys())[0]))
            remainder = channel_len % (self.sample_rate()*30)
            new_channel_len = channel_len - remainder
            x_num_epochs = int(new_channel_len/self.sample_rate()/30)
                        
            for channel in eeg_channels:
                x[channel] = eeg_channels.get(channel)[()][:new_channel_len]
            for channel in eog_channels:
                x[channel] = eog_channels.get(channel)[()][:new_channel_len]
            
            # There are more labels than epochs of signals. Removing last elements
            y = list(h5.get("hypnogram")[()])[:x_num_epochs]
            
            assert(len(y) == x_num_epochs)
        
        return x, y