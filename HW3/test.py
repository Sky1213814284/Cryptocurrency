import sys
import binascii
import hashlib

def convert():
    start = b'\x02'
    print(start)
    int_val = int.from_bytes(start, "little", signed=False)
    print(int_val)

if __name__ == "__main__":
    args = sys.argv
    globals()[args[1]](*args[2:])
