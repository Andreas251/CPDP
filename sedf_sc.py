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
    def label_mapping(self):
        return {
            "Sleep stage W": self.Labels.Wake,
            "Sleep stage 1": self.Labels.N1,
            "Sleep stage 2": self.Labels.N2,
            "Sleep stage 3": self.Labels.N3,
            "Sleep stage 4": self.Labels.N3,
            "Sleep stage R": self.Labels.REM,
            "Sleep stage ?": self.Labels.UNKNOWN,
            "Movement time": self.Labels.N1 # TODO: This is WRONG. Find out what we do with this type of stage!
        }
    
  
    def sample_rate(self):
        return 100
        
        
    def dataset_name(self):
        return "sedf_sc" # TODO: Just sedf?
    
    
    def channel_mapping(self):
        return {
            "EOG horizontal": {'ref1': self.TTRef.EL, 'ref2': self.TTRef.ER}, 
            "EEG Fpz-Cz": {'ref1': self.TTRef.Fpz, 'ref2': self.TTRef.Cz},
            "EEG Pz-Oz": {'ref1': self.TTRef.Pz, 'ref2': self.TTRef.Oz}
        }
    
    
    def list_records(self, basepath):
        paths_dict = {}
        
        record_paths = os.listdir(basepath)
        
        for path in record_paths:
            record_path = f"{basepath}{path}"
            
            for file in os.listdir(record_path):
                if "Hypnogram" in file:
                    hyp_path = f"{record_path}/{file}"
                elif "PSG" in file:
                    psg_path = f"{record_path}/{file}"
                else:
                    print("PSG or hypnogram file not found. Exiting..")
                    exit()
                    
            paths_dict[path] = [(psg_path, hyp_path)]
        
        return paths_dict
    
    
    def read_psg(self, record):
        psg_path, hyp_path = record
        psg_path = "../../data/sedf_from_physionet/sleep-telemetry/ST7012J0-PSG.edf"
        hyp_path = "../../data/sedf_from_physionet/sleep-telemetry/ST7012JP-Hypnogram.edf"
        
        
        x = dict()
        y = [] 
        
        # region x
        data = mne.io.read_raw_edf(psg_path)
        for channel in self.channel_mapping().keys():
            print(channel)
            channel_data = data.get_data(channel)[0]
            print(len(channel_data))
            
            
            x_num_epochs = int(len(channel_data)/self.sample_rate()/30)
            print(x_num_epochs)
            #print(channel_data[10000:10010])
            #print(channel_data[:10])
            #print(channel_data[-10:])
            
            print(channel_data[1020:1030])
            print(channel_data[-27500:-27490])
            
            old_dat = channel_data[0]
            idx = 0
            for el in channel_data:
                if el != old_dat:
                    print(old_dat)
                    print(el)
                    print(f"Index: {idx}")
                    break
                old_dat = el
                idx = idx + 1
            
            
            reversed_arr = channel_data[::-1]
            
            old_dat = reversed_arr[0]
            idx = 0
            for el in reversed_arr:
                if el != old_dat:
                    print(old_dat)
                    print(el)
                    print(f"Index: {idx}")
                    break
                old_dat = el
                idx = idx + 1
            
            exit()
            
            x[channel] = channel_data
        # endregion
        
        # region y
        hyp = mne.read_annotations(hyp_path) 
        
        for stage in hyp:
            stg = stage.get("description")
            
            assert stg != None
            
            #print(stage)
            
            dur = stage.get("duration")
            dur_in_epochs = int(dur/30)
                    
            for e in range(dur_in_epochs):
                y.append(stg)
               
        print(len(y))
        y = y[0:x_num_epochs] # Assuming that we first N labels
        # endregion
        
        exit()
        return x, y
