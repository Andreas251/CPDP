from .sdo_base import SleepdataOrg

class Mesa(SleepdataOrg):    
    def label_mapping(self):
        return {
            '0': self.Labels.Wake,
            '1': self.Labels.N1,
            '2': self.Labels.N2,
            '3': self.Labels.N3,
            '4': self.Labels.UNKNOWN,
            '5': self.Labels.REM,
        }
    
    def channel_mapping(self):
        return {
            "EOG-L": {'ref1': self.TTRef.EL, 'ref2': self.TTRef.Fpz},
            "EOG-R": {'ref1': self.TTRef.ER, 'ref2': self.TTRef.Fpz},
            "EEG1": {'ref1': self.TTRef.Fz, 'ref2': self.TTRef.Cz},
            "EEG2": {'ref1': self.TTRef.Cz, 'ref2': self.TTRef.Oz},
            "EEG3": {'ref1': self.TTRef.C4, 'ref2': self.TTRef.LPA}
        }
        