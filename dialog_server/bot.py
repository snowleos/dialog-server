#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from jabberbot import JabberBot
from jabberbot import botcmd
from dialog_server.classifier.TBayesClassifier import *
from dialog_server.classifier.TExactClassifier import *
from dialog_server.command.TCommand import *
from dialog_server.command.TCommandCreator import *
from dialog_server.exec_objects.TExecObjectBase import *
from dialog_server.fact_extract.TFactExtractor import *
import common_lib.common_ops as common_ops
import dialog_server.command_matcher.TCommandMatcher as TCommandMatcher
import dialog_server.command_matcher.TParser as TParser
from dialog_server.command_matcher.TCommandType import *

PROJECT_BASE_DIR = common_ops.GetProjectBaseDir()
print PROJECT_BASE_DIR


class YHBot(JabberBot):
    def __init__(self, jid, password):
        super(YHBot, self).__init__(jid, password)
        self.parser = TParser.TParser(
            confPath=PROJECT_BASE_DIR +
            "/conf/dialog_server.parser.conf",
            wizardConfPath=PROJECT_BASE_DIR +
            "/conf/extern_lib.wizard_bind.conf"
        )

        self.cmdMatcher = TCommandMatcher.TCommandMatcher()
        exactClassifier = TExactClassifier()
        self.cmdMatcher.ClassifiersList.append((None, exactClassifier))
        bayesClassifier = TBayesClassifier(
            common_ops.GetProjectBaseDir() +
            "/conf/bayes_classifier.conf"
        )
        bayesClassifier.LoadModel()
        self.cmdMatcher.ClassifiersList.append((TBayesFeatureExtractor(), bayesClassifier))
        self.factExtractor = TFactExtractor(PROJECT_BASE_DIR)


    @botcmd
    def echo(self, mess, args):
        response = 'mess: %s, args: %s' % (mess, args,)
        return response

    def unknown_command(self, mess, cmd, args):
        print u'%s' % mess
        command = TCommand()
        self.parser(command, u'%s %s' % (cmd, args))
        # extract facts
        factExtractor(command)

        commandsToExecList = list()
        self.cmdMatcher(command, commandsToExecList)

        #result = ("CmdType: %s" % execCommand.CmdType for execCommand in commandsToExecList)
        result = ("CmdType: %s" % GetCommandProperty(execCommand.CmdType, "Description").decode("utf-8") for execCommand in commandsToExecList)
        return u'Распознанные типы команд:\n%s' % '\n'.join(result)


def main():
    jid = 'yhbot@jabber.ru'
    password = 'uq0Pb2Frl'
    bot = YHBot(jid, password)
    bot.serve_forever()


if __name__ == '__main__':
    main()
