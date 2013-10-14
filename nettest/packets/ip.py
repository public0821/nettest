from nettest.packets.base import Packet
import socket
from nettest.packets.fields import BitField, IntegerField, Ipv4Field, BytesField

ipproto_dict = {'UDP':socket.IPPROTO_UDP
            , 'TCP':socket.IPPROTO_TCP
            , 'ICMP':socket.IPPROTO_ICMP}


class IpHeader(Packet):
    version = BitField(length=4, default=0x04)  #version
    ihl = BitField(length=4, default=0x05) #header length
    
    #type of service
    tos_priority = BitField(length=3, default=0) 
    tos_min_delay = BitField(length=1, default=0) 
    tos_max_throughput = BitField(length=1, default=0) 
    tos_highest_reliability = BitField(length=1, default=0) 
    tos_min_cost = BitField(length=1, default=0) 
    tos_zero = BitField(length=1, default=0)    #reserved service flag 
    
    tot_len = IntegerField(length=2, default=0)  #total length
    id = IntegerField(length=2, default=0)   #identification
    
    #fragment offset field
    frag_off_zero = BitField(length=1, default=0)   #reserved fragment flag 
    frag_off_donot_fragment = BitField(length=1, default=0)
    frag_off_more_fragment = BitField(length=1, default=0)
    frag_off_offset = BitField(length=13, default=0)
    
    ttl = IntegerField(length=1, default=64)     #time to live 
    protocol = IntegerField(length=1)     #protocol
    check = IntegerField(length=2, default=0)     #checksum 
    saddr = Ipv4Field()     #source address  
    daddr  = Ipv4Field()    #dest address 
    
    options= BytesField()

    fields = ['version', 'ihl']
    fields += ['tos_priority', 'tos_min_delay', 'tos_max_throughput', 'tos_highest_reliability', 'tos_min_cost', 'tos_zero']
    fields += ['tot_len', 'id']
    fields += ['frag_off_zero', 'frag_off_donot_fragment', 'frag_off_more_fragment', 'frag_off_offset']
    fields += ['ttl', 'protocol', 'check', 'saddr', 'daddr']
    fields += ['options']
