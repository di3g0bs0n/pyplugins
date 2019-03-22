#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys, os
import glob
import ast

from .plugin import IPlugin

class PluginLoader(object):

    def __init__(self, path = None):
        self.path = path

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        self.__path = value

    @staticmethod
    def getFiles(path, extension="*.py", exclude=None):
        if exclude is None:
            exclude = []
        _p = os.path.join(path, extension)
        return [fn for fn in glob.glob(_p) if not os.path.basename(fn) in exclude]

    @staticmethod
    def _getClassName(path):
        if not path.endswith(".py"):
            return False

        with open(path) as f:
            node = ast.parse(f.read())
        return [n for n in node.body if isinstance(n, ast.ClassDef)][0].name
    

    @staticmethod
    def getClassInstance(path, args=None):
        """
        Returns a class instance from a .py file.
        Args:
        path (str): Absolute path to .py file
        args (dict): Arguments passed via class constructor
        Returns:
        object: Class instance or None
        """
        if not path.endswith(".py"):
            return None

        if args is None:
            args = {}

        classname = PluginLoader._getClassName(path)
        basename = os.path.basename(path).replace(".py", "")
        sys.path.append(os.path.dirname(path))
        
        try:
            mod = __import__(basename, globals(), locals(), [classname], 0)
            class_ = getattr(mod, classname)
            instance = class_(**args)
        except Exception as e:
            print("[!] {}".format(str(e)))
            return None
        finally:
            sys.path.remove(os.path.dirname(path))
        return instance


    def run(self, method = 'run', args=None, classArgs = None):
        if self.path is None:
            raise Exception("You must set a path")
        
        if args is None:
            args = {}

        if classArgs is None:
            classArgs = {}

        response = {}
        
        sys.path.append(self.path)
		
        exclude = ["__init__.py", "loader.py"]

        for f in self.__class__.getFiles(self.path, "*.py", exclude=exclude):
            try:
                instance = self.__class__.getClassInstance(path = f, args = classArgs)
                
                # Check base
                if type(instance) is IPlugin:
                    continue

                if instance is not None:
                    if callable(method):
                        # Lambda function
                        args["instance"] = instance
                        output = method(**args)
                        # Review!
                        response[instance.__class__.NAME] = output  
                    else:
                        # Method
                        if hasattr(instance, method):
                            output = getattr(instance, method)(**args)
                            response[instance.__class__.NAME] = output
                        else:
                            continue

            except Exception as e:
                print("[!] {}".format(str(e)))
        sys.path.remove(self.path)
        return response


if __name__ == "__main__":

    loader = PluginLoader(path = "/tmp/foo")
    responses = loader.run()
    print(responses)