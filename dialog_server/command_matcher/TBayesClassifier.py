# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
from dialog_server.command_matcher.TCommandType import *
from dialog_server.command.TCommandCreator import *

class TBayesClassifier:
    Epsilon = 0.00000000001
    def __init__(self):
        """put fields here"""

    def __call__(self):
        """put default action here"""

