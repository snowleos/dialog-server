# vim: set fileencoding=utf-8
import sys
import os
import re
import json
import time
import subprocess
sys.path.append("../..")
from dialog_server.command_matcher.TCommandType import *
from dialog_server.command.TCommand import *
from dialog_server.command_matcher.TParser import *
from dialog_server.classifier.TBayesFeatureExtractor import *
import common_lib.common_ops as common_ops
PROJECT_BASE_DIR = os.getcwd() + "/../.."

# init all main objects

# example of how to use root extractor
from extern_lib.remorph_bind import TRemorphBind
Remorph = TRemorphBind(\
        confPath=PROJECT_BASE_DIR + \
        "/conf/extern_lib.remorph_bind.conf", \
        projBaseDir=PROJECT_BASE_DIR)

Remorph("поехали до дома") 
Remorph("поехали в ближайший ресторан") 
#Remorph("поехали") 

