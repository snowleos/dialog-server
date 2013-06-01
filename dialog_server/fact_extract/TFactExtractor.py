# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
from dialog_server.command.TCommand import *
from extern_lib.remorph_bind import TRemorphBind

"""
Берет TCommand, запускает на запросе Remorph
Вытягивает факты из реморфа и переколдовки
Добавляет в нашем формате для диалог менеджера
"""

class TFactExtractor:
    def __init__(self, projBaseDir):
        self.RemorphBind = TRemorphBind(projBaseDir,\
                projBaseDir + "/conf/extern_lib.remorph_bind.conf")
        """put fields here"""

    # facts are set  to tuples ("fact_type", "fact_value")
    def __GetFioFacts(self, command):
        retList = []
        for token in command.Preprocessed.get("Fio", []):
            retStr = ""
            for field in token:
                if field == u"FirstName":
                    retStr = " ".join([retStr, token[field]])
                if field == u"LastName":
                    retStr = " ".join([retStr, token[field]])
                if field == u"Patronymic":
                    retStr = " ".join([retStr, token[field]])

            retList.append(("person", retStr))
            print sys.stderr, "__GetFioFacts(): ", "person", retStr
        return retList

    def __GetRemorphFacts(self, command):
        factsList = self.RemorphBind(command.RawText.encode("utf-8"))
        retList = []
        # пока что берем только первый, самый лучший факт
        for token in factsList:
            if token["RuleNumber"] == 0:
                retList.append(("RuleName", token["RuleName"]))
                for fact in token["Value"]:
                    retList.append((fact, token["Value"][fact][0]))
        return retList

    def __GetRequestLexemsFacts(self, command):
        retList = []
        if len(command.RequestLexems) > 0:
            retList.append(("request", " ".join(command.RequestLexems)))
        return retList

    def __call__(self, command):
        fioFactsList = self.__GetFioFacts(command)
        if len(fioFactsList) > 0:
            command.FactsList.extend(fioFactsList)

        remorphFactsList = self.__GetRemorphFacts(command)
        if len(remorphFactsList) > 0:
            command.FactsList.extend(remorphFactsList)

        requestLexemsFacts = self.__GetRequestLexemsFacts(command)
        if len(requestLexemsFacts) > 0:
            command.FactsList.extend(requestLexemsFacts)


