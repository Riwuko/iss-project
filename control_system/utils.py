import importlib
import inspect
import pkgutil
import sys
from pyclbr import readmodule


def merge_dicts(dict1, dict2):
    """ Recursively merges dict2 into dict1 """
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


def discover_processes(namespace):
    discovered_processes = {name: importlib.import_module(name) for finder, name, ispkg in iter_namespace(namespace)}
    project_modules = discovered_processes.values()

    project_classes = [list((readmodule(module).keys())) for module in discovered_processes.keys()]
    project_classes = [str(project_class[0]) for project_class in project_classes if project_class]

    processes_meta_classes = {
        getattr(module, project_class): getattr(module, project_class).Meta
        for module, project_class in zip(project_modules, project_classes)
        if hasattr(getattr(module, project_class), "Meta")
    }
    return processes_meta_classes
