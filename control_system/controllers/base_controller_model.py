
class ControllerModel(object):
    def __init__(self, **kwargs):
        self.fuzzy_logic = False
        self._sample_time = 0.00
        self.max_value = kwargs.get("max_value", 20000)
        self.min_value = kwargs.get("min_value", 0)
        self._tuning_model = kwargs.get("tuner")
        self.set_points = kwargs.get("set_points", [])
        self._delta_time = kwargs.get("delta_time")

        self.restart()

    def restart(self):
        self._last_error = 0.0

    @property
    def set_points(self):
        return self._set_points

    @set_points.setter
    def set_points(self, setpoints: list):
        stepsCount = int(setpoints[-1]["range_to"])
        setpoints_list = [0] * stepsCount
        range_from = 0
        for i, setpoint in enumerate(setpoints):
            range_to = int(setpoint["range_to"])
            count = range_to - range_from
            setpoints_list[range_from:range_to] = [setpoint["value"]] * count
            range_from = int(setpoint["range_to"])
        self._set_points = setpoints_list

    @staticmethod
    def get_default_config(time_steps: int, simulation_time: int):
        time_steps = int(time_steps)
        set_points = {"range_to": time_steps, "value": 20}

        return {
            "set_points": [set_points],
            "min_value": 0,
            "max_value": 100,
            "P": 5.0,
            "I": 2.8,
            "D": 1.0,
            "delta_time": int(simulation_time)/time_steps,
        }


    def update(self):
        raise NotImplementedError
