from .sdo_base import SleepdataOrg

class Mros(SleepdataOrg):
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
            "C3": Mapping(self.TTRef.C3, self.TTRef.Fpz),
            "C4": Mapping(self.TTRef.C4, self.TTRef.Fpz),
            "A1": Mapping(self.TTRef.LPA, self.TTRef.Fpz),
            "A2": Mapping(self.TTRef.RPA, self.TTRef.Fpz),
            "ROC": Mapping(self.TTRef.ER, self.TTRef.Fpz),
            "LOC": Mapping(self.TTRef.EL, self.TTRef.Fpz)
        }
        