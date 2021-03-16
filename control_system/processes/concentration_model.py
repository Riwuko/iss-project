import numpy as np
from scipy.integrate import odeint

from .process_model import ProcessModel


class ConcentrationModel(ProcessModel):
    class Meta:
        slug = "concentration-model"

    @staticmethod
    def calculate_single_valve_flow(tank_area, valve={}):
        valve_capacity, valve_open = valve.get("valve_capacity"), valve.get("valve_open_percent")
        valve_flow = valve_capacity * (valve_open / 100)
        return valve_flow

    @staticmethod
    def calculate_valves_flow(tank_area, valves_list, whole_concentration):
        valves_substance_volume_increase = 0
        valves_liquid_height_sum = 0
        input_valves_amount = len(valves_list)

        for i in range(input_valves_amount):
            valve = valves_list[i]
            substance_concentration = valve.get("liquid_config", {}).get("liquid_concentration_A") 
            if not substance_concentration: # then it is output valve
                substance_concentration = whole_concentration
            single_valve_flow = ConcentrationModel.calculate_single_valve_flow(tank_area, valve)

            valves_substance_volume_increase += (single_valve_flow * substance_concentration)
            valves_liquid_height_sum += single_valve_flow

        return (valves_substance_volume_increase, valves_liquid_height_sum)


    @staticmethod
    def calculate_percentage_concentration(x, time, tank_area, valves_config):
        percentage_concentration = x[0]
        volume = x[2]
        
        output_tank_substance_volume, output_volume_increase = ConcentrationModel.calculate_valves_flow(tank_area, valves_config.get("output_valves",[]), percentage_concentration)
        input_tank_substance_volume, input_volume_increase = ConcentrationModel.calculate_valves_flow(tank_area, valves_config.get("input_valves",[]),percentage_concentration)

        dHdt = input_volume_increase/tank_area - output_volume_increase/tank_area
        dVdt = input_volume_increase - output_volume_increase
        dCadt = (input_tank_substance_volume - output_tank_substance_volume)/volume - (percentage_concentration*dVdt)/volume
        return [dCadt, dHdt, dVdt]

    def _validate_result(self, result_value, min_value=None, max_value=None):
        result_value = min_value if min_value and result_value < min_value else result_value
        result_value = max_value if max_value and result_value > max_value else result_value
        return result_value

    def run(self, config={}):
        ts = np.linspace(0, int(config["simulation_time"]), int(config["t_steps"]))
        level = config["initial_liquid_level"] if config["initial_liquid_level"] > 0 else 0.01
        volume = level * self._tank_area
        concentration = config["initial_liquid_concentration_A"] 
        level_changes = np.ones(len(ts)) * level
        volume_changes = np.ones(len(ts)) *  volume
        concentration_changes = np.ones(len(ts)) * concentration

        y0 = [concentration, level, volume]
        valves_config = config["valves_config"]

        for i in range(len(ts)-1):
            t = [ts[i],ts[i+1]]
            y = odeint(
                ConcentrationModel.calculate_percentage_concentration,
                y0,
                t,
                args=(
                    self._tank_area,
                    valves_config,
                ),
            )
            max_concentration_value = 100 if y[-1][1] > 0 else 1
            print( y[-1][1], max_concentration_value)
            y[-1][0] = self._validate_result(y[-1][0], min_value=0, max_value=max_concentration_value)
            y[-1][1] = self._validate_result(y[-1][1], min_value=0)

            y0 = y[-1] 
            concentration_changes[i+1] = y[-1][0]
            level_changes[i+1] = y[-1][1]
            volume_changes[i+1] = y[-1][2]
        return [
            {"name" : "concentration [%]",
             "results" : concentration_changes,
             "times": ts,
             "title": "Tank filling - liquid concentration of A",
             },
             { "name": "level [dm]",
             "results": level_changes,
             "times": ts,
             "title": "Tank filling - liquid level",
             },
            { "name": "volume [dm³]",
             "results": volume_changes,
             "times": ts,
             "title": "Tank filling - liquid volume",
             }
        ]
