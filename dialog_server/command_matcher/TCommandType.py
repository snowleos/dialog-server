# vim: set fileencoding=utf-8
import sys
sys.path.append("../..")
from dialog_server.exec_objects.TExecObjectSpecify import *
from dialog_server.exec_objects.TExecObjectOperation import *
from dialog_server.exec_objects.TExecObjectMetaCommand import *

class TCommandTypeProps:
    def __init__(self, name, execObjType):
        self.Name = name
        self.ExecObjType = execObjType
        self.ExecObj = None
    def GetExecObj(self):
        print self.ExecObjType
        self.ExecObj = self.ExecObjType(self.Name)
        return self.ExecObj

TCommandType = {
    "NoCommand":        TCommandTypeProps("NoCommand",      TExecObjectMetaCommand),
    "Search":           TCommandTypeProps("Search",         TExecObjectOperation),
    "Wiki":             TCommandTypeProps("Wiki",           TExecObjectOperation),
    "News":             TCommandTypeProps("News",           TExecObjectOperation),
    "Weather":          TCommandTypeProps("Weather",        TExecObjectOperation),
    "ExternalDevice":   TCommandTypeProps("ExternalDevice", TExecObjectOperation),
    "Notify":           TCommandTypeProps("Notify",         TExecObjectOperation),
    "ChatBotReply":     TCommandTypeProps("ChatBotReply",   TExecObjectOperation),
    "DontUnderstand":   TCommandTypeProps("DontUnderstand", TExecObjectSpecify),
    "RequestMoreInfo":  TCommandTypeProps("RequestMoreInfo",TExecObjectSpecify),
    "StopCurrentCmd":   TCommandTypeProps("StopCurrentCmd", TExecObjectMetaCommand),
    "RememberContext":  TCommandTypeProps("RememberContext",TExecObjectMetaCommand)
    }

