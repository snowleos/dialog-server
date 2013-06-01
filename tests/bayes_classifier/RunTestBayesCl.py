# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
import math

sys.path.append("../..")
from dialog_server.classifier.TBayesClassifier import *
from dialog_server.command.TCommand import *
from dialog_server.classifier.TBayesFeatureExtractor import *
from dialog_server.classifier.TModelIO import *
from dialog_server.classifier.TBayesModel import *
from dialog_server.command_matcher.TParser import *
import dialog_server.command_matcher.TCommandMatcher as TCommandMatcher
PROJECT_BASE_DIR = os.getcwd() + "/../.."

def LoadModel(self, modelFile):
    ModelIO = TModelIO()
    modelList = list()
    ModelIO.Read(modelFile, None, TBayesModel, modelList)
    self.Model = modelList[-1]

command = TCommand()
extr = TBayesFeatureExtractor()
commandMatcher = TCommandMatcher.TCommandMatcher()
bayesClassifier = TBayesClassifier()

#LoadModel(bayesClassifier, "bayes_model_real_features.txt")
bayesClassifier.StartLearn()
for line in open('preproc_cmds.txt'):
    command.Read(line[:-1])
    extr(command)
    bayesClassifier.Learn(command)
bayesClassifier.FinishLearn()


sum = 0.0
for cl in bayesClassifier.Model.Classes:
    #print cl, bayesClassifier.Model.Classes[cl]
    sum += bayesClassifier.Model.Classes[cl]
#print sum

invFeatDict = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))
TypeClassValDict = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))
for cl in bayesClassifier.Model.Classes:
    for feat in bayesClassifier.Model.FeatureProbs[cl]:
        #print feat.encode("utf-8") , bayesClassifier.Model.FeatureProbs[cl][feat]
        typePos = feat.find(": ")
        invFeatDict[feat[:typePos]][feat[typePos + 2:]][cl] = bayesClassifier.Model.FeatureProbs[cl][feat]
        TypeClassValDict[feat[:typePos]][cl][feat[typePos + 2:]] = bayesClassifier.Model.FeatureProbs[cl][feat]

"""
for tp in TypeClassValDict:
    print tp.encode("utf-8")
    for cl in TypeClassValDict[tp]:
        print "       ", cl
        sm = 0
        for val in TypeClassValDict[tp][cl]:
            print val.encode("utf-8"), ":", TypeClassValDict[tp][cl][val], 
            sm += TypeClassValDict[tp][cl][val]
        print "SUM:", sm
sys.exit(0)
"""

if True == True: #False:
    for tp in ["012"]:#invFeatDict:
        print tp.encode("utf-8")
        for val in invFeatDict[tp]:
            print "       ", val.encode("utf-8"),
            mx = 0.0
            mxx = 0.0
            mxall = 0.0
            for cl in invFeatDict[tp][val]:
                print cl, ":", invFeatDict[tp][val][cl], " ",
                mx += invFeatDict[tp][val][cl]
                mxx += invFeatDict[tp][val][cl] * invFeatDict[tp][val][cl]
                mxall += invFeatDict[tp][val][cl]
            
            print
            mx /= len(invFeatDict[tp][val])
            mxx /= len(invFeatDict[tp][val])
            mxall /= len(bayesClassifier.Model.Classes)
            dx = mxx - mx*mx
            dxall = 0
            for cl in bayesClassifier.Model.Classes:
                if cl in invFeatDict[tp][val]:
                    dxall += (mx - invFeatDict[tp][val][cl]) * (mx - invFeatDict[tp][val][cl])
                else:
                    dxall += mx*mx

            dxall /= float(len(bayesClassifier.Model.Classes))
            print "           ", "MX:", mx, "DX:", dx, "DXALL:", dxall
        print


avgDissim = 0.0
cmdCount = 0
avgAverage = 0.0
for line in open('preproc_cmds.txt'):
    cmdCount += 1
    probCommandsDict = defaultdict(lambda:None)
    commandsToExecList = list()
    command.Read(line[:-1])
    extr(command)
    bayesClassifier.Classify(command, probCommandsDict)
    commandMatcher.FindMostProbCommands(command, [probCommandsDict], commandsToExecList)

    if command.CmdType != commandsToExecList[0].CmdType:
        for feat in command.Features:
            print feat, 
        print
        for prob in probCommandsDict.values():
            print prob
        print command.RawText, command.CmdType, commandsToExecList[0].CmdType

    # count dissimilarity
    curDissim = 0.0
    curAverage = 0.0
    for prob in probCommandsDict.values():
        curAverage += math.sqrt(prob.Prob)
        curDissim += probCommandsDict[commandsToExecList[0].CmdType].Prob - prob.Prob
    curDissim /= len(probCommandsDict)
    curAverage /= len(probCommandsDict)

    avgDissim += curDissim
    avgAverage += curAverage

print >> sys.stderr, "AVERAGE DISSIM:", avgDissim / cmdCount
print >> sys.stderr, "TOTAL SQRT AVERAGE:", avgAverage / cmdCount


"""
        dxplus = 0.0
        dxminus = 0.0
        cntplus = 0.0
        cntminus = 0.0
        Eps = 0.0000001
        for cl in bayesClassifier.Model.Classes:
            if cl in invFeatDict[tp][val]:
                #print cl, invFeatDict[tp][val][cl]
                #print invFeatDict[tp][val][cl], ">=", (mxall - Eps)
                if invFeatDict[tp][val][cl] >= (mxall - Eps):
                    dxplus += (0.0 - mxall + invFeatDict[tp][val][cl])
                    cntplus += 1.0
                else:
                    dxminus += (mxall - invFeatDict[tp][val][cl])
                    cntminus += 1.0
            else:
                #print cl, 0
                dxminus += mxall
                cntminus += 1
        print "SCORE", dxminus, dxplus, cntplus, cntminus, "mxall:", mxall
        score = (dxminus / dxplus) * (cntplus / cntminus)

        print "           ", score , val.encode("utf-8"), mx, dx, len(invFeatDict[tp][val]) 

"""
