
class TunerModel(object):
    
    def add_tuning(self, terms:dict={})->dict:
        raise NotImplementedError

    @staticmethod
    def get_default_config():
        return {
            "amplification_factor": 8,
            "oscillation_period": 10,
        }
