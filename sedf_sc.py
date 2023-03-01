import os
import mne

from .base import SleepdataPipeline


class Sedf_SC(SleepdataPipeline):
    """
    ABOUT THIS DATASET
    
    The naming convention of records is as follows: SC4ssNE0 where:
    SC: Sleep Cassette study.
    ss: Subject number (notice that most subjects has 2 records), e.g. 00.
    N: Night (1 or 2).
    
    Channels included in dataset: ['EEG Fpz-Cz', 'EEG Pz-Oz', 'EOG horizontal', 'Resp oro-nasal', 'EMG submental', 'Temp rectal', 'Event marker'].

    
    EEG and EOG signals were each sampled at 100Hz.
    """        
    def sleep_stage_dict(self):
        return {
            "Sleep stage W": 0,
            "Sleep stage 1": 1,
            "Sleep stage 2": 2,
            "Sleep stage 3": 3,
            "Sleep stage 4": 3,
            "Sleep stage R": 4,
            "Sleep stage ?": "Unknown",
            "Movement time": 1 # TODO: This is WRONG. Find out what we do with this type of stage!
        }
  
    def sample_rate(self):
        return 100
        
        
    def dataset_name(self):
        return "sedf_sc"    
    
    
    def read_psg(self, record_path):
        record_dir = os.listdir(record_path)
        
        assert len(record_dir) == 2 # A record must contain only one PSG and one Hypnogram
        
        psg_filename = [s for s in record_dir if "PSG.edf".lower() in s.lower()][0]
        hyp_filename = [s for s in record_dir if "Hypnogram.edf".lower() in s.lower()][0]
        
        path_to_psg = record_path + psg_filename
        path_to_hypnogram = record_path + hyp_filename
        
        # Subject and record number is included in naming convention
        subject_number = psg_filename[3:5]
        record_number = psg_filename[5:6]
        
        # region PSG
        x = dict()
        
        data = mne.io.read_raw_edf(path_to_psg)
        
        for channel in self.relevant_channels():
            try:
                channel_data = data.get_data(channel)[0]
                # print(f"Data channel '{channel}' found. Getting data...")
            except ValueError:
                # print(f"ValueError: data channel '{channel}' not found. Skipping...")
                continue
            
            channel_data_resampled = self.resample_channel(
                channel_data, 
                input_rate=self.sample_rate()
            )
            x[self.channel_mapping()[channel]] = channel_data_resampled
        # endregion
        
        # region Labels
        y = []
        hyp = mne.read_annotations(path_to_hypnogram)        
        
        for stage in hyp:
            stg = self.sleep_stage_dict().get(stage.get("description"))
            
            # assert stg != None
                
            dur = stage.get("duration")
            num_epochs = int(dur/30)
            
            if stg != "Unknown":           
                for e in range(num_epochs):
                    y.append(stg)
        # endregion
        
        return x, y, subject_number, record_number
        