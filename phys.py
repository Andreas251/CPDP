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
            "0": self.Labels.N1,
            "1": self.Labels.N2,
            "2": self.Labels.N3,
            "3": self.Labels.REM,
            "4": self.Labels.UNKNOWN,
            "5": self.Labels.Wake,
        }
    
  
    def sample_rate(self):
        return 200
        
        
    def dataset_name(self):
        return "phys"
    
    
    def channel_mapping(self):
        return {
            "F3-M2": {'ref1': self.TTRef.F3, 'ref2': self.TTRef.RPA}, 
            "F4-M1": {'ref1': self.TTRef.F4, 'ref2': self.TTRef.LPA},
            "C3-M2": {'ref1': self.TTRef.C3, 'ref2': self.TTRef.RPA},
            "C4-M1": {'ref1': self.TTRef.C4, 'ref2': self.TTRef.LPA},
            "O1-M2": {'ref1': self.TTRef.O1, 'ref2': self.TTRef.RPA},
            "O2-M1": {'ref1': self.TTRef.O2, 'ref2': self.TTRef.LPA},
            "E1-M2": {'ref1': self.TTRef.EL, 'ref2': self.TTRef.RPA}
        }
    
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
            # Labels
            s1 = f['data']['sleep_stages']['nonrem1'][()].flatten()
            s2 = f['data']['sleep_stages']['nonrem2'][()].flatten()
            s3 = f['data']['sleep_stages']['nonrem3'][()].flatten()
            rem = f['data']['sleep_stages']['rem'][()].flatten()
            udf = f['data']['sleep_stages']['undefined'][()].flatten()
            w = f['data']['sleep_stages']['wake'][()].flatten()
            
            stacked = np.stack([s1,s2,s3,rem,udf,w])
            y = np.argmax(stacked, axis=0)
            
            # Data
            
            dic = dict()
            
            dataframe = r.to_dataframe()
            print(dataframe)
            
            exit()
            #print(np.argmax(np.stack([s1,s2,s3,rem,udf,w]).shape, axis=0))
            #curr = None
            #for i in range(am):
            #    if (s1[i] == 1):
            #        new = 's1'
            #    if (s2[i] == 1):
            #        new = 's2'
            #    if (s3[i] == 1):
            #        new = 's3'
            #    if (rem[i] == 1):
            #        new = 'rem'
            #    if (udf[i] == 1):
            #        new = 'udf'
            #    if (w[i] == 1):
            #        new = 'wake'
            #    
            #    if curr != new:
            #        print(i)
            #        print((i+1)/6000)
            #        print(new)
            #        curr = new
                #print(i)
                #values = [s1c, s2c, s3c, remc, udfc, wc]
                #val_sum = sum(values)
                #assert val_sum == 1, 'values: {}'.format(values)
                
                #print(i)
                #print([s1c, s2c, s3c, remc, udfc, wc])
            #print(nonrem1.shape)
            #s1 = s1.flatten()[:100000]
            #print(s1.shape)
            #s1 = [i for i, x in enumerate(s1) if x==1]
            #s2 = [i for i, x in enumerate(s2) if x==1]
            #s3 = [i for i, x in enumerate(s3) if x==1]
            #rem = [i for i, x in enumerate(rem) if x==1]
            #udf = [i for i, x in enumerate(udf) if x==1]
            #w = [i for i, x in enumerate(w) if x==1]
            
            #print(dwe)

            #i = 0
            #while(1):
            #    first_epoch = nonrem1[0][i*6000:(i*6000)+6000]
            #    print(first_epoch.shape)
            #    result = np.all(first_epoch == first_epoch[0])
            #    i += 1
            #    print(result)
                

            #wake = f['data']['sleep_stages']['wake']
            #print(labels.shape)
            #print(nonrem1[()])
            #print(wake[()])

        #mat = scipy.io.loadmat(filebase+'.mat')
        #print(mat['val'][0])
        #mat = scipy.io.loadmat(filebase+'-arousal.mat')
        #print(mat.keys())
        
        return dic, y