import collections.abc
import re

import numpy as np
from matplotlib import pyplot as plt

from .utils import discover_models, merge_dicts
from .processes.process_model import ProcessModel
from .controllers.controller_model import ControllerModel
from .decorators import ensure_config_format, ensure_output_format

class ProcessSimulator:
    def __init__(self, process_dict:dict, controller_dict:dict=None)->None:
        self._simulation_config = ProcessModel.get_default_simulation_config()
        self._controller_config = ControllerModel.get_default_controller_config(self.simulation_config.get("t_steps"))
        self.process_dict = process_dict
        self.controller_dict = controller_dict
        self._process = self._update_process()
        self._controller = self._update_controller()

    def _update_process(self)->ProcessModel:
        tank_area = self._simulation_config.get("tank_area", 1)
        return self.process_dict.get("model_class")(tank_area)

    def _update_controller(self)->ControllerModel:
        if not self.controller_dict:
            return None
        return self.controller_dict.get("model_class")(**self._controller_config)

    @property
    def simulation_config(self):
        return self._simulation_config
    
    @property
    def controller_config(self):
        return self._controller_config

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

    @ensure_output_format
    def simulate(self)->dict:
        return self._process.run(self._simulation_config, self._controller)
