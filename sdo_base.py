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
        assert os.path.exists(basepath), "Path does not exist"
        
        paths_dict = {}
        
        poly_path = f"{basepath}polysomnography/"
        hyp = "annotations-events-profusion"
        psg = "edfs"
        
        psg_path = f"{poly_path}{psg}/"
        hyp_path = f"{poly_path}{hyp}/"
        
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
            
            assert os.path.exists(psg_file_path), "File path does not exist"
            assert os.path.exists(hyp_file_path), "File path does not exist"
            
            paths_dict.setdefault(subject_number, []).append((psg_file_path, hyp_file_path))
        
        return paths_dict
    
    # Override this if needed
    def slice_channel(x, y_len):
        return x
    
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
        
        data = mne.io.read_raw_edf(path_to_psg)
        
        for channel in self.channel_mapping().keys():
            #try:
            #    sample_rate = self.channel_mapping()[channel]['sample_rate_override']
            #    print("Found overridden sample rate for channel: "+channel)
            #except KeyError:
            #    sample_rate = self.sample_rate()
            
            channel_data = data[channel]
            first_ref = channel_data[0][0]
            
            second_ref = channel_data[1]
            
            assert len(first_ref) == len(second_ref)
            
            relative_channel_data = first_ref - second_ref # TODO: Is is correct?
            
            final_channel_data = self.slice_channel(relative_channel_data, len(y))
            
            assert len(final_channel_data) == y_len*self.sample_rate()*30
            
            x[channel] = final_channel_data
        # endregion
        
        return x, y
