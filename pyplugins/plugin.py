#!/usr/bin/env python
# -*- coding: utf8 -*-


class IPlugin(object):

    NAME = "<base plugin>"
    VERSION = "0.0"
    DESCRIPTION = "<unknown>"

    def __init__(self):
        """
        Creates a new class instance for Plugin
        """
        pass

    @property 
    def name(self):
        return self.__class__.NAME

    @name.setter
    def name(self, value):
        self.__class__.NAME = value

    @property 
    def version(self):
        return self.__class__.VERSION

    @version.setter
    def version(self, value):
        self.__class__.VERSION = value

    @property 
    def description(self):
        return self.__class__.DESCRIPTION

    @description.setter
    def description(self, value):
        self.__class__.DESCRIPTION = value

    def run(self):
        raise NotImplementedError("You should call this method into your plugin")


