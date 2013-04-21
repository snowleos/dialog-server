# vim: set fileencoding=utf-8
import sys
import os
import re
import shlex
import subprocess
import ConfigParser

class TDerivatBind:
    def __init__(self, confPath=""):
        self.Conf = ConfigParser.ConfigParser()
        self.Conf.read(confPath)
        self.Conf.BinDirRelPath = self.Conf.get("Derivat", "BinDirRelPath")
        self.Conf.BinName = self.Conf.get("Derivat", "BinName")

    def __call__(self, etalonWord, checkWord):
        cmd = "( cd " + self.Conf.BinDirRelPath + \
                " ; iconv -f utf-8 -t cp1251 | perl " + self.Conf.BinName + ")"
        proc = subprocess.Popen(["-c", cmd],
                stdin = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                shell=True)
        moduleInput = "\t".join([etalonWord, checkWord]).encode("utf-8")
        out, err = proc.communicate(input=moduleInput)
        retVal = proc.returncode
        if retVal != 0 or out == None or out == "":
            raise Exception("Something wrong with TDerivatBind\n"+err)
        areSameRoot = int(out[:out.find("\t")])
        return areSameRoot    
