#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
from copy import deepcopy
from datetime import datetime
import sys
from pprint import pprint


def pretty_print(object):
    class decoder_stream:
        def write(self, s):
            if s.startswith("'") and s.endswith("'"):
                s = "'%s'" % s[1:-1].decode('string_escape')
            elif s.startswith("u'") and s.endswith("'"):
                s = "u'%s'" % s[2:-1].decode('unicode_escape').encode('utf8')
            sys.stdout.write(s)

    pprint(object, decoder_stream())


def log(comment, object):
    print comment
    if object is not None:
        pretty_print(object)
    print


# начальное состояние long-term memory, шаблоны команд и концептов
LTM = '''
commands:
  Weather:
    time: 'сейчас'
  go:
    dst:
    src:
    via: ''
  ScheduleMeeting:
    CmdType: "ScheduleMeeting"
    room:
    person:
'''

DICTIONARY = {
    'dst': 'место назначения',
    'src': 'исходную точку',
    'via': 'пункты следования',
    'room': 'комнату',
    'time': 'время',
    'duration': 'продолжительность',
    'CmdType': 'команду',
    'person': 'список приглашенных',
}


def aggregate_facts(facts):
    result = {}
    for (key, data) in facts:
        if not key in result:
            result[key] = []
        data = data.encode('utf8') if isinstance(data, unicode) else data
        result[key].append(data)
    for key in result:
        if len(result[key]) == 1:
            result[key] = result[key][0]
    return result


class DM(object):
    def __init__(self):
        # short-term memory, держит текущий стек контекстов
        self.stm = []

        # long-term memory, держит объекты из предыдущих контекстов
        self.ltm = yaml.load(LTM)
        log("Загрузили LTM", self.ltm)

    def supplement_context(self, facts):
        # аггрегируем факты с одинаковыми ключами
        facts = aggregate_facts(facts)

        # если поступила команда, переключаем контекст
        cmd = facts.pop('CmdType', None)
        if cmd:
            if cmd == 'Cancel':
                self.stm = []
            elif cmd in self.ltm['commands']:
                if (len(self.stm) and self.stm[-1].get('CmdType', None) != cmd) or (len(self.stm) == 0):
                        template = deepcopy(self.ltm['commands'][cmd])
                        for key in template:
                            if key == "person":
                                template[key] = []
                        template['CmdType'] = cmd
                        log("Нашли шаблон команды", template)
                        self.stm.append(template)
                        log("Переключили контекст", self.stm)
        if len(self.stm):
            # дополняем фактами текущий контекст
            context = self.stm[-1]
            log("Текущий контекст", context)
            for concept in context:
                if concept in facts:
                    if type(context[concept]) is list:
                        if type(facts[concept]) is list:
                            context[concept].extend(facts[concept])
                        else:
                            context[concept].append(facts[concept])
                    else:
                        context[concept] = facts[concept]

            log("Дополнили фактами", self.stm)

    def execute(self):
        if len(self.stm):
            context = self.stm[-1]
            log("Выполняем в контексте", context)

            # дополняем незаполненные поля
            for c_key in context:
                concept = context[c_key]
                if concept is None:
                    concept = self.try_guess(c_key)
                    if concept is None:
                        return {'ask': c_key}
                    else:
                        context[c_key] = concept
            self.stm.pop()
            return {'run': context}
        else:
            return {'ask': 'CmdType'}

    def try_guess(self, c_key):
        result = None
        if c_key == 'time':
            result = datetime.now()
        print "Guessing '%s': %s" % (c_key, result)
        return result

    def generate_phrase(self, cmd):
        phrase = []
        if 'run' in cmd:
            phrase.append("Запускаем:")
            for key in cmd['run']:
                if type(cmd['run'][key]) is list:
                    phrase.append("%s([ " % key)
                    phrase.append("%s" % ", ".join(cmd['run'][key]))
                    phrase.append(" ])")
                else:
                    phrase.append("%s(%s)" % (key, cmd['run'][key]))
        if 'ask' in cmd:
            phrase.append("Укажите")
            key = cmd['ask']
            if key in DICTIONARY:
                phrase.append(DICTIONARY[key])

        return ' '.join(
            word if isinstance(word, unicode) else word.decode('utf8')
            for word in phrase
        )


def main():
    dm = DM()
    print dm.generate_phrase({
        'run': {
            'hello': u'котя',
        }
    })
    dm.supplement_context([
        ('CmdType', 'go'),
        ('dst', u'велотрек в крылатском'),
    ])
    result = dm.generate_phrase(dm.execute())
    log("Результат выполнения", result)

    dm.supplement_context([
        ('src', 'Льва Толстого, 16'),
    ])
    result = dm.generate_phrase(dm.execute())
    log("Результат выполнения", result)

    dm.supplement_context([
        ('CmdType', 'ScheduleMeeting'),
        ('room', '404'),
    ])
    result = dm.generate_phrase(dm.execute())
    log("Результат выполнения", result)

    dm.supplement_context([
        ('duration', '1 час'),
    ])
    result = dm.generate_phrase(dm.execute())
    log("Результат выполнения", result)


if __name__ == '__main__':
    main()
