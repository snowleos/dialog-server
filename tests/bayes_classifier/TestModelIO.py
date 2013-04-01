# vim: set fileencoding=utf-8
import sys
sys.path.append("../..")
from dialog_server.classifier.TModelIO import *
from dialog_server.classifier.TBaseModel import *

modelList = list()
ModelIO = TModelIO()

ModelIO.Read("test_model.txt", None, TBaseModel, modelList)
ModelIO.Write("test_model.txt", None, modelList)
modelList[-1].Modified = True
modelList[-1].BinData += "_mod"
newModel = TBaseModel()
newModel.ModelId = ModelIO.GetNewModelId()
newModel.ContextId = "spec2"
newModel.Modified = True
newModel.BinData = "testModifiedModel"
modelList.append(newModel)
ModelIO.Write("test_model2.txt", None, modelList)
ModelIO.MoveToBackup("test_model2.txt")
ModelIO.Write("test_model2.txt", None, modelList)

