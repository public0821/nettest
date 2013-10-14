from  .base import Packet
from  .fields import IntegerField, MacField, Ipv4Field

ETH_P_ALL = 3           #Every packet (be careful!!!) 
ETH_P_IP = 0x800        #Internet Protocol packet
ETH_P_ARP = 0x806       #Address Resolution packet
ETH_P_IPV6 = 0x86dd     #IPv6 over bluebook       
ETH_P_RARP = 0x8035     #Reverse Addr Res packet    
    
class EtherHeader(Packet):
    h_dest = MacField( default='ff:ff:ff:ff:ff:ff') # destination eth addr  
    h_source = MacField(default='00:00:00:00:00:00')    # source ether addr 
    h_proto = IntegerField(length=2) # packet type ID field 
    
    fields = ['h_dest', 'h_source', 'h_proto']

