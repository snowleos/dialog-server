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
#       "ContextType": TODO <type of context that uses such operation>,
#                   e.g. if context was "common" and operation has "specific" then
#                   context would be switched to "specific"
#       "ModuleRelPath": <external module if command is TExecObjectOperation>,
#       "AdditionalLogicClass": TODO <here may be set additional handler class>,
#                   e.g. class that preapares input for exec object
#       "OnErrorOperation": TODO <what to do if error>,
#       "OnResultOperation": TODO <what to do if further result processing needed>,
#       "Description": <what operation means e.g. искать на поиске>,
#       "Priority": TODO <if we recognized several commands what to do first>,
#       "RequestFields": TODO <словарь полей запроса ключ:пор_номер значение:название_поля>
#   }

TCommandType = {
    "NoCommand": {
        "OperationType": TExecObjectStub,
        "ModuleRelPath": "../modules/search.py",
        "Description":   "ничего не делать"
        },

    "DefaultCommand": {
        #same as Search. If don't know whatta do, search it at Yandex!
        "OperationType": TExecObjectStub,
        "ContextType": "common",
        "ModuleRelPath": "../modules/search.py ",
        "AdditionalLogicClass": None,
        "OnResultOperation": "",
        "Description":   "сделать, что обычно",
        "Priority": 0,
        "RequestFields": {"0": "CommandText", "1": "Query"}
        },

    "Search": {
        "OperationType": TExecObjectOperation,
        "ModuleRelPath": "../modules/search.py ",
        "Description":   "найти в поиске"

        },

    "SearchQuestion": {
        # http://wiki.yandex-team.ru/AleksandrSibirjakov/VoprositelnyeZaprosy
        "OperationType": TExecObjectOperation,
        "ModuleRelPath": "../modules/search.py ",
        "Description":   "найти в ответах"

        },

    "Wiki": {
        "OperationType": TExecObjectOperation ,
        "ModuleRelPath": "../modules/wikipedia.py",
        "Description":   "найти в википедии"

        },

    "News": {
        "OperationType": TExecObjectOperation,
        "ModuleRelPath": "../modules/news.py",
        "Description":   "прочитать новости"

        },

    "Weather": {
        "OperationType": TExecObjectOperation,
        "ModuleRelPath": "../modules/weather.py",
        "Description":   "узнать погоду"

        },

    "ExternalDevice": {
        "OperationType": TExecObjectStub,
        "ModuleRelPath": " ",
        "Description":   "передать команду внешнему устройству"

        },

    "MakeCoffee": {
        "OperationType": TExecObjectStub,
        "ModuleRelPath": " ",
        "Description":   "сделать кофе",
        "RequestFields": {  "0": "CommandText",
                            "1": "Volume",
                            "2": "Hotness",
                            "3": "Type",
                            "4": "Sugar",
                            "5": "Strongness",
                            "6": "Filler",
                            "7": "Decoration"
                          }

        },

    #"Notify"
    #"ChatBotReply"
    #"DontUnderstand"
    #"RequestMoreInfo"
    #"StopCurrentCmd"
    #"RememberContext"
    }
