import yaml
from pathlib import Path
from enum import Enum, auto
import shlex
from functools import reduce


import xmltodict

def deep_get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)


with open('./apid.xml', 'rb') as f:
    q = xmltodict.parse(f)

opcode_lookup = {entry['title']:entry['@apid'] for entry in deep_get(q, 'apid_dictionary.apids.apid_definition')}


class COSMOS_TELEMETRY_KEYWORDS(Enum):
    APPEND_ID_ITEM = auto()
    APPEND_ITEM = auto()
    ID_ITEM = auto()
    TELEMETRY = auto()
    APPEND_ARRAY_ITEM = auto()


class COSMOS_DATA_TYPES(Enum):
    INT = auto()
    UINT = auto()
    FLOAT = auto()
    STRING = auto()
    BLOCK = auto()
    DERIVED = auto()

    
class COSMOS_ENDIANESS(Enum):
    BIG_ENDIAN = auto()
    LITTLE_ENDIAN = auto()


class COSMOS_TELEMETRY():
    
    def __init__(self, target, packet_name, endianess, description):
        self.target = target
        self.packet_name = packet_name
        self.endianess = endianess
        self.description = description
        self.items = []

    @staticmethod
    def representer(dumper, data):
        m = [i for i in data.items if 'CCSDS' not in i.name]
        d = {'name': data.packet_name,
             'desc': data.description,
             'opcode': int(opcode_lookup.get(data.packet_name, 0)),
             'fields': m}
        return dumper.represent_mapping(u'!Packet', d)


yaml.add_representer(COSMOS_TELEMETRY,
                     COSMOS_TELEMETRY.representer)
    

class COSMOS_TELEMETRY_APPEND_ITEM():
    yaml_tag = u'!Field'
    
    def __init__(self, name, bit_size, data_type, description, *args):
        self.name = name
        self.bit_size = bit_size
        self.data_type = data_type
        self.description = description

        self.__post_init__()

    def __post_init__(self):
        if 'Parent:' in self.description:
            self.description = None

    @staticmethod
    def representer(dumper, data):
        d = {}
        d['name'] = data.name
        d['desc'] = data.description
        d['type'] = d_type_to_ait(data.bit_size, data.data_type)
        #d['bytes'] = int(data.bit_size)
        d['units'] = None
        d['mask'] = None
        return dumper.represent_mapping(u'!Field', d)


yaml.add_representer(COSMOS_TELEMETRY_APPEND_ITEM,
                     COSMOS_TELEMETRY_APPEND_ITEM.representer)
    
@dataclass
class COSMOS_TELEMETRY_APPEND_ID_ITEM():
    
    def __init__(self, name, bit_size, data_type, id_value, description, *args):
        self.name = name
        self.bit_size = bit_size
        self.data_type = data_type
        self.id_value = id_value
        self.description = description


class COSMOS_TELEMETRY_APPEND_ARRAY_ITEM():

    def __init__(self, name, item_bit_size, item_data_type, array_bit_size, description, *args):
        self.name = name
        self.item_bit_size = item_bit_size
        self.item_data_type = item_data_type
        self.array_bit_size = array_bit_size
        self.description = description

    def __post_init__(self):
        if 'Parent:' in self.description:
            self.description = None

    @staticmethod
    def representer(dumper, data):
        slots = int(int(data.array_bit_size) / 8)
        d = {}
        d['name'] = data.name
        d['desc'] = data.description
        d['type'] = d_type_to_ait(data.item_bit_size, data.item_data_type, slots)
        #d['bytes'] = int(data.item_bit_size)
        d['units'] = None
        d['mask'] = None
        return dumper.represent_mapping(u'!Field', d)


yaml.add_representer(COSMOS_TELEMETRY_APPEND_ARRAY_ITEM,
                     COSMOS_TELEMETRY_APPEND_ARRAY_ITEM.representer)


def d_type_to_ait(num, d_type, array=False):
    if num == '8':
        s = f"{d_type[0]}{num}"
    else:
        s = f'MSB_{d_type[0]}{num}'
    if array:
        s += f'[{array}]'
    return s

lookup = {COSMOS_TELEMETRY_KEYWORDS.TELEMETRY: COSMOS_TELEMETRY,
          COSMOS_TELEMETRY_KEYWORDS.APPEND_ITEM: COSMOS_TELEMETRY_APPEND_ITEM,
          COSMOS_TELEMETRY_KEYWORDS.APPEND_ID_ITEM: COSMOS_TELEMETRY_APPEND_ID_ITEM,
          COSMOS_TELEMETRY_KEYWORDS.APPEND_ARRAY_ITEM: COSMOS_TELEMETRY_APPEND_ARRAY_ITEM}
    

s = './TO_tlm'

with Path(f'./{s}.txt').open() as f:
    d = f.readlines()
    d = [i.strip() for i in d]

res = []
current = None

# for i in d:
#     print(i)

for i in d:
    if not i:
        # Empty line seperating entries
        # Start over
        res.append(current)
        current = None
        continue
    
    items = shlex.split(i)
    if '#' in items[0]:
        #current.items.append(items)
        continue
    t = COSMOS_TELEMETRY_KEYWORDS[items[0]]
    k = lookup[t](*items[1:])

    if not current:
        current = k
    else:
        current.items.append(k)

# Pickup last
res.append(current)

with open(Path(f'./{s}.yaml'), 'w') as f:
    yaml.dump(res, f, sort_keys=False)
    print(yaml.dump(res, sort_keys=False))
