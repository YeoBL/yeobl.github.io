from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import ast

def bits_to_bytes(bits):
    """
    Convert a list of bits (0s and 1s) to a bytes object.
    Assumes that len(bits) is a multiple of 8.
    """
    # Join the bits into a string, e.g., '11010001...'
    bit_str = ''.join(str(bit) for bit in bits)
    # Convert that string to an integer.
    n = int(bit_str, 2)
    # Convert the integer to bytes.
    return n.to_bytes(len(bits) // 8, byteorder='big')

with open("convos.py", "r") as handler:
    txt = handler.read()
    txt = txt.replace("convos=", "")
    convos = ast.literal_eval(txt)

ct = b'G\x00z\xb4\xe3\xcbKi\xe3Q\xed\x17$\xf2}\x80\xca\xe3C\xb8\xa7[h\x01\xdb$\x16&S\xa6\x0b\xd7W^q\x02\x14TR\xe3\xb5\xa0M{\xa1\x1f\xc3\x0c'

keys = []
ivs = []

for convo in convos:
    res = []
    key_bits = []
    iv_bits = []
    basis1, basis2, bits1, bits2 = convo
    for i in range(0, len(basis1)):
        if basis1[i] == basis2[i]:
            key_bits.append(bits1[i])
            iv_bits.append(bits2[i])

    # Convert the bit lists to 16-byte values.
    key = bits_to_bytes(key_bits)
    iv = bits_to_bytes(iv_bits)
    keys.append(key)
    keys.append(iv)
    ivs.append(key)
    ivs.append(iv)

    # Your ciphertext given as bytes:
    ct = b'G\x00z\xb4\xe3\xcbKi\xe3Q\xed\x17$\xf2}\x80\xca\xe3C\xb8\xa7[h\x01\xdb$\x16&S\xa6\x0b\xd7W^q\x02\x14TR\xe3\xb5\xa0M{\xa1\x1f\xc3\x0c'

    # Create an AES cipher object in CBC mode.
for key in keys:
    for iv in ivs:
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Decrypt. (Depending on how the plaintext was padded, you might need to unpad.)
        decrypted = cipher.decrypt(ct)

        # If the plaintext was padded (e.g. with PKCS7), use unpad:
        try:
            decrypted = unpad(decrypted, AES.block_size)
        except ValueError:
            # if unpadding fails, it might not have been padded.
            pass

        # print(decrypted.decode('utf-8', errors='replace'))
        try:
            print(decrypted.decode('utf-8'))
        except:
            continue