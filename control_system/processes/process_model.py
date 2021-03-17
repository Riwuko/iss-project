class ProcessModel(object):
    def __init__(self, tank_area=1, min_level=0, max_level=20000):
        self.tank_area = tank_area
        self.min_level = min_level
        self.max_level = max_level

    @property
    def tank_area(self):
        return float(self._tank_area)

    @tank_area.setter
    def tank_area(self, value):
        self._tank_area = float(value) if float(value) > 0 else 1

    @property
    def min_level(self):
        return self._min_level

    @min_level.setter
    def min_level(self, value):
        self._min_level = float(value) if float(value) >= 0 else 0

    @property
    def max_level(self):
        return self._max_level

    @max_level.setter
    def max_level(self, value):
        self._max_level = float(value) if float(value) >= 0 else 1

    def run(self, config={}):
        raise NotImplementedError
