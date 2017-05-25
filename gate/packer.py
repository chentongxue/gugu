# coding=utf-8
import struct
import json


class DataPack(object):
    def __init__(self):
        self.fmt = 'iii'
        self.version = 0

    @property
    def head_len(self):
        return struct.calcsize(self.fmt)

    def pack(self, command_id, data):
        s = json.dumps(data)
        length = len(s) + self.head_len
        result = struct.pack(self.fmt, length, command_id, 0)
        result += s
        return result

    def unpack(self, data):
        head = data[0:self.head_len]
        result = struct.unpack(self.fmt, head)
        s = data[self.head_len:]
        s = json.loads(s)
        return result[1], s


if __name__ == '__main__':
    packer = DataPack()
    binary = packer.pack(100, {'k': 'v'})
    raw_data = packer.unpack(binary)
