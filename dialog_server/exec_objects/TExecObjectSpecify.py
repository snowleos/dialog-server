import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
from dialog_server.exec_objects.TExecObjectBase import *

class TExecObjectSpecify(TExecObjectBase):
    def __init__(self, name):
        TExecObjectBase.__init__(self, name)
        """put fields here"""

    def __call__(self):
        """put default action here"""

