import numpy as np

from .base_process_model import ProcessModel
from control_system.controllers.base_controller_model import ControllerModel


class TankFillingModel(ProcessModel):
    class Meta:
        slug = "tank-filling-model"
        control_value = "volume"

    @staticmethod
    def calculate_single_valve_flow(tank_area: float, valve: dict = {}) -> float:
        """Calculates single valve flow computed as how much height increases in the tank thanks to the given valve

        Parameters:
        tank_area -- area of the tank given in the main simulation configuration
        valve -- dict single valve data (capacity and degree of opening required)

        Returns:
        float -- single valve flow
        """
        valve_capacity, valve_open = valve.get("valve_capacity"), valve.get("valve_open_percent")
        valve_flow = valve_capacity / tank_area * (valve_open / 100)
        return valve_flow

    @staticmethod
    def calculate_valves_flow(tank_area: float, valves_list: list) -> float:
        """Calculates valve flow (input and volume increase/decrease) for all the valves in the given valves list (input valves or output valves).

        Parameters:
        tank_area -- area of the tank given in the main simulation configuration
        valves_list -- list with valves dicts for single valve type (input valves or the output valves)

        Returns:
        tuple with:
            valves_liquid_volume_increase - current change of liquid volume from all valves of single type(input or output) [dm³]
            valves_liquid_height_increase - current change of liquid height from all valves of single type(input or output) [dm]
        """
        valves_liquid_height_sum = 0

        for valve in valves_list:
            single_valve_flow = TankFillingModel.calculate_single_valve_flow(tank_area, valve)
            valves_liquid_height_sum += single_valve_flow

        return valves_liquid_height_sum

    def _calculate_process_flow(self, x: list, time: list, tank_area: float, valves_config: dict) -> list:
        """Calculates valve flow for all the input valves and separately for all the output valves.
        Then calculates liquid height changes in time and liquid volume changes in time.

        Parameters:
        x -- list with level and volume values calculated in previous step (as start parameters)
        time -- list with time moment for the current simulation step
        tank_area -- area of the tank given in the main simulation configuration
        valves_config -- valves configuration given in the main simulation configuration

        Returns:
        list of:
            dHdt - liquid height change calculated in this simulation step
            dVdt - liquid volume change calculated in this simulation step
        """
        output_level_increase = TankFillingModel.calculate_valves_flow(
            tank_area, valves_config.get("output_valves", [])
        )
        input_level_increase = TankFillingModel.calculate_valves_flow(tank_area, valves_config.get("input_valves", []))

        dHdt = input_level_increase - output_level_increase
        dVdt = input_level_increase * tank_area - output_level_increase * tank_area
        return [dHdt, dVdt]

    def _prepare_results_collections(self, ts, config: dict = {}, controller: ControllerModel = None):
        """Creates data dictionaries for storing simulation results for the model."""

        level = config["initial_liquid_level"]
        volume = level * self._tank_area
        valves_config = config["valves_config"]

        self._results["level"] = self._prepare_data(ts, "level [dm]", [level], "liquid level")
        self._results["volume"] = self._prepare_data(ts, "volume [dm³]", [volume], "liquid volume")
        for i, valve in enumerate(valves_config["input_valves"]):
            self._results[f"input_{i}_opens"] = self._prepare_data(
                ts, f"input_{i}_opens", [valve["valve_open_percent"]], f"inputs opens percentages"
            )

        if controller:
            assert len(controller.set_points) == len(ts)
            self._results["set_points"] = {"values": controller.set_points, "control_value": "volume"}

    def _control_valves_open_percentage(
        self, controller: ControllerModel, set_point: float, feedback_value: float, valves_config: dict
    ) -> dict:
        """Spcifies how the valves are gonna be selected for the automatic regulation.
        For tank filling model the controller takes first valve and updates it unless it is fully opened/closed; if the set_point value is then still not achieved, takes next valve.
        """
        error = set_point - feedback_value
        VOLUME_TOO_HIGH = (error < 0) 
        #if the volume is too high, order reverse so the 'stronger' valves will be closed
        valves = sorted(valves_config.get("input_valves"), key=lambda i: i["valve_capacity"], reverse=VOLUME_TOO_HIGH)
        for i, valve in enumerate(valves):
            valve["valve_open_percent"] = controller.update(error, self._last_error, set_point = set_point)
            percentage = valve["valve_open_percent"]
            if (set_point != feedback_value and (percentage != 0 and percentage != 100)) or set_point == feedback_value:
                break
        self._last_error = error
        return valves_config
    
        

    def run(self, config: dict = {}, controller: ControllerModel = None) -> dict:
        ts = np.linspace(0, int(config["simulation_time"]), int(config["steps_count"]))
        level = config["initial_liquid_level"]
        volume = level * self._tank_area
        valves_config = config["valves_config"]

        self._prepare_results_collections(ts, config, controller)

        for i in range(len(ts) - 1):
            level, volume = self._run_process(ts, i, [level, volume], valves_config, controller, volume)
            level = self._validate_result(level, min_value=0, max_value=self.max_level)
            volume = self._validate_result(volume, min_value=0)
            self._results["level"]["results"].append(level)
            self._results["volume"]["results"].append(volume)
            for i, valve in enumerate(valves_config["input_valves"]):
                self._results[f"input_{i}_opens"]["results"].append(valve["valve_open_percent"])
        return self._results
