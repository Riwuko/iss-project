import skfuzzy.control as ctrl
import skfuzzy as fuzz
import numpy as np
from .base_controller_model import ControllerModel
from control_system.decorators import ensure_values_range, check_set_point_change

class FuzzyController(ControllerModel):
    """Fuzzy Controller """

    class Meta:
        slug = "fuzzy-controller"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.terms = {}
        self.fuzzy_logic = True
        self.sim = None
        self._last_set_point = 0
        self._set_fuzzy_simulator()

    @ensure_values_range
    @check_set_point_change
    def update(self, error, last_error, set_point=0):
        reverse = False
        if error < 0: 
            error = abs(error)
            last_error = abs(last_error)
            reverse = True
        self._sim.input['delta'] = (error - last_error) / self._delta_time
        self._sim.input['error'] = error
        self._sim.compute()
        self._last_set_point = set_point
        output = self._sim.output['output']
        return output if not reverse else -output


    def _set_fuzzy_simulator(self):
        max_error_universe = self._last_set_point+1
        error_universe = np.arange(0, max_error_universe, 0.1)  
        output_universe = np.arange(0, 101, 0.1)
        error = ctrl.Antecedent(error_universe, 'error')
        delta = ctrl.Antecedent(error_universe, 'delta')
        output = ctrl.Consequent(output_universe, 'output')

        names = ['vlow', 'low', 'lmedium', 'hmedium', 'high', 'vhigh']
        error.automf(names=names)
        delta.automf(names=names)
        output.automf(names=names)
        
        output['vlow'] = fuzz.trimf(output.universe, [0, 0, 18])
        output['low'] = fuzz.trimf(output.universe, [8, 10, 15])
        output['lmedium'] = fuzz.trimf(output.universe, [10, 25, 45])
        output['hmedium'] = fuzz.trimf(output.universe, [30, 55, 65])
        output['high'] = fuzz.trimf(output.universe, [55, 70, 80])
        output['vhigh'] = fuzz.trimf(output.universe, [75, 100, 100])
        
        rule0 = ctrl.Rule(antecedent = (
            (error['vlow'] & delta['vlow']) |
            (error['vlow'] & delta['low']) |
            (error['vlow'] & delta['lmedium']) |
            (error['vlow'] & delta['hmedium']) |
            (error['vlow'] & delta['high']) |
            (error['vlow'] & delta['vhigh']) |
            
            (error['low'] & delta['vlow']) 

        ), consequent=output['vlow'])

        rule1 = ctrl.Rule(antecedent = (
            
            (error['low'] & delta['low']) |
            (error['low'] & delta['lmedium']) |
            (error['lmedium'] & delta['vlow']) |
            (error['lmedium'] & delta['low']) |
            (error['lmedium'] & delta['lmedium']) |
            (error['low'] & delta['hmedium']) |
            (error['low'] & delta['high']) |
            (error['lmedium'] & delta['hmedium']) |
            (error['hmedium'] & delta['vlow']) |
             (error['hmedium'] & delta['low']) |
            (error['low'] & delta['vhigh']) 

        ), consequent=output['low'])
        

        rule3 = ctrl.Rule(antecedent = (
            (error['lmedium'] & delta['high']) |
            (error['lmedium'] & delta['vhigh']) |
           (error['high'] & delta['vlow'])  |
            (error['hmedium'] & delta['lmedium']) |
            (error['hmedium'] & delta['hmedium']) |
            (error['hmedium'] & delta['high']) |
            (error['hmedium'] & delta['vhigh']) |
            
            (error['high'] & delta['low']) 
        ), consequent=output['lmedium'])

        rule2 = ctrl.Rule(antecedent = (
            (error['high'] & delta['lmedium']) |
            (error['high'] & delta['hmedium']) 
        ), consequent=output['hmedium'])

        rule4 = ctrl.Rule(antecedent = (
            (error['high'] & delta['high']) |
            (error['high'] & delta['vhigh']) 

        ), consequent=output['high'])

        rule5 = ctrl.Rule(antecedent = (
            (error['vhigh'] & delta['vlow']) |
            (error['vhigh'] & delta['low']) |
            (error['vhigh'] & delta['lmedium']) |
            (error['vhigh'] & delta['hmedium']) |
            (error['vhigh'] & delta['high']) |
            (error['vhigh'] & delta['vhigh']) 

        ), consequent=output['vhigh'])


        system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4, rule5])
        self._sim = ctrl.ControlSystemSimulation(system)
