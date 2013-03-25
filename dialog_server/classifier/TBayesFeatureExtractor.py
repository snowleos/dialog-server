# vim: set fileencoding=utf-8
import sys
import os
import re
import subprocess
sys.path.append("../..")
import dialog_server
from dialog_server.classifier.TBaseFeatureExtractor import *


"""
Most features  got from lemmer
Lemmer abbreveatures meaning: https://ossa2.yandex.ru/dict/lemmer.py?help=1


"""
TBayesFeatureTypes = {
        "001": "raw word",
        "002": "lexem",
        "003": "count of words",
        "004": "count of words without stop words ",
        "005": "count of Nouns",
        "006": "count of Verbs",
        "007": "Noun + падеж",
        "008": "формы глагола + падеж существительного, все со всеми",
        "009": "местоименное наречие ADVPRO",
        "010": "Глагол + все свойства",
        "011": "Noun + все свойства",
        "012": "count of Adjectives",
        "013": "Adj + свойства ",
        "014": "has anim",
        "015": "has geo",
        "016": "has yari",
        "017": "yari command type",
        "018": "Grammem of each word",
        "019": "совершенность + переходность глагола pf ipf tran intr",
        "020": "имеет местоимение SPRO или APRO"
        }


class TBayesFeatureExtractor(TBaseFeatureExtractor):
    def __init__(self):
        TBaseFeatureExtractor.__init__(self)

    def __call__(self, command):
        TBaseFeatureExtractor.__call__(self)
        featuresList = list()

        #"001": "raw word",
        for token in command.Preprocessed["Tokens"]:
            featuresList.append(u"001: " + token["Text"])

        #"002": "lexem",
        for lexem in command.Preprocessed["Morph"]:
            for lemma  in lexem["Lemmas"]:
                if lemma["Language"] == "ru":
                    featuresList.append(u"002: " + lemma["Text"])

        #"003": "count of words",
        featuresList.append(u"003: " + str(len(command.Preprocessed["Tokens"])))

        #"004": "count of words without stop words ",
        cnt004 = len(command.Preprocessed["Tokens"])
        if "StopWords" in command.Preprocessed:
            cnt004 = cnt004 - len(command.Preprocessed["StopWords"]["Tokens"])
        featuresList.append(u"004: " + str(cnt004))

        #"005": "count of Nouns",
        cnt005 = 0
        for lexem in command.Preprocessed["Morph"]:
            for lemma in lexem["Lemmas"]:
                if lemma["Language"] == "ru":
                    isNoun = 0
                    for grammem in lemma["Grammems"]:
                        if grammem[0:2] == "S ":
                            isNoun = 1
                    cnt005 += isNoun
        featuresList.append(u"005: " + str(cnt005))

        #"006": "count of Verbs",
        cnt006 = 0
        for lexem in command.Preprocessed["Morph"]:
            for lemma in lexem["Lemmas"]:
                if lemma["Language"] == "ru":
                    isV = 0
                    for grammem in lemma["Grammems"]:
                        if grammem[0:2] == "V ":
                            isV = 1
                    cnt006 += isV
        featuresList.append(u"006: " + str(cnt006))

        #"007": "Noun + падеж",
        for lexem in command.Preprocessed["Morph"]:
            for lemma in lexem["Lemmas"]:
                if lemma["Language"] == "ru":
                    for grammem in lemma["Grammems"]:
                        if grammem[0:2] == "S ":
                            matchPadej = re.search("abl|acc|dat|gen|ins|loc|nom|part|voc", grammem)
                            if matchPadej != None:
                                featuresList.append(u"007: " + lemma["Text"] + " " + matchPadej.group(0))

        #"008": "формы глагола + падеж существительного, все со всеми",
        allVerbs = list()
        allNouns = list()
        for lexem in command.Preprocessed["Morph"]:
            for lemma in lexem["Lemmas"]:
                if lemma["Language"] == "ru":
                    for grammem in lemma["Grammems"]:
                        if grammem[0:2] == "S ":
                            matchPadej = re.search("abl|acc|dat|gen|ins|loc|nom|part|voc", grammem)
                            if matchPadej != None:
                                allNouns.append(matchPadej.group(0))
                        elif grammem[0:2] == "V ":
                            matchForm = re.search("impers|indic|imper|intr|praes|tran", grammem)
                            if matchForm != None:
                                allVerbs.append(matchForm.group(0))
        for v in allVerbs:
            for n in allNouns:
                featuresList.append(u"008: " + v + " " + "n")

        #"009": "местоименное наречие ADVPRO",
        for lexem in command.Preprocessed["Morph"]:
            for lemma in lexem["Lemmas"]:
                if lemma["Language"] == "ru":
                    for grammem in lemma["Grammems"]:
                        if grammem[0:6] == "ADVPRO":
                            featuresList.append(u"009: " + lemma["Text"])

        #"010": "Глагол + все свойства",
        for lexem in command.Preprocessed["Morph"]:
            for lemma in lexem["Lemmas"]:
                if lemma["Language"] == "ru":
                    for grammem in lemma["Grammems"]:
                        if grammem[0:2] == "V ":
                            featuresList.append(u"010: " + lemma["Text"] + " " + grammem)

        #"011": "Noun + все свойства",
        for lexem in command.Preprocessed["Morph"]:
            for lemma in lexem["Lemmas"]:
                if lemma["Language"] == "ru":
                    for grammem in lemma["Grammems"]:
                        if grammem[0:2] == "S ":
                            featuresList.append(u"010: " + lemma["Text"] + " " + grammem)

        #"012": "count of Adjectives",
        #"013": "Adj + свойства ",
        #"014": "has anim",
        #"015": "has geo",
        #"016": "has yari",
        #"017": "yari command type",
        #"018": "Grammem of each word",
        #"019": "совершенность + переходность глагола pf ipf tran intr",
        #"020": "имеет местоимение SPRO или APRO",

        #for sss in featuresList:
        #    print sss

        command.Features = featuresList



