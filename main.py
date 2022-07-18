from hashlib import pbkdf2_hmac, sha256
import requests
from secret import RANDOM_DOT_ORG_API_KEY
import random

ENTROPY_BITS = 256


def generate_public_key(private_key):
    private_key_bytes = bytes.fromhex(private_key)
    public_key = sha256(private_key_bytes).hexdigest()
    return public_key

def generate_private_key(phrase):
    phrase_str = "".join(phrase)
    salt = "mnemonic"+phrase_str
    key = pbkdf2_hmac("sha512", phrase_str.encode("utf-8"), salt.encode("utf-8"), 2048, 64)
    return key.hex()

# generate mnuemonic phrase based on bip39
#   * generate a random 256-bit number
#   * hash it with sha256
#   * take first 256/32 bits of hash as a checksum
#   * append this checksum to the random number
#   * split concatenated number into 11 bit chunks
#   * convert each chunk to a word by using its base 10 value as an index in the bip39 word list
#   * return the list of words

def generate_phrase():
    ent = get_random() # get random number
    print(ent)
    hash = sha256(ent.encode("utf-8")).hexdigest() 
    cl = ENTROPY_BITS // 32 # checksum length
    checksum = hash[:cl//4] # get first checksum bits of hash ( divide by four because one hex digit represents four bits )
    ent_cs = ent + checksum
    print(hash)
    print(checksum)
    print(ent_cs)
    ent_cs_bits = bin(int(ent_cs, 16))[2:].zfill(ENTROPY_BITS)
    ent_cs_bit_chunks = [ent_cs_bits[i:i+11] for i in range(0, len(ent_cs_bits), 11)]
    print(ent_cs_bits)
    print(ent_cs_bit_chunks)
    words = []
    f = open('english.txt', 'r')
    words = f.read().splitlines()
    f.close()
    phrase = [words[int(chunk, 2)] for chunk in ent_cs_bit_chunks]
    # print(int('00111110001', 2))

    return phrase

def get_random():
    ENDPOINT = "https://api.random.org/json-rpc/4/invoke"
    params = {
        "apiKey": RANDOM_DOT_ORG_API_KEY,
        "n": "8",
        "size": ENTROPY_BITS,
        "format": "hex"
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "generateBlobs",
        "params": params,
        "id": 69
    }
    response = requests.post(ENDPOINT, json=payload)
    print(response.json())
    return response.json()["result"]["random"]["data"][random.randint(0, len(response.json()["result"]["random"]["data"])-1)]

if __name__ == "__main__":
    phrase = generate_phrase()
    # phrase = "world diesel only match guilt win laugh loan race disorder baby face market permit situate truly combine naive grit speak absurd point scrub sport".split(' ')
    print("Your seed phrase is: " + " ".join(phrase))
    private_key = generate_private_key(phrase)
    print("Your private key is: " + private_key)
    public_key = generate_public_key(private_key)
    print("Your address is: " + public_key)