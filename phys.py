import os
import mne
import wfdb
import h5py

import scipy.io
import numpy as np


from .base import SleepdataPipeline


class Phys(SleepdataPipeline):

    def label_mapping(self):
        return {
            #"Sleep stage W": self.Labels.Wake,
            #"Sleep stage 1": self.Labels.N1,
            #"Sleep stage 2": self.Labels.N2,
            #"Sleep stage 3": self.Labels.N3,
            #"Sleep stage 4": self.Labels.N3,
            #"Sleep stage R": self.Labels.REM,
            #"Sleep stage ?": self.Labels.UNKNOWN,
            #"Movement time": self.Labels.N1 # TODO: This is WRONG. Find out what we do with this type of stage!
        }
    
  
    def sample_rate(self):
        return 200
        
        
    def dataset_name(self):
        return "phys"
    
    
    def channel_mapping(self):
        return {
            #"EOG horizontal": {'ref1': self.TTRef.EL, 'ref2': self.TTRef.ER}, 
            #"EEG Fpz-Cz": {'ref1': self.TTRef.Fpz, 'ref2': self.TTRef.Cz},
            #"EEG Pz-Oz": {'ref1': self.TTRef.Pz, 'ref2': self.TTRef.Oz}
        }
    
    #record = wfdb.rdrecord('sample-data/test01_00s', sampfrom=800,
    #                       channels=[1, 3])
    
    def list_records(self, basepath):
        paths_dict = {}
        
        for subject in os.listdir(basepath):
            filebase = basepath+subject+'/'+subject
            
            data_path = filebase
            label_path = filebase+'-arousal.mat'
            
            exists = os.path.exists(label_path) and os.path.exists(data_path+'.hea')
            
            if not exists:
                print('The record for subject {} did not exist'.format(subject))
                continue
            
            paths_dict[subject] = [(data_path, label_path)]

        return paths_dict
    
    
    def read_psg(self, record):
        data_path, label_path = record
        
        try:
            r = wfdb.rdrecord(data_path)
        except ValueError:
            print("Could not read data file")
            return None

        with h5py.File(label_path, 'r') as f:
            print(f['data']['sleep_stages'].keys())
            nonrem1 = f['data']['sleep_stages']['nonrem1'][()]
            print(nonrem1.shape)
            
            i = 0
            while(1):
                first_epoch = nonrem1[0][i*5999:(i*5999)+5999]
                print(first_epoch.shape)
                result = np.all(first_epoch == first_epoch[0])
                i += 1
                print(result)
                
            exit()
            #wake = f['data']['sleep_stages']['wake']
            #print(labels.shape)
            #print(nonrem1[()])
            #print(wake[()])

        #mat = scipy.io.loadmat(filebase+'.mat')
        #print(mat['val'][0])
        #mat = scipy.io.loadmat(filebase+'-arousal.mat')
        #print(mat.keys())

        dataframe = r.to_dataframe()
        print(dataframe.shape)
        
        return 0