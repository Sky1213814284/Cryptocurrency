"SkyGodDollar"
import hashlib
import binascii
import rsa
import os.path
from datetime import datetime
import sys

def name():
    print("SkyGodDollar")

def genesis():
    with open("block_0.txt","w") as file:
        file.write("Lebron James is the greatest basketball player in the history.")
    print("Genesis block created in 'block_0.txt'")

def generate(filename):
    (pubkey, privkey) = rsa.newkeys(1024)
    pubkeyBytes = pubkey.save_pkcs1(format='PEM')
    privkeyBytes = privkey.save_pkcs1(format='PEM')
    pubkeyStr = pubkeyBytes.decode('ascii')
    privkeyStr = privkeyBytes.decode('ascii')
    tag = hashlib.sha256(pubkeyBytes).hexdigest()
    with open(filename, "w") as file:
        file.write(pubkeyStr)
        file.write(privkeyStr)
    print("New wallet generated in '" + filename + "'with signature " + str(tag[0:16]))

def address(filename):
    print(_address(filename))

def _address(filename):
    pubkey, _ = loadWallet(filename)
    pubkeyBytes = pubkey.save_pkcs1(format='PEM')
    tag = hashlib.sha256(pubkeyBytes).hexdigest()
    return tag[0:16]

def fund(address, amount, filename):
    with open(filename, "w") as file:
        file.write("From: SkyGod" + "\n")
        file.write("To: " + address + "\n")
        file.write("Amount: " + amount + "\n")
        time = str(datetime.now())
        file.write("Date: " + time)
    print("Funded wallet " + address + " with " + amount + " SkyGodDollars on " + time)

def transfer(source, dest, amount, filename):
    content = ""
    fst = "From: " + str(_address(source)) + "\n"
    content += fst
    sec = "To: " + dest + "\n"
    content += sec
    trd = "Amount: " + amount + "\n"
    content += trd
    time = str(datetime.now())
    frth = "Date: " + time + "\n"
    content += frth
    _ , privkey = loadWallet(source)
    content = content.encode("utf-8")
    encryption = rsa.sign(content, privkey, "SHA-256")
    with open(filename, "w") as file:
        file.write(fst)
        file.write(sec)
        file.write(trd)
        file.write(frth)
        file.write(bytesToString(encryption).decode("utf-8"))
    print("Transferred " + amount + " from " + source + " to " + dest + " and the statement to '" + filename + "' on " + time)

def balance(address):
    print(_balance(address))

def _balance(address):
    balance = 0
    block = 1
    filename = "block_" + str(block) +".txt"
    while os.path.exists(filename):
        with open(filename) as file:
            lines = file.readlines()[1:-2]
            for transaction in lines:
                temp = transaction.split(" ")
                if temp != ['\n']:
                    sender = temp[0]
                    receiver = temp[4]
                    amount = temp[2]
                    if sender == address:
                        balance -= int(amount)
                    elif receiver == address:
                        balance += int(amount) 
        block += 1
        filename = "block_" + str(block) +".txt"
    if os.path.exists("mempool.txt"):
        with open("mempool.txt") as file:
            lines = file.readlines()
            for transaction in lines:
                temp = transaction.strip().split(" ")
                if temp != ['']:
                    sender = temp[0]
                    receiver = temp[4]
                    amount = temp[2]
                    if sender == address:
                        balance -= int(amount)
                    elif receiver == address:
                        balance += int(amount)
    return balance


def verify(source, transaction):
    pubkey, _ = loadWallet(source)
    content = ""
    address = _address(source)
    with open(transaction) as file:
        lines = file.readlines()
        sender = lines[0].strip().split(" ")[1]
        receiver = lines[1].strip().split(" ")[1]
        print(receiver)
        amount = lines[2].strip().split(" ")[1]
        print(amount)
        time = lines[3]
        for i in range(4):
            content += lines[i]
        if sender == "SkyGod":
            with open("mempool.txt", 'a') as file:
                tran = sender + " transferred " + amount + " to " + receiver + " on " + time + "\n"
                file.write(tran)
            return True
        else:
            signature = lines[4].strip().encode("utf-8")
            signature = stringToBytes(signature)
            content = content.encode("utf-8")
            if rsa.verify(content, signature, pubkey) != "SHA-256":
                return False
            else:
                sourceBalance = _balance(address)
                print(sourceBalance)
                if sourceBalance < int(amount):
                    print("fail")
                    return False
                else:
                    with open("mempool.txt", 'a') as file:
                        tran = sender + " transferred " + amount + " to " + receiver + " on " + time + "\n"
                        file.write(tran)
                        print("transferred")
                    return True

def mine(difficulty):
    block = 0
    nonce = 0
    filename = "block_" + str(block) +".txt"
    while os.path.exists(filename):
        block += 1
        filename = "block_" + str(block) +".txt"
    prev = "block_" + str(block - 1) +".txt"
    content = hashFile(prev) + "\n\n"
    with open("mempool.txt",'r') as file:
        for line in file:
            content += line
    content += "\n" + "nonce: "
    goal = "0" * int(difficulty)
    while hashlib.sha256((content+str(nonce)).encode('utf-8')).hexdigest()[0:int(difficulty)] != goal:
        nonce += 1
    newfilename = "block_" + str(block) +".txt"
    with open(newfilename,'w') as file:
        file.write(content + str(nonce))
    with open("mempool.txt","w") as file:
        file.truncate(0)
    return True
    
def validate():
    block = 1
    filename = "block_" + str(block) + ".txt"
    while os.path.exists(filename):
        prevFilename = "block_" + str(block - 1) + ".txt"
        prevhash = hashFile(prevFilename)
        with open(filename, "r") as file:
            providedHash = file.readlines()[0].strip()
            if providedHash != prevhash:
                print("False")
                return False
        block += 1
        filename = "block_" + str(block) + ".txt"
    print("True")
    return True
        

# gets the hash of a file; from https://stackoverflow.com/a/44873382
def hashFile(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

# given an array of bytes, return a hex reprenstation of it
def bytesToString(data):
    return binascii.hexlify(data)

# given a hex reprensetation, convert it to an array of bytes
def stringToBytes(hexstr):
    return binascii.a2b_hex(hexstr)

# Load the wallet keys from a filename
def loadWallet(filename):
    with open(filename, mode='rb') as file:
        keydata = file.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)
    pubkey = rsa.PublicKey.load_pkcs1(keydata)
    return pubkey, privkey

# save the wallet to a file
def saveWallet(pubkey, privkey, filename):
    # Save the keys to a key format (outputs bytes)
    pubkeyBytes = pubkey.save_pkcs1(format='PEM')
    privkeyBytes = privkey.save_pkcs1(format='PEM')
    # Convert those bytes to strings to write to a file (gibberish, but a string...)
    pubkeyString = pubkeyBytes.decode('ascii')
    privkeyString = privkeyBytes.decode('ascii')
    # Write both keys to the wallet file
    with open(filename, 'w') as file:
        file.write(pubkeyString)
        file.write(privkeyString)
    return

if __name__ == '__main__':
    args = sys.argv
    globals()[args[1]](*args[2:])