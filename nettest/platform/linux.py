import socket
import struct
from fcntl import ioctl

# From bits/ioctls.h
SIOCGIFHWADDR  = 0x8927          # Get hardware address    
SIOCGIFADDR    = 0x8915          # get PA address          
SIOCGIFNETMASK = 0x891b          # get network PA mask     
SIOCGIFNAME    = 0x8910          # get iface name          
SIOCSIFLINK    = 0x8911          # set iface channel       
SIOCGIFCONF    = 0x8912          # get iface list          
SIOCGIFFLAGS   = 0x8913          # get flags               
SIOCSIFFLAGS   = 0x8914          # set flags               
SIOCGIFINDEX   = 0x8933          # name -> if_index mapping
SIOCGIFCOUNT   = 0x8938          # get number of devices
SIOCGSTAMP     = 0x8906          # get packet timestamp (as a timeval)

def __get_if(iff,cmd):
    s=socket.socket()
    ifreq = ioctl(s, cmd, struct.pack("16s16x",iff.encode()))
    s.close()
    return ifreq

def get_if_hwaddr(iff):
    """Get iff's mac address.
   
        Args:
            iff: interface name,  eg:  eth0
    
        Returns:
             6 bytes mac address 
            
    """
    return struct.unpack("18x6s8x",__get_if(iff,SIOCGIFHWADDR))[0]

def get_if_addr(iff):
    """Get iff's ipv4 address.
   
        Args:
            iff: interface name,  eg:  eth0
    
        Returns:
             4 bytes ipv4 address in network byte order
            
    """
    try:
        return __get_if(iff, SIOCGIFADDR)[20:24]
    except IOError:
        return b"\x00\x00\x00\x00"
        