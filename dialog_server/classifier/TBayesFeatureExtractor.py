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

Reach example of Wizard answer is at the end of file
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
        "012": "count of A Adjectives",
        "013": "A + свойства ",
        "014": "has anim",
        "015": "has geo",
        "016": "has yari",
        "017": "yari command type",
        "018": "Grammem of each word",
        "019": "совершенность + переходность глагола pf ipf tran intr",
        "020": "имеет местоимение SPRO или APRO",
        "021": "имеет Сущ в именительном или винительном ",
        "022": "имеет Сущ persn, patrn, famn, mf, anim",
        "023": "имеет Сущ geo, abbr, loc",
        "024": "имеет ANUM | A рядом с S",
        "025": "падеж сущ рядом с глаголом",
        "026": "отношение к-ва S к к-ву words without stop words",
        "027": "PR",
        "028": "наличие связки V PR S в такой последовательности",
        "029": "наличие связки PR|ADVPRO|SPRO|APRO и V не более чем через одно слово",
        "030": "наличие связки PR|ADVPRO|SPRO|APRO и S не более чем через одно слово",
        "031": "наличие связки V неPR S не более чем через одно слово",
        "032": "наличие слова на иностранном языке (но не на украинском)",
        "033": "связка ADVPRO или APRO и безличный глагол (как называется)"
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
                if lemma.get("Language", "none") == "ru":
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
                if lemma.get("Language", "none") == "ru":
                    isNoun = 0
                    for grammem in lemma.get("Grammems", []):
                        if grammem[0:2] == "S ":
                            isNoun = 1
                    cnt005 += isNoun
        featuresList.append(u"005: " + str(cnt005))

        #"006": "count of Verbs",
        cnt006 = 0
        for lexem in command.Preprocessed["Morph"]:
            for lemma in lexem["Lemmas"]:
                if lemma.get("Language", "none") == "ru":
                    isV = 0
                    for grammem in lemma.get("Grammems", []):
                        if grammem[0:2] == "V ":
                            isV = 1
                    cnt006 += isV
        featuresList.append(u"006: " + str(cnt006))

        #"007": "Noun + падеж",
        for lexem in command.Preprocessed["Morph"]:
            for lemma in lexem["Lemmas"]:
                if lemma.get("Language", "none") == "ru":
                    for grammem in lemma.get("Grammems", []):
                        if grammem[0:2] == "S ":
                            matchPadej = re.search("abl|acc|dat|gen|ins|loc|nom|part|voc", grammem)
                            if matchPadej != None:
                                featuresList.append(u"007: " + lemma["Text"] + " " + matchPadej.group(0))

        #"008": "формы глагола + падеж существительного, все со всеми",
        allVerbs = list()
        allNouns = list()
        for lexem in command.Preprocessed["Morph"]:
            for lemma in lexem["Lemmas"]:
                if lemma.get("Language", "none") == "ru":
                    for grammem in lemma.get("Grammems", []):
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
                if lemma.get("Language", "none") == "ru":
                    for grammem in lemma.get("Grammems", []):
                        if grammem[0:6] == "ADVPRO":
                            featuresList.append(u"009: " + lemma["Text"])

        #"010": "Глагол + все свойства",
        for lexem in command.Preprocessed["Morph"]:
            for lemma in lexem["Lemmas"]:
                if lemma.get("Language", "none") == "ru":
                    for grammem in lemma.get("Grammems", []):
                        if grammem[0:2] == "V ":
                            featuresList.append(u"010: " + lemma["Text"] + " " + grammem)

        #"011": "Noun + все свойства",
        for lexem in command.Preprocessed["Morph"]:
            for lemma in lexem["Lemmas"]:
                if lemma.get("Language", "none") == "ru":
                    for grammem in lemma.get("Grammems", []):
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
        #"021": "имеет Сущ в именительном или винительном ",
        #"022": "имеет Сущ persn, patrn, famn, mf, anim",
        #"023": "имеет Сущ geo, abbr, loc",
        #"024": "имеет ANUM | A рядом с S",
        #"025": "падеж сущ рядом с глаголом",
        #"026": "отношение к-ва S к к-ву words without stop words",
        #"027": "PR",
        #"028": "наличие связки V PR S в такой последовательности",
        #"029": "наличие связки PR|ADVPRO|SPRO|APRO и V не более чем через одно слово",
        #"030": "наличие связки PR|ADVPRO|SPRO|APRO и S не более чем через одно слово",
        #"031": "наличие связки V неPR S не более чем через одно слово"

        #for sss in featuresList:
        #    print sss

        command.Features = featuresList




#{"RawText": "\u0447\u0442\u043e \u0441\u043a\u0430\u0436\u0435\u0442 \u0432\u0438\u043a\u0438\u043f\u0435\u0434\u0438\u044f \u043f\u0440\u043e \u043a\u0440\u0435\u0434\u0438\u0442\u043d\u044b\u0439 \u0441\u043a\u043e\u0440\u0438\u043d\u0433", "LexemsList": ["\u0447\u0442\u043e", "\u0441\u043a\u0430\u0436\u0435\u0442", "\u0432\u0438\u043a\u0438\u043f\u0435\u0434\u0438\u044f", "\u043f\u0440\u043e", "\u043a\u0440\u0435\u0434\u0438\u0442\u043d\u044b\u0439", "\u0441\u043a\u043e\u0440\u0438\u043d\u0433"], "ResultText": "", "DebugText": "", "RequestLexems": [], 
#"Preprocessed": {"Morph": [
#{"Tokens": {"Begin": 0, "End": 1}, "Lemmas": [{"Text": "\u0447\u0442\u043e", "Grammems": ["ADVPRO"], "Language": "ru"}, {"Text": "\u0447\u0442\u043e", "Grammems": ["CONJ"], "Language": "ru"}, {"Text": "\u0447\u0442\u043e", "Grammems": ["SPRO nom sg n inan", "SPRO acc sg n inan"], "Language": "ru"}]}, 
#{"Tokens": {"Begin": 1, "End": 2}, "Lemmas": [{"Text": "\u0441\u043a\u0430\u0437\u0430\u0442\u044c", "Grammems": ["V inpraes sg indic 3p pf tran"], "Language": "ru"}]}, 
#{"Tokens": {"Begin": 2, "End": 3}, "Lemmas": [{"Text": "\u0432\u0438\u043a\u0438\u043f\u0435\u0434\u0438\u044f", "Grammems": ["S nom sg f inan"], "Language": "ru"}]}, 
#{"Tokens": {"Begin": 3, "End": 4}, "Lemmas": [{"Text": "\u043f\u0440\u043e", "Grammems": ["PR"], "Language": "ru"}]}, 
#{"Tokens": {"Begin": 4, "End": 5}, "Lemmas": [{"Text": "\u043a\u0440\u0435\u0434\u0438\u0442\u043d\u044b\u0439", "Grammems": ["A nom sg plen m", "A acc sg plen m inan"], "Language": "ru"}]}, 
#{"Tokens": {"Begin": 5, "End": 6}, "Lemmas": [{"Text": "\u0441\u043a\u043e\u0440\u0438\u043d\u0433", "Grammems": ["S nom sg m inan", "S acc sg m inan"], "Language": "ru"}]}], 
#"Delimiters": [{}, {"EndChar": 4, "Text": " ", "EndByte": 7, "BeginByte": 6, "BeginChar": 3}, {"EndChar": 11, "Text": " ", "EndByte": 20, "BeginByte": 19, "BeginChar": 10}, {"EndChar": 21, "Text": " ", "EndByte": 39, "BeginByte": 38, "BeginChar": 20}, {"EndChar": 25, "Text": " ", "EndByte": 46, "BeginByte": 45, "BeginChar": 24}, {"EndChar": 35, "Text": " ", "EndByte": 65, "BeginByte": 64, "BeginChar": 34}, {}], 
#"Tokens": [{"EndChar": 3, "Text": "\u0447\u0442\u043e", "EndByte": 6, "BeginByte": 0, "BeginChar": 0}, {"EndChar": 10, "Text": "\u0441\u043a\u0430\u0436\u0435\u0442", "EndByte": 19, "BeginByte": 7, "BeginChar": 4}, {"EndChar": 20, "Text": "\u0432\u0438\u043a\u0438\u043f\u0435\u0434\u0438\u044f", "EndByte": 38, "BeginByte": 20, "BeginChar": 11}, {"EndChar": 24, "Text": "\u043f\u0440\u043e", "EndByte": 45, "BeginByte": 39, "BeginChar": 21}, {"EndChar": 34, "Text": "\u043a\u0440\u0435\u0434\u0438\u0442\u043d\u044b\u0439", "EndByte": 64, "BeginByte": 46, "BeginChar": 25}, {"EndChar": 42, "Text": "\u0441\u043a\u043e\u0440\u0438\u043d\u0433", "EndByte": 79, "BeginByte": 65, "BeginChar": 35}], 
#"StopWords": {"Tokens": [0, 3], "RequestWithoutStopWords": "\u0441\u043a\u0430\u0436\u0435\u0442 \u0432\u0438\u043a\u0438\u043f\u0435\u0434\u0438\u044f \u043a\u0440\u0435\u0434\u0438\u0442\u043d\u044b\u0439 \u0441\u043a\u043e\u0440\u0438\u043d\u0433"}, "OriginalRequest": "\u0447\u0442\u043e \u0441\u043a\u0430\u0436\u0435\u0442 \u0432\u0438\u043a\u0438\u043f\u0435\u0434\u0438\u044f \u043f\u0440\u043e \u043a\u0440\u0435\u0434\u0438\u0442\u043d\u044b\u0439 \u0441\u043a\u043e\u0440\u0438\u043d\u0433", "ProcessedRequest": "\u0447\u0442\u043e \u0441\u043a\u0430\u0436\u0435\u0442 \u0432\u0438\u043a\u0438\u043f\u0435\u0434\u0438\u044f \u043f\u0440\u043e \u043a\u0440\u0435\u0434\u0438\u0442\u043d\u044b\u0439 \u0441\u043a\u043e\u0440\u0438\u043d\u0433"},
#"CmdType": "Wiki", "Prob": 0.0, "ExecStatus": 0, "Features": null, "CommandLexems": []}

