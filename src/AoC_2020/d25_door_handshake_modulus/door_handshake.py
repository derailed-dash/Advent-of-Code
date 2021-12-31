import os
import time

INPUT_FILE = "input/data.txt"
SAMPLE_INPUT_FILE = "input/sample_data.txt"

def main():
    # get absolute path where script lives
    script_dir = os.path.dirname(__file__) 
    print("Script location: " + script_dir)

    # path of input file
    input_file = os.path.join(script_dir, INPUT_FILE)
    # input_file = os.path.join(script_dir, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)
    card_public_key, door_public_key = read_input(input_file)
    card_loop_size = determine_loop_size(7, card_public_key)
    #door_loop_size = determine_loop_size(7, door_public_key)
    encryption_key = transform(card_loop_size, door_public_key)

    print(f"Encyption key = {encryption_key}")


def transform(loop_size, public_key):
    iteration = 0
    value = 1

    while iteration < loop_size:
        value *= public_key
        value %= 20201227
        iteration += 1
    
    return value


def determine_loop_size(subject, public_key):
    value = 1

    loop_count = 0
    while value != public_key:
        value *= subject
        value %= 20201227 
        loop_count += 1

    if value != public_key:
        raise ValueError(f"Value {value} exceeds public key {public_key}")
    
    return loop_count


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        data = f.read().splitlines()

    return int(data[0]), int(data[1])


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
