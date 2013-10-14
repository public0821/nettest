from .fields import BitField, Field
from nettest.exceptions import NettestError
import struct

class PacketMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = attrs.get('fields')
        if fields is None:
            raise NettestError(_("packet class must have 'fields' field"))
        _fields = []
        for fieldname in attrs['fields']:
            field = attrs.get(fieldname)
            if field is None:
                for baseclass in bases:
                    field = getattr(baseclass, fieldname)
                    if field is not None:
                        break
                else:
                    raise NettestError(_("field '%s' doesn't exsists in class %s")%(fieldname, name))
            if not cls.__check_field_type(cls, field):
                raise NettestError(_("field '%s' in class %s should be in type (Field, Packet, list)")%(fieldname, name))
            
            _fields.append((fieldname, field))
            if isinstance(field, Field):
                attrs[fieldname] = field.default_value
        if '_fields' in attrs:
            raise NettestError(_("the name '_fields' is reserved in class %s")%(name))
        attrs['_fields']= _fields   
        return super(PacketMeta, cls).__new__(cls, name, bases, attrs)
    
    @staticmethod
    def __check_field_type(cls, field):
        if not isinstance(field, (Field, Packet, list)):
            return False
        if isinstance(field, (list)):
            for subfield in field:
                if not cls.__check_field_type(cls, subfield):
                    return False
        return True
    
class BitDumper(object):
    def __init__(self):
        self.data= []
        self.data_len = []
        self.data_len_sum = 0

    def clear(self):
        self.data = []
        self.data_len = []
        self.data_len_sum = 0

    def push(self, data, length):
        data = int(data)
        if data < 0 or data > 2**length:
            raise NettestError(_("bit value out of range"))
        self.data.append(data)
        self.data_len.append(length)
        self.data_len_sum += length

    def dump(self):
        if self.data_len_sum % 8 != 0:
            raise NettestError(_("incorrect bit field length"))
        data = 0
        left_len = self.data_len_sum
        index = 0
        for field_data in self.data:
            data += field_data<<(left_len - self.data_len[index]) 
            left_len -= self.data_len[index]
            index += 1
        length = self.data_len_sum / 8
        if length == 1:
            return struct.pack('!B', int(data))
        elif length == 2:
            return struct.pack('!H', int(data))
        elif length == 4:
            return struct.pack('!I', int(data))
        elif length == 8:
            return struct.pack('!Q', int(data))
        else:
            raise NettestError(_("too long bit field"))
        
class BitLoader(object):
    def __init__(self, packet):
        self.fields = []
        self.bit_len_sum = 0
        self.packet = packet

    def clear(self):
        self.fields = []
        self.bit_len_sum = 0

    def push(self, fieldname, field):
        self.fields.append((fieldname,field))
        self.bit_len_sum += field.length

    def load(self, data):
        if self.bit_len_sum % 8 != 0:
            raise NettestError(_("incorrect bit field length"))
        byte_len = int(self.bit_len_sum / 8)
        data = data[:byte_len]
        loaded_len = 0
        for field_name, field in self.fields:
            field_data = field.from_netbytes(data, loaded_len)
            loaded_len += field.length
            setattr(self.packet, field_name, field_data)
        
        return byte_len

   

class Packet(object, metaclass=PacketMeta):
    
    '''define field order
    '''
    fields=[]
    
    def __init__(self):
        for field_name, field in self._fields:
            if isinstance(field, Packet):
                setattr(self, field_name, field.__class__())
                
    def dump(self):
        '''Serialize self to bytes
        '''
        data = b''
        bit_dumper = BitDumper()
        for field_name, field in self._fields:
            field_value = getattr(self, field_name)
            if field_value is None:
                raise NettestError(_("%s is None and haven't default value")%(field_name))
            if isinstance(field, BitField):
                bit_dumper.push(field_value, field.length)
                continue
            else:
                if bit_dumper.data_len_sum > 0:
                    data += bit_dumper.dump()
                    bit_dumper.clear()

            if isinstance(field, Packet):
                data += field_value.dump()
                continue
            data += field.to_netbytes(field_value)
        if bit_dumper.data_len_sum > 0:
            data += bit_dumper.dump()
        return data
    
#     def __dump_list_data(self, fields):
#         data = b''
#         for field in fields:
#             if isinstance(field, Packet):
#                 data += field.dump()
#                 continue
#             if isinstance(field, list):
#                 data += self.__dump_list_data()
#                 continue
#             if isinstance(field, Field):
#                 data += field.to_netbytes(field_value)
#                 continue
    
    def load(self, data):
        '''Deserialize bytes to a self.
        
            if success, return the total data length used
            else return None
        '''
        loaded_len = 0
        bit_loader = BitLoader(self)
        for field_name, field in self._fields:
            if isinstance(field, BitField):
                bit_loader.push(field_name, field)
                continue
            else:
                if bit_loader.bit_len_sum > 0:
                    loaded_len += bit_loader.load(data[loaded_len:])
                    bit_loader.clear()

            if isinstance(field, Packet):
                field_value = getattr(self, field_name)
                length = field_value.load(data[loaded_len:])
                if length is None:
                    return None
                loaded_len += length
                continue
            field_data = field.from_netbytes(data[loaded_len:])
            if field_data is None:
                return None
            loaded_len += field.length
            setattr(self, field_name, field_data)
            
        if bit_loader.bit_len_sum > 0:
            loaded_len += bit_loader.load(data[loaded_len:])
            
        return loaded_len
    
    def to_printable(self):
        string = ''
        string += '-'*20+str(self.__class__.__name__)+'-'*20+'\n'
        for field_name, field in self._fields:
            field_value = getattr(self, field_name)
            if field_value is None:
                string += '%s\tNone\n'%(field_name)
            elif isinstance(field, Packet):
                string += '%s\t%s\n'%(field_name, field_value.to_printable())
            else:
                string += '%s\t%s\n'%(field_name, field.to_printable(field_value))
        string += '-'*(40+len(self.__class__.__name__))+'\n'
        return string
    
    def __eq__(self, other):
        for field_name in self.fields:
            field_value1 = getattr(self, field_name)
            field_value2 = getattr(other, field_name)
            if field_value1 != field_value2:
                return False
        return True
    
    @property
    def length(self):
        total_len = 0
        bit_len = 0
        for field_name, field in self._fields:
            if isinstance(field, BitField):
                bit_len += field.length
            elif field.length > 0:
                total_len += field.length
            else:
                field_value = getattr(self, field_name)
                total_len += len(field_value)
        total_len += int(bit_len/8)
        return total_len
