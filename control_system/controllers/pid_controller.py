import time
from .controller_model import ControllerModel


class PIDController(ControllerModel):
    """PID Controller """

    class Meta:
        slug = "pid"

    def __init__(self, **kwargs):
        self._Kp = kwargs.get("P", 1.0)
        self._Ki = kwargs.get("I", 1.0)
        self._Kd = kwargs.get("D", 1.0)

        super().__init__(**kwargs)

    def update(self, set_point, feedback_value):
        error = set_point - feedback_value
        delta_error = error - self._last_error

        self._current_time = time.time()
        delta_time = self._current_time - self._last_time
        if delta_time < self._sample_time:
            return

        P_computed = self._Kp * error
        I_computed = self._Ki * error * delta_time
        D_computed = 0.0
        if delta_time > 0:
            D_computed = self._Kd * delta_error / delta_time

        self._last_time = self._current_time
        self._last_error = error

        output = P_computed + I_computed * D_computed
        output = self._min_value if output < self._min_value else output
        output = self._max_value if output > self._max_value else output
        return int(output)
