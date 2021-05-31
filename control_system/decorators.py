from collections import abc
from functools import wraps

def ensure_config_format(func):
    def ensure_input_format(config:dict)->dict:
        if isinstance(config, abc.Mapping):
            for k in config:
                if isinstance(config[k], abc.Mapping):
                    config[k] = ensure_input_format(config[k])
                elif isinstance(config[k], list):
                    list(map(ensure_input_format,config[k]))
                else:
                    config[k] = float(config[k])
        return config

    @wraps(func)
    def wrapper(self, config, **kwargs):
        config = ensure_input_format(config)
        return func(self, config=config, **kwargs)
    return wrapper

def ensure_output_format(func):
    def ensure_numeric_format(results:dict)->dict:
        for result_dict in results.values():
            result_dict["results"] = [
                format(number, ".5f") if number >= 0 else 0
                for number in result_dict.get("results", [])
            ]
            result_dict["times"] = [
                format(number, ".2f") for number in result_dict.get("times", [])
            ]
        return results

    @wraps(func)
    def wrapper(self, **kwargs):
        data = func(self, **kwargs)
        return ensure_numeric_format(data)
    return wrapper

def ensure_values_range(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        output = func(self, *args, **kwargs)
        output = self.min_value if output < self.min_value else output
        output = self.max_value if output > self.max_value else output
        return output
    return wrapper


def check_set_point_change(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        set_point = kwargs["set_point"]
        if set_point != self._last_set_point:
            self._set_fuzzy_simulator()
        return func(self, *args, **kwargs)
    return wrapper

