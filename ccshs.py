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
    
    
    def channel_mapping(self):
        return {
            "C3": "EEG_C3-Fpz",
            "C4": "EEG_C4-Fpz",
            "A1": "EEG_A1-Fpz",
            "A2": "EEG_A2-Fpz",
            "LOC": "EOG_EL-Fpz",
            "ROC": "EOG_ER-Fpz",
        }
        