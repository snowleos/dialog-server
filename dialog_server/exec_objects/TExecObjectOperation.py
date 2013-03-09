import sys
import os
import re
import subprocess
import shlex
sys.path.append("../..")
import dialog_server
from dialog_server.exec_objects.TExecObjectBase import *

class TExecObjectOperation(TExecObjectBase):
    def __init__(self, name):
        TExecObjectBase.__init__(self, name)
        self.ModuleRelPath = self.Conf.get(name, "ModuleRelPath")
        print "self.ModuleRelPath", self.ModuleRelPath

    def __call__(self, requestLexems):
        proc = subprocess.Popen(shlex.split(self.ModuleRelPath),
                stdin = subprocess.PIPE,
                stdout = subprocess.PIPE)
        moduleInput = " ".join(requestLexems).encode("utf-8")
        if moduleInput != "":
            moduleInput += "\n"
        out, err = proc.communicate(input=moduleInput)
        retVal = proc.returncode
        if out == None: out = ""
        if err == None: err = ""
        return retVal, unicode(out, "utf8"), unicode(err, "utf8")
