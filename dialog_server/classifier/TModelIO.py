# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
import weakref
sys.path.append("../..")
from datetime import datetime
import random
import dialog_server

class TModelIO:
    """
        read data from storage. parse fields to model objects
        if there is any modified model all modifications will be lost
        we remove unnesessary and rewrite  modified
    """
    def Read(self, tableName="", contextIdList=["common"], modelType=None, modelList=None):
        if modelList  == None:
            raise Exception("you have to pass modelList as list() object")
        remPosList = list()
        # 1. find models with unnesessary context
        if contextIdList != None:
            remPosList = [i for i in xrange(len(modelList)) if modelList[m].ContextId not in contextIdList]

        # 2. get list of model ids that are already in list
        existIds = dict((modelList[i].ModelId, i) for i in xrange(len(modelList)))

        # 3. read file. Contains: modelId \t contextId \t model in JSON
        for line in open(tableName, "r"):
            fields = line[:-1].decode('utf-8').split('\t')
            doAddModel = True
            if contextIdList != None:
                if fields[1] not in contextIdList:
                    doAddModel = False
            if doAddModel == True:
                if fields[0] in existIds.keys():
                    remPosList.append(existIds[fields[0]])
                newModel = modelType()
                newModel.ModelId = fields[0]
                newModel.ContextId = fields[1]
                newModel.Read(fields[2])
                modelList.append(newModel)

        # 4. remove unnesessary and replaced models
        for mId in reversed(sorted(remPosList)):
            del modelList[mId]
        # done
            
    """
        writes all modified models, listed in modelList
    """
    def Write(self, tableName="", contextIdList=["common"], modelList=None):
        if modelList  == None:
            raise Exception("you have to pass modelList as list() object")
        if os.path.exists(tableName):
            # 1. make .bak table
            bakTablename = tableName+".bak."+datetime.now().strftime("%s")
            os.rename(tableName, bakTablename)
            modifiedModelsDict = weakref.WeakValueDictionary()
            for model in modelList:
                if (model.Modified == True):
                    if contextIdList != None:
                        if model.ContextId in contextIdList:
                            modifiedModelsDict[model.ModelId] = model
                    else:
                        modifiedModelsDict[model.ModelId] = model

            FINP = open(bakTablename, "r")
            FOUT = open(tableName, "w")
            for line in FINP:
                fields = line[:-1].decode('utf-8').split('\t')
                if fields[0] in modifiedModelsDict.keys():
                    # write new model
                    newModel = modifiedModelsDict[fields[0]]
                    resLine = newModel.Write()
                    FOUT.write(fields[0] + "\t" + fields[1] + "\t" + resLine + "\n")
                    modifiedModelsDict[fields[0]].Modified = False
                    del modifiedModelsDict[fields[0]]
                else:
                    # write line without modifications
                    FOUT.write(line)
            # write new models
            for model in modifiedModelsDict.values():
                resLine = model.Write()
                FOUT.write(model.ModelId + "\t" + model.ContextId + "\t" + resLine + "\n")
                model.Modified = False
        else:
            FOUT = open(tableName, "w")
            # write all models in modelList
            for model in modelList:
                resLine = model.Write()
                FOUT.write(model.ModelId + "\t" + model.ContextId + "\t" + resLine + "\n")
                model.Modified = False
        # done
    @classmethod
    def GetNewModelId(cls):
        return datetime.now().strftime("%s%f") + str(random.randrange(1000000))

