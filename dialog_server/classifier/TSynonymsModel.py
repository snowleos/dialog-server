# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
from dialog_server.classifier.TBaseModel import *

class TSynonymsModel(TBaseModel):
    def __init__(self):
        TBaseModel.__init__(self)
        """put fields here"""

    def __call__(self):
        TBaseModel.__call__(self)
        """put default action here"""

