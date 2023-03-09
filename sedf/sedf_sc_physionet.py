import os

from .base_sedf import Base_Sedf


class Sedf_SC_PhysioNet(Base_Sedf):
    """
    ABOUT THIS DATASET
    
    The naming convention of records is as follows: SC4ssNE0 where:
    SC: Sleep Cassette study.
    ss: Subject number (notice that most subjects has 2 records), e.g. 00.
    N: Night (1 or 2).
    
    Channels included in dataset: ['EEG Fpz-Cz', 'EEG Pz-Oz', 'EOG horizontal', 'Resp oro-nasal', 'EMG submental', 'Temp rectal', 'Event marker'].

    
    EEG and EOG signals were each sampled at 100Hz.
    """ 
    def dataset_name(self):
        return "sedf_sc"
    
    
    def list_records(self, basepath):
        paths_dict = {}
        
        record_paths = os.listdir(basepath)
        psg_list = [s for s in record_paths if "PSG" in s]
        hyp_list = [s for s in record_paths if "Hypnogram" in s]
        
        assert len(psg_list) == len(hyp_list)
        
        for psg in psg_list:
            record_name = psg.split("-")[0]
            psg_path = f"{basepath}{psg}"
            
            # Finding hypnogram matching PSG
            hyp_file_matches = [s for s in hyp_list if record_name[:6] in s]
            assert len(hyp_file_matches) == 1
            
            hyp_path = f"{basepath}{hyp_file_matches[0]}"
            
            paths_dict[record_name] = [(psg_path, hyp_path)]
        
        return paths_dict
