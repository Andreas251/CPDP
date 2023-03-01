import os
import mne
import sys
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

from .base import SleepdataPipeline


class Abc(SleepdataPipeline):
    """
    ABOUT THIS DATASET 
    
    Channels included in dataset: ['F3', 'F4', 'C3', 'C4', 'O1', 'O2', 'M1', 'M2', 'E1', 'E2', 'ECG1', 'ECG2', 'LLeg1', 'LLeg2', 'RLeg1', 'RLeg2', 'Chin1', 'Chin2', 'Chin3', 'Airflow', 'Abdo', 'Thor', 'Snore', 'Sum', 'PosSensor', 'Ox Status', 'Pulse', 'SpO2', 'Nasal Pressure', 'CPAP Flow', 'CPAP Press', 'Pleth', 'Derived HR', 'Light', 'Manual Pos'].
    
    All channels are measured against Fpz according to https://sleepdata.org/datasets/abc/pages/montage-and-sampling-rate-information.md
    {EDF label}-Fpz (e.g. F3-Fpz) 
    
    EEG and EOG signals were each sampled at 256Hz.
    """
    def sleep_stage_dict(self):
        return {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            5: 4
        }
  
    def sample_rate(self):
        return 256
        
        
    def dataset_name(self):
        return "abc"
    
    
    def read_psg(self, record_path):
        path_to_psg = record_path
        path_to_hyp = 
        
        # edfs/baseline/abc-baseline-900001.edf
        # annotations-events-profusion/baseline/abc-baseline-900001-profusion.xml
        
        path_to_psg = record_path + "edfs/baseline/abc-baseline-900002.edf"
        path_to_hyp_prof = record_path + "annotations-events-profusion/baseline/abc-baseline-900002-profusion.xml"
        path_to_hyp = record_path + "annotations-events-nsrr/baseline/abc-baseline-900002-nsrr.xml"
        
        subject_number = ""
        record_number = ""
        
        # region x
        x = dict()
        
        data = mne.io.read_raw_edf(path_to_psg)
        
        for channel in data.ch_names:
            if channel in self.relevant_channels():
                channel_data = data[channel]
                
                relative_channel_data = channel_data[0][0] - channel_data[1] # TODO: Is is correct?
                mapped_channel_name = self.channel_mapping()[channel]
                
                x[mapped_channel_name] = relative_channel_data
        # endregion
        
        # region y
        y = []
        tree = ET.parse(path_to_hyp_prof)
        
        root = tree.getroot()
        
        sleep_stages = root.find("SleepStages")
        
        for stage in sleep_stages:
            y.append(stage.text)
        # endregion            
        
        sys.exit()
        return x, y, subject_number, record_number
        