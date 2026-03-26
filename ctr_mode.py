from saes_core import saes_encrypt

def increment_counter(counter: int) -> int:
    #counter: i need to add 1 to it, max = 65535 == 16bits -> reset to 0
    #return the counter
    #65536 la2ano when i reaches 65534 + 1 % 65535, it return 0, but it resets before it actually use the max
    counter = (counter + 1) % 65536
    return (counter)

def ctr_process_block(block: int, counter: int, key: int) -> int:
    #keystream is the counter after we applied saes to it, and we need to key ofcourse
    #then we XOR the keystream with the block, which is the plaintext and return it
    keystream = saes_encrypt(counter, key) 
    return (block ^ keystream)

def read_file_to_integers(filepath: str):
    #we need an empty list to store from file into integers
    integers = []
    with open(filepath, "rb") as f:
        last_chunk_was_1_byte = False
        while True:
            chunk = f.read(2) #i need to read only two bytes at a time
            if not chunk: # if empty -> EOF
                break
            if len(chunk) == 1:
                last_chunk_was_1_byte = True            #now we convert the chunk(2bytes) into integers
            num = int.from_bytes(chunk, 'big')
            integers.append(num)
    return (integers, last_chunk_was_1_byte)


def write_integers_to_file(integers_list: list[int], filepath: str, last_chunk_was_1_byte: bool):
    #we need to re write everything back to the file 
    #one edge case, there's a possibility that the last byte might be 1 and not 2.
    #se to fix think, we used to boolean to check and the if else :D
    with open(filepath, "wb") as f:
        for item in range(len(integers_list)):
            num = integers_list[item]
            if item == (len(integers_list) - 1) and (last_chunk_was_1_byte == True):
                f.write(num.to_bytes(1, 'big'))
            elif (item == len(integers_list) - 1):
                f.write(num.to_bytes(2, 'big'))
            else:
                f.write(num.to_bytes(2, 'big'))

def process_file_ctr(input_filepath: str, output_filepath: str, key: int, starting_counter: int = 0):
    
    #read the file, converting file into integers
    integers, last_chunk_was_1_byte = read_file_to_integers(input_filepath)
    
    # create an empty list to store the block, and set the counter
    processed_blocks = []
    cur_counter = starting_counter

    #i need to process the blocks and append them into the empty list
    for block in integers:
        processed_blocks_int = ctr_process_block(block, cur_counter, key)
        processed_blocks.append(processed_blocks_int)
        cur_counter = increment_counter(cur_counter)
    
    #now i need to write the processed blocks into the new file :D
    write_integers_to_file(processed_blocks, output_filepath, last_chunk_was_1_byte)

if __name__ == "__main__":
    #we need to get the input file path, output file path, key, and starting counter from the user
    input_file = input("Enter the input file path: ")
    output_file = input("Enter the output file path: ")
    key = int(input("Enter the key: "))
    starting_counter = int(input("Enter the starting counter: "))
    print("Encrypting..")
    process_file_ctr(input_file, output_file, key, starting_counter)
    print("Done!  Please Check the output file :D")


