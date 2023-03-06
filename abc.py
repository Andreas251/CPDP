import os
import mne
import xml.etree.ElementTree as ET

from .sdo_base import SleepdataOrg


class Abc(SleepdataOrg):
    """
    ABOUT THIS DATASET 
    
    Channels included in dataset: ['F3', 'F4', 'C3', 'C4', 'O1', 'O2', 'M1', 'M2', 'E1', 'E2', 'ECG1', 'ECG2', 'LLeg1', 'LLeg2', 'RLeg1', 'RLeg2', 'Chin1', 'Chin2', 'Chin3', 'Airflow', 'Abdo', 'Thor', 'Snore', 'Sum', 'PosSensor', 'Ox Status', 'Pulse', 'SpO2', 'Nasal Pressure', 'CPAP Flow', 'CPAP Press', 'Pleth', 'Derived HR', 'Light', 'Manual Pos'].
    
    All channels are measured against Fpz according to https://sleepdata.org/datasets/abc/pages/montage-and-sampling-rate-information.md
    {EDF label}-Fpz (e.g. F3-Fpz) 
    
    EEG and EOG signals were each sampled at 256Hz.
    """ 
    def sample_rate(self):
        return 256
        
        
    def dataset_name(self):
        return "abc"
    
    
    def label_mapping(self): # TODO Check if correct
        return {
            0: self.Labels.Wake,
            1: self.Labels.N1,
            2: self.Labels.N2,
            3: self.Labels.N3,
            4: self.Labels.Unknown,
            5: self.Labels.REM,
        }
    
    
    def channel_mapping(self):
        r2 = self.TTRef.Fz
        
        return {
            "F3": {'ref1': self.TTRef.F3, 'ref2': r2},
            "F4": {'ref1': self.TTRef.F4, 'ref2': r2},
            "C3": {'ref1': self.TTRef.C3, 'ref2': r2},
            "C4": {'ref1': self.TTRef.C4, 'ref2': r2},
            "O1": {'ref1': self.TTRef.O1, 'ref2': r2},
            "O2": {'ref1': self.TTRef.O2, 'ref2': r2},
            "M1": {'ref1': self.TTRef.LPA, 'ref2': r2},
            "M2": {'ref1': self.TTRef.RPA, 'ref2': r2},
            "E1": {'ref1': self.TTRef.EL, 'ref2': r2},
            "E2": {'ref1': self.TTRef.ER, 'ref2': r2},
        }