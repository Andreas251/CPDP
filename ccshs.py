import os
import mne
import sys

from .sdo_base import SleepdataOrg


class Ccshs(SleepdataOrg):
    """
    ABOUT THIS DATASET 
    
    Channels included in dataset: ['Airflow', 'CannulaFlow', 'SUM', 'Chest', 'ABD', 'Snore', 'M1', 'M2', 'C3', 'C4', 'O1', 'O2', 'F3', 'F4', 'T3', 'T4', 'E1', 'E2', 'ECG1', 'ECG2', 'Lchin', 'Rchin', 'Cchin', 'ECG3', 'Lleg1', 'Lleg2', 'Rleg1', 'Rleg2', 'SAO2Nellcor', 'PulseNellcor', 'PlethNellcor', 'EtCO2', 'Cap', 'RR', 'SaO2', 'Pulse', 'Position', 'DHR']

    
    EEG and EOG signals were each sampled at 200Hz.
    """  
    def sample_rate(self):
        return 128
        
        
    def dataset_name(self):
        return "ccshs"
    
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
        r2 = self.TTRef.Fpz
        
        return {
            "C3": {'ref1': self.TTRef.C3, 'ref2': r2},
            "C4": {'ref1': self.TTRef.C4, 'ref2': r2},
            "A1": {'ref1': self.TTRef.LPA, 'ref2': r2},
            "A2": {'ref1': self.TTRef.RPA, 'ref2': r2},
            "LOC": {'ref1': self.TTRef.EL, 'ref2': r2},
            "ROC": {'ref1': self.TTRef.ER, 'ref2': r2},
        }
        