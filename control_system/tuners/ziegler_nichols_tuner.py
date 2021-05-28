from .base_tuner_model import TunerModel
from control_system.constants import KD, KI, KP

class ZieglerNicholsTunerModel(TunerModel):
    """Ziegler Nichols PID Tunning Method """
    class Meta:
        slug = "Ziegler-Nichols"

    def __init__(self, **kwargs):
        """
        Ku - critical amplification factor
        Pu - period of oscillation 
        """
        
        self._Ku = kwargs.get("amplification_factor", 12)
        self._Pu = kwargs.get("oscillation_period", 12.1)

    def _calculate_P(self, terms, factor=0.5):
        if terms[KP]==0:
            return 0
        return self._Ku * factor
    
    def _calculate_I(self, terms):
        if terms[KI]==0:
            return 0
        return self._Pu / 1.2

    def _calculate_D(self, terms):
        if terms[KD]==0:
            return 0
        return self._Pu / 8


    def _tune_PID(self, terms, P_factor=0.5):
        return {KP: self._calculate_P(terms, P_factor), KI: self._calculate_I(terms), KD: self._calculate_D(terms)}

    def add_tuning(self, terms:dict)->dict:
        """
        Calculating the setting of the controller with Ziegler Nichols Tuning Method. 
        """
        if self._Pu<=0 and self._Ku<=0:
            return terms
            
        P = terms[KP] != 0
        I = terms[KI] != 0
        D = terms[KD] != 0

        if P and I and D: 
            tuned_terms = self._tune_PID(terms, P_factor = 0.6)
        if (P and I and not D) or (P and D and not I) or (I and D and not P):
            tuned_terms = self._tune_PID(terms, P_factor=0.45)
        if P or I or D:
            tuned_terms = self._tune_PID(terms, P_factor=0.5)

        return tuned_terms
        

