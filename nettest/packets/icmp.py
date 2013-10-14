
from nettest.packets.base import Packet
from nettest.packets.fields import IntegerField, BytesField
import os



class IcmpHeader(Packet):
    type = IntegerField(length=1, default=0) # message type
    code = IntegerField(length=1, default=0)    # type sub-code
    checksum = IntegerField(length=2, default=0)
    
    fields = ['type', 'code', 'checksum']
    
    
class IcmpEcho(Packet):
    header = IcmpHeader()
    id = IntegerField(length=2, default=os.getpid())
    sequence = IntegerField(length=2, default=0)
    timestamp = IntegerField(length=4, default=0)
    options = BytesField()
    fields = ['header', 'id', 'sequence', 'timestamp', 'options']

ICMP_ECHOREPLY  = 0    # Echo Reply            
ICMP_DEST_UNREACH  =  3    # Destination Unreachable    
ICMP_SOURCE_QUENCH =   4    # Source Quench        
ICMP_REDIRECT    =    5    # Redirect (change route)    
ICMP_ECHO     =   8    # Echo Request            
ICMP_TIME_EXCEEDED  =  11    # Time Exceeded        
ICMP_PARAMETERPROB =   12    # Parameter Problem        
ICMP_TIMESTAMP  =      13    # Timestamp Request        
ICMP_TIMESTAMPREPLY  =  14   # Timestamp Reply        
ICMP_INFO_REQUEST  =  15    # Information Request        
ICMP_INFO_REPLY    =    16   # Information Reply        
ICMP_ADDRESS   =     17    # Address Mask Request        
ICMP_ADDRESSREPLY  =  18    # Address Mask Reply        
NR_ICMP_TYPES    =    18


# Codes for UNREACH. 
#define ICMP_NET_UNREACH    0    /* Network Unreachable        */
#define ICMP_HOST_UNREACH    1    /* Host Unreachable        */
#define ICMP_PROT_UNREACH    2    /* Protocol Unreachable        */
#define ICMP_PORT_UNREACH    3    /* Port Unreachable        */
#define ICMP_FRAG_NEEDED    4    /* Fragmentation Needed/DF set    */
#define ICMP_SR_FAILED        5    /* Source Route failed        */
#define ICMP_NET_UNKNOWN    6
#define ICMP_HOST_UNKNOWN    7
#define ICMP_HOST_ISOLATED    8
#define ICMP_NET_ANO        9
#define ICMP_HOST_ANO        10
#define ICMP_NET_UNR_TOS    11
#define ICMP_HOST_UNR_TOS    12
#define ICMP_PKT_FILTERED    13    /* Packet filtered */
#define ICMP_PREC_VIOLATION    14    /* Precedence violation */
#define ICMP_PREC_CUTOFF    15    /* Precedence cut off */
#define NR_ICMP_UNREACH        15    /* instead of hardcoding immediate value */

# Codes for REDIRECT. 
#define ICMP_REDIR_NET        0    /* Redirect Net            */
#define ICMP_REDIR_HOST        1    /* Redirect Host        */
#define ICMP_REDIR_NETTOS    2    /* Redirect Net for TOS        */
#define ICMP_REDIR_HOSTTOS    3    /* Redirect Host for TOS    */

# Codes for TIME_EXCEEDED. 
#define ICMP_EXC_TTL        0    /* TTL count exceeded        */
#define ICMP_EXC_FRAGTIME    1    /* Fragment Reass time exceeded    */

