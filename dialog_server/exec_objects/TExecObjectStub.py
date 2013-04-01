import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
import ConfigParser
from dialog_server.exec_objects.TExecObjectBase import *

__all__ = ["TExecObjectStub"]
class TExecObjectStub(TExecObjectBase):
    def __init__(self, name):
        TExecObjectBase.__init__(self, name)

    def __call__(self, cmd):
        return 0, cmd.RawText, "You called command of type "+cmd.CmdType
