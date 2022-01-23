"""
Author: Darren
Date: 16/12/2021

Solving https://adventofcode.com/2021/day/16

We've received a transmission in BITS format. This is a single line hex string, e.g.
C200B40A82

The input data is a single outer packet, which contains one or more adjacent packets.
In turn, these packets can contain other packets.
Hex values should be converted to binary before decoding.

Individual packet structure:
vvvttt[n*p][x*0]
where v = 3 bit packet version
      t = 3 bit packet type
      p = literal (l) or operator (o)
      x = 0, to pad out remaining bits, given bit length must be //4

If t=4, then packet type is l (literal); else packet type is o (operator).

Part 1:
    We want the sum of version numbers of all packets.  
    Subpackets have version numbers, so we need to sum them.
    Parse input and convert from hex to binary. Create outer Packet from this data.
    Process the input bits according to the rules, and track how many bits consumed.
    Hold a list of subpackets.  Track the depth of subpackets.
    When creating subpackets, consume bits as needed to create the subpackets,
    and then pass the remaining bits to the next.
    To return the sum, just recurse.

Part 2:
    Now we need to calculate a value based on the packet type.
    This is pretty trivial.  Recurse in the same way as we did for the version sum.
"""
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

class Packet():
    """ Processes a BITS packet, including recursive processing of any inner packets. """
    VER_START = 0
    TYPE_START = 3
    VAL_START = 6
    
    def __init__(self, bin_input_stream: str, level=0) -> None:
        """ Creates a packet instance. Expects the input as str of bits. 
        Nesting level defaults to 0. Sub-packets have level incremented automatically. """
        
        self._bin_in_str = bin_input_stream     # The raw binary data given to the class
        self._processed_bin_digits = 0  # Increment this throughout stages
        self._level = level     # Nesting level.  Starts at level 0

        logger.debug("Lvl=%s: raw bin=%s", self._level, self._bin_in_str)
        
        self._literal_val = 0
        self._sub_packets: list[Packet] = []      # any nested packets
        self._version = int(self._bin_in_str[Packet.VER_START:Packet.TYPE_START], 2)
        self._processed_bin_digits += Packet.TYPE_START
        
        self._process_type()    # evaluate if literal or operation type and process accordingly
        self._bin_in_self = bin_input_stream[0:self._processed_bin_digits]   # All the bits that represent this packet
        self._remaining_from_stream = bin_input_stream[self._processed_bin_digits:] # Bits we haven't yet consumed from input
    
    def __len__(self):
        """ The length of this packet (including subpackets), but excluding extraneous data from the input stream """
        return len(self._bin_in_self)
    
    @property
    def value(self) -> int:
        """ Determine value for this type of packet, recursively. """
        val = 0
        
        if self._type == 0:  # recursive sum of values
            for sub_packet in self._sub_packets:
                val += sub_packet.value
        elif self._type == 1:   # recursive product of values
            val = 1
            for sub_packet in self._sub_packets:
                val *= sub_packet.value
        elif self._type == 2:   # minimum of sub-packets
            val = min(sub_packet.value for sub_packet in self._sub_packets)
        elif self._type == 3:   # maximum of sub-packets
            val = max(sub_packet.value for sub_packet in self._sub_packets)
        elif self._type == 4:   # return the value encoding in the literal (type 4) packet
            val = self._literal_val
        elif self._type == 5:   # 1 if 1st packet > 2nd packet, else 0
            val = 1 if self._sub_packets[0].value > self._sub_packets[1].value else 0
        elif self._type == 6:   # 1 if 1st packet < 2nd packet, else 0
            val = 1 if self._sub_packets[0].value < self._sub_packets[1].value else 0
        elif self._type == 7:   # 1 if 1st packet == 2nd packet, else 0
            val = 1 if self._sub_packets[0].value == self._sub_packets[1].value else 0
        else:
            assert False, "We should never get here!"
            
        return val
                
    @property
    def version_sum(self) -> int:
        """ The sum of the version of this packet, as well as the versions of all subpackets. """
        return self._version + sum(sub_packet.version_sum for sub_packet in self._sub_packets)

    @property
    def remaining_from_stream(self):
        """ Returns unconsumed BINARY digits. """
        return self._remaining_from_stream
      
    def _process_type(self):
        """ Determine whether literal (type 4) or operator (type other) packet """
        self._type = int(self._bin_in_str[Packet.TYPE_START:Packet.VAL_START], 2)
        self._processed_bin_digits += Packet.VAL_START - Packet.TYPE_START
        if self._type == 4: # literal
            self._literal_val = self._process_literal()
        else: # operator
            self._process_operator()
            
    def _process_literal(self):
        """ [5*l] where each block of 5 bits starts with a 1, except the last. """
        grp_len = 5
        # grab groups one at a time, until we grab the one starting with a 0
        
        groups_start = Packet.VAL_START
        grps = ""
        while True:
            group = self._bin_in_str[groups_start:groups_start + grp_len]
            grps += group[1:]  # Not interested in first digit of each group
            self._processed_bin_digits += grp_len
            if group[0] == '0':   # this is the last group
                break
            
            groups_start += grp_len 
        
        self._literal_bin = grps
        return int(self._literal_bin, 2) 

    def _process_operator(self):
        """ If m=0, next 15 bits are total length of subpackets: [m[bbbbbbbbbbbbbbb]s*[]]
        If m=1, next 11 bits are the number of subsequent subpackets """
        SUBPACKETS_LEN_FIELD_SZ = 15
        SUBPACKETS_CONTAINED_FIELD_SZ = 11
        
        len_type_id = int(self._bin_in_str[Packet.VAL_START])
        self._processed_bin_digits += 1
        
        if len_type_id == 0: 
            # Next 15 bits is number that represents total length (in bits) of subpackets

            sub_packets_start = Packet.VAL_START+1+SUBPACKETS_LEN_FIELD_SZ
            self._processed_bin_digits += SUBPACKETS_LEN_FIELD_SZ
            sub_packets_total_len = int(self._bin_in_str[Packet.VAL_START+1: sub_packets_start], 2)
            sub_packets_end = sub_packets_start + sub_packets_total_len
            
            # Extract the portion of this packet that contains all the sub_packets
            sub_packets_data = self._bin_in_str[sub_packets_start: sub_packets_end]
            
            # Parse these subpackets sequentially, until no more remain
            processed_bits = 0
            while processed_bits < sub_packets_total_len:
                sub_packet = Packet(sub_packets_data, self._level+1)
                processed_bits += len(sub_packet)
                self._sub_packets.append(sub_packet)
                sub_packets_data = sub_packet.remaining_from_stream
            
            self._processed_bin_digits += sub_packets_total_len
        else:
            # Next 11 bits are mumber that represents number of sub-packets contained       
            assert len_type_id == 1, "Len_type must be 0 or 1"
            self._processed_bin_digits += SUBPACKETS_CONTAINED_FIELD_SZ

            sub_packets_start = Packet.VAL_START+1+SUBPACKETS_CONTAINED_FIELD_SZ
            num_subpackets = int(self._bin_in_str[Packet.VAL_START+1: sub_packets_start], 2)
            sub_packets_data = self._bin_in_str[sub_packets_start:]
            
            # Parse these n subpackets sequentially, until no more remain
            processed_bits = 0
            while len(self._sub_packets) < num_subpackets:
                sub_packet = Packet(sub_packets_data, self._level+1)
                processed_bits += len(sub_packet)
                self._sub_packets.append(sub_packet)
                sub_packets_data = sub_packet.remaining_from_stream 
            
            self._processed_bin_digits += processed_bits               
            
    def __str__(self) -> str:
        """ Short representation at top level only """
        hex_repr = hex(int(self._bin_in_str, 2)).upper()[2:]
        show_len = 10
        if len(hex_repr) > show_len:
            hex_repr = hex_repr[:show_len] + "..."
        
        return (f"Packet:LVL={self._level},VerSum={self.version_sum},Ver={self._version}," + 
                 f"T={self._type},Val={self.value},hex={hex_repr}")
    
    def __repr__(self) -> str:
        """ Show packet information, including recursive detail """
        if self._sub_packets:
            val = ",".join(repr(sub_packet) for sub_packet in self._sub_packets)
        else:
            val = self._literal_val
            
        return ("\n" + ("  " * self._level) 
                + f"[Packet:LVL={self._level},VerSum={self.version_sum},Ver={self._version},T={self._type},value={val}]")

def main():
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        # Each line has a single outer packet. Actual input is only one line, but our test data has many lines.
        outer_packets_data = [hex_to_bin(line) for line in f.read().splitlines()]
    
    for outer_packet_data in outer_packets_data:
        packet = Packet(outer_packet_data)
        # logger.info(packet)
        logger.info(repr(packet))

def hex_to_bin(hex_value) -> str:
    """ Convert all hex digits to binary representation, with leading zeroes """
    bin_len = 4*len(hex_value)      # 4 bits per hex
    return "{0:0{width}b}".format(int(hex_value, 16), width=bin_len)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
