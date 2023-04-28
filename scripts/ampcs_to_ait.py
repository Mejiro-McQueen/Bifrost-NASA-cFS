import yaml
from pathlib import Path
from functools import reduce
import json
import xmltodict
import re
from collections import OrderedDict

with open('./command.xml') as f:
    data = f.read()



def dictionary_lens(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)


j = json.loads(json.dumps(xmltodict.parse(data), indent=4))
j = dictionary_lens(j, 'command_dictionary.command_definitions.fsw_command')


class AMPCS_CMD():
    def __init__(self, opcode, stem, description, category):
        self.opcode = opcode
        self.stem = stem
        self.description = str(description)
        self.category = category
        self.arguments = []

        if self.description:
            self.description = self.description.replace(':', ';')

    @staticmethod
    def representer(dumper, data):
        d = {'name': data.stem,
             'opcode': data.opcode,
             'type': 'command',
             'subsystem': data.category,
             'desc': data.description,
             'arguments': data.arguments
             }
        return dumper.represent_mapping(u'!Command', d)

    def __repr__(self):
        return str(self.__dict__)


class AMPCS_ARG():
    def __init__(self, name, data_type, bit_length, default, description):
        self.name = name
        self.data_type = data_type
        self.bit_length = int(bit_length)
        self.default = default
        self.description = description
    
        if self.default and '0x' not in self.default and not self.data_type == 'string':
            self.default = int(default)
            
        if self.data_type == 'string':
            length = int(self.bit_length / 8)
            self.data_type = f'S{length}'
        elif self.data_type == 'unsigned':
            if self.bit_length == 8:
                self.data_type = 'U8'
            else:
                self.data_type = f'MSB_U{self.bit_length}'
            
        if self.default or self.default == 0:
            self.tag = '!Fixed'
        else:
            self.tag = '!Argument'

        if self.description:
            self.description = self.description.replace(':', ';')

    @staticmethod
    def representer(dumper, data):
        d = {'name': data.name,
             'desc': str(data.description),
             'units': None,
             'type': data.data_type,
             'value': data.default
             }
        return dumper.represent_mapping(data.tag, d)

    def __repr__(self):
        return str(self.__dict__)

yaml.add_representer(AMPCS_ARG, AMPCS_ARG.representer)
    
yaml.add_representer(AMPCS_CMD, AMPCS_CMD.representer)

commands = OrderedDict()
for entry in j:
    cmd = AMPCS_CMD(entry['@opcode'], entry['@stem'], entry['description'], entry['categories']['category']['@value'])
    for (ampcs_arg_type, arg_list) in entry['arguments'].items():
        if isinstance(arg_list, dict):
            print(entry)
            arg_list = [arg_list]
        for arg in arg_list:
            if ampcs_arg_type == 'numeric_arg':
                arg = AMPCS_ARG(arg['@name'], arg['@type'], arg['@bit_length'], arg['@default_value'], arg['description'])
            elif ampcs_arg_type == 'fixed_string_arg':
                default = arg.get('@default_value', None)
                arg = AMPCS_ARG(arg['@name'], 'string', arg['@bit_length'], default, arg['description'])
            cmd.arguments.append(arg)
    commands[cmd.stem] = cmd

with open("cmd.yaml", 'w') as f:
    for i in list(commands.values()):
        x = yaml.dump([i], indent=2, default_style=False, default_flow_style=False, sort_keys=False)
        x = x.replace("'", '')
        f.write(x)
        f.write('\n')
