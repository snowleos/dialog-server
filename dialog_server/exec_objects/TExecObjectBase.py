import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server

class TExecObjectBase:
    def __init__(self, name):
        # fields set by TCommandCreator
        self.ExecModulePath = ""
        self.ModuleRelPath = ""
        self.Name = name

    def __call__(self):
        """put default action here"""


