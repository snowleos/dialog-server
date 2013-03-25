# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../../..")
import dialog_server
from dialog_server.classifier.classifier_learner.TLearnerBase import *

class TExactLearner(TLearnerBase):
    def __init__(self):
        TLearnerBase.__init__(self)
        """put fields here"""

    def __call__(self):
        TLearnerBase.__call__(self)
        """put default action here"""

