import collections.abc
import re

import numpy as np
from matplotlib import pyplot as plt

from . import processes
from .utils import discover_processes, merge_dicts


class ProcessSimulator:
    def __init__(self, process=None, simulation_name="", regulator=None):
        self._process = process
        self._regulator = regulator
        self._simulation_name = simulation_name
        self.config = ProcessSimulator.get_default_simulation_config()

    @staticmethod
    def get_default_simulation_config():
        return {
            "tank_area": 1,
            "simulation_time": 10,
            "t_steps": 100,
            "initial_liquid_level": 0,
            "initial_liquid_concentration_A": 0,
            "valves_config": {
                "input_valves": [
                    {
                        "valve_capacity": 5.5,  # [dm^3/s]
                        "valve_open_percent": 0,
                        "liquid_config": {
                            "liquid_concentration_A": 10,
                        },
                    },
                    {
                        "valve_capacity": 6,
                        "valve_open_percent": 10,
                        "liquid_config": {
                            "liquid_concentration_A": 10,
                        },
                    },
                ],
                "output_valves": [
                    {
                        "valve_capacity": 5.5,
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

    def _ensure_config_format(self, config):
        for k in config:
            if isinstance(config[k], collections.abc.Mapping):
                config[k] = self._ensure_config_format(config[k])
            elif isinstance(config[k], list):
                list(map(self._ensure_config_format, config[k]))
            else:
                config[k] = float(config[k])
        return config

    def _ensure_results_format(self):
        if self._results:
            for result_dict in self._results:
                result_dict["results"] = [
                    format(number, ".5f") if number >= 0 else 0
                    for number in result_dict.get("results", [])
                ]
                result_dict["times"] = [
                    format(number, ".2f") for number in result_dict.get("times", [])
                ]

    def simulate(self, simulation_config={}):
        config = self._ensure_config_format(simulation_config)
        config = merge_dicts(self.config, simulation_config)
        self._results = self._process.run(config)
        self._ensure_results_format()
        return self._results
