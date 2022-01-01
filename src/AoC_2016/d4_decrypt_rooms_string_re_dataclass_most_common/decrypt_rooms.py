"""
Author: Darren
Date: 24/05/2021

Solving https://adventofcode.com/2016/day/4

Solution:

Part 1:
    Regex to parse input data.
    For each room, count chars.
    Then use collections.Counter to determine the top 5 chars.
    Use this to compare to the checksum, to identify valid rooms.
    Finally, sum checksums for all valid rooms.

Part 2:
    Shift char using some basic char to ascii (ord) and ascii to char (chr),
    plus some mod operations.

"""
import logging
import os
import time
import re
from dataclasses import dataclass
from collections import Counter
import string

# pylint: disable=logging-fstring-interpolation

SCRIPT_DIR = os.path.dirname(__file__) 
INPUT_FILE = "input/input.txt"
SAMPLE_INPUT_FILE = "input/sample_input.txt"

@dataclass
class Room:
    """ Dataclass for a room """
    enc_name: str
    sector_id: int
    checksum: str


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:\t%(message)s")
        
    # input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        data = f.read().splitlines()
                
    # match any str followed by -ddd[xxxxx], where is a digit and x is any alpha char
    # e.g. nzydfxpc-rclop-qwzhpc-qtylyntyr-769[oshgk]
    pattern = re.compile(r"(\D+)-(\d+)\[([a-z]{5})\]")
    rooms: list[Room] = []
        
    for line in data:
        match = pattern.match(line)
        if match:
            enc_name, sector_id, checksum = match.groups()
            room = Room(enc_name, int(sector_id), checksum)
            if is_valid_room(room):
                rooms.append(room)

    # Part 1
    sector_id_sum = sum(room.sector_id for room in rooms)
    logging.info(f"Sector ID sum: {sector_id_sum}")
    
    # Part 2
    for room in rooms:
        decrypted_room = decrypt_room(room)
        logging.debug("Room: %s", decrypted_room)
        
        if decrypted_room == "northpole object storage":
            logging.info("Found %s with sector id %d", decrypted_room, room.sector_id)
            break
    

def decrypt_room(room: Room) -> str:
    """ Decrypt room names.
    Replace "-" with " ".
    Then, shift all a-z chars by the sector ID

    Args:
        room (Room): Encrypted room

    Returns:
        str: Decrypted room
    """
    enc_str = room.enc_name.replace("-", " ")
    
    # Now shift each letter by the sector_id value. z wraps back to a.
    decrypted_str = []
    for char in enc_str:
        if char in string.ascii_lowercase:
            # conver to ascii code
            ascii_code = ord(char)
            
            # wrap around
            ascii_code += (room.sector_id % 26)

            # Note: z=122.  If we exceed this, we need to subtract 26.
            if (ascii_code > 122):
                ascii_code -= 26
                
            decrypted_str.append(chr(ascii_code))
        else:
            assert char == " ", "It must be a space"
            decrypted_str.append(char)
    
    return "".join(decrypted_str)
    

def is_valid_room(room: Room) -> bool:
    """ Room is valid if descending counts of most frequent chars in room.enc_name
    matches the chars in the checksum.  Where char counts are tied, sort by alphabetic order.

    Args:
        room (Room): The room to check

    Returns:
        bool: is valid
    """
    # create dict of char:count(char) for each char in 'abcde...'
    char_counts = {char:room.enc_name.count(char) for char in string.ascii_lowercase}

    # Create a multiset from the dict, which stores item, count
    # Then use most_common(5) to retrieve the 5 most common items in the multiset
    top_five_counts = Counter(char_counts).most_common(5)
    logging.debug(top_five_counts)
    
    # create a str from the most common chars and compare it to the checksum
    top_five_chars = "".join([item[0] for item in top_five_counts])
    if top_five_chars == room.checksum:
        return True
    
    return False


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
