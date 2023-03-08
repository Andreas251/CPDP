from .sdo_base import SleepdataOrg

# Does not work at the moment because of different samplerates across records.

class Cfs(SleepdataOrg):
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
            "C3": {'ref1': self.TTRef.C3, 'ref2': self.TTRef.Fpz},
            "C4": {'ref1': self.TTRef.C4, 'ref2': self.TTRef.Fpz},
            "M1": {'ref1': self.TTRef.LPA, 'ref2': self.TTRef.Fpz},
            "M2": {'ref1': self.TTRef.RPA, 'ref2': self.TTRef.Fpz},
            "LOC": {'ref1': self.TTRef.EL, 'ref2': self.TTRef.Fpz},
            "ROC": {'ref1': self.TTRef.ER, 'ref2': self.TTRef.Fpz}
        }
        