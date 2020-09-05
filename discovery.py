# -*- coding: utf-8 -*-
# © 2016 QYT Technology
# Authored by: Liu tianlong (tlzmkm@gmail.com)
import os
import importlib
import pkgutil
from importlib import import_module
import hapi
import sys
import traceback


def module_has_submodule(package, module_name):
    """See if 'module' is in 'package'."""
    name = ".".join([package.__name__, module_name])
    try:
        # None indicates a cached miss; see mark_miss() in Python/import.c.
        return sys.modules[name] is not None
    except KeyError:
        pass
    try:
        package_path = package.__path__  # No __path__, then not a package.
    except AttributeError:
        # Since the remainder of this function assumes that we're dealing with
        # a package (module with a __path__), so if it's not, then bail here.
        return False
    for finder in sys.meta_path:
        if finder.find_module(name, package_path):
            return True
    for entry in package_path:
        try:
            # Try the cached finder.
            finder = sys.path_importer_cache[entry]
            if finder is None:
                # Implicit import machinery should be used.
                try:
                    file_, _, _ = importlib.util.find_spec(module_name, [entry])
                    if file_:
                        file_.close()
                    return True
                except ImportError:
                    continue
            # Else see if the finder knows of a loader.
            elif finder.find_module(name):
                return True
            else:
                continue
        except KeyError:
            # No cached finder, so try and make one.
            for hook in sys.path_hooks:
                try:
                    finder = hook(entry)
                    # XXX Could cache in sys.path_importer_cache
                    if finder.find_module(name):
                        return True
                    else:
                        # Once a finder is found, stop the search.
                        break
                except ImportError:
                    # Continue the search for a finder.
                    continue
            else:
                # No finder found.
                # Try the implicit import machinery if searching a directory.
                if os.path.isdir(entry):
                    try:
                        file_, _, _ = importlib.util.find_spec(module_name, [entry])
                        if file_:
                            file_.close()
                        return True
                    except ImportError:
                        pass
                        # XXX Could insert None or NullImporter
    else:
        # Exhausted the search, so the module cannot be found.
        return False


def auto_discover(defaults=True, models=True):
    for importer, mod, is_package in pkgutil.walk_packages(hapi.__path__, prefix='hapi.'):
        try:
            if 'defaults' in mod and defaults:
                module = import_module(mod)
            elif 'models' in mod and models:
                module = import_module(mod)
                print(module)
            else:
                continue
        except ImportError as e:
            print(mod)
            print(e)
            print(traceback.format_exc())
        else:
            try:
                if defaults:
                    import_module("%s.defaults" % mod)
            except ImportError:
                if module_has_submodule(module, "defaults"):
                    raise
            try:
                if models:
                    import_module("%s.models" % mod)
            except ImportError:
                if module_has_submodule(module, "models"):
                    raise


# def register_model():
#     DeviceSensor.