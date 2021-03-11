import numpy as np
from scipy.integrate import odeint
from .process_model import ProcessModel

class TankFillingModel(ProcessModel):
    class Meta:
        slug = "tank-filling-model"

    @staticmethod
    def calculate_valve_flow(tank_area, valve={}):
        valve_capacity, valve_open = valve.get("valve_capacity"), valve.get("valve_open_percent")
        valve_flow = valve_capacity/tank_area * (valve_open / 100)
        return valve_flow

    @staticmethod
    def calculate_level_increase(liquid_level, time, tank_area, valves_config):
        input_valves_amount = len(valves_config.get("input_valves", []))
        
        input_increase = 0
        for i in range(input_valves_amount):
            valve = valves_config["input_valves"][i]
            input_flow = TankFillingModel.calculate_valve_flow(tank_area, valve)
            input_increase += input_flow
        
        valve = valves_config["output_valves"][0]
        output_flow = TankFillingModel.calculate_valve_flow(tank_area, valve)
    
        return input_increase - output_flow
    
    def run(self, config={}):
        ts = np.linspace(config["t_start"], config["t_stop"], config["t_steps"])
        results = np.zeros(config["t_steps"])
        
        level = config["initial_liquid_level"]
        valves_config = config["valves_config"]

        for i in range(config["t_steps"]): 
            y = odeint(TankFillingModel.calculate_level_increase, level, ts, args=(
                self._tank_area, 
                valves_config
            ))
            level = y[-1]
            results[i] = level
        return [results]
        