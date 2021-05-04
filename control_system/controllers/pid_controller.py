import time
from .base_controller_model import ControllerModel
from control_system.decorators import ensure_values_range

class PIDController(ControllerModel):
    """PID Controller """

    class Meta:
        slug = "pid"

    def __init__(self, **kwargs):
        self._Kp = kwargs.get("P", 1.0)
        self._Ki = kwargs.get("I", 1.0)
        self._Kd = kwargs.get("D", 1.0)

        super().__init__(**kwargs)


    def _compute_P_I_D(self, error, delta_error, delta_time):
        P_computed = self._Kp * error
        I_computed = self._Ki * error * delta_time
        D_computed = 0.0
        if delta_time > 0:
            D_computed = self._Kd * delta_error / delta_time
        return P_computed, I_computed, D_computed

    @ensure_values_range
    def update(self, set_point, feedback_value):
        error = set_point - feedback_value
        delta_error = error - self._last_error

        self._current_time = time.time()
        delta_time = self._current_time - self._last_time
        if delta_time < self._sample_time:
            return

        if self._tuning_model:
            P_computed, I_computed, D_computed = self._tuning_model.add_tuning(0, self._Kp, self._Ki, self._Kd, error, delta_error, delta_time)
        else:
            P_computed, I_computed, D_computed = self._compute_P_I_D(error, delta_error, delta_time)
        

        self._last_time = self._current_time
        self._last_error = error

        return int(P_computed + I_computed * D_computed)
