from control_system.utils import merge_dicts

from .processes.base_process_model import ProcessModel
from .controllers.base_controller_model import ControllerModel
from .tuners.base_tuner_model import TunerModel
from .decorators import ensure_config_format, ensure_output_format

class ProcessSimulator:

    def __init__(self, process_dict:dict, controller_dict:dict=None, controller_tuning_dict:dict=None)->None:
        self._simulation_config = ProcessModel.get_default_config()
        steps_count = self.simulation_config.get("steps_count")
        simulation_time = self.simulation_config.get("simulation_time")
        self._controller_config = ControllerModel.get_default_config(steps_count, simulation_time)
        self.process_dict = process_dict
        self.controller_dict = controller_dict
        self._controller_tuning_dict = controller_tuning_dict
        self._controller_tuning_config = TunerModel.get_default_config()
        self._process = self._update_process()
        self._controller = self._update_controller()
        self._controller_tuner = self._update_controller_tuner()
        

    def _update_process(self)->ProcessModel:
        tank_area = self._simulation_config.get("tank_area", 1)
        self._process = self.process_dict.get("model_class")(tank_area)
        return self._process

    def _update_controller(self)->ControllerModel:
        if not self.controller_dict:
            return None
        self._controller = self.controller_dict.get("model_class")(**self._controller_config, tuner=self._controller_tuner)
        return self._controller

    def _update_controller_tuner(self)->ControllerModel:
        if not self._controller_tuning_dict:
            return None
        self._controller_tuner = self._controller_tuning_dict.get("model_class")(**self._controller_tuning_config)
        self._update_controller()
        return self._controller_tuner

    @property
    def controller_tuning_dict(self):
        return self.controller_tuning_dict

    @property
    def simulation_config(self):
        return self._simulation_config
    
    @property
    def controller_config(self):
        return self._controller_config

    @property
    def controller_tuner(self):
        return self._controller_tuner

    @property
    def controller_tuning_config(self):
        return self._controller_tuning_config
        
    @simulation_config.setter
    @ensure_config_format
    def simulation_config(self, config):
        self._simulation_config = merge_dicts(self._simulation_config, config)
        self._process = self._update_process()

    @controller_config.setter
    @ensure_config_format
    def controller_config(self, config:dict):
        self._controller_config = merge_dicts(self._controller_config, config)
        self._controller = self._update_controller()

    @controller_tuning_dict.setter
    def controller_tuning_dict(self, tuning_dict:dict):
        self._controller_tuning_dict = tuning_dict
        self._controller_tuner = self._update_controller_tuner()

    @controller_tuning_config.setter
    @ensure_config_format
    def controller_tuning_config(self, config:dict):
        self._controller_tuning_config = merge_dicts(self._controller_tuning_config, config)
        self._controller_tuner = self._update_controller_tuner()

    @ensure_output_format
    def simulate(self)->dict:
        return self._process.run(self._simulation_config, self._controller)
