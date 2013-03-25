# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
from dialog_server.classifier.TBaseFeatureExtractor import *

class TSynonymsFeatureExtractor(TBaseFeatureExtractor):
    def __init__(self):
        TBaseFeatureExtractor.__init__(self)
        """put fields here"""

    def __call__(self):
        TBaseFeatureExtractor.__call__(self)
        """put default action here"""

