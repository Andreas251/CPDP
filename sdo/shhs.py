from .sdo_base import SleepdataOrg

class Shhs(SleepdataOrg):

    def channel_mapping(self):
        return {
            "EEG(sec)": self.Mapping(self.TTRef.C3, self.TTRef.RPA),
            "EEG": self.Mapping(self.TTRef.C4, self.TTRef.LPA),
            "EOG(L)": self.Mapping(self.TTRef.EL, self.TTRef.Nz),
            "EOG(R)": self.Mapping(self.TTRef.ER, self.TTRef.Nz)
        }
        