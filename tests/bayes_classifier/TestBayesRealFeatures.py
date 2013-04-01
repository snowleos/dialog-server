# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
from dialog_server.classifier.TBayesClassifier import *
from dialog_server.command.TCommand import *
from dialog_server.classifier.TBayesFeatureExtractor import *
from dialog_server.classifier.TModelIO import *
from dialog_server.command_matcher.TParser import *
PROJECT_BASE_DIR = os.getcwd() + "/../.."

bayesClassifier = TBayesClassifier()
extr = TBayesFeatureExtractor()

command = TCommand()
bayesClassifier.StartLearn()
for line in open('preproc_cmds.txt'):
    command.Read(line[:-1])
    extr(command)
    bayesClassifier.Learn(command)
bayesClassifier.FinishLearn()

ModelIO = TModelIO()

ModelIO.Write("bayes_model_real_features.txt", None, [bayesClassifier.Model])
print "Modified", bayesClassifier.Model.Modified

probCommandsDict = defaultdict(lambda:None)

# init all main objects
parser = TParser(\
        confPath=PROJECT_BASE_DIR + \
        "/conf/dialog_server.parser.conf",\
        wizardConfPath=PROJECT_BASE_DIR + \
        "/conf/extern_lib.wizard_bind.conf")

for line in [u'читай википедию', u'скока градусов на улице', u'кто такой Билл Гейтс', u'новостная сводка', u'в чем смысл жизни', u'сегодня будет пурга']:
    parser(command, line)
    print line
    extr(command)
    print 'CmdType: ', bayesClassifier.Classify(command, probCommandsDict)
    for prob in probCommandsDict.values():
        print prob

# test on same data :)
"""
for line in open('preproc_cmds.txt'):
    command.Read(line[:-1])
    print command.RawText
    extr(command)
    cmdType = bayesClassifier.Classify(command, probCommandsDict)
    print "'"+cmdType+"'", "'"+command.CmdType+"'"
    if cmdType not in command.CmdType:
        print probCommandsDict
"""
