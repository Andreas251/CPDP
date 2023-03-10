import os
import mne
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
import warnings

import sys
sys.path.append('../SleepDataPipeline')
from SleepDataPipeline.base import SleepdataPipeline

class SleepdataOrg(SleepdataPipeline):
    """
    ABOUT THIS
    """

    def label_mapping(self): 
        return {
            '0': self.Labels.Wake,
            '1': self.Labels.N1,
            '2': self.Labels.N2,
            '3': self.Labels.N3,
            '4': self.Labels.N3,
            '5': self.Labels.REM,
            '9': self.Labels.UNKNOWN
        }
    
    @property
    @abstractmethod
    def channel_mapping(self):
        pass
    
    def dataset_name(self):
        return self.__class__.__name__.lower()
    
    def list_records(self, basepath):
        
        assert os.path.exists(basepath), "Path does not exist"

        paths_dict = {}
        
        poly_path = f"{basepath}polysomnography/"
        hyp = "annotations-events-profusion"
        psg = "edfs"
        
        psg_path = f"{poly_path}{psg}"
        hyp_path = f"{poly_path}{hyp}"
        
        psg_files = []
        
        for dir, subdir, filenames in os.walk(psg_path):
            for file in filenames:
                psg_files.append(dir + "/" + file)
                
        psg_files = sorted(psg_files)

        for idx in range(len(psg_files)):
            psg_file_path = psg_files[idx]

            hyp_file_path = psg_file_path.replace('/'+psg+'/', '/'+hyp+'/', 1).replace('.edf', '-profusion.xml', 1)
            splits = hyp_file_path.split("-")
            subject_number = splits[-2]
            
            assert os.path.exists(psg_file_path), f"File {psg_file_path} does not exist"
            
            labels_exist = os.path.exists(hyp_file_path)
            
            if not labels_exist:
                self.log_warning(f"File does not exist, skipping this record", subject=None, record=hyp_file_path)
                continue
            
            paths_dict.setdefault(subject_number, []).append((psg_file_path, hyp_file_path))
        
        assert len(paths_dict) > 0, "No filepaths detected"
        
        return paths_dict
    
    # Override this if needed
    def slice_channel(self, x, y_len, sample_rate):
        epoch_diff = (len(x)/sample_rate/30 - y_len)

        assert epoch_diff < 1.0, "Epoch diff can't be bigger than 1. Sample_rate might be off"
        assert epoch_diff >= 0, "Epoch diff can't be negative. You have more labels than you have data"
        
        x_len = y_len*sample_rate*30
        return x[:x_len]
    
    def read_psg(self, record):
        path_to_psg, path_to_hyp = record

        y = []
        tree = ET.parse(path_to_hyp)
        
        root = tree.getroot()
            
        sleep_stages = root.find("SleepStages")
        
        for stage in sleep_stages:
            y.append(stage.text)

        x = dict()
        
        data = mne.io.read_raw_edf(path_to_psg, verbose=False)
        sample_rate = int(data.info['sfreq'])

        for channel in self.channel_mapping().keys():
            try:
                channel_data = data[channel]
            except ValueError:
                print('Channel {channel} was not found in the record. Possibilities are {channels}'.format(channel=channel,
                                                                                                           channels=data.ch_names))
                continue
            
            first_ref = channel_data[0][0]
            
            second_ref = channel_data[1]
            
            assert len(first_ref) == len(second_ref)
            
            relative_channel_data = first_ref - second_ref # TODO: Is is correct?
            
            final_channel_data = self.slice_channel(relative_channel_data, len(y), sample_rate)
            
            assert len(final_channel_data) == len(y)*sample_rate*30, f"Channel length was {len(final_channel_data)}, but according to the number of labels it should be {len(y)*sample_rate*30}. Check the sample rate or override slice_channels if needed."
            
            x[channel] = (final_channel_data, sample_rate)
        
        assert len(x) > 0, "No data detected"
        
        return x, y
