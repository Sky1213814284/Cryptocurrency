import sys
import binascii
import json
import hashlib

def parse(filename): 
    with open(filename, mode="rb") as file:
        #check magic number
        counter = -1
        puppet = {}
        blockinfo = []
        previous_hash = ""
        previous_time = 0
        while True:
            index = 0
            block = {}
            magic = file.read(4)
            txns = []
            #print(magic)
            if magic != b'':
                counter += 1
                if not check_magic(magic):
                    print("error 1 block " + str(counter))
                    return
                block["height"] = counter
                size = file.read(4)
                size = convert(size)
                rest = file.read(size)
                #print("size of whole block", len(rest))
                #print("content of whole block", rest)
                header = rest[0:80]
                currenthash = hashlib.sha256(hashlib.sha256(header).digest()).hexdigest()
                version = convert(header[0:4])
                block["version"] = version
                if version != 1:
                    print("error 2 block " + str(counter))
                    return
                prevhash = ltob(binascii.hexlify(header[4:4+32]).decode())
                if counter != 0:
                    previous_hash = ltob(previous_hash)
                    if prevhash != previous_hash:
                        print("error 3 block " + str(counter))
                        return
                    else:
                        previous_hash = currenthash
                else:
                    previous_hash = currenthash
                block["previous_hash"] = prevhash
                merklehash = ltob(binascii.hexlify(header[36:36+32]).decode())
                block["merkle_hash"] = merklehash
                time = convert(header[68:68+4])
                block["timestamp"] = time
                currenttime = time
                if counter != 0:
                    if previous_time - currenttime > 7200:
                        print("error 4 block " + str(counter))
                        return
                    else:
                        previous_time = currenttime
                else:
                    previous_time = currenttime
                nbits = ltob(binascii.hexlify(header[72:72+4]).decode())
                block["nbits"] = nbits
                nonce = convert(header[76:80])
                block["nonce"] = nonce
                #print(nonce)
                #print(nbits)
                #print(time)
                #print(merklehash)
                #print(prevhash)
                #print("version", version)
                txn_countb = rest[80:81]
                btr = check_compact(txn_countb)
                txn_count = 0
                index += 80
                index += 1
                if btr == 0:
                    txn_count = convert(txn_countb)
                else:
                    txn_count = convert(rest[index:index + btr])
                block["txn_count"] = txn_count
                transactions = []
                index += btr
                #print("index", index)
                for i in range(txn_count):
                    txn_start_index = index
                    #print("start_index", txn_start_index)
                    transaction = {}
                    trans_version = convert(rest[index:index + 4])
                    #print("trans_version", trans_version)
                    transaction["version"] = trans_version
                    if trans_version != 1:
                        print("error 5 block " + str(counter))
                        return
                    index += 4
                    tx_in_countb = rest[index:index+1]
                    btr1 = check_compact(tx_in_countb)
                    tx_in_count = 0
                    index += 1
                    if btr1 == 0:
                        tx_in_count = convert(tx_in_countb)
                    else:
                        tx_in_count = convert(rest[index:index+btr1])
                    transaction["txn_in_count"] = tx_in_count
                    txn_inputs = []
                    index += btr1
                    for j in range(tx_in_count):
                        txn_input = {}
                        hash_str = binascii.hexlify(rest[index:index+32]).decode()
                        utxo_hash = ltob(hash_str)
                        txn_input["utxo_hash"] = utxo_hash
                        index += 32
                        utxo_index = convert(rest[index:index + 4])
                        txn_input["index"] = utxo_index
                        #print(utxo_index)
                        index += 4
                        input_script_size_b = rest[index:index + 1]
                        #print(input_script_size_b)
                        btr2 = check_compact(input_script_size_b)
                        #print(btr2)
                        input_script_size = 0
                        index += 1
                        if btr2 == 0:
                            input_script_size = convert(input_script_size_b)
                        else:
                            input_script_size = convert(binascii.hexlify(rest[index:index + btr2]))
                        index += btr2
                        #print(input_script_size)
                        txn_input["input_script_size"] = input_script_size
                        tx_in = binascii.hexlify(rest[index:index + input_script_size]).decode()
                        txn_input["input_script_bytes"] = tx_in
                        #print(tx_in)
                        index += input_script_size
                        seq = convert(rest[index:index + 4])
                        txn_input["sequence"] = seq
                        index += 4
                        #print(seq)
                        txn_inputs.append(txn_input)
                    tx_out_countb = rest[index:index + 1]
                    btr3 = check_compact(tx_out_countb)
                    tx_out_count = 0
                    index += 1
                    if btr3 == 0:
                        tx_out_count = convert(tx_out_countb)
                    else:
                        tx_out_count = convert(rest[index:index + btr3])
                    #print("tx_out_count",tx_out_count)
                    index += btr3
                    transaction["txn_inputs"] = txn_inputs
                    transaction["txn_out_count"] = tx_out_count
                    tx_outputs = []
                    for k in range(tx_out_count):
                        txn_output = {}
                        amount = convert(rest[index:index + 8])
                        txn_output["satoshis"] = amount
                        index += 8
                        #print(amount)
                        output_script_size_b = rest[index:index+1]
                        btr4 = check_compact(output_script_size_b)
                        index += 1
                        output_script_size = 0
                        if btr4 == 0:
                            output_script_size = convert(output_script_size_b)
                        else:
                            output_script_size = convert(rest[index:index+btr4])
                        index += btr4
                        txn_output["output_script_size"] = output_script_size
                        #print(output_script_size)
                        tx_out = binascii.hexlify(rest[index:index + output_script_size]).decode()
                        txn_output["output_script_bytes"] = tx_out
                        index += output_script_size
                        #print(tx_out)
                        tx_outputs.append(txn_output)
                    transaction["txn_outputs"] = tx_outputs
                    lock_time = convert(rest[index:index+4])
                    index += 4
                    transaction["lock_time"] = lock_time
                    #print(lock_time)
                    transactions.append(transaction)
                    txn_end_index = index
                    #print("end_index", txn_end_index)
                    txns.append(rest[txn_start_index:txn_end_index])
                computed_merkle = build_merkle(txns)
                txns = []
                #print(ltob(computed_merkle[0]))
                #print(merklehash)
                if merklehash != ltob(computed_merkle[0]):
                    print("error 6 block " + str(counter))
                    return
                block["transactions"] = transactions
                blockinfo.append(block)
            else:
                puppet["blocks"] = blockinfo
                puppet["height"] = counter + 1
                name = filename + ".json"
                with open(name, "w") as outfile:
                    outfile.write(json.dumps(puppet, indent = 4))
                print("no errors " + str(counter + 1) + " blocks")
                return

def check_magic(b):
    goal = b'\xf9\xbe\xb4\xd9'
    if b != goal:
        return False
    else:
        return True

def convert(b):
    int_val = int.from_bytes(b, "little", signed=False)
    return int_val

def check_compact(b):
    b = convert(b)
    #print(b)
    if b < 253:
        return 0
    elif b == 253:
        return 2
    elif b == 254:
        return 4
    elif b == 255:
        return 8

def build_merkle(txns):
    result = txns
    for i in range(len(result)):
        result[i] = hashlib.sha256(hashlib.sha256(result[i]).digest()).digest()
    while len(result) > 1:
        temp = []
        if len(result) % 2 != 0:
            result.append(result[-1])
        for j in range(0,len(result),2):
            concate = result[j] + result[j+1]
            hash_concate = hashlib.sha256(hashlib.sha256(concate).digest()).digest()
            temp.append(hash_concate)
        result = temp
    result[0] = result[0].hex()
    return result

#convert little endian string to big endian string
def ltob(b):
    #conversion from little endian string to big endian string is cited from stackoverflow https://stackoverflow.com/questions/46109815/convert-string-from-big-endian-to-little-endian-or-vice-versa-in-python
    hash_bytearr = bytearray.fromhex(b)
    hash_bytearr.reverse()
    result = ''.join(format(x, '02x') for x in hash_bytearr)
    return result

if __name__ == "__main__":
    args = sys.argv
    globals()[args[1]](*args[2:])