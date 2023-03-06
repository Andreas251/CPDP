import os
from h5py import File
import scipy.io
import numpy as np
import pandas as pd
import mne

from .base import SleepdataPipeline


class Svuh(SleepdataPipeline):
    """
    ABOUT THIS DATASET 
    
    """
  
    def sample_rate(self):
        return 200
        
        
    def dataset_name(self):
        return "isruc"
    
    
    def label_mapping(self):
        return 0
        #return {
        #    "0": self.Labels.Wake,
        #    "1": self.Labels.N1,
        #    "2": self.Labels.N2,
        #    "3": self.Labels.N3,
        #    "5": self.Labels.REM,
        #}
    
    
    def channel_mapping(self):
        return 0
        #return {
        #    "F3_A2": {'ref1': self.TTRef.F3, 'ref2': self.TTRef.A2},
        #    "C3_A2": {'ref1': self.TTRef.C3, 'ref2': self.TTRef.A2},
        #    "F4_A1": {'ref1': self.TTRef.F4, 'ref2': self.TTRef.A1},
        #    "C4_A1": {'ref1': self.TTRef.C4, 'ref2': self.TTRef.A1},
        #    "O1_A2": {'ref1': self.TTRef.O1, 'ref2': self.TTRef.A2},
        #    "O2_A1": {'ref1': self.TTRef.O2, 'ref2': self.TTRef.A1},
        #    "ROC_A1": {'ref1': self.TTRef.ER, 'ref2': self.TTRef.A1},
        #    "LOC_A2": {'ref1': self.TTRef.EL, 'ref2': self.TTRef.A2},
        #}
    
    
    def list_records(self, basepath):
        file_base = "ucddb"
        file_path = basepath+'/'+file_base
        subject_ids = ["002","003","005","006","007","008","009","010","011","012","013","014","015","017","018","019",
                      "020","021","022","023","024","025","026","027","028"]
        
        dic = dict()
        
        for id in subject_ids:
            prepend = file_path+id
            
            if os.path.isfile(prepend+".rec"):
                print("Renamed files to .edf")
                os.rename(prepend+".rec", prepend+".edf")
                
            dic[id] = [(prepend+".edf", prepend+"_stage.txt")]
            
        return dic
    
    def read_psg(self, record):
        print(record)
        (datapath, labelpath) = record
        
        data = mne.io.read_raw_edf(datapath)
        print(data.ch_names)
        
        exit()
        
        return 0
        #datapath, labelpath = record
        #
        #x = dict()
        #
        #mat = scipy.io.loadmat(datapath)
        #for key in self.channel_mapping().keys():
        #    chnl = np.array(mat[key]).flatten()
        #    x[key] = chnl
        #    
        #with open(labelpath, "r") as f:
        #    y = list(map(lambda x: x[0], f.readlines()))
        #    
        #return x, y