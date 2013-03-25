# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
from dialog_server.classifier.TBayesClassifier import *
from dialog_server.command.TCommand import *

bayesClassifier = TBayesClassifier()

def GetFeatures(command):
    command.Features = [
        'll: %s' % command.Preprocessed[-1],          # get last letter
        'pll: %s' % command.Preprocessed[-2],          # get pre last letter
        'fl: %s' % command.Preprocessed[0],           # get first letter
        'sl: %s' % command.Preprocessed[1],           # get second letter
        ]

command = TCommand()
bayesClassifier.StartLearn()
for line in open('names.txt'):
    sample = line.decode('utf-8').split()
    command.Preprocessed = sample[0]
    command.CmdType = sample[1]
    GetFeatures(command)
    bayesClassifier.Learn(command)
bayesClassifier.FinishLearn()

tmpStr = bayesClassifier.Model.Write()
bayesClassifier.Model.Read(tmpStr)
from dialog_server.classifier.TModelIO import *
import weakref

ModelIO = TModelIO()

ModelIO.Write("bayes_model.txt", None, [bayesClassifier.Model])
print "Modified", bayesClassifier.Model.Modified


probCommandsDict = defaultdict(lambda:0)

command.Preprocessed = u'Паглафья'
GetFeatures(command)
print 'gender: ', bayesClassifier.Classify(command, probCommandsDict)
command.Preprocessed = u'Антон'
GetFeatures(command)
print 'gender: ', bayesClassifier.Classify(command, probCommandsDict)
command.Preprocessed = u'Светлана'
GetFeatures(command)
print 'gender: ', bayesClassifier.Classify(command, probCommandsDict)
command.Preprocessed = u'Кирилл'
GetFeatures(command)
print 'gender: ', bayesClassifier.Classify(command, probCommandsDict)
