import re

import numpy as np
from matplotlib import pyplot as plt

from . import processes
from .utils import discover_processes, merge_dicts


class ProcessSimulator:
    def __init__(self, process, simulation_name="", regulator=None):
        self._process = process
        self._regulator = regulator
        self._simulation_name = simulation_name
        self.config = self.get_default_simulation_config()

    def get_default_simulation_config(self):
        return {
            "t_start": 0,
            "t_stop": 10,
            "t_steps": 100,
            "initial_liquid_level": 0,
            "valves_config": {
                "input_valves": [
                    {
                        "valve_capacity": 50,  # [dm^3/min]
                        "valve_open_percent": 0,
                        "liquid_config": {
                            "liquid_concentration_A": 10,
                        },
                    },
                    {
                        "valve_capacity": 80,
                        "valve_open_percent": 10,
                        "liquid_config": {
                            "liquid_concentration_A": 10,
                        },
                    },
                ],
                "output_valves": [
                    {
                        "valve_capacity": 60,
                        "valve_open_percent": 10,
                    }
                ],
            },
        }

    @staticmethod
    def get_process_dict():
        processes_meta_classes = discover_processes(namespace=processes)

        process_dict = {}
        for class_name, meta in processes_meta_classes.items():
            name = (meta.slug.capitalize()).replace("-", " ")
            process_dict[meta.slug] = {"process_name": name, "process_class": class_name}
        return process_dict

    @staticmethod
    def get_process_list():
        processes_meta_classes = discover_processes(namespace=processes)

        process_list = []
        for _, meta in processes_meta_classes.items():
            name = (meta.slug.capitalize()).replace("-", " ")
            process_list.append({"process_slug": meta.slug, "process_name": name})
        return process_list

    def simulate(self, simulation_config={}):
        config = merge_dicts(self.config, simulation_config)
        self._results = self._process.run(config)
        self._ensure_results_format()
        return self._results

    def _ensure_results_format(self):
        if self._results:
            self._results = np.array(self._results).tolist()

    def draw_simulation(self):
        ts = np.linspace(self.config["t_start"], self.config["t_stop"], self.config["t_steps"])
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(ts, self._results, "b-", linewidth=3)
        plt.ylabel(self._simulation_name)
