import numpy as np
from scipy.integrate import odeint
from .process_model import ProcessModel


class ConcentrationModel(ProcessModel):
    class Meta:
        slug = "concentration-model"

    @staticmethod
    def calculate_valve_flow(valve={}):
        valve_capacity, valve_open = valve.get("valve_capacity"), valve.get("valve_open_percent")
        valve_flow = valve_capacity * (valve_open / 100)
        return valve_flow
        
    @staticmethod
    def calculate_percentage_concentration(x, time, tank_area, valves_config):
        percentage_concentration = x[0]
        volume = x[1]
        
        output_flow = ConcentrationModel.calculate_valve_flow(valves_config["output_valves"][0])
        output_substance_volume = output_flow * percentage_concentration
        
        input_substance_volume = 0
        input_increase = 0
        input_valves_amount = len(valves_config.get("input_valves", []))
        for i in range(input_valves_amount):
            valve = valves_config["input_valves"][i]
            substance_concentration = valve["liquid_config"]["liquid_concentration_A"]
            input_flow = ConcentrationModel.calculate_valve_flow(valve)
            
            input_substance_volume += input_flow * substance_concentration
            input_increase += input_flow
    
        dVdt = input_increase - output_flow
        dCadt = (input_substance_volume - output_substance_volume)/volume - (percentage_concentration*dVdt)/volume
        return [dCadt, dVdt]
    
    def run(self, config={}):
        ts = np.linspace(config["t_start"], config["t_stop"], config["t_steps"])
        level_changes = np.ones(len(ts))*1.0
        concentration_changes = np.ones(len(ts))*0.0
        
        y0 = [0,1]
        valves_config = config["valves_config"]
        
        for i in range(config["t_steps"]): 
            y = odeint(ConcentrationModel.calculate_percentage_concentration, y0, ts, args=(
                self._tank_area, 
                valves_config,
            ))

            y0 = y[-1]
            concentration_changes[i] = y[-1][0]
            level_changes[i] = y[-1][1]
        return [concentration_changes, level_changes]
