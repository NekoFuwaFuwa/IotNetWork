import sys
import string

key = 0x0B00B135

def xor_enc(data):
    n = bytearray()
    k1 = key & 0xff
    k2 = (key >> 8) & 0xff
    k3 = (key >> 16) & 0xff
    k4 = (key >> 24) & 0xff

    for byte in data:
        tmp = byte ^ k1
        tmp ^= k2
        tmp ^= k3
        tmp ^= k4
        n.append(tmp)

    return bytes(n)

def ci_enc(data):
    chars = " " + string.punctuation + string.digits + string.ascii_letters
    chars = list(chars)
    k = ['Z', 'U', 't', '1', '.', '\\', '4', 'K', 'j', 'R', 'W', 'k', 'A', '?', 'u', '!', 'b', '[', 'm', ';', '{', '^', ',', 'X', 'r', 'V', '$', "'", ' ', 'C', 'i', ']', '6', '%', 'J', '~', 'p', 'O', 'z', '"', 'F', 'L', '5', 'd', 'E', 'q', '7', '<', 'H', '&', '2', 'S', 'G', 'P', 'o', '`', '8', '/', 'Y', '3', 'I', ')', 's', '-', 'a', 'M', '(', 'v', 'w', 'f', 'g', '@', '+', 'D', 'n', 'y', '9', ':', 'x', 'B', 'c', 'l', '|', 'Q', '#', '0', 'h', '*', 'N', 'T', '}', '_', '>', 'e', '=']

    cipher = ""
    for i in data:
        index = chars.index(i)
        cipher += k[index]
    
    return cipher


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} [data]")
        sys.exit()
    
    #data = sys.argv[1].encode()

    op = ci_enc(sys.argv[1])
    data = op

    for _ in range(7):
        op = ci_enc(op)
        data = op

    print("XOR'ing {} bytes of data...".format(len(data)))
    print(data)
    xor_data = xor_enc(data.encode())
    print("".join([f"0x{byte:02X}, " for byte in xor_data]))

    
if __name__ == "__main__":
    main()
