from control_system.controllers.base_controller_model import ControllerModel
from scipy.integrate import odeint


class ProcessModel(object):
    def __init__(self, tank_area=1, min_level=0, max_level=None):
        self.tank_area = tank_area
        self.min_level = min_level
        self.max_level = max_level
        self._last_error = 0.0
        self._results = {}

    @staticmethod
    def get_default_config():
        return {
            "tank_area": 1,
            "simulation_time": 10,
            "steps_count": 100,
            "initial_liquid_level": 0,
            "initial_liquid_concentration_A": 0,
            "valves_config": {
                "input_valves": [
                    {
                        "valve_capacity": 5.0,
                        "valve_open_percent": 10,
                        "liquid_config": {
                            "liquid_concentration_A": 10,
                        },
                    },
                    {
                        "valve_capacity": 6,
                        "valve_open_percent": 10,
                        "liquid_config": {
                            "liquid_concentration_A": 100,
                        },
                    },
                ],
                "output_valves": [
                    {
                        "valve_capacity": 5.0,
                        "valve_open_percent": 10,
                    }
                ],
            },
        }

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

    def _calculate_process_flow(self):
        raise NotImplementedError

    def _control_valves_open_percentage(
        self, controller: ControllerModel, set_point: float, controll_value: float, valves_config: dict
    ) -> dict:
        raise NotImplementedError

    def _prepare_data(self, ts: list, name: str, results: list, title: str) -> dict:
        return {
            "name": name,
            "results": results,
            "title": title,
            "times": ts,
        }

    def _prepare_results_collections(self, ts, config: dict = {}, controller: ControllerModel = None):
        raise NotImplementedError

    def _validate_result(self, result_value: float, min_value: float = None, max_value: float = None) -> float:
        result_value = min_value if min_value is not None and result_value < min_value else result_value
        result_value = max_value if max_value is not None and result_value > max_value else result_value
        return result_value

    def _run_process(
        self,
        ts: list,
        i: int,
        start_values=[],
        valves_config: dict = {},
        controller: ControllerModel = None,
        feedback_value: float = None,
    ) -> list:

        FUZZY_CONTROLLER = controller and controller.fuzzy_logic
        PID_CONTROLLER = controller and not FUZZY_CONTROLLER

        if PID_CONTROLLER and not(all(value == 0 for value in controller.terms.values())):
            valves_config = self._control_valves_open_percentage(
                controller, self._results["set_points"]["values"][i], feedback_value, valves_config
            )

        elif FUZZY_CONTROLLER:
            valves_config = self._control_valves_open_percentage(
                controller, self._results["set_points"]["values"][i], feedback_value, valves_config
            )

            
        y = odeint(
            self._calculate_process_flow,
            start_values,
            [ts[i], ts[i + 1]],
            args=(self._tank_area, valves_config),
        )
        return y[-1]

    def run(self, config: dict = {}, controller: ControllerModel = None):
        """Runs the model process simulation. Creates time array due to sent configuration
        and uses scipy.odeint for ordinary differential equation solving in the loop over time.

        Parameters:
        config -- simulation configuration

        Returns:
        dict -- json formatted simulation data and results

        """
        raise NotImplementedError
