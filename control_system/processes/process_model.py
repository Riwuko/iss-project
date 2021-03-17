class ProcessModel(object):
    def __init__(self, tank_area=1, min_level=0, max_level=None):
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
        if value:
            self._min_level = float(value) if float(value) >= 0 else 0
        else:
            self._min_level = None

    @property
    def max_level(self):
        return self._max_level

    @max_level.setter
    def max_level(self, value):
        if value:
            self._max_level = float(value) if float(value) >= 0 else 1
        else:
            self._max_level = None

    def _ensure_config_format(self, config:dict)->dict:
        """Takes simulation configuration and recursively changes all numeric values to float.

        Parameters:
        config -- simulation configuration

        Returns:
        dict - json formatted simulation configuration with all numbers as floats
        """
        raise NotImplementedError

    def _get_results_dict(self, *args, **kwargs):
        """Takes calculated simulation results as an array of floats and creates JSON formatted simulation data dict.
        
        Parameters:
        results_array -- simulation results array of floats

        Returns:
        dict -- json formatted simulation data and results

        """
        raise NotImplementedError

    def run(self, config={}):
        """Runs the model process simulation. Creates time array due to sent configuration 
        and uses scipy.odeint for ordinary differential equation solving in the loop over time.
        
        Parameters:
        config -- simulation configuration

        Returns:
        dict -- json formatted simulation data and results

        """
        raise NotImplementedError
