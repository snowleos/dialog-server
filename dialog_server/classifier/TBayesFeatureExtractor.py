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
        "033": "связка ADVPRO или APRO и безличный глагол (как называется)",
        "034": "PART частица",
        "035": " наличие true или отсутствие false частицы 'не' PART частица"
        }


class TBayesFeatureExtractor(TBaseFeatureExtractor):
    def __init__(self):
        TBaseFeatureExtractor.__init__(self)

    def __Append(self, featuresList, feat):
        # do not add same strings
        if len(featuresList) == 0:
            featuresList.append(feat)
        else:
            if featuresList[-1] != feat:
                featuresList.append(feat)

    def __HasLemmasOfDifferentWordType(self, lexem, wordType):
        hasDifferent = False
        for lemma in lexem.get("Lemmas", {}):
            for grammem in lemma.get("Grammems", []):
                if wordType not in grammem:
                    hasDifferent = True
        return hasDifferent

    def __call__(self, command):
        TBaseFeatureExtractor.__call__(self)
        featuresList = list()

        """
        #"001": "raw word",
        for token in command.Preprocessed.get("Tokens", {}):
            self.__Append(featuresList, u"001: " + token["Text"])
        """


        #"002": "lexem",
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma  in lexem.get("Lemmas", {}):
                if lemma.get("Language", "none") == "ru":
                    self.__Append(featuresList, u"002: " + lemma.get("Text", ""))

        #"003": "count of words",
        self.__Append(featuresList, u"003: " + str(len(command.Preprocessed.get("Tokens", {}))))

        #"004": "count of words without stop words ",
        cnt004 = len(command.Preprocessed.get("Tokens", {}))
        if "StopWords" in command.Preprocessed:
            cnt004 = cnt004 - len(command.Preprocessed["StopWords"]["Tokens"])
        self.__Append(featuresList, u"004: " + str(cnt004))

        #"005": "count of Nouns",
        cnt005 = 0
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma in lexem.get("Lemmas", []):
                if lemma.get("Language", "none") == "ru":
                    isNoun = 0
                    for grammem in lemma.get("Grammems", []):
                        if grammem[0:2] == "S ":
                            isNoun = 1
                    cnt005 += isNoun
        self.__Append(featuresList, u"005: " + str(cnt005))

        #"006": "count of Verbs",
        cnt006 = 0
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma in lexem.get("Lemmas", []):
                if lemma.get("Language", "none") == "ru":
                    isV = 0
                    for grammem in lemma.get("Grammems", []):
                        if grammem[0:2] == "V ":
                            isV = 1
                    cnt006 += isV
        self.__Append(featuresList, u"006: " + str(cnt006))

        #"007": "Noun + падеж",
        for lexem in command.Preprocessed.get("Morph", []):
            if self.__HasLemmasOfDifferentWordType(lexem, u"S ") == False:
                for lemma in lexem.get("Lemmas", []):
                    if lemma.get("Language", "none") == "ru":
                        for grammem in lemma.get("Grammems", []):
                            if grammem[0:2] == "S ":
                                matchPadej = re.search("abl|acc|dat|gen|ins|loc|nom|part|voc", grammem)
                                if matchPadej != None:
                                    self.__Append(featuresList, u"007: " + lemma.get("Text", "") + " " + matchPadej.group(0))

        #"008": "формы глагола + падеж существительного, все со всеми",
        allVerbs = list()
        allNouns = list()
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma in lexem.get("Lemmas", []):
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
                self.__Append(featuresList, u"008: " + v + " " + "n")

        #"009": "местоименное наречие ADVPRO",
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma in lexem.get("Lemmas", []):
                if lemma.get("Language", "none") == "ru":
                    for grammem in lemma.get("Grammems", []):
                        if grammem[0:6] == "ADVPRO":
                            self.__Append(featuresList, u"009: " + lemma.get("Text", ""))

        #"010": "Глагол + все свойства",
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma in lexem.get("Lemmas", []):
                if lemma.get("Language", "none") == "ru":
                    for grammem in lemma.get("Grammems", []):
                        if grammem[0:2] == "V ":
                            self.__Append(featuresList, u"010: " + lemma.get("Text", "") + " " + grammem)

        #"011": "Noun + все свойства",
        for lexem in command.Preprocessed.get("Morph", []):
            if self.__HasLemmasOfDifferentWordType(lexem, u"S ") == False:
                for lemma in lexem.get("Lemmas", []):
                    if lemma.get("Language", "none") == "ru":
                        for grammem in lemma.get("Grammems", []):
                            if grammem[0:2] == "S ":
                                self.__Append(featuresList, u"011: " + lemma.get("Text", "") + " " + grammem)

        #"012": "count of Adjectives",
        cnt = 0
        #print command.RawText
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma in lexem.get("Lemmas", []):
                for grammem in lemma.get("Grammems", []):
                    if grammem[0:2] == "A ":
                        cnt += 1
                        break
        if cnt > 0:
            self.__Append(featuresList, u"012: " + str(cnt))
        #"013": "Adj + свойства ",
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma in lexem.get("Lemmas", []):
                isOnlyAdj = True # добавляем только явные прилагательные
                for grammem in lemma.get("Grammems", []):
                    if grammem[0:2] != "A ":
                        isOnlyAdj = False
                if len(lemma.get("Grammems", [])) > 0 and isOnlyAdj == True:
                    self.__Append(featuresList, u"013: " + lemma.get("Text", "") + " " + grammem[0])


        #"014": "has anim",
        #"015": "has geo",
        #"016": "has yari",
        #"017": "yari command type",
        #"018": "Grammem of each word",
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma in lexem.get("Lemmas", []):
                # добавляем максимум первые три граммемы
                cnt = 0
                for grammem in lemma.get("Grammems", []):
                    cnt += 1
                    if cnt <= 3:
                        self.__Append(featuresList, u"018: " + grammem)

        #"019": "совершенность + переходность глагола pf ipf tran intr",
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma in lexem.get("Lemmas", []):
                if lemma.get("Language", "none") == "ru":
                    for grammem in lemma.get("Grammems", []):
                        for gr in grammem.split(" "):
                            if gr in ["pf", "ipf", "tran", "intr"]:
                                self.__Append(featuresList, u"019: " + gr)

        #"020": "имеет местоимение SPRO или APRO",
        #"021": "имеет Сущ в именительном или винительном ",
        #"022": "имеет Сущ persn, patrn, famn, mf, anim",
        hasAnimNoun = False
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma in lexem.get("Lemmas", []):
                if lemma.get("Language", "none") == "ru":
                    for grammem in lemma.get("Grammems", []):
                        for gr in grammem.split(" "):
                            if gr in ["persn", "patrn", "famn", "mf", "anim"]:
                                hasAnimNoun = True
        if hasAnimNoun == True:
            self.__Append(featuresList, u"022: 1")

        #"023": "имеет Сущ geo, abbr, loc",
        #"024": "имеет ANUM | A рядом с S",
        #"025": "падеж сущ рядом с глаголом",
        #"026": "отношение к-ва S к к-ву words without stop words",

        #"027": "PR",
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma in lexem.get("Lemmas", []):
                if "PR" in lemma.get("Grammems", []):
                    self.__Append(featuresList, u"027: " + lemma.get("Text", ""))

        #"028": "наличие связки V PR S в такой последовательности",
        #"029": "наличие связки PR|ADVPRO|SPRO|APRO и V не более чем через одно слово",
        feature029found = False
        prFound = False
        verbFound = False
        wordDist = 0
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma in lexem.get("Lemmas", []):
                for grammem in lemma.get("Grammems", []):
                    if ("PR " in grammem) or ("ADVPRO " in grammem) or ("SPRO " in grammem) or ("APRO " in grammem):
                        prFound = True
                if wordDist > 3:
                    prFound = False
                    verbFound = False
                    wordDist = 0
                elif prFound == True:
                    wordDist += 1
                    for grammem in lemma.get("Grammems", []):
                        if grammem[0:2] == "V ":
                            verbFound = True
                if verbFound == True and prFound == True and wordDist <= 3:
                    feature029found = True
        if feature029found == True:
            self.__Append(featuresList, u"029: " + "1")

        #"030": "наличие связки PR|ADVPRO|SPRO|APRO и S не более чем через одно слово",
        feature030found = False
        prFound = False
        nounFound = False
        wordDist = 0
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma in lexem.get("Lemmas", []):
                for grammem in lemma.get("Grammems", []):
                    if ("PR " in grammem) or ("ADVPRO " in grammem) or ("SPRO " in grammem) or ("APRO " in grammem):
                        prFound = True
                if wordDist > 3:
                    prFound = False
                    nounFound = False
                    wordDist = 0
                elif prFound == True:
                    wordDist += 1
                    for grammem in lemma.get("Grammems", []):
                        if grammem[0:2] == "S ":
                            nounFound = True
                if nounFound == True and prFound == True and wordDist <= 3:
                    feature030found = True
        if feature030found == True:
            self.__Append(featuresList, u"030: " + "1")

        #"031": "наличие связки V неPR S не более чем через одно слово"
        feature031Found = False
        verbFound = False
        prFound = False
        nounFound = False
        wordDist = 0
        #tokenLen = 0
        for lexem in command.Preprocessed.get("Morph", []):
            #tokens = lexem.get("Tokens", {})
            #tokensLen = int(tokens.get("End", "0")) - int(tokens.get("Begin", "0"))
            for lemma in lexem.get("Lemmas", []):
                for grammem in lemma.get("Grammems", []):
                    if grammem[0:3] == "PR ":
                        prFound = True
                if wordDist > 3 or prFound == True:
                    verbFound = False
                    prFound = False
                    nounFound = False
                    wordDist = 0

                elif verbFound == False:
                    for grammem in lemma.get("Grammems", []):
                        if grammem[0:2] == "V ":
                            verbFound = True
                            prFound = False
                            nounFound = False
                            wordDist = 1
                
                elif verbFound == True:
                    wordDist += 1
                    for grammem in lemma.get("Grammems", []):
                        if grammem[0:2] == "S ":
                            nounFound = True
                
                if verbFound == True and nounFound == True and wordDist <= 3:
                    feature031Found = True
        if feature031Found == True:
            self.__Append(featuresList, u"031: " + "1")



        #"032": "наличие слова на иностранном языке (но не на украинском)",
        #"033": "связка ADVPRO или APRO и безличный глагол (как называется)",
        #"034": "PART частица"
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma in lexem.get("Lemmas", []):
                if "PART" in lemma.get("Grammems", []):
                    self.__Append(featuresList, u"034: " + lemma.get("Text", ""))

        #"035": " наличие true или отсутствие false частицы 'не' PART частица"
        hasPartNot = 0
        for lexem in command.Preprocessed.get("Morph", []):
            for lemma in lexem.get("Lemmas", []):
                if (lemma.get("Text", "") == u"не") and ("PART" in lemma.get("Grammems", [])):
                    hasPartNot = 1
        self.__Append(featuresList, u"035: " + str(hasPartNot))

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

