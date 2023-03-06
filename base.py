import os
from abc import ABC, abstractmethod
from scipy.signal import resample_poly
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from h5py import File
from enum import Enum, auto, IntEnum

# TODO
# Fix sedf

class SleepdataPipeline(ABC):
    def __init__(
        self, 
        max_num_subjects, 
        dataset_path, 
        output_path, 
        port_on_init=True, 
        data_format="hdf5"
    ):
        self.max_num_subjects = max_num_subjects
        self.dataset_path = dataset_path
        self.output_path = output_path
        
        if data_format == "hdf5":
            self.write_function = self.write_record_to_database_hdf5
        elif data_format == "parquet":
            self.write_function = self.write_record_to_database_parquet
        else:
            print("Invalid data format. Must be one of [hdf5, parquet].")
            exit(1)
        
        if port_on_init:
            paths_dict = self.list_records(basepath=self.dataset_path)
            self.port_data(write_function=self.write_function, paths_dict=paths_dict)
            
    class Labels(IntEnum):
        Wake = 0
        N1 = 1
        N2 = 2
        N3 = 3
        REM = 4
        
    class TTRef(Enum):
        Fp1 = auto()
        Fp2 = auto()
        F7 = auto()
        F3 = auto()
        Fz = auto()
        F4 = auto()
        F8 = auto()
        A1 = auto()
        T3 = auto()
        C3 = auto()
        Cz = auto()
        C4 = auto()
        T4 = auto()
        A2 = auto()
        T5 = auto()
        P3 = auto()
        Pz = auto()
        P4 = auto()
        T6 = auto()
        O1 = auto()
        O2 = auto()
        EL = auto()
        ER = auto()

        def __str__(self):
            return self.name
    
    
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
    
    
    @abstractmethod
    def list_records(self):
        """
        Function to list needed information about original dataset structure, in order for read_psg to have needed information about where to find PSGs and hypnograms.
        
        Return
        paths_dict: A dictionary containing a key for each subject. Each subject has a list of record paths in the form of a tuple i.e a path for PSG and a path for hypnogram.
        """
        pass
    
    
    @abstractmethod
    def read_psg(self, record):
        """
        Function to read PSG data along with labels. Data can be in the format of HDF, EDF and so on.
        
        Returns 
        x: A dictionary of data from available PSG channels for a record in the dataset. Data channels must contain data at sample rate 128 Hz. Dictionary keys must be prepended with either "EEG " or "EOG " depending on type of channel.
        y: A list of labels for 30 second data chunks for all records in dataset.
        """
        pass
    
    @abstractmethod
    def channel_mapping(self):
        """
        Function for mapping to new channel name in following format: 
        {channel type}_{electrode 1}-{electrode 2}
        Example: EEG_C3-M2
        
        The EEG placements follows the 10-20/10-10 EEG naming convention.
        https://en.wikipedia.org/wiki/10%E2%80%9320_system_(EEG)
        
        """
        pass
    
    def __mapping(self,ctype, ref1, ref2):
        return '{t}_{r1}-{r2}'.format(t=ctype,
                                      r1=ref1,
                                      r2=ref2)
    
    def __map_channels(self, dic):
        new_dict = dict()
        
        for key in dic.keys():
            mapping = self.channel_mapping()
            
            try:
                chnl = mapping[key]
            except KeyError:
                continue
                
            ref1 = chnl['ref1']
            ref2 = chnl['ref2']
            
            ctype = 'EOG' if ref1 in [self.TTRef.EL,
                                      self.TTRef.ER] else 'EEG'
            
            new_key = self.__mapping(ctype, ref1, ref2)
            new_dict[new_key] = self.resample_channel(dic[key]) # TODO: Test that resampling works
            
        return new_dict
    
    
    def __map_labels(self, labels):
        return list(map(lambda x: self.label_mapping()[x], labels))
    
    
    def resample_channel(self, channel, output_rate=128):
        """
        Function to resample a single data channel to the desired sample rate.
        
        Default output rate = 128 Hz
        """

        channel_resampled = resample_poly(
            channel,
            output_rate,
            self.sample_rate(),
            axis=0
        )

        return channel_resampled
    
    
    def write_record_to_database_parquet(self, output_basepath, subject_number, record_number, x, y):
        """
        Function to write PSG data along with labels to the shared database containing all datasets in Parquet format.
        """
        
        psg_table = pa.table(x)
        hyp_table = pa.table({"labels": y})
        
        output_path = output_basepath + f"s_{subject_number}/r_{record_number}/"
        
        Path(output_path).mkdir(parents=True, exist_ok=True) # Because Parquet does not create directory
        pq.write_table(psg_table, output_path + "psg.parquet")
        pq.write_table(hyp_table, output_path + "hypnogram.parquet")
        
        
    def write_record_to_database_hdf5(self, output_basepath, subject_number, record_number, x, y): 
        """
        Function to write PSG data along with labels to the shared database containing all datasets in HDF5 format.
        """
        Path(output_basepath).mkdir(parents=True, exist_ok=True)
        
        with File(f"{output_basepath}{self.dataset_name()}.hdf5", "a") as f:
            grp_subject = f.create_group(f"{subject_number}")
            subgrp_record = grp_subject.create_group(f"{record_number}")
            
            subsubgrp_psg = subgrp_record.create_group("psg")
            
            for channel_name, channel_data in x.items():
                subsubgrp_psg.create_dataset(channel_name, data=channel_data)
            
            subgrp_record.create_dataset("hypnogram", data=y)
        
        
    def port_data(self, write_function, paths_dict): # TODO: Test
        for subject_number in list(paths_dict.keys())[:self.max_num_subjects]:
            record_number = 0
            
            for record in paths_dict[subject_number]:
                x, y = self.read_psg(record)
    
                x = self.__map_channels(x)
                y = self.__map_labels(y)
         
                write_function(
                    f"{self.output_path}/",
                    subject_number,
                    record_number,
                    x, 
                    y
                )
                
                record_number = record_number + 1
  