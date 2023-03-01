import os
from abc import ABC, abstractmethod
from scipy.signal import resample_poly
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from h5py import File


class SleepdataPipeline(ABC):
    def __init__(self, max_num_records, dataset_path, output_path, port_on_init=True, data_format="hdf5"):
        self.max_num_records = max_num_records
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
            self.port_data(write_function=self.write_function)
        
    
    @property
    @abstractmethod
    def sleep_stage_dict(self):
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
    def read_psg(self, record_path):
        """
        Function to read PSG data along with labels. Data can be in the format of HDF, EDF and so on.
        
        Returns 
        x: A dictionary of data from available PSG channels for a record in the dataset. Data channels must contain data at sample rate 128 Hz. Dictionary keys must be prepended with either "EEG " or "EOG " depending on type of channel.
        y: A list of labels for 30 second data chunks for all records in dataset.
        subject_number: Number of subject from dataset.
        record_number: Number of record for given subject
        """
        pass
    
    
    def channel_mapping(self):
        """
        Function for mapping to new channel name in following format: 
        {channel type}_{electrode 1}-{electrode 2}
        Example: EEG_C3-M2
        
        The EEG placements follows the 10-20/10-10 EEG naming convention.
        https://en.wikipedia.org/wiki/10%E2%80%9320_system_(EEG)
        
        """
        return {
            "EOG horizontal": "EOG_E1-E2", 
            "EEG Fpz-Cz": "EEG_Fpz-Cz",
            "EEG Pz-Oz": "EEG_Pz-Oz",
            "E1-M2": "EOG_E1-M2",
            "E2-M2": "EOG_E2-M2",
            "C3-M2": "EEG_C3-M2",
            "C4-M1": "EEG_C4-M1",
            "F3-M2": "EEG_F3-M2",
            "F4-M1": "EEG_F4-M1",
            "O1-M2": "EEG_O1-M2",
            "O2-M1": "EEG_O2-M1"
        }
    
    
    def relevant_channels(self):
        return self.channel_mapping().keys()
    
    
    def resample_channel(self, channel, input_rate, output_rate=128):
        """
        Function to resample a single data channel to the desired sample rate.
        
        Default output rate = 128 Hz
        """

        channel_resampled = resample_poly(
            channel,
            output_rate,
            input_rate,
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
        
        
    def port_data(self, write_function):
        record_dirs = os.listdir(self.dataset_path)
        
        if self.max_num_records:
            record_dirs = record_dirs[:self.max_num_records]
        
        for record_dir in record_dirs:
            record_path = self.dataset_path + record_dir + "/"
            
            x, y, subject_number, record_number = self.read_psg(record_path)
            
            write_function(
                f"{self.output_path}/",
                subject_number,
                record_number,
                x, 
                y
            ) 
        