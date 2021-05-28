from control_system.constants import KP, KI, KD
from .base_controller_model import ControllerModel
from control_system.decorators import ensure_values_range

class PIDController(ControllerModel):
    """PID Controller """

    class Meta:
        slug = "pid"

    def __init__(self, **kwargs):
        self.terms = {
            KP : kwargs.get("P", 1.0),
            KI : kwargs.get("I", 1.0),
            KD : kwargs.get("D", 1.0),
        }
        self._last_I = 1

        super().__init__(**kwargs)


    def _compute_P_I_D(self, terms, error, last_error):
        P_computed = terms[KP] * error
        I_computed = self._last_I + terms[KI] * error * self._delta_time
        D_computed = terms[KD] * (error - last_error) / self._delta_time
        self._last_I = I_computed
        return P_computed + I_computed + D_computed

    @ensure_values_range
    def update(self, error, last_error):
        terms = self.terms
        if self._tuning_model:
            terms = self._tuning_model.add_tuning(self.terms)
        

        return self._compute_P_I_D(terms, error, last_error)
