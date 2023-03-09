import mne
from abc import abstractmethod

from .base import SleepdataPipeline


class Base_Sedf(SleepdataPipeline):
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
            "Movement time": self.Labels.UNKNOWN
        }
    
  
    def sample_rate(self):
        return 100
        
        
    @property
    @abstractmethod    
    def dataset_name(self):
        pass
    
    
    def channel_mapping(self):
        return {
            "EOG horizontal": {'ref1': self.TTRef.EL, 'ref2': self.TTRef.ER}, 
            "EEG Fpz-Cz": {'ref1': self.TTRef.Fpz, 'ref2': self.TTRef.Cz},
            "EEG Pz-Oz": {'ref1': self.TTRef.Pz, 'ref2': self.TTRef.Oz}
        }
    
    
    @abstractmethod    
    def list_records(self):
        pass
    
    
    def read_psg(self, record):
        psg_path, hyp_path = record    
        
        x = dict()
        y = [] 
        
        # region x
        data = mne.io.read_raw_edf(psg_path)
            
        for channel in self.channel_mapping().keys():
            channel_data = data.get_data(channel)[0]
            chnl_len = len(channel_data)
            
            x[channel] = channel_data
        # endregion
        
        # region y
        hyp = mne.read_annotations(hyp_path)
        
        labels = list(hyp.description)
        labels.pop()
        durations = list(hyp.duration)
        durations.pop()
        
        assert len(labels) == len(durations)
        
        for label, duration in zip(labels, durations):
            assert label != None
            assert duration != None
            
            dur_in_epochs = int(duration/30)
                    
            for e in range(dur_in_epochs):
                y.append(label)
               
        assert len(y)*self.sample_rate()*30 == chnl_len
        
        # endregion
        
        return x, y