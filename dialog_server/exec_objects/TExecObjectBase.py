import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
import ConfigParser

class TExecObjectBase:
    #static members. Used by inherited classes
    ProjectBaseDir = ""
    ConfPath = ""
    def __init__(self, name):
        self.ExecModulePath = ""
        self.Conf = None
        self.ModuleRelPath = ""
        self.Name = name
        self.ReadConfig()
        """put fields here"""

    def __call__(self):
        """put default action here"""

    def ReadConfig(self):
        self.Conf = ConfigParser.ConfigParser()
        print self.ConfPath
        self.Conf.read(self.ConfPath)

