import numpy as np
from scipy.integrate import odeint

from .process_model import ProcessModel


class TankFillingModel(ProcessModel):
    class Meta:
        slug = "tank-filling-model"

    @staticmethod
    def calculate_single_valve_flow(tank_area:float, valve:dict={})->float:
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
    def calculate_valves_flow(tank_area:float, valves_list:list)->float:
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
        valves_amount = len(valves_list)

        #loop over all the valves in the valves_list
        for i in range(valves_amount):
            valve = valves_list[i]
            single_valve_flow = TankFillingModel.calculate_single_valve_flow(tank_area, valve)
            valves_liquid_height_sum += single_valve_flow

        return valves_liquid_height_sum


    @staticmethod
    def calculate_level_increase(x:list, time:list, tank_area:float, valves_config:dict)->list:
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
        input_level_increase = TankFillingModel.calculate_valves_flow(
            tank_area, valves_config.get("input_valves", [])
        )

        dHdt = input_level_increase - output_level_increase
        dVdt = input_level_increase*tank_area - output_level_increase*tank_area
        return [dHdt, dVdt]

    def _validate_result(self, result_value:float, min_value:float=None, max_value:float=None)->float:
        result_value = min_value if min_value and result_value < min_value else result_value
        result_value = max_value if max_value and result_value > max_value else result_value
        return result_value

    def _get_results_dict(self, level_results:list, volume_results:list, ts:list)->dict:
        return [
                {
                    "name": "level [dm]",
                    "results": level_results,
                    "times": ts,
                    "title": "Tank filling - liquid level",
                },
                {
                    "name": "volume [dm³]",
                    "results": volume_results,
                    "times": ts,
                    "title": "Tank filling - liquid volume",
                }
            ]

    def run(self, config:dict={})->dict:
        ts = np.linspace(0, int(config["simulation_time"]), int(config["t_steps"]))

        level = config["initial_liquid_level"]
        volume = level * self._tank_area

        level_results = np.ones(len(ts)) * level
        volume_results = np.ones(len(ts)) * volume
        valves_config = config["valves_config"]

        for i in range(len(ts) - 1):
            t = [ts[i], ts[i + 1]]
            y = odeint(
                TankFillingModel.calculate_level_increase,
                [level, volume],
                t,
                args=(self._tank_area, valves_config),
            )
            level = self._validate_result(y[-1][0], min_value=0, max_value=self.max_level)
            volume = self._validate_result(y[-1][1], min_value=0)
            level_results[i + 1] = level
            volume_results[i + 1] = volume
        return self._get_results_dict(level_results, volume_results, ts)
        
