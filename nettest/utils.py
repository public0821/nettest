import struct
import array

def mac2str(mac):
    """Converts mac address to string .
   
        Args:
            mac: 6 bytes mac address
    
        Returns:
            readable string 
            
    """
    return '%02x:%02x:%02x:%02x:%02x:%02x'%tuple(int(x) for x in struct.unpack('BBBBBB', mac))

def str2mac(s):
    """Converts string to mac address .
   
        Args:
            s: 'xx:xx:xx:xx:xx:xx' format string
    
        Returns:
            6 bytes mac address 
            
    """
    mac = tuple(int(x,16) for x in s.split(":"))
    return struct.pack('BBBBBB', mac[0], mac[1], mac[2], mac[3], mac[4], mac[5])


   
def checksum(data):
    '''Calculate checksum
    
        more about checksum, see http://tools.ietf.org/html/rfc1071
    '''
    if len(data) & 1:
        data = data + '\0'
    words = array.array('h', data)
    checksum = 0
    for word in words:
        checksum += (word & 0xffff)
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = checksum + (checksum >> 16)

    return (~checksum) & 0xffff
