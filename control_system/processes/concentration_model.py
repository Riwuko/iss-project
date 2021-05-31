import numpy as np

from .base_process_model import ProcessModel
from control_system.controllers.base_controller_model import ControllerModel


class ConcentrationModel(ProcessModel):
    class Meta:
        slug = "concentration-model"
        control_value = "concentration"

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
        valve_flow = valve_capacity * (valve_open / 100)
        return valve_flow

    @staticmethod
    def calculate_valves_flow(tank_area: float, valves_list: list, whole_concentration: float) -> tuple:
        """Calculates valve flow (input and volume increase/decrease) for all the valves in the given valves list (input valves or output valves).

        Parameters:
        tank_area -- area of the tank given in the main simulation configuration
        valves_list -- list with valves dicts for single valve type (input valves or the output valves)
        whole_concentration -- current percentage concentration of the A substance in the whole tank liquid

        Returns:
        tuple with:
            valves_liquid_volume_increase - current change of liquid volume from all valves of single type(input or output) [dm³]
            valves_liquid_height_increase - current change of liquid height from all valves of single type(input or output) [dm]
        """
        valves_liquid_volume_increase = 0
        valves_liquid_height_sum = 0

        for valve in valves_list:
            substance_concentration = valve.get("liquid_config", {}).get("liquid_concentration_A")
            if not substance_concentration:  # then it is output valve
                substance_concentration = whole_concentration
            single_valve_flow = ConcentrationModel.calculate_single_valve_flow(tank_area, valve)

            valves_liquid_volume_increase += single_valve_flow * substance_concentration
            valves_liquid_height_sum += single_valve_flow

        return (valves_liquid_volume_increase, valves_liquid_height_sum)

    def _calculate_process_flow(self, x: list, time: list, tank_area: float, valves_config: dict) -> list:
        """Calculates valve flow for all the input valves and separately for all the output valves.
        Then calculates liquid precentage concentration of the A substance changes in time,
        liquid height changes in time and liquid volume changes in time.

        Parameters:
        x -- list with concentration, level and volume values calculated in previous step (as start parameters)
        time -- list with time moment for the current simulation step
        tank_area -- area of the tank given in the main simulation configuration
        valves_config -- valves configuration given in the main simulation configuration

        Returns:
        list of:
            dCadt - liquid percentage concentration of the A substance in this simulation step [%]
            dHdt - liquid height change calculated in this simulation step [dm]
            dVdt - liquid volume change calculated in this simulation step [dm³]
        """
        percentage_concentration = x[0]
        volume = x[2]

        (output_tank_substance_volume, output_volume_increase,) = ConcentrationModel.calculate_valves_flow(
            tank_area, valves_config.get("output_valves", []), percentage_concentration
        )
        (input_tank_substance_volume, input_volume_increase,) = ConcentrationModel.calculate_valves_flow(
            tank_area, valves_config.get("input_valves", []), percentage_concentration
        )

        dHdt = input_volume_increase / tank_area - output_volume_increase / tank_area
        dVdt = input_volume_increase - output_volume_increase
        dCadt = (input_tank_substance_volume - output_tank_substance_volume) / volume - (
            percentage_concentration * dVdt
        ) / volume
        return [dCadt, dHdt, dVdt]

    def _prepare_results_collections(self, ts, config: dict = {}, controller: ControllerModel = None):
        """Creates data dictionaries for storing simulation results for the model."""
        level = config["initial_liquid_level"] if config["initial_liquid_level"] > 0 else 0.01
        volume = level * self._tank_area
        concentration = config["initial_liquid_concentration_A"]
        valves_config = config["valves_config"]

        self._results["level"] = self._prepare_data(ts, "level [dm]", [level], "liquid level")
        self._results["volume"] = self._prepare_data(ts, "volume [dm³]", [volume], "liquid volume")
        self._results["concentration"] = self._prepare_data(
            ts, "concentration [%]", [concentration], "liquid concentration of A"
        )
        for i, valve in enumerate(valves_config["input_valves"]):
            self._results[f"input_{i}_opens"] = self._prepare_data(
                ts, f"input_{i}_opens", [valve["valve_open_percent"]], f"inputs opens percentages"
            )

        if controller:
            assert len(controller.set_points) == len(ts)
            self._results["set_points"] = {"values": controller.set_points, "control_value": "concentration"}

    def _control_valves_open_percentage(
        self, controller: ControllerModel, set_point: float, feedback_value: float, valves_config: dict
    ) -> dict:
        """Spcifies how the valves are gonna be selected for the automatic regulation.
        """
        error = set_point - feedback_value

        CONCENTRATION_TOO_HIGH = (error < 0) 
        CONCENTRATION_TOO_LOW = (error > 0)
        
        for valve in valves_config.get("input_valves"):
            concentration = valve["liquid_config"]["liquid_concentration_A"]

            if CONCENTRATION_TOO_HIGH: #error < 0 so pid response for error will be lower than 0: "close!"
                do_open = -error
                do_close = error
                if concentration > set_point: #concentration higher
                    valve["valve_open_percent"] = controller.update(do_close, self._last_error, set_point = set_point)
                elif concentration <= set_point: #concentration lower 
                    valve["valve_open_percent"] = controller.update(do_open, self._last_error, set_point = set_point)
            elif CONCENTRATION_TOO_LOW: #error > 0 so pid response for error will be greater than 0: "open!"
                do_open = error
                do_close = -error 
                if concentration >= set_point:
                    valve["valve_open_percent"] = controller.update(do_open, self._last_error, set_point = set_point)
                elif concentration < set_point:
                    valve["valve_open_percent"] = controller.update(do_close, self._last_error, set_point = set_point)
            
        self._last_error = error
        return valves_config

    def run(self, config: dict = {}, controller: ControllerModel = None) -> dict:
        ts = np.linspace(0, int(config["simulation_time"]), int(config["steps_count"]))
        level = config["initial_liquid_level"] if config["initial_liquid_level"] > 0 else 0.01
        volume = level * self._tank_area
        concentration = config["initial_liquid_concentration_A"]
        valves_config = config["valves_config"]

        self._prepare_results_collections(ts, config, controller)

        for i in range(len(ts) - 1):
            concentration, level, volume = self._run_process(
                ts, i, [concentration, level, volume], valves_config, controller, concentration
            )

            level = self._validate_result(level, min_value=0)
            volume = self._validate_result(volume, min_value=0.01)
            max_concentration = 100 if level != 0 else 0
            concentration = self._validate_result(concentration, min_value=0, max_value=max_concentration)
            self._results["concentration"]["results"].append(concentration)
            self._results["level"]["results"].append(level)
            self._results["volume"]["results"].append(volume)
            for i, valve in enumerate(valves_config["input_valves"]):
                self._results[f"input_{i}_opens"]["results"].append(valve["valve_open_percent"])
        return self._results
