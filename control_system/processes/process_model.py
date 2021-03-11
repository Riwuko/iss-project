
class ProcessModel:

    def __init__(self, tank_area=1, min_level=0, max_level=20000):
        self._tank_area = tank_area
        self._min_level = min_level
        self._max_level = max_level
    
    def run(self, config={}):
        raise NotImplementedError
