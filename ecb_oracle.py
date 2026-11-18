import requests
def request_encrypt(text):
    r = requests.get("http://aes.cryptohack.org/ecb_oracle/encrypt/" + text.encode().hex())
    return r.json()['ciphertext']

def pad_input(s):
    pad = 'A' * (16 - len(s) % 16)
    return pad + s + pad

def decrypt_flag():
    chars = "abcdefghijklmnopqrstuvwxyz1234567890_{}"
    flag = ""
    while not flag.endswith('}'):
        for c in chars:
            guess = flag + c
            padded = pad_input(guess)
            ct = request_encrypt(padded)
            size = 2 * ((16 - len(guess) % 16) + len(guess))
            part1, part2 = ct[:size], ct[size:size*2]
            if part1 == part2:
                flag += c
                print(flag)
                break
        else:
            raise ValueError(f"Aucun caractère ne correspond après : {flag!r}")
    return flag
if __name__ == '__main__':
    decrypt_flag()