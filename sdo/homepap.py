from .sdo_base import SleepdataOrg

class Homepap(SleepdataOrg):
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
        #d = multi_key_dict()
        #d["E1"] = Mapping(self.TTRef.C3, self.TTRef.Fpz)
        #d["E2"] = Mapping(self.TTRef.C4, self.TTRef.Fpz)
        #d["F3"] = Mapping(self.TTRef.LPA, self.TTRef.Fpz)
        #d["F4"] = Mapping(self.TTRef.RPA, self.TTRef.Fpz)
        #d["C3"] = Mapping(self.TTRef.ER, self.TTRef.Fpz)
        #d["C4"] = Mapping(self.TTRef.EL, self.TTRef.Fpz)
        #
        #d["O1"] = Mapping(self.TTRef.C3, self.TTRef.Fpz)
        #d["O2"] = Mapping(self.TTRef.C4, self.TTRef.Fpz)
        #d["M1"] = Mapping(self.TTRef.LPA, self.TTRef.Fpz)
        #d["M2"] = Mapping(self.TTRef.RPA, self.TTRef.Fpz)
        #d["E1-M2"] = Mapping(self.TTRef.ER, self.TTRef.Fpz)
        #d["E2-M1"] = Mapping(self.TTRef.EL, self.TTRef.Fpz)
        #return d
        
        return {
            "E1": Mapping(self.TTRef.EL, self.TTRef.Fpz),
            "E2": Mapping(self.TTRef.ER, self.TTRef.Fpz),
            "F3": Mapping(self.TTRef.F3, self.TTRef.Fpz),
            "F4": Mapping(self.TTRef.F4, self.TTRef.Fpz),
            "C3": Mapping(self.TTRef.C3, self.TTRef.Fpz),
            "C4": Mapping(self.TTRef.C4, self.TTRef.Fpz),
            "O1": Mapping(self.TTRef.O1, self.TTRef.Fpz),
            "O2": Mapping(self.TTRef.O2, self.TTRef.Fpz),
            "M1": Mapping(self.TTRef.LPA, self.TTRef.Fpz),
            "M2": Mapping(self.TTRef.RPA, self.TTRef.Fpz),
            "E1-M2": Mapping(self.TTRef.EL, self.TTRef.RPA),
            "E2-M1": Mapping(self.TTRef.ER, self.TTRef.LPA),
            "F3-M2": Mapping(self.TTRef.F3, self.TTRef.RPA),
            "F4-M1": Mapping(self.TTRef.F4, self.TTRef.LPA),
            "C3-M2": Mapping(self.TTRef.C3, self.TTRef.RPA),
            "C4-M1": Mapping(self.TTRef.C4, self.TTRef.LPA),
            "O1-M2": Mapping(self.TTRef.O1, self.TTRef.RPA),
            "O2-M1": Mapping(self.TTRef.O2, self.TTRef.LPA)
        }
        