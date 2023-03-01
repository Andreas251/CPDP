import os
from h5py import File

from .base import SleepdataPipeline


class Dcsm(SleepdataPipeline):
    """
    ABOUT THIS DATASET 
    
    Channels included in dataset: ['ABDOMEN', 'C3-M2', 'C4-M1', 'CHIN', 'E1-M2', 'E2-M2', 'ECG-II', 'F3-M2', 'F4-M1', 'LAT', 'NASAL', 'O1-M2', 'O2-M1', 'RAT', 'SNORE', 'SPO2', 'THORAX'].
    
    EEG and EOG signals were each sampled at 256Hz.
    """
    def sleep_stage_dict(self):
        return {
            "W": 0,
            "N1": 1,
            "N2": 2,
            "N3": 3,
            "REM": 4
        }
  
    def sample_rate(self):
        return 256
        
        
    def dataset_name(self):
        return "dcsm"
    
    
    def read_psg(self, record_path):
        record_dir = os.listdir(record_path)
        
        assert len(record_dir) == 2 # A record must contain only one PSG and one Hypnogram
        
        psg_filename = [s for s in record_dir if "psg.h5".lower() in s.lower()][0]
        hyp_filename = [s for s in record_dir if "hypnogram.ids".lower() in s.lower()][0]
        
        path_to_psg = record_path + psg_filename
        path_to_hypnogram = record_path + hyp_filename
        
        subject_number = record_path.split("/")[-2]
        record_number = "00" # There is only a single record per subject
        
        with File(path_to_psg, "r") as h5:
            x = dict()

            h5channels = h5.get("channels")
            
            for channel in self.relevant_channels():
                if channel in h5channels.keys():
                    channel_data = h5channels[channel][:]

                    channel_data_resampled = self.resample_channel(
                        channel_data, 
                        input_rate=self.sample_rate()
                    )

                    x[self.channel_mapping()[channel]] = channel_data_resampled
                
        with open(path_to_hypnogram) as f:
            hypnogram = f.readlines()

            y = []

            for element in hypnogram:
                prev_stages_time, stage_time, label = element.rstrip().split(",")
                prev_stages_time = int(prev_stages_time)
                stage_time = int(stage_time)

                n_epochs_in_stage = int(stage_time/30)

                for label_entry in range(n_epochs_in_stage):
                    stg = self.sleep_stage_dict()[label]
                    # assert stg != None
                    
                    y.append(stg)
                    
        return x, y, subject_number, record_number
        