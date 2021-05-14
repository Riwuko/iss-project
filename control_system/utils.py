import importlib
import inspect
from functools import lru_cache
import pkgutil
import sys
from pyclbr import readmodule
from control_system import controllers, processes, tuners

def merge_dicts(dict1, dict2):
    """ Recursively merges dict2 into dict1 """
    if not dict2:
        return dict1
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        return dict2
    for k in dict2:
        if k in dict1:
            dict1[k] = merge_dicts(dict1[k], dict2[k])
        else:
            dict1[k] = dict2[k]
    return dict1


def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def discover_models(namespace):
    discovered_packages = {
        name: importlib.import_module(name) for finder, name, ispkg in iter_namespace(namespace)
    }
    project_modules = discovered_packages.values()

    project_classes = [list((readmodule(module).keys())) for module in discovered_packages.keys()]
    project_classes = [str(project_class[0]) for project_class in project_classes if project_class]

    models_meta_classes = {
        getattr(module, project_class): getattr(module, project_class).Meta
        for module, project_class in zip(project_modules, project_classes)
        if hasattr(getattr(module, project_class), "Meta")
    }
    return models_meta_classes

def get_models_dict(namespace)->dict:
    processes_meta_classes = discover_models(namespace=namespace)

    process_dict = {}
    for class_name, meta in processes_meta_classes.items():
        name = (meta.slug.capitalize()).replace("-", " ")
        process_dict[meta.slug] = {"model_name": name, "model_class": class_name}
    return process_dict

def get_models_list(namespace)->list:
    processes_meta_classes = discover_models(namespace=namespace)

    process_list = []
    for _, meta in processes_meta_classes.items():
        name = (meta.slug.capitalize()).replace("-", " ")
        if hasattr(meta, "control_value"):
            process_list.append({"model_slug": meta.slug, "model_name": name, "control_value": meta.control_value})
        else:
            process_list.append({"model_slug": meta.slug, "model_name": name})
    return process_list

def get_project_items():
    return {
        "process_list": get_models_list(processes),
        "process_dict": get_models_dict(processes),
        "controller_list": get_models_list(controllers),
        "controller_dict": get_models_dict(controllers),
        "tuner_list": get_models_list(tuners),
        "tuner_dict": get_models_dict(tuners),
    }




