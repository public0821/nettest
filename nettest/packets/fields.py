from abc import abstractmethod
from nettest import utils
from nettest.exceptions import NettestError
import socket
import struct

class Field(object):
    def __init__(self, length=0, default=None):
        self._default_value = default
        self._length = length
    
    @property
    def default_value(self):
        return self._default_value
    
    @property
    def length(self):
        return self._length
    
    #return bytes    
    @abstractmethod    
    def to_netbytes(self, value):
        """Convert the value to bytes in network byte order .
   
        Args:
            value: data to be converted.
    
        Returns:
            bytes in network byte order 
            
        """
        pass
    
 
    def from_netbytes(self, data):
        """Restore data from the bytes .
   
        Args:
            value: bytes to be restored (in network byte order ).
    
        Returns:
            formated data
            
        """
        return None
    
    @abstractmethod    
    def to_printable(self, value):
        """Convert the value to printable object.
   
        Args:
            value: data to be converted.
    
        Returns:
            an object can be outputted by print() function
            
        """
        pass

class IntegerField(Field):
    
    LEN_TO_FMT={1:'!B', 2:'!H', 4:'!I', 8:'!Q'}
    
    def __init__(self, length, default=0):
        if length not in self.LEN_TO_FMT.keys():
            raise NettestError(_("unsupported integer length: %d")%(length))
        super(IntegerField , self).__init__(length=length, default=default)
    
    def to_netbytes(self, value):
        data = struct.pack(self.LEN_TO_FMT[self.length], int(value))
        return data
    
    def from_netbytes(self, data):
        value = struct.unpack(self.LEN_TO_FMT[self.length], data[:self.length])[0]
        return value
    
    def to_printable(self, value):
        return '%s (%d)'%(hex(int(value)), int(value))

class Ipv4Field(Field):
    
    def __init__(self, default='0.0.0.0'):
        super(Ipv4Field , self).__init__(length=4, default=default)
    
    def to_netbytes(self, value):
        if isinstance(value, str):
            return socket.inet_aton(value)
        elif isinstance(value, bytes):
            return value[:4]
        elif isinstance(value, int):
            return struct.pack('!I', int(value))
        raise NettestError(_("invailed ip value {0}").format(value))
    
    def from_netbytes(self, data):
        return socket.inet_ntoa(data[:4])
    
    def to_printable(self, value):
        if isinstance(value, bytes):
            return socket.inet_ntoa(value[:4])
        elif isinstance(value, int):
            return socket.inet_ntoa(struct.pack('!I', value))
        
        return str(value)
    
class MacField(Field):
    
    def __init__(self, default='0.0.0.0'):
        super(MacField , self).__init__(length=6,default=default)
    
    def to_netbytes(self, value):
        if isinstance(value, bytes):
            return value[:6]
        return utils.str2mac(value)
    
    def from_netbytes(self, data):
        return utils.mac2str(data[:6])
    
    def to_printable(self, value):
        return str(value)
    
#class CharField(Field):
    #def __init__(self, max_length=0, default='', encoding='utf-8'):
        #super(CharField, self).__init__(default=default)
        #self.encoding = encoding
        #self.max_length = max_length
        
    #def to_netbytes(self, value):
        #return str(value).encode(self.encoding)[:self.max_length]
    
    ##make sure value's length not max than max_length
    #def to_printable(self, value):
        #return str(value).encode(self.encoding)[:self.max_length].decode(self.encoding)

class BytesField(Field):
    def __init__(self, default=b''):
        super(BytesField, self).__init__(default=default)
        
    def to_netbytes(self, value):
        if not isinstance(value, bytes):
            raise NettestError(_("not bytes value: ") + str(value))
        return value
    
    def to_printable(self, value):
        if not isinstance(value, bytes):
            raise NettestError(_("not bytes value: ") + str(value))
        return value
    
class FieldList(Field):
    def __init__(self, fieldtype, default=[]):
        super(BytesField, self).__init__(default=default)
        self.field = fieldtype()
        
    def to_netbytes(self, values):
        data = b''
        if not isinstance(values, []):
            raise NettestError(_("not list value: ") + str(values))
        for value in values:
            data += self.field.to_netbytes(value)
        return data
    
    def to_printable(self, values):
        data = []
        if not isinstance(values, []):
            raise NettestError(_("not list value: ") + str(values))
        for value in values:
            data.append(self.field.to_printable(value))
        return data
    
class BitField(Field):
    def __init__(self, length, default=0):
        super(BitField, self).__init__(length=length, default=default)
        if not (1 <= length <= 64):
            raise NettestError(_("bit field's length should between 1 and 64: ") + str(length))

    def to_netbytes(self, value):
        raise NettestError(_("bit field can't convert to netbytes"))

            
    def from_netbytes(self, data, start):
        '''
        '''
        data_len = len(data)
        if data_len == 1:
            value = struct.unpack('!B', data)[0]
        elif data_len == 2:
            value =  struct.unpack('!H', data)[0]
        elif data_len == 4:
            value =  struct.unpack('!I', data)[0]
        elif data_len == 8:
            value =  struct.unpack('!Q', data)[0]
        
        temp_bit = 0x0000000000000001
        bit_mask = 0
        for i in range(data_len * 8 - (self.length + start), data_len * 8 - start):
            bit_mask += temp_bit << i
                
        return (value & bit_mask) >> (data_len * 8 - (self.length + start))

    def to_printable(self, value):
        return '%s (%d)'%(hex(int(value)), int(value))
