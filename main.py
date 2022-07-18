from hashlib import pbkdf2_hmac, sha256
import random
import requests
from secret import RANDOM_DOT_ORG_API_KEY


NUM_WORDS = 24


def generate_public_key(private_key):
    private_key_bytes = bytes.fromhex(private_key)
    public_key = sha256(private_key_bytes).hexdigest()
    return public_key

def generate_private_key(phrase):
    phrase_str = " ".join(phrase)
    salt = "mnemonic"+phrase_str
    key = pbkdf2_hmac("sha512", phrase_str.encode("utf-8"), salt.encode("utf-8"), 2048, 64)
    return key.hex()

def generate_phrase():
    phrase = []
    words = []

    f = open("english.txt", "r") # TXT file can be found at: https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt
    words = f.read().splitlines()
    f.close()

    indexes = get_random_indexes(NUM_WORDS)
    for i in indexes:
        phrase.append(words[i])

    return phrase

def get_random_indexes(num_indexes):
    ENDPOINT = "https://api.random.org/json-rpc/4/invoke"
    params = {
        "apiKey": RANDOM_DOT_ORG_API_KEY,
        "n": num_indexes,
        "min": 0,
        "max": 2048,
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": params,
        "id": 69
    }
    response = requests.post(ENDPOINT, json=payload)
    return response.json()["result"]["random"]["data"]


if __name__ == "__main__":
    phrase = generate_phrase()
    # phrase = "world diesel only match guilt win laugh loan race disorder baby face market permit situate truly combine naive grit speak absurd point scrub sport".split(' ')
    print("Your seed phrase is: " + " ".join(phrase))
    private_key = generate_private_key(phrase)
    print("Your private key is: " + private_key)
    public_key = generate_public_key(private_key)
    print("Your address is: " + public_key)