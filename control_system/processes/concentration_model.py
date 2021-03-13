import numpy as np
from scipy.integrate import odeint

from .process_model import ProcessModel


class ConcentrationModel(ProcessModel):
    class Meta:
        slug = "concentration-model"

    @staticmethod
    def calculate_valve_flow(tank_area, valve={}):
        valve_capacity, valve_open = valve.get("valve_capacity"), valve.get("valve_open_percent")
        valve_flow = valve_capacity / tank_area * (valve_open / 100)
        return valve_flow

    @staticmethod
    def calculate_percentage_concentration(x, time, tank_area, valves_config):
        percentage_concentration = x[0]
        height = x[1]

        output_flow = ConcentrationModel.calculate_valve_flow(tank_area, valves_config["output_valves"][0])
        output_substance_volume = output_flow * percentage_concentration

        input_tank_substance_height = 0
        input_increase = 0
        input_valves_amount = len(valves_config.get("input_valves", []))
        for i in range(input_valves_amount):
            valve = valves_config["input_valves"][i]
            substance_concentration = valve["liquid_config"]["liquid_concentration_A"]
            input_flow = ConcentrationModel.calculate_valve_flow(tank_area, valve)

            input_tank_substance_height += input_flow * substance_concentration
            input_increase += input_flow

        dHdt = input_increase - output_flow

        dCadt = (input_tank_substance_height - output_substance_volume) / (height*tank_area) - (percentage_concentration * dHdt * tank_area) / (height*tank_area)
        return [dCadt, dHdt]

    def run(self, config={}):
        ts = np.linspace(0, int(config["simulation_time"]), int(config["t_steps"]))
        level = config["initial_liquid_level"] if config["initial_liquid_level"] > 0 else 1
        concentration = config["initial_liquid_concentration_A"] 
        level_changes = np.ones(len(ts)) * level
        concentration_changes = np.ones(len(ts)) * concentration

        y0 = [concentration, level]
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

            y0 = y[-1]
            concentration_changes[i+1] = y[-1][0]
            level_changes[i+1] = y[-1][1]
        return [
            {"name" : "concentration",
             "results" : concentration_changes,
             "times": ts,
             "title": "Tank filling - liquid concentration of A",
             },
             { "name": "volume",
             "results": level_changes,
             "times": ts,
             "title": "Tank filling - liquid level",
             }
        ]
