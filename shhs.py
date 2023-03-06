from .sdo_base import SleepdataOrg

class Shhs(SleepdataOrg):

    def sample_rate(self):
        return 125
        
    def dataset_name(self):
        return "shhs"
    
    def label_mapping(self):
        return {
            '0': self.Labels.Wake,
            '1': self.Labels.N1,
            '2': self.Labels.N2,
            '3': self.Labels.N3,
            '4': self.Labels.Unknown,
            '5': self.Labels.REM,
        }
    
    def channel_mapping(self):
        return {
            "EEG(sec)": {'ref1': self.TTRef.C3, 'ref2': self.TTRef.RPA},
            "EEG": {'ref1': self.TTRef.C4, 'ref2': self.TTRef.LPA},
            "EOG(L)": {'ref1': self.TTRef.EL, 'ref2': self.TTRef.Nz},
            "EOG(R)": {'ref1': self.TTRef.ER, 'ref2': self.TTRef.Nz}
        }
        