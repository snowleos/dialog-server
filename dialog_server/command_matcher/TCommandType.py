# vim: set fileencoding=utf-8
import sys
sys.path.append("../..")
from dialog_server.exec_objects.TExecObjectSpecify import *
from dialog_server.exec_objects.TExecObjectOperation import *
from dialog_server.exec_objects.TExecObjectMetaCommand import *
from dialog_server.exec_objects.TExecObjectStub import *

class TCommandTypeProps:
    def __init__(self, name, execObjType):
        self.Name = name
        self.ExecObjType = execObjType
        self.ExecObj = None
    def GetExecObj(self):
        print self.ExecObjType
        self.ExecObj = self.ExecObjType(self.Name)
        return self.ExecObj

#   "ExampleOperation": {
#       "OperationType": <type of operation>,
#       "ContextType": <type of context that uses such operation>,
#                   e.g. if context was "common" and operation has "specific" then
#                   context would be switched to "specific"
#       "ModuleRelPath": <external module if command is TExecObjectOperation>,
#       "AdditionalLogicClass": <here may be set additional handler class>,
#                   e.g. class that preapares input for exec object
#       "OnErrorOperation": <what to do if error>,
#       "OnResultOperation": <what to do if further result processing needed>
#   }

TCommandType = {
    "NoCommand": {
        "OperationType": TExecObjectStub,
        "ModuleRelPath": "../modules/search.py"
        },

    "DefaultCommand": {
        #same as Search. If don't know whatta do, search it at Yandex!
        "OperationType": TExecObjectStub,
        "ModuleRelPath": "../modules/search.py "
        },

    "Search": {
        "OperationType": TExecObjectOperation,
        "ModuleRelPath": "../modules/search.py "
        },

    "SearchQuestion": {
        # http://wiki.yandex-team.ru/AleksandrSibirjakov/VoprositelnyeZaprosy
        "OperationType": TExecObjectOperation,
        "ModuleRelPath": "../modules/search.py "
        },

    "Wiki": {
        "OperationType": TExecObjectOperation ,
        "ModuleRelPath": "../modules/wikipedia.py"
        },

    "News": {
        "OperationType": TExecObjectOperation,
        "ModuleRelPath": "../modules/news.py"
        },

    "Weather": {
        "OperationType": TExecObjectOperation,
        "ModuleRelPath": "../modules/weather.py"
        },

    "ExternalDevice": {
        "OperationType": TExecObjectStub,
        "ModuleRelPath": " "
        },

    "MakeCoffee": {
        "OperationType": TExecObjectStub,
        "ModuleRelPath": " "
        },

    #"Notify"
    #"ChatBotReply"
    #"DontUnderstand"
    #"RequestMoreInfo"
    #"StopCurrentCmd"
    #"RememberContext"
    }
