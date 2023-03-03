import os
import mne
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

from .base import SleepdataPipeline


class SleepdataOrg(SleepdataPipeline):
    """
    ABOUT THIS
    """
    @property
    @abstractmethod
    def label_mapping(self): 
        pass
    
    
    @property
    @abstractmethod
    def sample_rate(self):
        pass
    
    
    @property
    @abstractmethod
    def dataset_name(self):
        pass
    
    
    def list_records(self, basepath):
        paths_dict = {}
        
        poly_path = f"{basepath}polysomnography/"
        hyp = "annotations-events-profusion"
        psg = "edfs"
        
        psg_path = f"{poly_path}{psg}/"
        hyp_path = f"{poly_path}{hyp}/"
        
        psg_files = []
        hyp_files = []
        
        for dir, subdir, filenames in os.walk(psg_path):
            for file in filenames:
                psg_files.append(dir + "/" + file)
                
        for dir, subdir, filenames in os.walk(hyp_path):
            for file in filenames:
                hyp_files.append(dir + "/" + file)
                
        psg_files = sorted(psg_files)
        hyp_files = sorted(hyp_files)
        
        for idx in range(len(psg_files)):
            psg_file_path = psg_files[idx]
            hyp_file_path = hyp_files[idx]

            subject_number = psg_file_path.split("-")[-1].split(".")[0]

            paths_dict.setdefault(subject_number, []).append((psg_file_path, hyp_file_path))
        
        return paths_dict
    
    
    def read_psg(self, record):
        path_to_psg, path_to_hyp = record
        
        # region y
        y = []
        tree = ET.parse(path_to_hyp)
        
        root = tree.getroot()
        
        sleep_stages = root.find("SleepStages")
        
        for stage in sleep_stages:
            y.append(stage.text)
        # endregion
        
        # region x
        x = dict()
        
        x_len = len(y)*self.sample_rate()*30
        
        data = mne.io.read_raw_edf(path_to_psg)
        
        for channel in data.ch_names:
            channel_data = data[channel]

            relative_channel_data = channel_data[0][0] - channel_data[1] # TODO: Is is correct?

            x[channel] = relative_channel_data[:x_len]
        # endregion
        
        return x, y
        